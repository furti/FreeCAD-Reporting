from collections import defaultdict
import re


class TreeNode(object):
    def __init__(self, text, offset, elements=None):
        self.text = text
        self.offset = offset
        self.elements = elements or []

    def __iter__(self):
        for el in self.elements:
            yield el


class TreeNode1(TreeNode):
    def __init__(self, text, offset, elements):
        super(TreeNode1, self).__init__(text, offset, elements)
        self.__ = elements[3]
        self.Columns = elements[2]
        self.FromClause = elements[4]


class TreeNode2(TreeNode):
    def __init__(self, text, offset, elements):
        super(TreeNode2, self).__init__(text, offset, elements)
        self.__ = elements[1]
        self.Reference = elements[2]


class TreeNode3(TreeNode):
    def __init__(self, text, offset, elements):
        super(TreeNode3, self).__init__(text, offset, elements)
        self.__ = elements[2]
        self.BooleanExpression = elements[3]


class TreeNode4(TreeNode):
    def __init__(self, text, offset, elements):
        super(TreeNode4, self).__init__(text, offset, elements)
        self.__ = elements[2]


class TreeNode5(TreeNode):
    def __init__(self, text, offset, elements):
        super(TreeNode5, self).__init__(text, offset, elements)
        self.GroupByOperand = elements[0]


class TreeNode6(TreeNode):
    def __init__(self, text, offset, elements):
        super(TreeNode6, self).__init__(text, offset, elements)
        self._ = elements[2]
        self.GroupByOperand = elements[3]


class TreeNode7(TreeNode):
    def __init__(self, text, offset, elements):
        super(TreeNode7, self).__init__(text, offset, elements)
        self.Column = elements[0]


class TreeNode8(TreeNode):
    def __init__(self, text, offset, elements):
        super(TreeNode8, self).__init__(text, offset, elements)
        self._ = elements[2]
        self.Column = elements[3]


class TreeNode9(TreeNode):
    def __init__(self, text, offset, elements):
        super(TreeNode9, self).__init__(text, offset, elements)
        self.__ = elements[2]
        self.Literal = elements[3]


class TreeNode10(TreeNode):
    def __init__(self, text, offset, elements):
        super(TreeNode10, self).__init__(text, offset, elements)
        self.BooleanComparison = elements[0]
        self.__ = elements[3]
        self.BooleanOperator = elements[2]
        self.BooleanExpression = elements[4]


class TreeNode11(TreeNode):
    def __init__(self, text, offset, elements):
        super(TreeNode11, self).__init__(text, offset, elements)
        self._ = elements[3]
        self.BooleanExpression = elements[2]


class TreeNode12(TreeNode):
    def __init__(self, text, offset, elements):
        super(TreeNode12, self).__init__(text, offset, elements)
        self.__ = elements[2]
        self.BooleanOperator = elements[1]
        self.BooleanExpression = elements[3]


class TreeNode13(TreeNode):
    def __init__(self, text, offset, elements):
        super(TreeNode13, self).__init__(text, offset, elements)
        self.Operand = elements[4]
        self._ = elements[3]
        self.ComparisonOperator = elements[2]


class TreeNode14(TreeNode):
    def __init__(self, text, offset, elements):
        super(TreeNode14, self).__init__(text, offset, elements)
        self.FunctionName = elements[0]
        self._ = elements[5]


class TreeNode15(TreeNode):
    def __init__(self, text, offset, elements):
        super(TreeNode15, self).__init__(text, offset, elements)
        self.MultiParamFunctionName = elements[0]
        self._ = elements[3]


class TreeNode16(TreeNode):
    def __init__(self, text, offset, elements):
        super(TreeNode16, self).__init__(text, offset, elements)
        self._ = elements[2]


class TreeNode17(TreeNode):
    def __init__(self, text, offset, elements):
        super(TreeNode17, self).__init__(text, offset, elements)
        self._ = elements[0]


class ParseError(SyntaxError):
    pass


FAILURE = object()


class Grammar(object):
    REGEX_1 = re.compile('^[a-zA-Z0-9]')
    REGEX_2 = re.compile('^[0-9]')
    REGEX_3 = re.compile('^[ \\t\\r\\n]')
    REGEX_4 = re.compile('^[ \\t\\r\\n]')

    def _read_Statement(self):
        address0, index0 = FAILURE, self._offset
        cached = self._cache['Statement'].get(index0)
        if cached:
            self._offset = cached[1]
            return cached[0]
        index1, elements0 = self._offset, []
        address1 = FAILURE
        chunk0 = None
        if self._offset < self._input_size:
            chunk0 = self._input[self._offset:self._offset + 6]
        if chunk0 is not None and chunk0.lower() == 'Select'.lower():
            address1 = TreeNode(self._input[self._offset:self._offset + 6], self._offset)
            self._offset = self._offset + 6
        else:
            address1 = FAILURE
            if self._offset > self._failure:
                self._failure = self._offset
                self._expected = []
            if self._offset == self._failure:
                self._expected.append('`Select`')
        if address1 is not FAILURE:
            elements0.append(address1)
            address2 = FAILURE
            address2 = self._read___()
            if address2 is not FAILURE:
                elements0.append(address2)
                address3 = FAILURE
                address3 = self._read_Columns()
                if address3 is not FAILURE:
                    elements0.append(address3)
                    address4 = FAILURE
                    address4 = self._read___()
                    if address4 is not FAILURE:
                        elements0.append(address4)
                        address5 = FAILURE
                        address5 = self._read_FromClause()
                        if address5 is not FAILURE:
                            elements0.append(address5)
                            address6 = FAILURE
                            index2 = self._offset
                            address6 = self._read_WhereClause()
                            if address6 is FAILURE:
                                address6 = TreeNode(self._input[index2:index2], index2)
                                self._offset = index2
                            if address6 is not FAILURE:
                                elements0.append(address6)
                                address7 = FAILURE
                                index3 = self._offset
                                address7 = self._read_GroupByClause()
                                if address7 is FAILURE:
                                    address7 = TreeNode(self._input[index3:index3], index3)
                                    self._offset = index3
                                if address7 is not FAILURE:
                                    elements0.append(address7)
                                    address8 = FAILURE
                                    index4 = self._offset
                                    address8 = self._read_Semicolon()
                                    if address8 is FAILURE:
                                        address8 = TreeNode(self._input[index4:index4], index4)
                                        self._offset = index4
                                    if address8 is not FAILURE:
                                        elements0.append(address8)
                                    else:
                                        elements0 = None
                                        self._offset = index1
                                else:
                                    elements0 = None
                                    self._offset = index1
                            else:
                                elements0 = None
                                self._offset = index1
                        else:
                            elements0 = None
                            self._offset = index1
                    else:
                        elements0 = None
                        self._offset = index1
                else:
                    elements0 = None
                    self._offset = index1
            else:
                elements0 = None
                self._offset = index1
        else:
            elements0 = None
            self._offset = index1
        if elements0 is None:
            address0 = FAILURE
        else:
            address0 = self._actions.make_statement(self._input, index1, self._offset, elements0)
            self._offset = self._offset
        self._cache['Statement'][index0] = (address0, self._offset)
        return address0

    def _read_FromClause(self):
        address0, index0 = FAILURE, self._offset
        cached = self._cache['FromClause'].get(index0)
        if cached:
            self._offset = cached[1]
            return cached[0]
        index1, elements0 = self._offset, []
        address1 = FAILURE
        chunk0 = None
        if self._offset < self._input_size:
            chunk0 = self._input[self._offset:self._offset + 4]
        if chunk0 is not None and chunk0.lower() == 'From'.lower():
            address1 = TreeNode(self._input[self._offset:self._offset + 4], self._offset)
            self._offset = self._offset + 4
        else:
            address1 = FAILURE
            if self._offset > self._failure:
                self._failure = self._offset
                self._expected = []
            if self._offset == self._failure:
                self._expected.append('`From`')
        if address1 is not FAILURE:
            elements0.append(address1)
            address2 = FAILURE
            address2 = self._read___()
            if address2 is not FAILURE:
                elements0.append(address2)
                address3 = FAILURE
                address3 = self._read_Reference()
                if address3 is not FAILURE:
                    elements0.append(address3)
                else:
                    elements0 = None
                    self._offset = index1
            else:
                elements0 = None
                self._offset = index1
        else:
            elements0 = None
            self._offset = index1
        if elements0 is None:
            address0 = FAILURE
        else:
            address0 = self._actions.prepare_from_clause(self._input, index1, self._offset, elements0)
            self._offset = self._offset
        self._cache['FromClause'][index0] = (address0, self._offset)
        return address0

    def _read_WhereClause(self):
        address0, index0 = FAILURE, self._offset
        cached = self._cache['WhereClause'].get(index0)
        if cached:
            self._offset = cached[1]
            return cached[0]
        index1, elements0 = self._offset, []
        address1 = FAILURE
        address1 = self._read___()
        if address1 is not FAILURE:
            elements0.append(address1)
            address2 = FAILURE
            chunk0 = None
            if self._offset < self._input_size:
                chunk0 = self._input[self._offset:self._offset + 5]
            if chunk0 is not None and chunk0.lower() == 'Where'.lower():
                address2 = TreeNode(self._input[self._offset:self._offset + 5], self._offset)
                self._offset = self._offset + 5
            else:
                address2 = FAILURE
                if self._offset > self._failure:
                    self._failure = self._offset
                    self._expected = []
                if self._offset == self._failure:
                    self._expected.append('`Where`')
            if address2 is not FAILURE:
                elements0.append(address2)
                address3 = FAILURE
                address3 = self._read___()
                if address3 is not FAILURE:
                    elements0.append(address3)
                    address4 = FAILURE
                    address4 = self._read_BooleanExpression()
                    if address4 is not FAILURE:
                        elements0.append(address4)
                    else:
                        elements0 = None
                        self._offset = index1
                else:
                    elements0 = None
                    self._offset = index1
            else:
                elements0 = None
                self._offset = index1
        else:
            elements0 = None
            self._offset = index1
        if elements0 is None:
            address0 = FAILURE
        else:
            address0 = self._actions.prepare_where_clause(self._input, index1, self._offset, elements0)
            self._offset = self._offset
        self._cache['WhereClause'][index0] = (address0, self._offset)
        return address0

    def _read_GroupByClause(self):
        address0, index0 = FAILURE, self._offset
        cached = self._cache['GroupByClause'].get(index0)
        if cached:
            self._offset = cached[1]
            return cached[0]
        index1, elements0 = self._offset, []
        address1 = FAILURE
        address1 = self._read___()
        if address1 is not FAILURE:
            elements0.append(address1)
            address2 = FAILURE
            chunk0 = None
            if self._offset < self._input_size:
                chunk0 = self._input[self._offset:self._offset + 8]
            if chunk0 is not None and chunk0.lower() == 'Group By'.lower():
                address2 = TreeNode(self._input[self._offset:self._offset + 8], self._offset)
                self._offset = self._offset + 8
            else:
                address2 = FAILURE
                if self._offset > self._failure:
                    self._failure = self._offset
                    self._expected = []
                if self._offset == self._failure:
                    self._expected.append('`Group By`')
            if address2 is not FAILURE:
                elements0.append(address2)
                address3 = FAILURE
                address3 = self._read___()
                if address3 is not FAILURE:
                    elements0.append(address3)
                    address4 = FAILURE
                    index2, elements1 = self._offset, []
                    address5 = FAILURE
                    address5 = self._read_GroupByOperand()
                    if address5 is not FAILURE:
                        elements1.append(address5)
                        address6 = FAILURE
                        remaining0, index3, elements2, address7 = 0, self._offset, [], True
                        while address7 is not FAILURE:
                            index4, elements3 = self._offset, []
                            address8 = FAILURE
                            address8 = self._read__()
                            if address8 is not FAILURE:
                                elements3.append(address8)
                                address9 = FAILURE
                                chunk1 = None
                                if self._offset < self._input_size:
                                    chunk1 = self._input[self._offset:self._offset + 1]
                                if chunk1 == ',':
                                    address9 = TreeNode(self._input[self._offset:self._offset + 1], self._offset)
                                    self._offset = self._offset + 1
                                else:
                                    address9 = FAILURE
                                    if self._offset > self._failure:
                                        self._failure = self._offset
                                        self._expected = []
                                    if self._offset == self._failure:
                                        self._expected.append('","')
                                if address9 is not FAILURE:
                                    elements3.append(address9)
                                    address10 = FAILURE
                                    address10 = self._read__()
                                    if address10 is not FAILURE:
                                        elements3.append(address10)
                                        address11 = FAILURE
                                        address11 = self._read_GroupByOperand()
                                        if address11 is not FAILURE:
                                            elements3.append(address11)
                                        else:
                                            elements3 = None
                                            self._offset = index4
                                    else:
                                        elements3 = None
                                        self._offset = index4
                                else:
                                    elements3 = None
                                    self._offset = index4
                            else:
                                elements3 = None
                                self._offset = index4
                            if elements3 is None:
                                address7 = FAILURE
                            else:
                                address7 = TreeNode6(self._input[index4:self._offset], index4, elements3)
                                self._offset = self._offset
                            if address7 is not FAILURE:
                                elements2.append(address7)
                                remaining0 -= 1
                        if remaining0 <= 0:
                            address6 = TreeNode(self._input[index3:self._offset], index3, elements2)
                            self._offset = self._offset
                        else:
                            address6 = FAILURE
                        if address6 is not FAILURE:
                            elements1.append(address6)
                        else:
                            elements1 = None
                            self._offset = index2
                    else:
                        elements1 = None
                        self._offset = index2
                    if elements1 is None:
                        address4 = FAILURE
                    else:
                        address4 = TreeNode5(self._input[index2:self._offset], index2, elements1)
                        self._offset = self._offset
                    if address4 is not FAILURE:
                        elements0.append(address4)
                    else:
                        elements0 = None
                        self._offset = index1
                else:
                    elements0 = None
                    self._offset = index1
            else:
                elements0 = None
                self._offset = index1
        else:
            elements0 = None
            self._offset = index1
        if elements0 is None:
            address0 = FAILURE
        else:
            address0 = self._actions.prepare_group_by_clause(self._input, index1, self._offset, elements0)
            self._offset = self._offset
        self._cache['GroupByClause'][index0] = (address0, self._offset)
        return address0

    def _read_Columns(self):
        address0, index0 = FAILURE, self._offset
        cached = self._cache['Columns'].get(index0)
        if cached:
            self._offset = cached[1]
            return cached[0]
        index1, elements0 = self._offset, []
        address1 = FAILURE
        address1 = self._read_Column()
        if address1 is not FAILURE:
            elements0.append(address1)
            address2 = FAILURE
            remaining0, index2, elements1, address3 = 0, self._offset, [], True
            while address3 is not FAILURE:
                index3, elements2 = self._offset, []
                address4 = FAILURE
                address4 = self._read__()
                if address4 is not FAILURE:
                    elements2.append(address4)
                    address5 = FAILURE
                    chunk0 = None
                    if self._offset < self._input_size:
                        chunk0 = self._input[self._offset:self._offset + 1]
                    if chunk0 == ',':
                        address5 = TreeNode(self._input[self._offset:self._offset + 1], self._offset)
                        self._offset = self._offset + 1
                    else:
                        address5 = FAILURE
                        if self._offset > self._failure:
                            self._failure = self._offset
                            self._expected = []
                        if self._offset == self._failure:
                            self._expected.append('","')
                    if address5 is not FAILURE:
                        elements2.append(address5)
                        address6 = FAILURE
                        address6 = self._read__()
                        if address6 is not FAILURE:
                            elements2.append(address6)
                            address7 = FAILURE
                            address7 = self._read_Column()
                            if address7 is not FAILURE:
                                elements2.append(address7)
                            else:
                                elements2 = None
                                self._offset = index3
                        else:
                            elements2 = None
                            self._offset = index3
                    else:
                        elements2 = None
                        self._offset = index3
                else:
                    elements2 = None
                    self._offset = index3
                if elements2 is None:
                    address3 = FAILURE
                else:
                    address3 = TreeNode8(self._input[index3:self._offset], index3, elements2)
                    self._offset = self._offset
                if address3 is not FAILURE:
                    elements1.append(address3)
                    remaining0 -= 1
            if remaining0 <= 0:
                address2 = TreeNode(self._input[index2:self._offset], index2, elements1)
                self._offset = self._offset
            else:
                address2 = FAILURE
            if address2 is not FAILURE:
                elements0.append(address2)
            else:
                elements0 = None
                self._offset = index1
        else:
            elements0 = None
            self._offset = index1
        if elements0 is None:
            address0 = FAILURE
        else:
            address0 = self._actions.prepare_columns(self._input, index1, self._offset, elements0)
            self._offset = self._offset
        self._cache['Columns'][index0] = (address0, self._offset)
        return address0

    def _read_Column(self):
        address0, index0 = FAILURE, self._offset
        cached = self._cache['Column'].get(index0)
        if cached:
            self._offset = cached[1]
            return cached[0]
        index1, elements0 = self._offset, []
        address1 = FAILURE
        index2 = self._offset
        address1 = self._read_Asterisk()
        if address1 is FAILURE:
            self._offset = index2
            address1 = self._read_MultiParamFunction()
            if address1 is FAILURE:
                self._offset = index2
                address1 = self._read_Function()
                if address1 is FAILURE:
                    self._offset = index2
                    address1 = self._read_Operand()
                    if address1 is FAILURE:
                        self._offset = index2
        if address1 is not FAILURE:
            elements0.append(address1)
            address2 = FAILURE
            index3 = self._offset
            address2 = self._read_AsClause()
            if address2 is FAILURE:
                address2 = TreeNode(self._input[index3:index3], index3)
                self._offset = index3
            if address2 is not FAILURE:
                elements0.append(address2)
            else:
                elements0 = None
                self._offset = index1
        else:
            elements0 = None
            self._offset = index1
        if elements0 is None:
            address0 = FAILURE
        else:
            address0 = self._actions.make_column(self._input, index1, self._offset, elements0)
            self._offset = self._offset
        self._cache['Column'][index0] = (address0, self._offset)
        return address0

    def _read_GroupByOperand(self):
        address0, index0 = FAILURE, self._offset
        cached = self._cache['GroupByOperand'].get(index0)
        if cached:
            self._offset = cached[1]
            return cached[0]
        index1 = self._offset
        address0 = self._read_MultiParamFunction()
        if address0 is FAILURE:
            self._offset = index1
            address0 = self._read_Function()
            if address0 is FAILURE:
                self._offset = index1
                address0 = self._read_Operand()
                if address0 is FAILURE:
                    self._offset = index1
        self._cache['GroupByOperand'][index0] = (address0, self._offset)
        return address0

    def _read_AsClause(self):
        address0, index0 = FAILURE, self._offset
        cached = self._cache['AsClause'].get(index0)
        if cached:
            self._offset = cached[1]
            return cached[0]
        index1, elements0 = self._offset, []
        address1 = FAILURE
        address1 = self._read___()
        if address1 is not FAILURE:
            elements0.append(address1)
            address2 = FAILURE
            chunk0 = None
            if self._offset < self._input_size:
                chunk0 = self._input[self._offset:self._offset + 2]
            if chunk0 is not None and chunk0.lower() == 'As'.lower():
                address2 = TreeNode(self._input[self._offset:self._offset + 2], self._offset)
                self._offset = self._offset + 2
            else:
                address2 = FAILURE
                if self._offset > self._failure:
                    self._failure = self._offset
                    self._expected = []
                if self._offset == self._failure:
                    self._expected.append('`As`')
            if address2 is not FAILURE:
                elements0.append(address2)
                address3 = FAILURE
                address3 = self._read___()
                if address3 is not FAILURE:
                    elements0.append(address3)
                    address4 = FAILURE
                    address4 = self._read_Literal()
                    if address4 is not FAILURE:
                        elements0.append(address4)
                    else:
                        elements0 = None
                        self._offset = index1
                else:
                    elements0 = None
                    self._offset = index1
            else:
                elements0 = None
                self._offset = index1
        else:
            elements0 = None
            self._offset = index1
        if elements0 is None:
            address0 = FAILURE
        else:
            address0 = self._actions.prepare_as_clause(self._input, index1, self._offset, elements0)
            self._offset = self._offset
        self._cache['AsClause'][index0] = (address0, self._offset)
        return address0

    def _read_BooleanExpression(self):
        address0, index0 = FAILURE, self._offset
        cached = self._cache['BooleanExpression'].get(index0)
        if cached:
            self._offset = cached[1]
            return cached[0]
        index1 = self._offset
        index2, elements0 = self._offset, []
        address1 = FAILURE
        address1 = self._read_BooleanComparison()
        if address1 is not FAILURE:
            elements0.append(address1)
            address2 = FAILURE
            address2 = self._read___()
            if address2 is not FAILURE:
                elements0.append(address2)
                address3 = FAILURE
                address3 = self._read_BooleanOperator()
                if address3 is not FAILURE:
                    elements0.append(address3)
                    address4 = FAILURE
                    address4 = self._read___()
                    if address4 is not FAILURE:
                        elements0.append(address4)
                        address5 = FAILURE
                        address5 = self._read_BooleanExpression()
                        if address5 is not FAILURE:
                            elements0.append(address5)
                        else:
                            elements0 = None
                            self._offset = index2
                    else:
                        elements0 = None
                        self._offset = index2
                else:
                    elements0 = None
                    self._offset = index2
            else:
                elements0 = None
                self._offset = index2
        else:
            elements0 = None
            self._offset = index2
        if elements0 is None:
            address0 = FAILURE
        else:
            address0 = self._actions.make_simple_boolean_expression(self._input, index2, self._offset, elements0)
            self._offset = self._offset
        if address0 is FAILURE:
            self._offset = index1
            address0 = self._read_BooleanComparison()
            if address0 is FAILURE:
                self._offset = index1
                index3, elements1 = self._offset, []
                address6 = FAILURE
                chunk0 = None
                if self._offset < self._input_size:
                    chunk0 = self._input[self._offset:self._offset + 1]
                if chunk0 == '(':
                    address6 = TreeNode(self._input[self._offset:self._offset + 1], self._offset)
                    self._offset = self._offset + 1
                else:
                    address6 = FAILURE
                    if self._offset > self._failure:
                        self._failure = self._offset
                        self._expected = []
                    if self._offset == self._failure:
                        self._expected.append('"("')
                if address6 is not FAILURE:
                    elements1.append(address6)
                    address7 = FAILURE
                    address7 = self._read__()
                    if address7 is not FAILURE:
                        elements1.append(address7)
                        address8 = FAILURE
                        address8 = self._read_BooleanExpression()
                        if address8 is not FAILURE:
                            elements1.append(address8)
                            address9 = FAILURE
                            address9 = self._read__()
                            if address9 is not FAILURE:
                                elements1.append(address9)
                                address10 = FAILURE
                                chunk1 = None
                                if self._offset < self._input_size:
                                    chunk1 = self._input[self._offset:self._offset + 1]
                                if chunk1 == ')':
                                    address10 = TreeNode(self._input[self._offset:self._offset + 1], self._offset)
                                    self._offset = self._offset + 1
                                else:
                                    address10 = FAILURE
                                    if self._offset > self._failure:
                                        self._failure = self._offset
                                        self._expected = []
                                    if self._offset == self._failure:
                                        self._expected.append('")"')
                                if address10 is not FAILURE:
                                    elements1.append(address10)
                                    address11 = FAILURE
                                    remaining0, index4, elements2, address12 = 0, self._offset, [], True
                                    while address12 is not FAILURE:
                                        index5, elements3 = self._offset, []
                                        address13 = FAILURE
                                        address13 = self._read___()
                                        if address13 is not FAILURE:
                                            elements3.append(address13)
                                            address14 = FAILURE
                                            address14 = self._read_BooleanOperator()
                                            if address14 is not FAILURE:
                                                elements3.append(address14)
                                                address15 = FAILURE
                                                address15 = self._read___()
                                                if address15 is not FAILURE:
                                                    elements3.append(address15)
                                                    address16 = FAILURE
                                                    address16 = self._read_BooleanExpression()
                                                    if address16 is not FAILURE:
                                                        elements3.append(address16)
                                                    else:
                                                        elements3 = None
                                                        self._offset = index5
                                                else:
                                                    elements3 = None
                                                    self._offset = index5
                                            else:
                                                elements3 = None
                                                self._offset = index5
                                        else:
                                            elements3 = None
                                            self._offset = index5
                                        if elements3 is None:
                                            address12 = FAILURE
                                        else:
                                            address12 = TreeNode12(self._input[index5:self._offset], index5, elements3)
                                            self._offset = self._offset
                                        if address12 is not FAILURE:
                                            elements2.append(address12)
                                            remaining0 -= 1
                                    if remaining0 <= 0:
                                        address11 = TreeNode(self._input[index4:self._offset], index4, elements2)
                                        self._offset = self._offset
                                    else:
                                        address11 = FAILURE
                                    if address11 is not FAILURE:
                                        elements1.append(address11)
                                    else:
                                        elements1 = None
                                        self._offset = index3
                                else:
                                    elements1 = None
                                    self._offset = index3
                            else:
                                elements1 = None
                                self._offset = index3
                        else:
                            elements1 = None
                            self._offset = index3
                    else:
                        elements1 = None
                        self._offset = index3
                else:
                    elements1 = None
                    self._offset = index3
                if elements1 is None:
                    address0 = FAILURE
                else:
                    address0 = self._actions.make_complex_boolean_expression(self._input, index3, self._offset, elements1)
                    self._offset = self._offset
                if address0 is FAILURE:
                    self._offset = index1
        self._cache['BooleanExpression'][index0] = (address0, self._offset)
        return address0

    def _read_BooleanComparison(self):
        address0, index0 = FAILURE, self._offset
        cached = self._cache['BooleanComparison'].get(index0)
        if cached:
            self._offset = cached[1]
            return cached[0]
        index1, elements0 = self._offset, []
        address1 = FAILURE
        address1 = self._read_Operand()
        if address1 is not FAILURE:
            elements0.append(address1)
            address2 = FAILURE
            address2 = self._read__()
            if address2 is not FAILURE:
                elements0.append(address2)
                address3 = FAILURE
                address3 = self._read_ComparisonOperator()
                if address3 is not FAILURE:
                    elements0.append(address3)
                    address4 = FAILURE
                    address4 = self._read__()
                    if address4 is not FAILURE:
                        elements0.append(address4)
                        address5 = FAILURE
                        address5 = self._read_Operand()
                        if address5 is not FAILURE:
                            elements0.append(address5)
                        else:
                            elements0 = None
                            self._offset = index1
                    else:
                        elements0 = None
                        self._offset = index1
                else:
                    elements0 = None
                    self._offset = index1
            else:
                elements0 = None
                self._offset = index1
        else:
            elements0 = None
            self._offset = index1
        if elements0 is None:
            address0 = FAILURE
        else:
            address0 = self._actions.make_boolean_comparison(self._input, index1, self._offset, elements0)
            self._offset = self._offset
        self._cache['BooleanComparison'][index0] = (address0, self._offset)
        return address0

    def _read_BooleanOperator(self):
        address0, index0 = FAILURE, self._offset
        cached = self._cache['BooleanOperator'].get(index0)
        if cached:
            self._offset = cached[1]
            return cached[0]
        index1 = self._offset
        chunk0 = None
        if self._offset < self._input_size:
            chunk0 = self._input[self._offset:self._offset + 3]
        if chunk0 is not None and chunk0.lower() == 'And'.lower():
            address0 = self._actions.make_boolean_operator_and(self._input, self._offset, self._offset + 3)
            self._offset = self._offset + 3
        else:
            address0 = FAILURE
            if self._offset > self._failure:
                self._failure = self._offset
                self._expected = []
            if self._offset == self._failure:
                self._expected.append('`And`')
        if address0 is FAILURE:
            self._offset = index1
            chunk1 = None
            if self._offset < self._input_size:
                chunk1 = self._input[self._offset:self._offset + 2]
            if chunk1 is not None and chunk1.lower() == 'Or'.lower():
                address0 = self._actions.make_boolean_operator_or(self._input, self._offset, self._offset + 2)
                self._offset = self._offset + 2
            else:
                address0 = FAILURE
                if self._offset > self._failure:
                    self._failure = self._offset
                    self._expected = []
                if self._offset == self._failure:
                    self._expected.append('`Or`')
            if address0 is FAILURE:
                self._offset = index1
        self._cache['BooleanOperator'][index0] = (address0, self._offset)
        return address0

    def _read_ComparisonOperator(self):
        address0, index0 = FAILURE, self._offset
        cached = self._cache['ComparisonOperator'].get(index0)
        if cached:
            self._offset = cached[1]
            return cached[0]
        index1 = self._offset
        chunk0 = None
        if self._offset < self._input_size:
            chunk0 = self._input[self._offset:self._offset + 2]
        if chunk0 == '>=':
            address0 = self._actions.make_comp_operator_gte(self._input, self._offset, self._offset + 2)
            self._offset = self._offset + 2
        else:
            address0 = FAILURE
            if self._offset > self._failure:
                self._failure = self._offset
                self._expected = []
            if self._offset == self._failure:
                self._expected.append('">="')
        if address0 is FAILURE:
            self._offset = index1
            chunk1 = None
            if self._offset < self._input_size:
                chunk1 = self._input[self._offset:self._offset + 2]
            if chunk1 == '<=':
                address0 = self._actions.make_comp_operator_lte(self._input, self._offset, self._offset + 2)
                self._offset = self._offset + 2
            else:
                address0 = FAILURE
                if self._offset > self._failure:
                    self._failure = self._offset
                    self._expected = []
                if self._offset == self._failure:
                    self._expected.append('"<="')
            if address0 is FAILURE:
                self._offset = index1
                chunk2 = None
                if self._offset < self._input_size:
                    chunk2 = self._input[self._offset:self._offset + 2]
                if chunk2 == '!=':
                    address0 = self._actions.make_comp_operator_neq(self._input, self._offset, self._offset + 2)
                    self._offset = self._offset + 2
                else:
                    address0 = FAILURE
                    if self._offset > self._failure:
                        self._failure = self._offset
                        self._expected = []
                    if self._offset == self._failure:
                        self._expected.append('"!="')
                if address0 is FAILURE:
                    self._offset = index1
                    chunk3 = None
                    if self._offset < self._input_size:
                        chunk3 = self._input[self._offset:self._offset + 1]
                    if chunk3 == '=':
                        address0 = self._actions.make_comp_operator_eq(self._input, self._offset, self._offset + 1)
                        self._offset = self._offset + 1
                    else:
                        address0 = FAILURE
                        if self._offset > self._failure:
                            self._failure = self._offset
                            self._expected = []
                        if self._offset == self._failure:
                            self._expected.append('"="')
                    if address0 is FAILURE:
                        self._offset = index1
                        chunk4 = None
                        if self._offset < self._input_size:
                            chunk4 = self._input[self._offset:self._offset + 1]
                        if chunk4 == '>':
                            address0 = self._actions.make_comp_operator_gt(self._input, self._offset, self._offset + 1)
                            self._offset = self._offset + 1
                        else:
                            address0 = FAILURE
                            if self._offset > self._failure:
                                self._failure = self._offset
                                self._expected = []
                            if self._offset == self._failure:
                                self._expected.append('">"')
                        if address0 is FAILURE:
                            self._offset = index1
                            chunk5 = None
                            if self._offset < self._input_size:
                                chunk5 = self._input[self._offset:self._offset + 1]
                            if chunk5 == '<':
                                address0 = self._actions.make_comp_operator_lt(self._input, self._offset, self._offset + 1)
                                self._offset = self._offset + 1
                            else:
                                address0 = FAILURE
                                if self._offset > self._failure:
                                    self._failure = self._offset
                                    self._expected = []
                                if self._offset == self._failure:
                                    self._expected.append('"<"')
                            if address0 is FAILURE:
                                self._offset = index1
                                chunk6 = None
                                if self._offset < self._input_size:
                                    chunk6 = self._input[self._offset:self._offset + 6]
                                if chunk6 is not None and chunk6.lower() == 'IS NOT'.lower():
                                    address0 = self._actions.make_comp_operator_is_not(self._input, self._offset, self._offset + 6)
                                    self._offset = self._offset + 6
                                else:
                                    address0 = FAILURE
                                    if self._offset > self._failure:
                                        self._failure = self._offset
                                        self._expected = []
                                    if self._offset == self._failure:
                                        self._expected.append('`IS NOT`')
                                if address0 is FAILURE:
                                    self._offset = index1
                                    chunk7 = None
                                    if self._offset < self._input_size:
                                        chunk7 = self._input[self._offset:self._offset + 2]
                                    if chunk7 is not None and chunk7.lower() == 'IS'.lower():
                                        address0 = self._actions.make_comp_operator_is(self._input, self._offset, self._offset + 2)
                                        self._offset = self._offset + 2
                                    else:
                                        address0 = FAILURE
                                        if self._offset > self._failure:
                                            self._failure = self._offset
                                            self._expected = []
                                        if self._offset == self._failure:
                                            self._expected.append('`IS`')
                                    if address0 is FAILURE:
                                        self._offset = index1
        self._cache['ComparisonOperator'][index0] = (address0, self._offset)
        return address0

    def _read_Function(self):
        address0, index0 = FAILURE, self._offset
        cached = self._cache['Function'].get(index0)
        if cached:
            self._offset = cached[1]
            return cached[0]
        index1, elements0 = self._offset, []
        address1 = FAILURE
        address1 = self._read_FunctionName()
        if address1 is not FAILURE:
            elements0.append(address1)
            address2 = FAILURE
            address2 = self._read__()
            if address2 is not FAILURE:
                elements0.append(address2)
                address3 = FAILURE
                chunk0 = None
                if self._offset < self._input_size:
                    chunk0 = self._input[self._offset:self._offset + 1]
                if chunk0 == '(':
                    address3 = TreeNode(self._input[self._offset:self._offset + 1], self._offset)
                    self._offset = self._offset + 1
                else:
                    address3 = FAILURE
                    if self._offset > self._failure:
                        self._failure = self._offset
                        self._expected = []
                    if self._offset == self._failure:
                        self._expected.append('"("')
                if address3 is not FAILURE:
                    elements0.append(address3)
                    address4 = FAILURE
                    address4 = self._read__()
                    if address4 is not FAILURE:
                        elements0.append(address4)
                        address5 = FAILURE
                        index2 = self._offset
                        address5 = self._read_Asterisk()
                        if address5 is FAILURE:
                            self._offset = index2
                            address5 = self._read_Operand()
                            if address5 is FAILURE:
                                self._offset = index2
                        if address5 is not FAILURE:
                            elements0.append(address5)
                            address6 = FAILURE
                            address6 = self._read__()
                            if address6 is not FAILURE:
                                elements0.append(address6)
                                address7 = FAILURE
                                chunk1 = None
                                if self._offset < self._input_size:
                                    chunk1 = self._input[self._offset:self._offset + 1]
                                if chunk1 == ')':
                                    address7 = TreeNode(self._input[self._offset:self._offset + 1], self._offset)
                                    self._offset = self._offset + 1
                                else:
                                    address7 = FAILURE
                                    if self._offset > self._failure:
                                        self._failure = self._offset
                                        self._expected = []
                                    if self._offset == self._failure:
                                        self._expected.append('")"')
                                if address7 is not FAILURE:
                                    elements0.append(address7)
                                else:
                                    elements0 = None
                                    self._offset = index1
                            else:
                                elements0 = None
                                self._offset = index1
                        else:
                            elements0 = None
                            self._offset = index1
                    else:
                        elements0 = None
                        self._offset = index1
                else:
                    elements0 = None
                    self._offset = index1
            else:
                elements0 = None
                self._offset = index1
        else:
            elements0 = None
            self._offset = index1
        if elements0 is None:
            address0 = FAILURE
        else:
            address0 = self._actions.make_calculation(self._input, index1, self._offset, elements0)
            self._offset = self._offset
        self._cache['Function'][index0] = (address0, self._offset)
        return address0

    def _read_FunctionName(self):
        address0, index0 = FAILURE, self._offset
        cached = self._cache['FunctionName'].get(index0)
        if cached:
            self._offset = cached[1]
            return cached[0]
        index1 = self._offset
        chunk0 = None
        if self._offset < self._input_size:
            chunk0 = self._input[self._offset:self._offset + 3]
        if chunk0 is not None and chunk0.lower() == 'Sum'.lower():
            address0 = self._actions.make_sum_operator(self._input, self._offset, self._offset + 3)
            self._offset = self._offset + 3
        else:
            address0 = FAILURE
            if self._offset > self._failure:
                self._failure = self._offset
                self._expected = []
            if self._offset == self._failure:
                self._expected.append('`Sum`')
        if address0 is FAILURE:
            self._offset = index1
            chunk1 = None
            if self._offset < self._input_size:
                chunk1 = self._input[self._offset:self._offset + 5]
            if chunk1 is not None and chunk1.lower() == 'Count'.lower():
                address0 = self._actions.make_count_operator(self._input, self._offset, self._offset + 5)
                self._offset = self._offset + 5
            else:
                address0 = FAILURE
                if self._offset > self._failure:
                    self._failure = self._offset
                    self._expected = []
                if self._offset == self._failure:
                    self._expected.append('`Count`')
            if address0 is FAILURE:
                self._offset = index1
                chunk2 = None
                if self._offset < self._input_size:
                    chunk2 = self._input[self._offset:self._offset + 3]
                if chunk2 is not None and chunk2.lower() == 'Min'.lower():
                    address0 = self._actions.make_min_operator(self._input, self._offset, self._offset + 3)
                    self._offset = self._offset + 3
                else:
                    address0 = FAILURE
                    if self._offset > self._failure:
                        self._failure = self._offset
                        self._expected = []
                    if self._offset == self._failure:
                        self._expected.append('`Min`')
                if address0 is FAILURE:
                    self._offset = index1
                    chunk3 = None
                    if self._offset < self._input_size:
                        chunk3 = self._input[self._offset:self._offset + 3]
                    if chunk3 is not None and chunk3.lower() == 'Max'.lower():
                        address0 = self._actions.make_max_operator(self._input, self._offset, self._offset + 3)
                        self._offset = self._offset + 3
                    else:
                        address0 = FAILURE
                        if self._offset > self._failure:
                            self._failure = self._offset
                            self._expected = []
                        if self._offset == self._failure:
                            self._expected.append('`Max`')
                    if address0 is FAILURE:
                        self._offset = index1
                        chunk4 = None
                        if self._offset < self._input_size:
                            chunk4 = self._input[self._offset:self._offset + 4]
                        if chunk4 is not None and chunk4.lower() == 'Type'.lower():
                            address0 = self._actions.make_type_operator(self._input, self._offset, self._offset + 4)
                            self._offset = self._offset + 4
                        else:
                            address0 = FAILURE
                            if self._offset > self._failure:
                                self._failure = self._offset
                                self._expected = []
                            if self._offset == self._failure:
                                self._expected.append('`Type`')
                        if address0 is FAILURE:
                            self._offset = index1
        self._cache['FunctionName'][index0] = (address0, self._offset)
        return address0

    def _read_MultiParamFunction(self):
        address0, index0 = FAILURE, self._offset
        cached = self._cache['MultiParamFunction'].get(index0)
        if cached:
            self._offset = cached[1]
            return cached[0]
        index1, elements0 = self._offset, []
        address1 = FAILURE
        address1 = self._read_MultiParamFunctionName()
        if address1 is not FAILURE:
            elements0.append(address1)
            address2 = FAILURE
            address2 = self._read__()
            if address2 is not FAILURE:
                elements0.append(address2)
                address3 = FAILURE
                chunk0 = None
                if self._offset < self._input_size:
                    chunk0 = self._input[self._offset:self._offset + 1]
                if chunk0 == '(':
                    address3 = TreeNode(self._input[self._offset:self._offset + 1], self._offset)
                    self._offset = self._offset + 1
                else:
                    address3 = FAILURE
                    if self._offset > self._failure:
                        self._failure = self._offset
                        self._expected = []
                    if self._offset == self._failure:
                        self._expected.append('"("')
                if address3 is not FAILURE:
                    elements0.append(address3)
                    address4 = FAILURE
                    address4 = self._read__()
                    if address4 is not FAILURE:
                        elements0.append(address4)
                        address5 = FAILURE
                        index2 = self._offset
                        address5 = self._read_Asterisk()
                        if address5 is FAILURE:
                            self._offset = index2
                            address5 = self._read_Operand()
                            if address5 is FAILURE:
                                self._offset = index2
                        if address5 is not FAILURE:
                            elements0.append(address5)
                            address6 = FAILURE
                            remaining0, index3, elements1, address7 = 0, self._offset, [], True
                            while address7 is not FAILURE:
                                index4, elements2 = self._offset, []
                                address8 = FAILURE
                                address8 = self._read__()
                                if address8 is not FAILURE:
                                    elements2.append(address8)
                                    address9 = FAILURE
                                    chunk1 = None
                                    if self._offset < self._input_size:
                                        chunk1 = self._input[self._offset:self._offset + 1]
                                    if chunk1 == ',':
                                        address9 = TreeNode(self._input[self._offset:self._offset + 1], self._offset)
                                        self._offset = self._offset + 1
                                    else:
                                        address9 = FAILURE
                                        if self._offset > self._failure:
                                            self._failure = self._offset
                                            self._expected = []
                                        if self._offset == self._failure:
                                            self._expected.append('","')
                                    if address9 is not FAILURE:
                                        elements2.append(address9)
                                        address10 = FAILURE
                                        address10 = self._read__()
                                        if address10 is not FAILURE:
                                            elements2.append(address10)
                                            address11 = FAILURE
                                            index5 = self._offset
                                            address11 = self._read_Asterisk()
                                            if address11 is FAILURE:
                                                self._offset = index5
                                                address11 = self._read_Operand()
                                                if address11 is FAILURE:
                                                    self._offset = index5
                                            if address11 is not FAILURE:
                                                elements2.append(address11)
                                            else:
                                                elements2 = None
                                                self._offset = index4
                                        else:
                                            elements2 = None
                                            self._offset = index4
                                    else:
                                        elements2 = None
                                        self._offset = index4
                                else:
                                    elements2 = None
                                    self._offset = index4
                                if elements2 is None:
                                    address7 = FAILURE
                                else:
                                    address7 = TreeNode16(self._input[index4:self._offset], index4, elements2)
                                    self._offset = self._offset
                                if address7 is not FAILURE:
                                    elements1.append(address7)
                                    remaining0 -= 1
                            if remaining0 <= 0:
                                address6 = TreeNode(self._input[index3:self._offset], index3, elements1)
                                self._offset = self._offset
                            else:
                                address6 = FAILURE
                            if address6 is not FAILURE:
                                elements0.append(address6)
                                address12 = FAILURE
                                chunk2 = None
                                if self._offset < self._input_size:
                                    chunk2 = self._input[self._offset:self._offset + 1]
                                if chunk2 == ')':
                                    address12 = TreeNode(self._input[self._offset:self._offset + 1], self._offset)
                                    self._offset = self._offset + 1
                                else:
                                    address12 = FAILURE
                                    if self._offset > self._failure:
                                        self._failure = self._offset
                                        self._expected = []
                                    if self._offset == self._failure:
                                        self._expected.append('")"')
                                if address12 is not FAILURE:
                                    elements0.append(address12)
                                else:
                                    elements0 = None
                                    self._offset = index1
                            else:
                                elements0 = None
                                self._offset = index1
                        else:
                            elements0 = None
                            self._offset = index1
                    else:
                        elements0 = None
                        self._offset = index1
                else:
                    elements0 = None
                    self._offset = index1
            else:
                elements0 = None
                self._offset = index1
        else:
            elements0 = None
            self._offset = index1
        if elements0 is None:
            address0 = FAILURE
        else:
            address0 = self._actions.make_multiparam_calculation(self._input, index1, self._offset, elements0)
            self._offset = self._offset
        self._cache['MultiParamFunction'][index0] = (address0, self._offset)
        return address0

    def _read_MultiParamFunctionName(self):
        address0, index0 = FAILURE, self._offset
        cached = self._cache['MultiParamFunctionName'].get(index0)
        if cached:
            self._offset = cached[1]
            return cached[0]
        chunk0 = None
        if self._offset < self._input_size:
            chunk0 = self._input[self._offset:self._offset + 6]
        if chunk0 is not None and chunk0.lower() == 'Concat'.lower():
            address0 = self._actions.make_concat_operator(self._input, self._offset, self._offset + 6)
            self._offset = self._offset + 6
        else:
            address0 = FAILURE
            if self._offset > self._failure:
                self._failure = self._offset
                self._expected = []
            if self._offset == self._failure:
                self._expected.append('`Concat`')
        self._cache['MultiParamFunctionName'][index0] = (address0, self._offset)
        return address0

    def _read_Operand(self):
        address0, index0 = FAILURE, self._offset
        cached = self._cache['Operand'].get(index0)
        if cached:
            self._offset = cached[1]
            return cached[0]
        index1 = self._offset
        address0 = self._read_Null()
        if address0 is FAILURE:
            self._offset = index1
            address0 = self._read_Number()
            if address0 is FAILURE:
                self._offset = index1
                address0 = self._read_Literal()
                if address0 is FAILURE:
                    self._offset = index1
                    address0 = self._read_Reference()
                    if address0 is FAILURE:
                        self._offset = index1
        self._cache['Operand'][index0] = (address0, self._offset)
        return address0

    def _read_Reference(self):
        address0, index0 = FAILURE, self._offset
        cached = self._cache['Reference'].get(index0)
        if cached:
            self._offset = cached[1]
            return cached[0]
        remaining0, index1, elements0, address1 = 1, self._offset, [], True
        while address1 is not FAILURE:
            chunk0 = None
            if self._offset < self._input_size:
                chunk0 = self._input[self._offset:self._offset + 1]
            if chunk0 is not None and Grammar.REGEX_1.search(chunk0):
                address1 = TreeNode(self._input[self._offset:self._offset + 1], self._offset)
                self._offset = self._offset + 1
            else:
                address1 = FAILURE
                if self._offset > self._failure:
                    self._failure = self._offset
                    self._expected = []
                if self._offset == self._failure:
                    self._expected.append('[a-zA-Z0-9]')
            if address1 is not FAILURE:
                elements0.append(address1)
                remaining0 -= 1
        if remaining0 <= 0:
            address0 = self._actions.make_reference(self._input, index1, self._offset, elements0)
            self._offset = self._offset
        else:
            address0 = FAILURE
        self._cache['Reference'][index0] = (address0, self._offset)
        return address0

    def _read_Literal(self):
        address0, index0 = FAILURE, self._offset
        cached = self._cache['Literal'].get(index0)
        if cached:
            self._offset = cached[1]
            return cached[0]
        index1, elements0 = self._offset, []
        address1 = FAILURE
        chunk0 = None
        if self._offset < self._input_size:
            chunk0 = self._input[self._offset:self._offset + 1]
        if chunk0 == '\'':
            address1 = TreeNode(self._input[self._offset:self._offset + 1], self._offset)
            self._offset = self._offset + 1
        else:
            address1 = FAILURE
            if self._offset > self._failure:
                self._failure = self._offset
                self._expected = []
            if self._offset == self._failure:
                self._expected.append('"\'"')
        if address1 is not FAILURE:
            elements0.append(address1)
            address2 = FAILURE
            remaining0, index2, elements1, address3 = 0, self._offset, [], True
            while address3 is not FAILURE:
                index3, elements2 = self._offset, []
                address4 = FAILURE
                index4 = self._offset
                chunk1 = None
                if self._offset < self._input_size:
                    chunk1 = self._input[self._offset:self._offset + 1]
                if chunk1 == '\'':
                    address4 = TreeNode(self._input[self._offset:self._offset + 1], self._offset)
                    self._offset = self._offset + 1
                else:
                    address4 = FAILURE
                    if self._offset > self._failure:
                        self._failure = self._offset
                        self._expected = []
                    if self._offset == self._failure:
                        self._expected.append('"\'"')
                self._offset = index4
                if address4 is FAILURE:
                    address4 = TreeNode(self._input[self._offset:self._offset], self._offset)
                    self._offset = self._offset
                else:
                    address4 = FAILURE
                if address4 is not FAILURE:
                    elements2.append(address4)
                    address5 = FAILURE
                    if self._offset < self._input_size:
                        address5 = TreeNode(self._input[self._offset:self._offset + 1], self._offset)
                        self._offset = self._offset + 1
                    else:
                        address5 = FAILURE
                        if self._offset > self._failure:
                            self._failure = self._offset
                            self._expected = []
                        if self._offset == self._failure:
                            self._expected.append('<any char>')
                    if address5 is not FAILURE:
                        elements2.append(address5)
                    else:
                        elements2 = None
                        self._offset = index3
                else:
                    elements2 = None
                    self._offset = index3
                if elements2 is None:
                    address3 = FAILURE
                else:
                    address3 = TreeNode(self._input[index3:self._offset], index3, elements2)
                    self._offset = self._offset
                if address3 is not FAILURE:
                    elements1.append(address3)
                    remaining0 -= 1
            if remaining0 <= 0:
                address2 = TreeNode(self._input[index2:self._offset], index2, elements1)
                self._offset = self._offset
            else:
                address2 = FAILURE
            if address2 is not FAILURE:
                elements0.append(address2)
                address6 = FAILURE
                chunk2 = None
                if self._offset < self._input_size:
                    chunk2 = self._input[self._offset:self._offset + 1]
                if chunk2 == '\'':
                    address6 = TreeNode(self._input[self._offset:self._offset + 1], self._offset)
                    self._offset = self._offset + 1
                else:
                    address6 = FAILURE
                    if self._offset > self._failure:
                        self._failure = self._offset
                        self._expected = []
                    if self._offset == self._failure:
                        self._expected.append('"\'"')
                if address6 is not FAILURE:
                    elements0.append(address6)
                else:
                    elements0 = None
                    self._offset = index1
            else:
                elements0 = None
                self._offset = index1
        else:
            elements0 = None
            self._offset = index1
        if elements0 is None:
            address0 = FAILURE
        else:
            address0 = self._actions.make_literal(self._input, index1, self._offset, elements0)
            self._offset = self._offset
        self._cache['Literal'][index0] = (address0, self._offset)
        return address0

    def _read_Number(self):
        address0, index0 = FAILURE, self._offset
        cached = self._cache['Number'].get(index0)
        if cached:
            self._offset = cached[1]
            return cached[0]
        remaining0, index1, elements0, address1 = 1, self._offset, [], True
        while address1 is not FAILURE:
            chunk0 = None
            if self._offset < self._input_size:
                chunk0 = self._input[self._offset:self._offset + 1]
            if chunk0 is not None and Grammar.REGEX_2.search(chunk0):
                address1 = TreeNode(self._input[self._offset:self._offset + 1], self._offset)
                self._offset = self._offset + 1
            else:
                address1 = FAILURE
                if self._offset > self._failure:
                    self._failure = self._offset
                    self._expected = []
                if self._offset == self._failure:
                    self._expected.append('[0-9]')
            if address1 is not FAILURE:
                elements0.append(address1)
                remaining0 -= 1
        if remaining0 <= 0:
            address0 = self._actions.make_number(self._input, index1, self._offset, elements0)
            self._offset = self._offset
        else:
            address0 = FAILURE
        self._cache['Number'][index0] = (address0, self._offset)
        return address0

    def _read_Asterisk(self):
        address0, index0 = FAILURE, self._offset
        cached = self._cache['Asterisk'].get(index0)
        if cached:
            self._offset = cached[1]
            return cached[0]
        chunk0 = None
        if self._offset < self._input_size:
            chunk0 = self._input[self._offset:self._offset + 1]
        if chunk0 == '*':
            address0 = self._actions.make_asterisk(self._input, self._offset, self._offset + 1)
            self._offset = self._offset + 1
        else:
            address0 = FAILURE
            if self._offset > self._failure:
                self._failure = self._offset
                self._expected = []
            if self._offset == self._failure:
                self._expected.append('"*"')
        self._cache['Asterisk'][index0] = (address0, self._offset)
        return address0

    def _read_Semicolon(self):
        address0, index0 = FAILURE, self._offset
        cached = self._cache['Semicolon'].get(index0)
        if cached:
            self._offset = cached[1]
            return cached[0]
        index1, elements0 = self._offset, []
        address1 = FAILURE
        address1 = self._read__()
        if address1 is not FAILURE:
            elements0.append(address1)
            address2 = FAILURE
            chunk0 = None
            if self._offset < self._input_size:
                chunk0 = self._input[self._offset:self._offset + 1]
            if chunk0 == ';':
                address2 = TreeNode(self._input[self._offset:self._offset + 1], self._offset)
                self._offset = self._offset + 1
            else:
                address2 = FAILURE
                if self._offset > self._failure:
                    self._failure = self._offset
                    self._expected = []
                if self._offset == self._failure:
                    self._expected.append('";"')
            if address2 is not FAILURE:
                elements0.append(address2)
            else:
                elements0 = None
                self._offset = index1
        else:
            elements0 = None
            self._offset = index1
        if elements0 is None:
            address0 = FAILURE
        else:
            address0 = TreeNode17(self._input[index1:self._offset], index1, elements0)
            self._offset = self._offset
        self._cache['Semicolon'][index0] = (address0, self._offset)
        return address0

    def _read_Null(self):
        address0, index0 = FAILURE, self._offset
        cached = self._cache['Null'].get(index0)
        if cached:
            self._offset = cached[1]
            return cached[0]
        chunk0 = None
        if self._offset < self._input_size:
            chunk0 = self._input[self._offset:self._offset + 4]
        if chunk0 is not None and chunk0.lower() == 'Null'.lower():
            address0 = self._actions.make_null(self._input, self._offset, self._offset + 4)
            self._offset = self._offset + 4
        else:
            address0 = FAILURE
            if self._offset > self._failure:
                self._failure = self._offset
                self._expected = []
            if self._offset == self._failure:
                self._expected.append('`Null`')
        self._cache['Null'][index0] = (address0, self._offset)
        return address0

    def _read__(self):
        address0, index0 = FAILURE, self._offset
        cached = self._cache['_'].get(index0)
        if cached:
            self._offset = cached[1]
            return cached[0]
        remaining0, index1, elements0, address1 = 0, self._offset, [], True
        while address1 is not FAILURE:
            chunk0 = None
            if self._offset < self._input_size:
                chunk0 = self._input[self._offset:self._offset + 1]
            if chunk0 is not None and Grammar.REGEX_3.search(chunk0):
                address1 = TreeNode(self._input[self._offset:self._offset + 1], self._offset)
                self._offset = self._offset + 1
            else:
                address1 = FAILURE
                if self._offset > self._failure:
                    self._failure = self._offset
                    self._expected = []
                if self._offset == self._failure:
                    self._expected.append('[ \\t\\r\\n]')
            if address1 is not FAILURE:
                elements0.append(address1)
                remaining0 -= 1
        if remaining0 <= 0:
            address0 = TreeNode(self._input[index1:self._offset], index1, elements0)
            self._offset = self._offset
        else:
            address0 = FAILURE
        self._cache['_'][index0] = (address0, self._offset)
        return address0

    def _read___(self):
        address0, index0 = FAILURE, self._offset
        cached = self._cache['__'].get(index0)
        if cached:
            self._offset = cached[1]
            return cached[0]
        remaining0, index1, elements0, address1 = 1, self._offset, [], True
        while address1 is not FAILURE:
            chunk0 = None
            if self._offset < self._input_size:
                chunk0 = self._input[self._offset:self._offset + 1]
            if chunk0 is not None and Grammar.REGEX_4.search(chunk0):
                address1 = TreeNode(self._input[self._offset:self._offset + 1], self._offset)
                self._offset = self._offset + 1
            else:
                address1 = FAILURE
                if self._offset > self._failure:
                    self._failure = self._offset
                    self._expected = []
                if self._offset == self._failure:
                    self._expected.append('[ \\t\\r\\n]')
            if address1 is not FAILURE:
                elements0.append(address1)
                remaining0 -= 1
        if remaining0 <= 0:
            address0 = TreeNode(self._input[index1:self._offset], index1, elements0)
            self._offset = self._offset
        else:
            address0 = FAILURE
        self._cache['__'][index0] = (address0, self._offset)
        return address0


class Parser(Grammar):
    def __init__(self, input, actions, types):
        self._input = input
        self._input_size = len(input)
        self._actions = actions
        self._types = types
        self._offset = 0
        self._cache = defaultdict(dict)
        self._failure = 0
        self._expected = []

    def parse(self):
        tree = self._read_Statement()
        if tree is not FAILURE and self._offset == self._input_size:
            return tree
        if not self._expected:
            self._failure = self._offset
            self._expected.append('<EOF>')
        raise ParseError(format_error(self._input, self._failure, self._expected))


def format_error(input, offset, expected):
    lines, line_no, position = input.split('\n'), 0, 0
    while position <= offset:
        position += len(lines[line_no]) + 1
        line_no += 1
    message, line = 'Line ' + str(line_no) + ': expected ' + ', '.join(expected) + '\n', lines[line_no - 1]
    message += line + '\n'
    position -= len(line) + 1
    message += ' ' * (offset - position)
    return message + '^'

def parse(input, actions=None, types=None):
    parser = Parser(input, actions, types)
    return parser.parse()
