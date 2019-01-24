import FreeCAD
import FreeCADGui
import string
import json

from FreeCAD import Units
from pivy import coin
from report_utils.resource_utils import uiPath
from sql import freecad_sql_parser

from PySide2.QtWidgets import QTableWidgetItem
from PySide2.QtWidgets import QTextEdit
from PySide2.QtWidgets import QGroupBox
from PySide2.QtWidgets import QLineEdit
from PySide2.QtWidgets import QFormLayout
from PySide2.QtWidgets import QPushButton
from PySide2.QtWidgets import QCheckBox

SQL_PARSER = freecad_sql_parser.newParser()

COLUMN_NAMES = list(string.ascii_uppercase)

DEBUG = True


def statementsToDict(reportStatements):
    statements = []

    for reportStatement in reportStatements:
        statements.append({
            'header': reportStatement.header,
            'plainTextStatement': reportStatement.plainTextStatement,
            'htmlStatement': reportStatement.htmlStatement,
            'skipRowsAfter': reportStatement.skipRowsAfter,
            'skipColumnNames': reportStatement.skipColumnNames,
            'printResultInBold': reportStatement.printResultInBold
        })

    return {
        'statements': statements
    }


def dictToStatements(statementDict):
    reportStatements = []

    for statement in statementDict['statements']:
        reportStatement = ReportStatement(statement['header'],
                                          statement['plainTextStatement'], statement['htmlStatement'],
                                          statement['skipRowsAfter'], statement['skipColumnNames'],
                                          statement['printResultInBold'])

        reportStatements.append(reportStatement)

    return reportStatements


def nextColumnName(actualColumnName):
    if actualColumnName is None:
        return COLUMN_NAMES[0]

    nextIndex = COLUMN_NAMES.index(actualColumnName) + 1

    if nextIndex >= len(COLUMN_NAMES):
        nextIndex -= len(COLUMN_NAMES)

    return COLUMN_NAMES[nextIndex]


def lineRange(startColumn, endColumn, lineNumber):
    return cellRange(startColumn, lineNumber, endColumn, lineNumber)


def cellRange(startColumn, startLine, endColumn, endLine):
    return '%s%s:%s%s' % (startColumn, startLine, endColumn, endLine)


def buildCellName(columnName, lineNumber):
    return '%s%s' % (columnName, lineNumber)


def literalText(text):
    return "'%s" % (text)


class ReportSpreadsheet(object):
    def __init__(self, spreadsheet):
        self.spreadsheet = spreadsheet
        self.lineNumber = 1

    def clearAll(self):
        self.spreadsheet.clearAll()

    def printHeader(self, header, numberOfColumns):
        spreadsheet = self.spreadsheet

        if header is None or header == '':
            return

        headerCell = 'A%s' % (self.lineNumber)

        self.setCellValue(headerCell, header)
        spreadsheet.setStyle(headerCell, 'bold|underline', 'add')

        if numberOfColumns > 1:
            lastColumnCell = COLUMN_NAMES[numberOfColumns - 1]

            spreadsheet.mergeCells(
                lineRange('A', lastColumnCell, self.lineNumber))

        self.lineNumber += 1

    def printColumnLabels(self, columnLabels):
        spreadsheet = self.spreadsheet

        columnName = None

        for columnLabel in columnLabels:
            columnName = nextColumnName(columnName)
            cellName = buildCellName(columnName, self.lineNumber)

            self.setCellValue(cellName, columnLabel)

        spreadsheet.setStyle(
            lineRange('A', columnName, self.lineNumber), 'bold', 'add')

        self.lineNumber += 1

    def printRows(self, rows, skipRowsAfter=False, printResultInBold=False):
        lineNumberBefore = self.lineNumber

        columnName = 'A'

        for row in rows:
            columnName = None

            for column in row:
                columnName = nextColumnName(columnName)
                cellName = buildCellName(columnName, self.lineNumber)

                self.setCellValue(cellName, column)

            self.lineNumber += 1

        if printResultInBold:
            self.spreadsheet.setStyle(
                cellRange('A', lineNumberBefore, columnName, self.lineNumber), 'bold', 'add')

        if not skipRowsAfter:
            self.lineNumber += 2

    def setCellValue(self, cell, value):
        if value is None:
            convertedValue = ''
        elif isinstance(value, Units.Quantity):
            convertedValue = value.UserString
        else:
            convertedValue = str(value)

        convertedValue = literalText(convertedValue)

        if DEBUG:
            print('set %s to %s for %s' %
                  (cell, convertedValue, self.spreadsheet))

        self.spreadsheet.set(cell, convertedValue)

    def recompute(self):
        self.spreadsheet.recompute()


class ReportEntryWidget(QGroupBox):
    def __init__(self, header, statement, skipRowsAfter, skipColumnNames, printResultInBold, panel, index):
        super().__init__()

        self.panel = panel
        self.index = index

        self.headerEdit = QLineEdit(header)
        self.statementEdit = QTextEdit(statement)
        self.skipRowsAfterEdit = QCheckBox('Skip Empty Rows After Statement')
        self.skipColumnNamesEdit = QCheckBox('Skip Column Names')
        self.printResultInBoldEdit = QCheckBox('Print Result in bold')
        self.removeButton = QPushButton('Remove')

        self.skipRowsAfterEdit.setChecked(skipRowsAfter)
        self.skipColumnNamesEdit.setChecked(skipColumnNames)
        self.printResultInBoldEdit.setChecked(printResultInBold)

        self.removeButton.clicked.connect(self.remove)

        self.initUi()

    def initUi(self):
        self.layout = QFormLayout()

        self.layout.addRow('Header', self.headerEdit)
        self.layout.addRow('Statement', self.statementEdit)
        self.layout.addRow(' ', self.skipColumnNamesEdit)
        self.layout.addRow(' ', self.skipRowsAfterEdit)
        self.layout.addRow(' ', self.printResultInBoldEdit)
        self.layout.addRow(' ', self.removeButton)

        self.setLayout(self.layout)

    def getHeader(self):
        return self.headerEdit.text()

    def getPlainTextStatement(self):
        return self.statementEdit.toPlainText()

    def getHtmlStatement(self):
        return self.statementEdit.toHtml()

    def shouldSkipColumnNames(self):
        return self.skipColumnNamesEdit.isChecked()

    def shouldSkipRowsAfter(self):
        return self.skipRowsAfterEdit.isChecked()

    def shouldPrintResultInBold(self):
        return self.printResultInBoldEdit.isChecked()

    def remove(self):
        self.panel.removeRow(self)


class ReportConfigPanel():
    def __init__(self, report, freecadObject):
        self.report = report
        self.freecadObject = freecadObject
        self.entries = []

        self.form = FreeCADGui.PySideUic.loadUi(uiPath('report_config.ui'))

        self.form.Title.setText('%s Config' % (freecadObject.Label))
        self.scrollAreaWidget = self.form.ScrollArea.widget()

        self.form.AddStatementButton.clicked.connect(
            self.addRow)

        self.setupRows()

    def setupRows(self):
        for statement in self.report.statements:
            statementText = statement.htmlStatement

            if statementText is None:
                statementText = statement.plainTextStatement

            self.addRow(statement.header, statementText,
                        statement.skipRowsAfter, statement.skipColumnNames, statement.printResultInBold)

    def addRow(self, header=None, statement=None, skipRowsAfter=False, skipColumnNames=False, printResultInBold=False):
        widget = ReportEntryWidget(header, statement, skipRowsAfter,
                                   skipColumnNames, printResultInBold, self, len(self.entries))

        self.entries.append(widget)

        self.scrollAreaWidget.layout().addWidget(widget)

    def removeRow(self, widget):
        self.entries.pop(widget.index)
        layoutItem = self.scrollAreaWidget.layout().takeAt(widget.index)

        layoutItem.widget().deleteLater()

    def accept(self):
        self.saveIntoConfig()

        FreeCADGui.Control.closeDialog()

        self.report.execute(self.freecadObject)

    def reject(self):
        FreeCADGui.Control.closeDialog()

    def saveIntoConfig(self):
        self.report.statements.clear()

        for entry in self.entries:
            reportStatement = ReportStatement(
                entry.getHeader(), entry.getPlainTextStatement(), entry.getHtmlStatement(), entry.shouldSkipRowsAfter(), entry.shouldSkipColumnNames(), entry.shouldPrintResultInBold())

            self.report.statements.append(reportStatement)


class ReportStatement(object):
    def __init__(self, header, plainTextStatement, htmlStatement=None, skipRowsAfter=False, skipColumnNames=False, printResultInBold=False):
        self.header = header
        self.plainTextStatement = plainTextStatement
        self.htmlStatement = htmlStatement
        self.statement = SQL_PARSER.parse(plainTextStatement)
        self.skipRowsAfter = skipRowsAfter
        self.skipColumnNames = skipColumnNames
        self.printResultInBold = printResultInBold

        if DEBUG:
            print('parsed statement %s' % (plainTextStatement))
            print('to %s' % (self.statement))

    def execute(self):
        return self.statement.execute()

    def getColumnNames(self):
        return self.statement.getColumnNames()

    def serializeState(self):
        return [self.header, self.plainTextStatement, self.htmlStatement, self.skipRowsAfter, self.skipColumnNames, self.printResultInBold]

    @staticmethod
    def deserializeState(state):
        stateItems = len(state)

        if stateItems == 2:
            return ReportStatement(state[0], state[1])

        if stateItems == 5:
            return ReportStatement(state[0], state[1], state[2], state[3], state[4])

        return ReportStatement(state[0], state[1], state[2], state[3], state[4], state[5])


class Report():
    def __init__(self, obj, fileObject=None):
        obj.Proxy = self

        # obj.addProperty("App::PropertyBool", "SkipComputing", "Settings",
        #                 "When true no calculation of this report is performed, even when the document gets recomputed").SkipComputing = False

        obj.addProperty("App::PropertyLink", "Result", "Settings",
                        "The spreadsheet to print the results to")

        self.statements = [
            # ReportStatement, ...
        ]

    def execute(self, fp):
        # if fp.SkipComputing:
        #     return

        if not fp.Result:
            FreeCAD.Console.PrintError(
                'No spreadsheet attached to %s. Could not recompute result' % (fp.Label))

        spreadsheet = ReportSpreadsheet(fp.Result)
        spreadsheet.clearAll()

        lineNumber = 1

        for statement in self.statements:
            columnNames = statement.getColumnNames()

            spreadsheet.printHeader(statement.header, len(columnNames))

            if not statement.skipColumnNames:
                spreadsheet.printColumnLabels(columnNames)

            rows = statement.execute()

            spreadsheet.printRows(
                rows, statement.skipRowsAfter, statement.printResultInBold)

        spreadsheet.recompute()

    def exportJson(self, fileObject):
        try:
            jsonDict = statementsToDict(self.statements)

            json.dump(jsonDict, fileObject, sort_keys=True,
                      indent=4, ensure_ascii=False)
        finally:
            fileObject.close()

    def importJson(self, fileObject):
        try:
            jsonDict = json.load(fileObject, encoding='utf-8')

            self.statements = dictToStatements(jsonDict)
        finally:
            fileObject.close()

    def __getstate__(self):
        return [statement.serializeState() for statement in self.statements]

    def __setstate__(self, state):
        self.statements = [ReportStatement.deserializeState(
            serializedState) for serializedState in state]

        return None


class ViewProviderReport():
    def __init__(self, vobj):
        vobj.Proxy = self

    def attach(self, vobj):
        self.ViewObject = vobj
        self.Object = vobj.Object
        self.report = self.Object.Proxy

        self.coinNode = coin.SoGroup()
        vobj.addDisplayMode(self.coinNode, "Standard")

    def onChanged(self, vp, prop):
        pass

    def doubleClicked(self, vobj):
        return self.setEdit(vobj, 0)

    def setEdit(self, vobj, mode):
        if mode == 0:
            panel = ReportConfigPanel(self.report, self.Object)
            FreeCADGui.Control.showDialog(panel)

            return True

        return False

    def unsetEdit(self, vobj, mode):
        # FreeCADGui.Control.closeDialog()
        return False

    def claimChildren(self):
        return [self.Object.Result]

    def getDisplayModes(self, obj):
        return ["Standard"]

    def getDefaultDisplayMode(self):
        return "Standard"

    def updateData(self, fp, prop):
        pass

    def __getstate__(self):
        return None

    def __setstate__(self, state):
        return None


def createReport(fileObject=None):
    import Spreadsheet

    reportObject = FreeCAD.ActiveDocument.addObject(
        "App::FeaturePython", "Report")
    report = Report(reportObject)

    if fileObject is not None:
        report.importJson(fileObject)

    result = FreeCAD.ActiveDocument.addObject("Spreadsheet::Sheet", "Result")
    reportObject.Result = result

    ViewProviderReport(reportObject.ViewObject)


if __name__ == "__main__":
    if FreeCAD.ActiveDocument is None:
        print('Create a document to continue.')
    else:
        createReport()
