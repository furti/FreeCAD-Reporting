import FreeCAD
import FreeCADGui
from pivy import coin
from report_utils.resource_utils import uiPath

from PySide2.QtWidgets import QTableWidgetItem, QTextEdit


class ReportConfigTable():
    def __init__(self, report, qtTable):
        self.report = report
        self.qtTable = qtTable

        # self.qtTable.itemDoubleClicked.connect(self.doubleClicked)

        self.setupTable()

    def setupTable(self):
        for statement in self.report.statements:
            self.addRow(statement.header, statement.plainTextStatement)

    def addRow(self, header=None, statement=None):
        rowPosition = self.qtTable.rowCount()
        self.qtTable.insertRow(rowPosition)

        headerEdit = QTableWidgetItem(header)
        statementEdit = QTextEdit(statement)

        self.qtTable.setItem(rowPosition, 0, headerEdit)
        self.qtTable.setCellWidget(rowPosition, 1, statementEdit)

    def removeRow(self):
        selectionModel = self.qtTable.selectionModel()

        if selectionModel.hasSelection():
            for selection in selectionModel.selectedRows():
                self.qtTable.removeRow(selection.row())

    def saveIntoConfig(self):
        self.report.statements.clear()

        for row in range(self.qtTable.rowCount()):
            headerEdit = self.qtTable.item(row, 0)
            statementEdit = self.qtTable.cellWidget(row, 1)

            reportStatement = ReportStatement(headerEdit.text(), statementEdit.toPlainText())

            self.report.statements.append(reportStatement)


class ReportConfigPanel():
    def __init__(self, report, freecadObject):
        self.report = report
        self.freecadObject = freecadObject

        self.form = FreeCADGui.PySideUic.loadUi(uiPath('report_config.ui'))

        self.reportConfigTable = ReportConfigTable(
            self.report, self.form.ReportTable)
        self.form.AddStatementButton.clicked.connect(
            self.reportConfigTable.addRow)
        self.form.RemoveStatementButton.clicked.connect(
            self.reportConfigTable.removeRow)

    def accept(self):
        self.reportConfigTable.saveIntoConfig()

        FreeCADGui.Control.closeDialog()

        self.report.execute(self.freecadObject)

    def reject(self):
        FreeCADGui.Control.closeDialog()


class ReportStatement(object):
    def __init__(self, header, plainTextStatement):
        self.header = header
        self.plainTextStatement = plainTextStatement


class Report():
    def __init__(self, obj, fileObject=None):
        obj.Proxy = self

        obj.addProperty("App::PropertyBool", "SkipComputing", "Settings",
                        "When true no calculation of this report is performed, even when the document gets recomputed").SkipComputing = False

        obj.addProperty("App::PropertyLink", "Result", "Settings",
                        "The spreadsheet to print the results to")

        self.statements = [
            # ReportStatement, ...
        ]

    def execute(self, fp):
        if fp.SkipComputing:
            return

        if not fp.Result:
            FreeCAD.Console.PrintError(
                'No spreadsheet attached to %s. Could not recompute result' % (fp.Label))

        spreadsheet = fp.Result

        spreadsheet.clearAll()

        spreadsheet.set("A1", "Test")
        spreadsheet.set("B1", "More")

        spreadsheet.setStyle('A1:B1', 'bold', 'add')

        spreadsheet.recompute()

    def __getstate__(self):
        return None

    def __setstate__(self, state):
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


def createReport():
    import Spreadsheet

    reportObject = FreeCAD.ActiveDocument.addObject(
        "App::FeaturePython", "Report")
    report = Report(reportObject)

    result = FreeCAD.ActiveDocument.addObject("Spreadsheet::Sheet", "Result")
    reportObject.Result = result

    ViewProviderReport(reportObject.ViewObject)


if __name__ == "__main__":
    if FreeCAD.ActiveDocument is None:
        print('Create a document to continue.')
    else:
        createReport()
