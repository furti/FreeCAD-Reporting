import re

from itertools import groupby
from . import sql_grammar
from report_utils import logger

TYPE_REGEX = re.compile("<class '([^']+)'>")


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
            elif not column.static:
                nonGroupingFound = True

        if groupingFound and nonGroupingFound:
            raise SqlStatementValidationError(
                'Can not mix functions and non functions in select clause')

    def execute(self, objectList):
        result = []

        for o in objectList:
            result.append([column.execute(o) for column in self.columns])

        if len(result) == 0:
            return result

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
        self.static = isinstance(dataExtractor, StaticExtractor)

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


class GroupedLists(object):
    def __init__(self):
        self.groups = [
            #(key, list),...
        ]

    def append(self, key, o):
        matchingGroups = [group for group in self.groups if group[0] == key]
        groupList = None

        if len(matchingGroups) == 0:
            groupList = []

            self.groups.append((key, groupList))
        else:
            groupList = matchingGroups[0][1]

        groupList.append(o)

    def toGroupedList(self):
        groupedList = []

        for group in self.groups:
            key = group[0]
            value = group[1]

            logger.debug('Group %s:%s', (key, value), compact=False)
            groupedList.append(value)

        return groupedList


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
        groups = GroupedLists()

        for o in objectList:
            keys = self.extractColumns(o)

            groups.append(keys, o)

        return groups.toGroupedList()

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


class AsClause(object):
    def __init__(self, name):
        self.name = name


class IdentityExtractor(object):
    def extract(self, o):
        return o

    def resetState(self):
        pass

    def __str__(self):
        return '$identity'

    def __eq__(self, obj):
        return isinstance(obj, IdentityExtractor)


class NoneExtractor(object):
    def extract(self, o):
        return None

    def resetState(self):
        pass

    def __str__(self):
        return 'NULL'

    def __eq__(self, obj):
        return isinstance(obj, NoneExtractor)


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

    def __eq__(self, obj):
        return isinstance(obj, CalculationExtractor) and self.calculation == obj.calculation


class ArithmeticExtractor(object):
    def __init__(self, arithmeticOperation):
        self.arithmeticOperation = arithmeticOperation

    def extract(self, o):
        return self.arithmeticOperation.execute(o)

    def resetState(self):
        pass

    def __str__(self):
        return '%s' % (self.arithmeticOperation)

    def __eq__(self, obj):
        return isinstance(obj, ArithmeticExtractor) and self.arithmeticOperation == obj.arithmeticOperation


class Reference(object):
    def __init__(self, value):
        self.value = value
        self.properties = value.split('.')

    def getValue(self, o):
        actualValue = o

        for p in self.properties:
            if hasattr(actualValue, p):
                actualValue = getattr(actualValue, p)
            else:
                return None

        return actualValue

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


class ArithmeticOperation(BooleanExpression):
    def __init__(self, leftDataExtractor, rightDataExtractor, arithmeticOperator):
        self.leftDataExtractor = leftDataExtractor
        self.rightDataExtractor = rightDataExtractor
        self.arithmeticOperator = arithmeticOperator

    def execute(self, o):
        left = self.leftDataExtractor.extract(o)
        right = self.rightDataExtractor.extract(o)

        if left is None or right is None:
            return None

        return self.arithmeticOperator.calculate(left, right)

    def __str__(self):
        return '(%s %s %s)' % (self.leftDataExtractor, self.arithmeticOperator, self.rightDataExtractor)

    def __eq__(self, obj):
        if not isinstance(obj, ArithmeticOperation):
            return False

        if self.leftDataExtractor != obj.leftDataExtractor:
            return False

        if self.rightDataExtractor != obj.rightDataExtractor:
            return False

        return self.arithmeticOperator == obj.arithmeticOperator


class MultiplyArithmeticOperator(object):
    def calculate(self, left, right):
        return left * right

    def __str__(self):
        return '*'

    def __eq__(self, obj):
        return isinstance(obj, MultiplyArithmeticOperator)


class DivideArithmeticOperator(object):
    def calculate(self, left, right):
        return left / right

    def __str__(self):
        return '/'

    def __eq__(self, obj):
        return isinstance(obj, DivideArithmeticOperator)


class AddArithmeticOperator(object):
    def calculate(self, left, right):
        return left + right

    def __str__(self):
        return '+'

    def __eq__(self, obj):
        return isinstance(obj, AddArithmeticOperator)


class SubtractArithmeticOperator(object):
    def calculate(self, left, right):
        return left - right

    def __str__(self):
        return '-'

    def __eq__(self, obj):
        return isinstance(obj, SubtractArithmeticOperator)


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


class IsComparisonOperator(object):
    def compare(self, left, right):
        if left is None and right is None:
            return True

        if left is not None and right is not None:
            return left == right

        return False

    def __str__(self):
        return 'IS'


class IsNotComparisonOperator(object):
    def compare(self, left, right):
        if left is None and right is None:
            return False

        if left is not None and right is not None:
            return left != right

        return True

    def __str__(self):
        return 'IS NOT'


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
    def __init__(self):
        self.grouping = True

    def execute(self, left, right):
        if left is None:
            return right

        if right is None:
            return left

        return left + right

    def __str__(self):
        return 'SUM'

    def __eq__(self, obj):
        return isinstance(obj, SumFunctionOperator)


class CountFunctionOperator(FunctionOperator):
    def __init__(self):
        self.grouping = True

    def execute(self, left, right):
        if left is None:
            return 1

        if right is None:
            return left

        return left + 1

    def __str__(self):
        return 'COUNT'

    def __eq__(self, obj):
        return isinstance(obj, CountFunctionOperator)


class MinFunctionOperator(FunctionOperator):
    def __init__(self):
        self.grouping = True

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

    def __eq__(self, obj):
        return isinstance(obj, MinFunctionOperator)


class MaxFunctionOperator(FunctionOperator):
    def __init__(self):
        self.grouping = True

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

    def __eq__(self, obj):
        return isinstance(obj, MaxFunctionOperator)


class ConcatFunctionOperator(FunctionOperator):
    def __init__(self):
        self.grouping = False

    def execute(self, left, rightValues):
        if rightValues is None or len(rightValues) == 0:
            return ''

        result = ''

        for value in rightValues:
            if value is not None:
                result += str(value)

        return result

    def __str__(self):
        return 'CONCAT'

    def __eq__(self, obj):
        return isinstance(obj, ConcatFunctionOperator)


class TypeFunctionOperator(FunctionOperator):
    def __init__(self):
        self.grouping = False

    def execute(self, left, right):
        toUse = right

        if hasattr(right, 'Proxy'):
            toUse = right.Proxy

        typeString = str(type(toUse))

        match = TYPE_REGEX.match(typeString)

        return match.group(1)

    def __str__(self):
        return 'TYPE'

    def __eq__(self, obj):
        return isinstance(obj, TypeFunctionOperator)


class Calculation(object):
    def __init__(self, operator, dataExtractor, name):
        self.operator = operator
        self.dataExtractor = dataExtractor
        self.name = name
        self.grouping = operator.grouping

    def execute(self, o, currentValue):
        value = self.dataExtractor.extract(o)

        return self.operator.execute(currentValue, value)

    def __str__(self):
        return '%s(%s)' % (self.operator, self.dataExtractor)

    def __eq__(self, obj):
        return isinstance(obj, Calculation) and self.operator == obj.operator and self.dataExtractor == obj.dataExtractor


class MultiParamCalculation(object):
    def __init__(self, operator, dataExtractors, name):
        self.operator = operator
        self.dataExtractors = dataExtractors
        self.name = name
        self.grouping = operator.grouping

    def execute(self, o, currentValue):
        values = [dataExtractor.extract(o)
                  for dataExtractor in self.dataExtractors]

        return self.operator.execute(currentValue, values)

    def __str__(self):
        return '%s(%s)' % (self.operator, [str(extractor) for extractor in self.dataExtractors])

    def __eq__(self, obj):
        if not isinstance(obj, MultiParamCalculation) or not self.operator == obj.operator:
            return False

        for dataExtractor in self.dataExtractors:
            if not dataExtractor in obj.dataExtractors:
                return False

        return True

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
    if element is None:
        return (NoneExtractor(), 'Null', False)

    if isinstance(element, Asterisk):
        return (IdentityExtractor(), '*', False)

    if isinstance(element, int) or isinstance(element, str):
        return (StaticExtractor(element), str(element), False)

    if isinstance(element, Reference):
        return (ReferenceExtractor(element), element.value, False)

    if isinstance(element, Calculation) or isinstance(element, MultiParamCalculation):
        return (CalculationExtractor(element), element.name, element.grouping)

    if isinstance(element, ArithmeticOperation):
        return (ArithmeticExtractor(element), str(element), False)

    return (None, None, None)


def findExtractors(elements):
    extractors = []

    for element in elements:
        extractor = findExtractor(element)

        if extractor[0] is not None:
            extractors.append(extractor)
        elif hasattr(element, 'elements'):
            extractors.extend(findExtractors(element.elements))

    return extractors


def findColumns(elements):
    columns = []

    for element in elements:
        if isinstance(element, Column):
            columns.append(element)
        elif hasattr(element, 'elements'):
            columns.extend(findColumns(element.elements))

    return columns


def findLiteral(elements):
    for element in elements:
        if isinstance(element, str):
            return element
        elif hasattr(element, 'elements'):
            literal = findLiteral(element.elements)

            if literal is not None:
                return literal

    return None


def extractGroupByColumns(elements):
    columns = []

    for element in elements:
        extractor, name, grouping = findExtractor(element)

        if extractor is not None:
            columns.append(Column(name, extractor, grouping))
        elif hasattr(element, 'elements'):
            columns.extend(extractGroupByColumns(element.elements))

    return columns


def findAsClause(elements):
    for element in elements:
        if isinstance(element, AsClause):
            return element
        elif hasattr(element, 'elements'):
            asClause = findAsClause(element.elements)

            if asClause is not None:
                return asClause

    return None


def extractColumn(elements):
    column = None

    for element in elements:
        extractor, name, grouping = findExtractor(element)

        if extractor is not None:
            column = Column(name, extractor, grouping)

            break
        elif hasattr(element, 'elements'):
            column = findColumns(element.elements)

            if column is not None:
                break

    if column is not None:
        asClause = findAsClause(elements)

        if asClause is not None:
            column.columnName = asClause.name

    return column


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
        columns = findColumns(elements)

        return Columns(columns)

    def make_column(self, input, start, end, elements):
        return extractColumn(elements)

    def prepare_from_clause(self, input, start, end, elements):
        reference = findReference(elements)

        return FromClause(reference)

    def prepare_where_clause(self, input, start, end, elements):
        booleanExpression = findBooleanExpression(elements)

        return WhereClause(booleanExpression)

    def prepare_group_by_clause(self, input, start, end, elements):
        columns = extractGroupByColumns(elements)

        return GroupByClause(columns)

    def prepare_as_clause(self, input, start, end, elements):
        literal = findLiteral(elements)

        return AsClause(literal)

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

    def make_arithmetic_operation(self, input, start, end, elements):
        leftDataExctractor = findExtractor(elements[0])
        arithmeticOperator = elements[2]
        rightDataExtractor = findExtractor(elements[4])

        operation = ArithmeticOperation(
            leftDataExctractor[0], rightDataExtractor[0], arithmeticOperator)

        return operation

    def make_multiply_arithmetic_operator(self, input, start, end):
        return MultiplyArithmeticOperator()

    def make_divide_arithmetic_operator(self, input, start, end):
        return DivideArithmeticOperator()

    def make_add_arithmetic_operator(self, input, start, end):
        return AddArithmeticOperator()

    def make_subtract_arithmetic_operator(self, input, start, end):
        return SubtractArithmeticOperator()

    def make_asterisk(self, input, start, end):
        return Asterisk()

    def make_number(self, input, start, end, elements):
        return int(input[start:end], 10)

    def make_null(self, input, start, end):
        return None

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

    def make_comp_operator_is(self, input, start, end):
        return IsComparisonOperator()

    def make_comp_operator_is_not(self, input, start, end):
        return IsNotComparisonOperator()

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

    def make_concat_operator(self, input, start, end):
        return ConcatFunctionOperator()

    def make_type_operator(self, input, start, end):
        return TypeFunctionOperator()

    def make_calculation(self, input, start, end, elements):
        operator = findFunctionOperator(elements)

        for element in elements:
            extractor = findExtractor(element)

            if extractor[0] is not None:
                return Calculation(operator, extractor[0], input[start:end])

    def make_multiparam_calculation(self, input, start, end, elements):
        operator = findFunctionOperator(elements)

        extractors = findExtractors(elements)

        return MultiParamCalculation(operator, [extractor[0] for extractor in extractors], input[start:end])


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
