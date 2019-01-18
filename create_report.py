import FreeCAD
import FreeCADGui

import report


class CreateReportCommand:
    toolbarName = 'Reporting_Tools'
    commandName = 'Create_Report'

    def GetResources(self):
        from report_utils.resource_utils import iconPath
        return {'MenuText': "Create Report",
                'ToolTip': "Create a new Report object to execute SQL Statements",
                'Pixmap': iconPath('CreateConfig.svg')
                }

    def Activated(self):
        report.createReport()

    def IsActive(self):
        """If there is no active document we can't do anything."""
        return not FreeCAD.ActiveDocument is None


if __name__ == "__main__":
    command = CreateReportCommand()

    if command.IsActive():
        command.Activated()
    else:
        qtutils.showInfo("No open Document", "There is no open document")
else:
    import reporting_toolbars
    reporting_toolbars.toolbarManager.registerCommand(
        CreateReportCommand())
