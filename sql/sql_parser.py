from . import sql_grammar


def printElements(elements):
    for element in elements:
        print(element)


class SelectStatement(object):
    def __init__(self):
        self.documentObjectsSupplier = None
        self.singleObjectSupplier = None
        self.columns = None
        self.fromClause = None
        self.whereClause = None

    def execute(self):
        objectList = self.getObjectList()

        result = self.columns.execute(objectList)

        return result

    def getObjectList(self):
        objectList = self.fromClause.getObjects(
            self.documentObjectsSupplier, self.singleObjectSupplier)

        if self.whereClause is None:
            return objectList
        else:
            return [o for o in objectList if self.whereClause.matches(o)]

    def __str__(self):
        return 'Select %s %s %s' % (self.columns, self.fromClause, self.whereClause)


class Columns(object):
    def __init__(self, columns):
        self.columns = columns

    def execute(self, objectList):
        result = []

        for o in objectList:
            result.append([column.execute(o) for column in self.columns])

        return result

    def __str__(self):
        return '%s' % [column.__str__() for column in self.columns]


class Column(object):
    def __init__(self, columnName, dataExtractor, grouping):
        self.columnName = columnName
        self.dataExtractor = dataExtractor
        self.grouping = grouping

    def execute(self, o):
        return self.dataExtractor.extract(o)

    def __str__(self):
        return '%s:%s' % (self.columnName, self.dataExtractor)


class FromClause(object):
    def __init__(self, reference):
        self.reference = reference

    def getObjects(self, documentObjectsSupplier, singleObjectSupplier):
        referenceValue = self.reference.value

        if(referenceValue == 'document'):
            return documentObjectsSupplier()
        else:
            return singleObjectSupplier(referenceValue)

    def __str__(self):
        return 'From %s' % self.reference


class WhereClause(object):
    def __init__(self, booleanExpression):
        if booleanExpression is None:
            raise ValueError('BooleanExpression must not be None')

        self.booleanExpression = booleanExpression

    def matches(self, o):
        return self.booleanExpression.execute(o)

    def __str__(self):
        return 'Where %s' % (self.booleanExpression)


class IdentityExtractor(object):
    def extract(self, o):
        return o

    def __str__(self):
        return '$identity'


class StaticExtractor(object):
    def __init__(self, value):
        self.value = value

    def extract(self, o):
        return self.value

    def __str__(self):
        return '$%s' % (self.value)


class ReferenceExtractor(object):
    def __init__(self, ref):
        self.ref = ref

    def extract(self, o):
        return self.ref.getValue(o)

    def __str__(self):
        return self.ref.__str__()


class Reference(object):
    def __init__(self, value):
        self.value = value

    def getValue(self, o):
        return getattr(o, self.value)

    def __str__(self):
        return '$%s' % self.value


class Asterisk(object):
    def __init__(self):
        pass

# Boolean Start


class BooleanExpression(object):
    def execute(self, o):
        raise NotImplementedError('Subclasses must override this method')


class SimpleBooleanExpression(BooleanExpression):
    def __init__(self, leftExpression, rightExpression, booleanOperator):
        self.leftExpression = leftExpression
        self.rightExpression = rightExpression
        self.booleanOperator = booleanOperator

    def execute(self, o):
        left = self.leftExpression.execute(o)
        right = self.rightExpression.execute(o)

        return self.booleanOperator.compare(left, right)

    def __str__(self):
        return '%s %s %s' % (self.leftExpression, self.booleanOperator, self.rightExpression)


class BooleanComparison(BooleanExpression):
    def __init__(self, leftDataExtractor, rightDataExtractor, comparisonOperator):
        self.leftDataExtractor = leftDataExtractor
        self.rightDataExtractor = rightDataExtractor
        self.comparisonOperator = comparisonOperator

    def execute(self, o):
        left = self.leftDataExtractor.extract(o)
        right = self.rightDataExtractor.extract(o)

        return self.comparisonOperator.compare(left, right)

    def __str__(self):
        return '%s %s %s' % (self.leftDataExtractor, self.comparisonOperator, self.rightDataExtractor)


class GreaterThanOrEqualsComparisonOperator(object):
    def compare(self, left, right):
        return left >= right

    def __str__(self):
        return '>='


class LessThanOrEqualsComparisonOperator(object):
    def compare(self, left, right):
        return left <= right

    def __str__(self):
        return '<='


class NotEqualsComparisonOperator(object):
    def compare(self, left, right):
        return left != right

    def __str__(self):
        return '!='


class EqualsComparisonOperator(object):
    def compare(self, left, right):
        return left == right

    def __str__(self):
        return '='


class GreaterThanComparisonOperator(object):
    def compare(self, left, right):
        return left > right

    def __str__(self):
        return '>'


class LessThanComparisonOperator(object):
    def compare(self, left, right):
        return left < right

    def __str__(self):
        return '<'


class AndBooleanOperator(object):
    def compare(self, left, right):
        return left and right

    def __str__(self):
        return 'AND'


class OrBooleanOperator(object):
    def compare(self, left, right):
        return left or right

    def __str__(self):
        return 'OR'
# Boolean end


def findReference(elements):
    for element in elements:
        if isinstance(element, Reference):
            return element


def findBooleanExpression(elements):
    for element in elements:
        if isinstance(element, BooleanExpression):
            return element


def findExtractor(element):
    if isinstance(element, Asterisk):
        return (IdentityExtractor(), '*', False)

    if isinstance(element, int) or isinstance(element, str):
        return (StaticExtractor(element), str(element), False)

    if isinstance(element, Reference):
        return (ReferenceExtractor(element), element.value, False)

    # if isinstance(element, Calculation):
    #     return (CalculationExtractor(element), element.name, True)

    return (None, None, None)


def extractColumns(elements):
    columns = []

    for element in elements:
        extractor, name, grouping = findExtractor(element)

        if extractor is not None:
            columns.append(Column(name, extractor, grouping))
        elif hasattr(element, 'elements'):
            columns.extend(extractColumns(element.elements))

    return columns


def prepareSelectStatement(statement, elements):
    for element in elements:
        if isinstance(element, FromClause):
            statement.fromClause = element
        elif isinstance(element, Columns):
            statement.columns = element
        elif isinstance(element, WhereClause):
            statement.whereClause = element


class ParserActions(object):
    def make_statement(self, input, start, end, elements):
        selectStatement = SelectStatement()

        prepareSelectStatement(selectStatement, elements)

        return selectStatement

    def make_reference(self, input, start, end, elements):
        value = input[start:end]

        return Reference(value)

    def prepare_columns(self, input, start, end, elements):
        columns = extractColumns(elements)

        return Columns(columns)

    def prepare_from_clause(self, input, start, end, elements):
        reference = findReference(elements)

        return FromClause(reference)

    def prepare_where_clause(self, input, start, end, elements):
        booleanExpression = findBooleanExpression(elements)

        return WhereClause(booleanExpression)

    def make_boolean_comparison(self, input, start, end, elements):
        leftDataExctractor = findExtractor(elements[0])
        comparisonOperator = elements[2]
        rightDataExtractor = findExtractor(elements[4])

        return BooleanComparison(leftDataExctractor[0], rightDataExtractor[0], comparisonOperator)

    def make_simple_boolean_expression(self, input, start, end, elements):
        leftExpression = elements[0]
        booleanOperator = elements[2]
        rightExpression = elements[4]

        return SimpleBooleanExpression(leftExpression, rightExpression, booleanOperator)

    def make_asterisk(self, input, start, end):
        return Asterisk()

    def make_number(self, input, start, end, elements):
        return int(input[start:end], 10)

    def make_literal(self, input, start, end, elements):
        return input[start + 1:end - 1]

    def make_comp_operator_gte(self, input, start, end):
        return GreaterThanOrEqualsComparisonOperator()

    def make_comp_operator_lte(self, input, start, end):
        return LessThanOrEqualsComparisonOperator()

    def make_comp_operator_neq(self, input, start, end):
        return NotEqualsComparisonOperator()

    def make_comp_operator_eq(self, input, start, end):
        return EqualsComparisonOperator()

    def make_comp_operator_gt(self, input, start, end):
        return GreaterThanComparisonOperator()

    def make_comp_operator_lt(self, input, start, end):
        return LessThanComparisonOperator()

    def make_boolean_operator_and(self, input, start, end):
        return AndBooleanOperator()

    def make_boolean_operator_or(self, input, start, end):
        return OrBooleanOperator()


class SqlParser(object):
    def __init__(self, documentObjectsSupplier, singleObjectSupplier):
        if documentObjectsSupplier is None:
            raise AssertionError('documentObjectsSupplier must not be none')

        if singleObjectSupplier is None:
            raise AssertionError('singleObjectSupplier must not be none')

        self.documentObjectsSupplier = documentObjectsSupplier
        self.singleObjectSupplier = singleObjectSupplier

    def parse(self, sqlString):
        sqlStatement = sql_grammar.parse(sqlString, actions=ParserActions())

        sqlStatement.documentObjectsSupplier = self.documentObjectsSupplier
        sqlStatement.singleObjectSupplier = self.singleObjectSupplier

        return sqlStatement


def newParser(documentObjectsSupplier, singleObjectSupplier):
    return SqlParser(documentObjectsSupplier, singleObjectSupplier)
