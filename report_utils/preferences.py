try:
    import FreeCAD

    params = FreeCAD.ParamGet('User parameter:Plugins/Furti/Reporting')
except ModuleNotFoundError:
    class DummyParams(object):
        def __init__(self):
            self.debug = False
        
        def GetBool(self, paramName, defaultValue=False):
            if paramName == 'Debug':
                return self.debug
            
            return defaultValue
        
    params = DummyParams()



def debug():
    return params.GetBool('Debug')


def setupMissingParams():
    if params.GetBool('Debug') is False:
        params.SetBool('Debug', False)
