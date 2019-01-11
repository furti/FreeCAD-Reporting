var sql = require("./sql");

function SelectStatement() {}

SelectStatement.prototype.validate = function() {
  // At least one column
  // From clause set
  // No grouping functions and normal columns mixed without group by
};

function FromClause(reference) {
  this.reference = reference;
}

function WhereClause(filter) {
  this.filter = filter;
}

function Column(columnName, dataExtractor, grouping) {
  this.columnName = columnName;
  this.dataExtractor = dataExtractor;
  this.grouping = grouping;
}

function Columns(columns) {
  this.columns = columns;
}

function Reference(value) {
  this.value = value;
}

Reference.prototype.getValue = function(o) {
  return o[this.value];
};

function IdentityExtractor() {}

IdentityExtractor.prototype.extract = function(row) {
  return row;
};

function StaticExtractor(value) {
  this.value = value;
}

StaticExtractor.prototype.extract = function() {
  return this.value;
};

function ReferenceExtractor(reference) {
  this.reference = reference;
}

ReferenceExtractor.prototype.extract = function(row) {
  return this.reference.getValue(row);
};

function CalculationExtractor(calculation) {
  this.calculation = calculation;
}

CalculationExtractor.prototype.extract = function(row, currentValue) {
  return this.calculation.calculate(row, currentValue);
};

function Calculation(operator, dataExtractor, name) {
  this.operator = operator;
  this.dataExtractor = dataExtractor;
  this.name = name;
}

Calculation.prototype.calculate = function(o, currentValue) {
  var value = this.dataExtractor.extract(o);

  return this.operator.calculate(currentValue, value);
};

function SumOperator() {
  this.isOperator = true;
}

function CountOperator() {
  this.isOperator = true;
}

function OrBooleanOperator() {}

function AndBooleanOperator() {}

function EqualsComparisonOperator() {}

function BooleanComparison(leftExtractor, rightExtractor, comparisonOperator) {
  this.leftExtractor = leftExtractor;
  this.rightExtractor = rightExtractor;
  this.comparisonOperator = comparisonOperator;
}

function getReference(elements) {
  for (element of elements) {
    if (element instanceof Reference) {
      return element;
    }
  }
}

function prepareSelectStatementWithElements(statement, elements) {
  for (element of elements) {
    if (element instanceof FromClause) {
      statement.fromClause = element;
    }

    if (element instanceof Columns) {
      statement.columns = element;
    }

    if (element instanceof WhereClause) {
      statement.whereClause = element;
    }
  }
}

function extractColumns(elements) {
  var columns = [];

  for (element of elements) {
    if (element === "*") {
      columns.push(new Column("*", new IdentityExtractor(), false));
    } else if (typeof element === "number") {
      columns.push(
        new Column(element.toString(), new StaticExtractor(element), false)
      );
    } else if (typeof element === "string") {
      columns.push(new Column(element, new StaticExtractor(element), false));
    } else if (element instanceof Reference) {
      columns.push(
        new Column(element.value, new ReferenceExtractor(element), false)
      );
    } else if (element instanceof Calculation) {
      columns.push(
        new Column(element.name, new CalculationExtractor(element), true)
      );
    } else if (Array.isArray(element.elements)) {
      columns = columns.concat(extractColumns(element.elements));
    }
  }

  return columns;
}

var actions = {
  make_number: function(input, start, end, elements) {
    return parseInt(input.substring(start, end), 10);
  },

  make_reference: function(input, start, end, elements) {
    return new Reference(input.substring(start, end));
  },

  make_from_clause: function(input, start, end, elements) {
    var reference = getReference(elements);

    return new FromClause(reference);
  },

  make_where_clause: function(input, start, end, elements) {
    // console.log("%o", elements);
    return new WhereClause();
  },

  make_boolean_operator_and: function(input, start, end, elements) {
    return new AndBooleanOperator();
  },

  make_boolean_operator_or: function(input, start, end, elements) {
    return new OrBooleanOperator();
  },

  make_comp_operator_eq: function(input, start, end, elements) {
    return new EqualsComparisonOperator();
  },

  make_boolean_comparison: function(input, start, end, elements) {
    console.log("%o", elements);

    return elements;
  },

  make_select_statement: function(input, start, end, elements) {
    var selectStatement = new SelectStatement();

    prepareSelectStatementWithElements(selectStatement, elements);

    return selectStatement;
  },

  make_literal: function(input, start, end, elements) {
    return input.substring(start + 1, end - 1);
  },

  sum_operator: function(input, start, end, elements) {
    return new SumOperator();
  },

  count_operator: function(input, start, end, elements) {
    return new CountOperator();
  },

  min_operator: function(input, start, end, elements) {
    throw "min not implemented";
  },

  max_operator: function(input, start, end, elements) {
    throw "max not implemented";
  },

  make_function: function(input, start, end, elements) {
    // var filtered = elements.filter(element => {
    //   return element !== "(" && element !== ")" && element.trim().length > 0;
    // });

    var operator;
    var dataExtractor;

    for (element of elements) {
      if (element.isOperator) {
        operator = element;
      } else if (element === "*") {
        dataExtractor = new IdentityExtractor();
      } else if (typeof element === "number" || typeof element === "string") {
        dataExtractor = new StaticExtractor(element);
      } else if (element instanceof Reference) {
        dataExtractor = new ReferenceExtractor(element);
      }
    }

    if (!operator || !dataExtractor) {
      throw "Unsupported calculation! Operator: " +
        operator +
        ", Extractor: " +
        dataExtractor;
    }

    return new Calculation(
      operator,
      dataExtractor,
      input.substring(start, end)
    );
  },

  prepare_columns: function(input, start, end, elements) {
    var columns = extractColumns(elements);

    return new Columns(columns);
  },

  prepare_asterisk: function(input, start, end, elements) {
    return "*";
  }
};

function doParse(sqlString) {
  console.log("------------------");
  console.log(sqlString + "\n");

  var statement = sql.parse(sqlString, { actions: actions });

  console.log("%o", statement);
}

// doParse(`SELECT * FROM document;`);

// doParse(`SELECT *
// FROM wall`);

// doParse(`SELECT *, 453, 'somestring', col
// FROM wall`);

// doParse(`SELECT Count(*), Sum(43), Sum(numb) FROM document;`);

doParse(`SELECT Count(*), Sum(43), Sum(numb) FROM document Where numb = 14;`);
