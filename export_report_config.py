import FreeCAD
import FreeCADGui

from report_utils.resource_utils import iconPath
from report_utils.selection_utils import findSelectedReportConfig
from report_utils import qtutils


class ExportReportConfigCommand:
    toolbarName = 'Reporting_Tools'
    commandName = 'Export_Report'

    def GetResources(self):
        return {'MenuText': "Export Report",
                'ToolTip': "Exports the configuration stored inside the Report object to a JSON file",
                'Pixmap': iconPath('ExportConfig.svg')
                }

    def Activated(self):
        reportConfig = findSelectedReportConfig()

        if reportConfig is None:
            qtutils.showInfo(
                "No Report selected", "Select exactly one Report object to export its content")

            return

        selectedFile = qtutils.userSelectedFile(
            'Export Location', qtutils.JSON_FILES, False)

        if selectedFile is None:
            return

        fileObject = open(selectedFile, 'w')

        reportConfig.exportJson(fileObject)

    def IsActive(self):
        """If there is no active document we can't do anything."""
        return not FreeCAD.ActiveDocument is None


if __name__ == "__main__":
    command = ExportReportConfigCommand()

    if command.IsActive():
        command.Activated()
    else:
        qtutils.showInfo("No open Document", "There is no open document")
else:
    import reporting_toolbars
    reporting_toolbars.toolbarManager.registerCommand(
        ExportReportConfigCommand())
