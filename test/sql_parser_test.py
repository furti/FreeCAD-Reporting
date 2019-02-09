from sql import sql_parser


class ProxyObject(object):
    pass


class DocumentObject(object):
    def __init__(self, name, tag, role, num, list=None):
        self.name = name
        self.tag = tag
        self.role = role
        self.num = num
        self.list = list

    def __str__(self):
        return 'name: %s, tag: %s, role: %s, num: %s' % (self.name, self.tag, self.role, self.num)


list1 = ['list1']
list2 = ['list2']

wall = DocumentObject('Wall', 'inside', 'wall', 1, list1)
window = DocumentObject('Window', 'living', 'window', 2, list1)
space = DocumentObject('Space', 'living', 'space', 3, list2)
space001 = DocumentObject('Space001', 'bedroom', 'space', 4, list1)
space002 = DocumentObject('Space002', 'bedroom', 'space', 5, list2)
space003 = DocumentObject('Space003', 'something', 'space', 6)
norole = DocumentObject('Something', None, None, None)

norole.Proxy = ProxyObject()

documentObjects = [
    wall,
    window,
    space,
    space001,
    space002,
    space003,
    norole
]


def documentObjectsSupplier():
    return documentObjects


def singleObjectSupplier(objectName):
    return [documentObject for documentObject in documentObjects if documentObject.name == objectName]


sqlParser = sql_parser.newParser(documentObjectsSupplier, singleObjectSupplier)


def executeStatement(statementString, doPrint=True, includeStatement=False):
    print('--------------------------------')

    print(statementString)
    statement = sqlParser.parse(statementString)

    if doPrint:
        print(statement)

    result = statement.execute()

    if doPrint:
        for columns in result:
            print([str(element) for element in columns])

    if includeStatement:
        return (result, statement)
    else:
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
                      [space001], [space002], [space003], [norole]]


def selectAsteriskFromWall():
    result = executeStatement('Select * From Wall')

    assert result == [[wall]]


def selectNameFromDocument():
    result = executeStatement('Select name From document')

    assert result == [['Wall'], ['Window'], [
        'Space'], ['Space001'], ['Space002'], ['Space003'], ['Something']]


def selectNameAndStaticValuesFromDocument():
    result = executeStatement("Select name, 42,'literal' From document")

    assert result == [['Wall', 42, 'literal'], ['Window', 42, 'literal'], [
        'Space', 42, 'literal'], ['Space001', 42, 'literal'], ['Space002', 42, 'literal'], ['Space003', 42, 'literal'], ['Something', 42, 'literal']]


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


def selectWithBracketsWhereClauseReversed():
    result = executeStatement(
        "Select * From document Where (tag = 'living' or tag='something') and role = 'space'")

    assert result == [[space], [space003]]


def shouldFilterNoneAttributes():
    result = executeStatement(
        "Select * From document Where role IS NOT Null")

    assert result == [[wall], [window],  [space],
                      [space001], [space002], [space003]]


def shouldOnlyShowNoneAttributes():
    result = executeStatement(
        "Select * From document Where role IS Null")

    assert result == [[norole]]


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


def selectWithUnknownPropertyShouldIgnoreObject():
    result = executeStatement(
        "Select * From document Where unkown = 'bedroom'")

    assert result == []


def selectStateShouldBeResetBetweenCalls():
    result, statement = executeStatement(
        "Select Count(*) From document Where role = 'space'", includeStatement=True)

    assert result == [[4]]

    result = statement.execute()

    print(result)

    assert result == [[4]]


def columnNamesShouldBeCorrect():
    result, statement = executeStatement(
        "Select name, 42,'literal' From document", includeStatement=True)

    columnNames = statement.getColumnNames()

    print(columnNames)

    assert columnNames == ['name', '42', 'literal']


def runGroupByClause():
    result = executeStatement(
        "Select role, count(*) From document Group By role")

    assert result == [['wall', 1], ['window', 1], ['space', 4], [None, 1]]


def invalidGroupByClauseShouldThrow():
    exceptionMessage = None

    try:
        result = executeStatement(
            "Select name, count(*) From document Group By role")
    except sql_parser.SqlStatementValidationError as e:
        exceptionMessage = str(e)

    assert exceptionMessage == 'Only columns from the group by clause are allowed in the select clause'


def staticColumnAndFunction():
    result = executeStatement(
        "Select 'Sum', Sum(num) From document")

    assert result == [['Sum', 21]]


def emptyResultShouldNotThrowOnFunction():
    result = executeStatement(
        "Select count(*) From document where role = 'xxx'")

    assert result == []


def concatFunction():
    result = executeStatement(
        "Select concat(tag, ' ', role) From document")

    assert result == [['inside wall'], ['living window'], ['living space'],
                      ['bedroom space'], ['bedroom space'], ['something space'], [' ']]


def concatFunctionInGroupBy():
    result = executeStatement(
        "Select concat(tag, ' ', role), count(*) From document Group By concat(tag, ' ', role)")

    assert result == [['inside wall', 1], ['living window', 1], ['living space', 1],
                      ['bedroom space', 2], ['something space', 1], [' ', 1]]


def unhashableTypeInGroupBy():
    result = executeStatement(
        "Select list, count(*) From document Where list IS NOT NULL Group By list")

    assert result == [[list1, 3], [list2, 2]]


def typeFunction():
    result = executeStatement(
        "Select type(*) From document")

    assert result == [['test.sql_parser_test.DocumentObject'], ['test.sql_parser_test.DocumentObject'],
                      ['test.sql_parser_test.DocumentObject'], ['test.sql_parser_test.DocumentObject'], ['test.sql_parser_test.DocumentObject'], ['test.sql_parser_test.DocumentObject'], ['test.sql_parser_test.ProxyObject']]

def renamedColumnNamesShouldBeCorrect():
    result, statement = executeStatement(
        "Select name As 'Something', 42 As 'Number','literal' From document", includeStatement=True)

    columnNames = statement.getColumnNames()

    print('columnNames %s' % (columnNames))

    assert columnNames == ['Something', 'Number', 'literal']

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
    selectWithBracketsWhereClauseReversed()
    shouldFilterNoneAttributes()
    shouldOnlyShowNoneAttributes()
    selectWithSumFunction()
    selectWithCountFunction()
    selectWithMinFunction()
    selectWithMaxFunction()
    selectWithUnknownPropertyShouldIgnoreObject()
    selectStateShouldBeResetBetweenCalls()
    columnNamesShouldBeCorrect()
    runGroupByClause()
    invalidGroupByClauseShouldThrow()
    staticColumnAndFunction()
    emptyResultShouldNotThrowOnFunction()
    concatFunction()
    concatFunctionInGroupBy()
    unhashableTypeInGroupBy()
    typeFunction()
    renamedColumnNamesShouldBeCorrect()
