import FreeCAD
from pivy import coin


class Report():
    def __init__(self, obj, fileObject=None):
        obj.Proxy = self

        obj.addProperty("App::PropertyBool", "SkipComputing", "Settings",
                        "When true no calculation of this report is performed, even when the document gets recomputed").SkipComputing = False

        obj.addProperty("App::PropertyLink", "Result", "Settings",
                        "The spreadsheet to print the results to")

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
        self.textureConfig = self.Object.Proxy

        self.coinNode = coin.SoGroup()
        vobj.addDisplayMode(self.coinNode, "Standard")

    def onChanged(self, vp, prop):
        pass

    def doubleClicked(self, vobj):
        return self.setEdit(vobj, 0)

    def setEdit(self, vobj, mode):
        if mode == 0:
            print('edit')
        #     panel = TextureConfigPanel(self.textureConfig, self.Object)
        #     FreeCADGui.Control.showDialog(panel)

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
