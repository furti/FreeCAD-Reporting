import FreeCAD
import FreeCADGui

from report_utils.resource_utils import iconPath
from report_utils.selection_utils import findSelectedReportConfig
from report_utils import qtutils

XLSX_FILES = "XLSX Files (*.xlsx)"

class ExportReportXLSCommand:
    toolbarName = 'Reporting_Tools'
    commandName = 'Export_Report_XLS'

    def GetResources(self):
        return {'MenuText': "Export Report XLS",
                'ToolTip': "Exports the configuration stored inside the Report object to a XLS file",
                'Pixmap': iconPath('ExportConfig.svg')
                }

    def Activated(self):
        reportConfig = findSelectedReportConfig()

        if reportConfig is None:
            qtutils.showInfo(
                "No Report selected", "Select exactly one Report object to export its content")

            return

        selectedFile = qtutils.userSelectedFile(
            'Export Location', XLSX_FILES, False)

        if selectedFile is None:
            return

        reportConfig.exportXLS(selectedFile)

    def IsActive(self):
        """If there is no active document we can't do anything."""
        return not FreeCAD.ActiveDocument is None


if __name__ == "__main__":
    command = ExportReportXLSCommand()

    if command.IsActive():
        command.Activated()
    else:
        qtutils.showInfo("No open Document", "There is no open document")
else:
    import reporting_toolbars
    reporting_toolbars.toolbarManager.registerCommand(
        ExportReportXLSCommand())
