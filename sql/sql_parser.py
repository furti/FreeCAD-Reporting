from . import sql_grammar

def printElements(elements):
    for element in elements:
        print(element)

class SelectStatement(object):
    def __init__(self):
        self.fromClause = None
    
    def __str__(self):
        return 'Select %s'%self.fromClause

class FromClause(object):
    def __init__(self, reference):
        print(reference)
        self.reference = reference
    
    def __str__(self):
        return 'From %s'%self.reference

class Reference(object):
    def __init__(self, value):
        self.value = value
    
    def __str__(self):
        return '$%s'%self.value

def findReference(elements):
    for element in elements:
        if isinstance(element, Reference):
            return element

def prepareSelectStatement(statement, elements):
    for element in elements:
        if isinstance(element, FromClause):
            statement.fromClause = element

class ParserActions(object):
    def make_statement(self, input, start, end, elements):
        selectStatement = SelectStatement()

        prepareSelectStatement(selectStatement, elements)

        return selectStatement
    
    def make_reference(self, input, start, end, elements):
        value = input[start:end]

        return Reference(value)
    
    def prepare_from_clause(self, input, start, end, elements):
        reference = findReference(elements)

        return FromClause(reference)

def parse(sqlString):
    return sql_grammar.parse(sqlString, actions=ParserActions())