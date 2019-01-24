from collections import OrderedDict
import FreeCAD, FreeCADGui

class ReportingToolbarManager:
    Toolbars =  OrderedDict()

    def registerCommand(self, command):
        FreeCADGui.addCommand(command.commandName, command)
        self.Toolbars.setdefault(command.toolbarName, []).append(command)

toolbarManager = ReportingToolbarManager()

# import commands here
import create_report
import export_report_config
import import_report_config