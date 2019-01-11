from sql import sql_parser


class DocumentObject(object):
    def __init__(self, name, tag, role, num):
        self.name = name
        self.tag = tag
        self.role = role
        self.num = num

    def __str__(self):
        return 'name: %s, tag: %s, role: %s, num: %s' % (self.name, self.tag, self.role, self.num)


wall = DocumentObject('Wall', 'inside', 'wall', 1)
window = DocumentObject('Window', 'living', 'window', 2)
space = DocumentObject('Space', 'living', 'space', 3)
space001 = DocumentObject('Space001', 'bedroom', 'space', 4)
space002 = DocumentObject('Space002', 'bedroom', 'space', 5)
space003 = DocumentObject('Space003', 'something', 'space', 6)

documentObjects = [
    wall,
    window,
    space,
    space001,
    space002,
    space003
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
        for columns in result:
            print([element.__str__() for element in columns])

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

    assert result == [[wall], [window],  [space],
                      [space001], [space002], [space003]]


def selectAsteriskFromWall():
    result = executeStatement('Select * From Wall')

    assert result == [[wall]]


def selectNameFromDocument():
    result = executeStatement('Select name From document')

    assert result == [['Wall'], ['Window'], [
        'Space'], ['Space001'], ['Space002'], ['Space003']]


def selectNameAndStaticValuesFromDocument():
    result = executeStatement("Select name, 42,'literal' From document")

    assert result == [['Wall', 42, 'literal'], ['Window', 42, 'literal'], [
        'Space', 42, 'literal'], ['Space001', 42, 'literal'], ['Space002', 42, 'literal'], ['Space003', 42, 'literal']]


def selectWithSimpleWhereClause():
    result = executeStatement("Select * From document Where name = 'Wall'")

    assert result == [[wall]]


def selectWithAndWhereClause():
    result = executeStatement(
        "Select * From document Where role = 'space' and tag = 'bedroom'")

    assert result == [[space001], [space002]]


def selectWithOrWhereClause():
    result = executeStatement(
        "Select * From document Where role = 'space' or tag = 'inside'")

    assert result == [[wall], [space], [space001], [space002], [space003]]


def selectWithBracketsWhereClause():
    result = executeStatement(
        "Select * From document Where role = 'space' and (tag = 'living' or tag='something')")

    assert result == [[space], [space003]]

def selectWithSumFunction():
    result = executeStatement(
        "Select Sum(num) From document")

    assert result == [[21]]

def selectWithCountFunction():
    result = executeStatement(
        "Select Count(*) From document Where role = 'space'")

    assert result == [[4]]

def selectWithMinFunction():
    result = executeStatement(
        "Select Min(num) From document")

    assert result == [[1]]

def selectWithMaxFunction():
    result = executeStatement(
        "Select Max(num) From document")

    assert result == [[6]]

def run():
    statementShouldParseWithDifferentStyles()
    selectAsteriskFromDocument()
    selectAsteriskFromWall()
    selectNameFromDocument()
    selectNameAndStaticValuesFromDocument()
    selectWithSimpleWhereClause()
    selectWithAndWhereClause()
    selectWithOrWhereClause()
    selectWithBracketsWhereClause()
    selectWithSumFunction()
    selectWithCountFunction()
    selectWithMinFunction()
    selectWithMaxFunction()
