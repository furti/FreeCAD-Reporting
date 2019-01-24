import FreeCAD
import FreeCADGui

import report
from report_utils.resource_utils import iconPath
from report_utils.selection_utils import findSelectedReportConfig
from report_utils import qtutils


class ImportReportConfigCommand:
    toolbarName = 'Reporting_Tools'
    commandName = 'Import_Report'

    def GetResources(self):
        return {'MenuText': "Import Report",
                'ToolTip': "Import a new Report object from a JSOn File",
                'Pixmap': iconPath('ImportConfig.svg')
                }

    def Activated(self):
        selectedFile = qtutils.userSelectedFile(
            'Config File', qtutils.JSON_FILES)

        if selectedFile is None:
            return

        fileObject = open(selectedFile, 'r')

        report.createReport(fileObject)

    def IsActive(self):
        """If there is no active document we can't do anything."""
        return not FreeCAD.ActiveDocument is None


if __name__ == "__main__":
    command = ImportReportConfigCommand()

    if command.IsActive():
        command.Activated()
    else:
        qtutils.showInfo("No open Document", "There is no open document")
else:
    import reporting_toolbars
    reporting_toolbars.toolbarManager.registerCommand(
        ImportReportConfigCommand())
