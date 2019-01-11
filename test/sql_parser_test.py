from sql import sql_parser


class DocumentObject(object):
    def __init__(self, name):
        self.name = name


wall = DocumentObject('Wall')
window = DocumentObject('Window')
space = DocumentObject('Space')
space001 = DocumentObject('Space001')
space002 = DocumentObject('Space002')

documentObjects = [
    wall,
    window,
    space,
    space001,
    space002
]


def documentObjectsSupplier():
    return documentObjects


def singleObjectSupplier(objectName):
    return [documentObject for documentObject in documentObjects if documentObject.name == objectName]


sqlParser = sql_parser.newParser(documentObjectsSupplier, singleObjectSupplier)


def executeStatement(statementString, doPrint=True):
    print('--------------------------------')

    print(statementString)
    statement = sqlParser.parse(statementString)
    
    if doPrint:
        print(statement)

    result = statement.execute()

    if doPrint:
        print(result)

    return result

# Test Cases


def statementShouldParseWithDifferentStyles():
    # With Semicolon
    executeStatement('Select * From document;')

    # Without Semicolon
    executeStatement('Select * From document')

    # With newlines
    executeStatement('Select * \nFrom document\n;')


def selectAsteriskFromDocument():
    result = executeStatement('Select * From document')

    assert result == [[wall], [window],  [space], [space001], [space002]]


def selectAsteriskFromWall():
    result = executeStatement('Select * From Wall')

    assert result == [[wall]]


def selectNameFromDocument():
    result = executeStatement('Select name From document')

    assert result == [['Wall'], ['Window'], [
        'Space'], ['Space001'], ['Space002']]


def selectNameAndStaticValuesFromDocument():
    result = executeStatement("Select name, 42,'literal' From document")

    assert result == [['Wall', 42, 'literal'], ['Window', 42, 'literal'], [
        'Space', 42, 'literal'], ['Space001', 42, 'literal'], ['Space002', 42, 'literal']]

def selectWithSimpleWhereClause():
    result = executeStatement("Select * From document Where name = 'Wall'")

    assert result == [[wall]]

def run():
    statementShouldParseWithDifferentStyles()
    selectAsteriskFromDocument()
    selectAsteriskFromWall()
    selectNameFromDocument()
    selectNameAndStaticValuesFromDocument()
    selectWithSimpleWhereClause()
