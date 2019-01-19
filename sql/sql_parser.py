from itertools import groupby
from . import sql_grammar
from report_utils import logger


def printElements(elements, intent=''):
    for element in elements:
        if(hasattr(element, 'text')):
            print('%s{"%s" (%s)}' % (intent, element.text, element))
        else:
            print('%s{%s}' % (intent, element))

        if(hasattr(element, 'elements')):
            printElements(element.elements, intent + '  ')


class SqlStatementValidationError(Exception):
    def __init__(self, message):
        super().__init__(message)


class SelectStatement(object):
    def __init__(self):
        self.documentObjectsSupplier = None
        self.singleObjectSupplier = None
        self.columns = None
        self.fromClause = None
        self.whereClause = None
        self.groupByClause = None

    def validate(self):
        if self.columns is None:
            raise SqlStatementValidationError('No columns defined')

        if self.fromClause is None:
            raise SqlStatementValidationError('No fromClause defined')

        if self.groupByClause is not None:
            self.groupByClause.validate()
            self.columns.validate(self.groupByClause.columns)
        else:
            self.columns.validate()

    def execute(self):
        self.resetState()

        objectList = self.getObjectList()

        if self.groupByClause is not None:
            groupedList = self.groupByClause.execute(objectList)

            result = self.columns.executeWithGroups(groupedList)
        else:
            result = self.columns.execute(objectList)

        return result

    def getColumnNames(self):
        return self.columns.getNames()

    def getObjectList(self):
        objectList = self.fromClause.getObjects(
            self.documentObjectsSupplier, self.singleObjectSupplier)

        if self.whereClause is None:
            return objectList
        else:
            return [o for o in objectList if self.whereClause.matches(o)]

    def resetState(self):
        self.columns.resetState()

        if self.groupByClause is not None:
            self.groupByClause.resetState()

    def __str__(self):
        return 'Select %s %s %s' % (self.columns, self.fromClause, self.whereClause)


class Columns(object):
    def __init__(self, columns):
        self.columns = columns
        self.grouping = True in [column.grouping for column in columns]

    def validate(self, groupByColumns=None):
        if groupByColumns is None:
            self.validateNonGrouping()
        else:
            self.validateGrouping(groupByColumns)

    def validateGrouping(self, groupByColumns):
        # All non grouping columns must also be in the group by clause
        nonGroupingColumns = [
            column for column in self.columns if not column.grouping]

        for column in nonGroupingColumns:
            if not column in groupByColumns:
                raise SqlStatementValidationError(
                    'Only columns from the group by clause are allowed in the select clause')

    def validateNonGrouping(self):
        groupingFound = False
        nonGroupingFound = False

        for column in self.columns:
            if column.grouping:
                groupingFound = True
            else:
                nonGroupingFound = True

        if groupingFound and nonGroupingFound:
            raise SqlStatementValidationError(
                'Can not mix functions and non functions in select clause')

    def execute(self, objectList):
        result = []

        for o in objectList:
            result.append([column.execute(o) for column in self.columns])

        if self.grouping:
            return [result[-1]]

        return result

    def executeWithGroups(self, groupedList):
        result = []

        for objectList in groupedList:
            # Lets reset all function state before each group
            self.resetState()

            groupResult = [None] * len(self.columns)

            for o in objectList:
                for index, column in enumerate(self.columns):
                    if column.grouping:
                        groupResult[index] = column.execute(o)
                    elif groupResult[index] is None:
                        # It is enough to execute non grouping columns only once
                        # They should give us the same result for each element in the group
                        groupResult[index] = column.execute(o)

            result.append(groupResult)

        return result

    def getNames(self):
        return [column.columnName for column in self.columns]

    def resetState(self):
        if self.grouping:
            for column in self.columns:
                column.resetState()

    def __str__(self):
        return '%s' % [column.__str__() for column in self.columns]


class Column(object):
    def __init__(self, columnName, dataExtractor, grouping):
        self.columnName = columnName
        self.dataExtractor = dataExtractor
        self.grouping = grouping

    def execute(self, o):
        return self.dataExtractor.extract(o)

    def resetState(self):
        if self.grouping:
            self.dataExtractor.resetState()

    def __str__(self):
        return '%s:%s' % (self.columnName, self.dataExtractor)

    def __eq__(self, obj):
        if not isinstance(obj, Column):
            return False

        return self.dataExtractor == obj.dataExtractor


class GroupByClause(object):
    def __init__(self, columns):
        self.columns = columns

    def validate(self):
        for column in self.columns:
            if column.grouping:
                raise SqlStatementValidationError(
                    'Can not use functions in group by clause')

            if isinstance(column.dataExtractor, IdentityExtractor):
                raise SqlStatementValidationError(
                    'Can not use * in group by clause')

    def execute(self, objectList):
        groups = {}

        for o in objectList:
            keys = self.extractColumns(o)

            if not keys in groups:
                groups[keys] = []

            groups[keys].append(o)

        groupedList = []

        for key, group in groups.items():
            logger.debug('Group %s:%s', (key, [o for o in group]))
            groupedList.append([o for o in group])

        return groupedList

    def extractColumns(self, o):
        return tuple([column.execute(o) for column in self.columns])

    def resetState(self):
        # Nothing to reset for now. No functions allowed in group by clause
        pass

    def __str__(self):
        return '%s' % [column.__str__() for column in self.columns]


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

    def resetState(self):
        pass

    def __str__(self):
        return '$identity'

    def __eq__(self, obj):
        return isinstance(obj, IdentityExtractor)


class StaticExtractor(object):
    def __init__(self, value):
        self.value = value

    def extract(self, o):
        return self.value

    def resetState(self):
        pass

    def __str__(self):
        if isinstance(self.value, str):
            return "'%s'" % (self.value)
        else:
            return '%s' % (self.value)

    def __eq__(self, obj):
        return isinstance(obj, StaticExtractor)


class ReferenceExtractor(object):
    def __init__(self, ref):
        self.ref = ref

    def extract(self, o):
        return self.ref.getValue(o)

    def resetState(self):
        pass

    def __str__(self):
        return self.ref.__str__()

    def __eq__(self, obj):
        return isinstance(obj, ReferenceExtractor) and self.ref == obj.ref


class CalculationExtractor(object):
    def __init__(self, calculation):
        self.calculation = calculation
        self.currentValue = None

    def extract(self, o):
        self.currentValue = self.calculation.execute(o, self.currentValue)

        return self.currentValue

    def resetState(self):
        self.currentValue = None

    def __str__(self):
        return '%s' % (self.calculation)


class Reference(object):
    def __init__(self, value):
        self.value = value

    def getValue(self, o):
        if hasattr(o, self.value):
            return getattr(o, self.value)

        return None

    def __str__(self):
        return '$%s' % self.value

    def __eq__(self, obj):
        return isinstance(obj, Reference) and self.value == obj.value


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
        return '(%s %s %s)' % (self.leftExpression, self.booleanOperator, self.rightExpression)


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
        return '(%s %s %s)' % (self.leftDataExtractor, self.comparisonOperator, self.rightDataExtractor)


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

# Functions Start


class FunctionOperator(object):
    pass


class SumFunctionOperator(FunctionOperator):
    def execute(self, left, right):
        if left is None:
            return right

        if right is None:
            return left

        return left + right

    def __str__(self):
        return 'SUM'


class CountFunctionOperator(FunctionOperator):
    def execute(self, left, right):
        if left is None:
            return 1

        if right is None:
            return left

        return left + 1

    def __str__(self):
        return 'COUNT'


class MinFunctionOperator(FunctionOperator):
    def execute(self, left, right):
        if left is None:
            return right

        if right is None:
            return left

        if left < right:
            return left
        else:
            return right

    def __str__(self):
        return 'MIN'


class MaxFunctionOperator(FunctionOperator):
    def execute(self, left, right):
        if left is None:
            return right

        if right is None:
            return left

        if left > right:
            return left
        else:
            return right

    def __str__(self):
        return 'MAX'


class Calculation(object):
    def __init__(self, operator, dataExtractor, name):
        self.operator = operator
        self.dataExtractor = dataExtractor
        self.name = name

    def execute(self, o, currentValue):
        value = self.dataExtractor.extract(o)

        return self.operator.execute(currentValue, value)

    def __str__(self):
        return '%s(%s)' % (self.operator, self.dataExtractor)
# Functions End


def findReference(elements):
    for element in elements:
        if isinstance(element, Reference):
            return element


def findBooleanExpression(elements):
    for element in elements:
        if isinstance(element, BooleanExpression):
            return element


def findFunctionOperator(elements):
    for element in elements:
        if isinstance(element, FunctionOperator):
            return element


def findExtractor(element):
    if isinstance(element, Asterisk):
        return (IdentityExtractor(), '*', False)

    if isinstance(element, int) or isinstance(element, str):
        return (StaticExtractor(element), str(element), False)

    if isinstance(element, Reference):
        return (ReferenceExtractor(element), element.value, False)

    if isinstance(element, Calculation):
        return (CalculationExtractor(element), element.name, True)

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
        elif isinstance(element, GroupByClause):
            statement.groupByClause = element


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

    def prepare_group_by_clause(self, input, start, end, elements):
        columns = extractColumns(elements)

        return GroupByClause(columns)

    def make_boolean_comparison(self, input, start, end, elements):
        leftDataExctractor = findExtractor(elements[0])
        comparisonOperator = elements[2]
        rightDataExtractor = findExtractor(elements[4])

        comparison = BooleanComparison(
            leftDataExctractor[0], rightDataExtractor[0], comparisonOperator)

        return comparison

    def make_simple_boolean_expression(self, input, start, end, elements):
        leftExpression = elements[0]
        booleanOperator = elements[2]
        rightExpression = elements[4]
        expression = SimpleBooleanExpression(
            leftExpression, rightExpression, booleanOperator)

        return expression

    def make_complex_boolean_expression(self, input, start, end, elements):
        firstExpression = elements[2]
        lastElement = elements[-1]

        # No additional expression found
        if lastElement.text == '':
            return firstExpression

        # Otherwise build a expression from the first expression and the additional expression
        additionalExpressionElements = lastElement.elements[0].elements

        booleanOperator = additionalExpressionElements[1]
        rightExpression = additionalExpressionElements[3]

        expression = SimpleBooleanExpression(
            firstExpression, rightExpression, booleanOperator)

        return expression

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

    def make_sum_operator(self, input, start, end):
        return SumFunctionOperator()

    def make_count_operator(self, input, start, end):
        return CountFunctionOperator()

    def make_min_operator(self, input, start, end):
        return MinFunctionOperator()

    def make_max_operator(self, input, start, end):
        return MaxFunctionOperator()

    def make_calculation(self, input, start, end, elements):
        operator = findFunctionOperator(elements)

        for element in elements:
            extractor = findExtractor(element)

            if extractor[0] is not None:
                return Calculation(operator, extractor[0], input[start:end])


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

        sqlStatement.validate()

        return sqlStatement


def newParser(documentObjectsSupplier, singleObjectSupplier):
    return SqlParser(documentObjectsSupplier, singleObjectSupplier)
