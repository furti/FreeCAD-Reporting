import FreeCAD
import FreeCADGui


class ReportingWorkbench (FreeCADGui.Workbench):
    "SQL Like Reporting for FreeCAD"

    MenuText = "Reporting"
    ToolTip = "Create Reports using SQL"

    def __init__(self):
        from report_utils.resource_utils import iconPath
        self.__class__.Icon = iconPath("Workbench.svg")

    def Initialize(self):
        # Initialize the module
        import reporting_toolbars

        for name, commands in reporting_toolbars.toolbarManager.Toolbars.items():
            self.appendToolbar(
                name, [command.commandName for command in commands])

#    def Activated(self):

#   def Deactivated(self):


FreeCADGui.addWorkbench(ReportingWorkbench())

# Setup Preferences
from report_utils import preferences

preferences.setupMissingParams()
