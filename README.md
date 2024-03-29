# FreeCAD-Reporting
The Reporting Workbench makes it possible to extract informations out of a FreeCAD document pretty easily. It can be used via Python or via the GUI. A bit like the "Arch Schedule" Tool on steroids ;)

![Intro](./Documentation/intro.png)


## Motivation

I was working on an personal Architecture Project. After there where a lot of walls, windows, doors etc. in the model, I needed an easy way to get the information out of the model. I was not happy with the arch schedule tool, as I think it is not as flexible as it could be. As I work with SQL (Structured Query Language https://en.wikipedia.org/wiki/SQL) a lot during work, I decided to give it a try and create a SQL Module for FreeCAD.

## Getting started

<details>
<summary>
This section gives you a step by step introduction on how to get startet with the workbench. It will guide you through the process of creating a simple report to extract some data out of a FreeCAD Document.

more...
</summary>
    
1. First you should install the Reporting Workbench. It is available from the addon manager directly in FreeCAD. Go to ```Tools > Addon Manager```, scroll down select the ```Reporting``` entry and click ```Install```. It's best to restart FreeCAD after the installation is done.

![Addon Manager](./Documentation/addon_manager.png)

2. Next you should download the sample File [Simple_House.FCStd](./Documentation/Simple_House.FCStd) and open it in FreeCAD. Now you should see something like this.

![Sample House](./Documentation/Sample_House.png)
    
This file contains a simple House with some rooms and doors. Its not pretty, but it should be good enough to extract some data out of it ;)

3. Now that the file is set up, we should fire up the report workbench and create our first report.

![Create Report](./Documentation/create_report.png)

4. Now we have a empty Report object. Lets fill it with data. Lets say we want to query some informations about the rooms inside the house. Double click the ```Report``` object in the Treeview and the configuration shows up. Click ```Add Statement``` to add a new statement.

![Add Statement](./Documentation/add_statement.png)

5. Now fill in "Rooms" into the ```Header``` field and the following statement into the ```Statement``` field

```sql
Select Label, Area
From document
Where IfcRole = 'Space'
```

6. Click ```OK```. The Task dialog closes and the report recomputes.

7. Expand the Report in the Treeview and you should see a Spreadsheet named ```Result```. Double click on it to see its content.

![Report Result](./Documentation/report_result.png)

What do we see here?
 - (1) The header we added in the Report Config
 - (2) The column names extracted from our statement
 - (3) The list of objects matching our statement and the values extracted for each column

8. This is pretty good. But I think we can do even better. Double click the Report in the Treeview again. Click on ```Add Statement``` and add "Living Area" in the ```Header``` field. Also enable ```Skip empty rows after statement``` here and add the following in the ```Statement``` field:

```sql
Select Tag, Sum(Area)
From document
Where IfcRole = 'Space'
Group By Tag
```

9. Click ```Add Statement``` once again and leave the ```Header``` field empty. Enable ```Skip Column Names``` and ```Print Result in Bold``` and add the following to the ```Statement``` field:

```sql
Select 'Total', Sum(Area)
From document
Where IfcRole = 'Space'
```

10. If you look at the ```Result``` Spreadsheet again you see that there is some more data below the room list now

![Report Result Extended](./Documentation/report_result_extended.png)

 - (1) The living area on the upper floor
 - (2) The living area on the ground floor
 - (3) And the overall living area for the entire building

11. This is the end of the getting started guide. Whats next?
 - Feel free to play around and add more Reports or more statements to the Report we created right now.
 - If you are familiar with the Python in FreeCAD, you might want to read the ```Getting started with python``` section
 - Read the ```SQL Reference``` section for an overview of the supported SQL Features

</details>

## Getting started with python

<details>
<summary>

This section gives you a step by step introduction on how to get startet with the sql module in python.

more...
</summary>

1. First you should install the Reporting Workbench. It is available from the addon manager directly in FreeCAD. Go to ```Tools > Addon Manager```, scroll down select the ```Reporting``` entry and click ```Install```. It's best to restart FreeCAD after the installation is done.

![Addon Manager](./Documentation/addon_manager.png)

2. Next you should download the sample File [Simple_House.FCStd](./Documentation/Simple_House.FCStd) and open it in FreeCAD. Now you should see something like this.

![Sample House](./Documentation/Sample_House.png)
    
This file contains a simple House with some rooms and doors. Its not pretty, but it should be good enough to extract some data out of it ;)

3. Now that everything is set up, open the python console and import the SQL Parser and create a new instance. The parser can be used to parse as may statements as you want.

```python
from sql import freecad_sql_parser
sql_parser = freecad_sql_parser.newParser()
```

4. Now use the sql_parser to parse a statement. You can execute a parsed statement as often as you want.

```python
select_all = sql_parser.parse('Select * from document')
```

5. Now execute the statement. This will give you a list of all objects in the document.

```python
all_objects = select_all.execute()
str(all_objects)
'[[<App::GeometryPython object>], [<App::GeometryPython object>], [<App::GeometryPython object>], [<Sketcher::SketchObject>], [<group object>], [<Sketcher::SketchObject>], [<Sketcher::SketchObject>], [<Part::PartFeature>], [<Sketcher::SketchObject>], [<Part::PartFeature>], [<Sketcher::SketchObject>], [<Part::PartFeature>], [<Sketcher::SketchObject>], [<Part::PartFeature>], [<Sketcher::SketchObject>], [<Part::PartFeature>], [<Sketcher::SketchObject>], [<Part::PartFeature>], [<Sketcher::SketchObject>], [<Part::PartFeature>], [<Sketcher::SketchObject>], [<Part::PartFeature>], [<Part::PartFeature>], [<Sketcher::SketchObject>], [<Part::PartFeature>], [<Part::PartFeature>], [<Part::PartFeature>], [<Part::PartFeature>], [<Part::PartFeature>], [<Part::PartFeature>], [<Part::PartFeature>], [<Part::PartFeature>], [<Part::PartFeature>], [<Part::PartFeature>], [<Part::PartFeature>], [<Part::PartFeature>], [<Part::PartFeature>]]'
```

</details>

## How To...

<details>
<summary>
Check this section for a list of common sql queries.

more...
</summary>

### General

[... add a Result Row for a Statement](./Documentation/Howto/General/add_result_row_in_report.md)

[... create a report collection](./Documentation/Howto/General/create_report_collection.md)

### Architecture
[... get a list of arch objects by role](./Documentation/Howto/Arch/get_number_of_objects_by_role.md)

</details>

## SQL Reference

<details>
<summary>
Check out this section when you want to know something about SQL and what features are supported by this Workbench.

more...
</summary>
SQL (Structured Query Language) is a language that is normally used to manage and retrieve data from databases. But with this workbench, we can use it to select data from FreeCAD documents.

A Select statement basically looks like this

```sql
Select <Columns>
From <Source>
Where <Expression>
Group By <GroupingColumns>
```

```Select``` and ```From``` clauses are mandatory, ```Where``` and ```Group By``` are optional.

### Select \<Columns>

Columns is a comma separated list of attributes you want in the result.

```sql
Select Attribute1, Attribute2, 'sometext', sum(Attribute3) As 'Sum'
From document
```

You can use ```*``` as a special property in the select clause, to retrieve the whole object instead of a single property. This might be expecially useful when you want to perform certain operations on some objects in python. You can select them with a select statement, and process them afterwards.

You can also use functions to aggregate data for a given attribute. Supported functions are
 - **Sum**: Calculates the Sum of the given attribute
 - **Count**: Counts all not ```None``` attributes. You might want to use ```Count(*)``` to get the number of selected objects
 - **Min**: Gets the minimum Value of the given Attribute
 - **Max**: Gets the maximum Value of the given Attribute

There are also some non grouping functions. These can be used like normal references or static values:
 - **Concat**: Takes a comma separated list of references or static values and combines them to a single string value. (e.g. Concat(Label, ': ', Area))
 - **Type**: Returns the type of the given object. When the object has a "Proxy" Attribute, the type of the Proxy will be returned.
 - **Lower**: Returns a text representation of the argument converted to lower case. This can be useful when comparing strings and sometimes they are upper case, and sometimes they are lowercase.
 - **Upper**: Returns a text representation of the argument converted to upper case. This can be useful when comparing strings and sometimes they are upper case, and sometimes they are lowercase.

Without a group by clause, it is not possible to mix references and aggregating functions in a select statements. The only exceptions are static values (E.g. "Select 'Number of objects', Count(*).."). 
Only a single row will be returned for such a query. See ```Group by``` for more details on mixing attributes and functions.

#### Column names

By default the name of a column will be the literal text of the expression. E.g.
 - "sum(Attribute3)"
 - "Attribute2"
 - "sometext"

Sometimes this is not what you want. Especially for columns containing a function. You can use the ```AS``` clause to give a column a explicit name like we did with the ```sum(Attribute3)``` column above.

#### Arithmetics

You can use simple arithmetics inside a column. E.g.

```sql
Select Area / 2
From document
```

The following operators are available:
 - *: Multiplication
 - /: Division
 - +: Addition
 - -: Subtraction

### From \<Source>

The objects from the document you want to select.

**document** is a special keyword, that selects all objects in the active document. This is the only supported source right now.

### Where \<Expression>

The where clause can be used to filter the objects in the From clause.

```sql
Select *
From document
Where IfcRole = 'Space' AND (Label = 'UF_Cooridor' OR Label = 'GF_Corridor')
```

Normally you want to compare Attributes for some given values. A comparison is written in the form ```Left ComparisonOperator Right``` Where ```Left``` and ```Right``` can either be Attributes or static values. You can use the following comparison operators:
 - **=**: Checks if the left value is equals to the right value
 - **!=**: Checks if the left value is not equals to the right value
 - **>**: Checks if the left value is greater than the right value
 - **<**: Checks if the left value is less than the right value
 - **>=**: Checks if the left value is greater than or equals to the right value
 - **<=**: Checks if the left value is less than or equals to the right value

There are also two special comparison operators available to check for ```None```. This normally means, that a given object does not have the given attribute or it has no value assigend.
 - **IS NULL**: Checks if the left value is None.
 - **IS NOT NULL**: Check if the left value is not None. This is especially usefull to filter all objects that do not have the given attribute assigned.

There is also the special comparison operator ```LIKE``` available that let you compare text using a pattern. The pattern can contain the following special characters:
 - **?** matches a single character
 - **%** matches zero, one or more characters.
For example the pattern ```Body0?1``` would match the strings ```Body001``` or ```Body011``` but would not match ```Body002```. And the pattern ```Body%``` would match all strings starting with Body. E.g. ```Body001``` or ```Body123```. You can also mix multiple special characters in the pattern.

To combine multiple comparisons you can use the ```AND``` and ```OR``` keywords. You can also use Brackets ```(``` ```)``` to build complex expressions.

### Group By \<GroupingColumns>

The Group by clause can be used to group objects by given attributes. We saw this before. It is not possible to mix attributes and functions without a group by clause.

```sql
Select Tag, Sum(Area)
From document
Where IfcRole = 'Space'
Group By Tag
```

What does this query do? When it runs it groups all the spaces in the document by their ```Tag``` Attribute. So wen we have spaces with 3 different tags, we will get 3 rows when executing the statement. Each row will contain the Tag, and the sum of the area of all spaces for the given group.

You can use multiple attributes non grouping functions and even static values like numbers or text in the Group By clause. But the select part can only contain single attributes, that are also referenced in the group by clause. Functions in the select clause can reference other attributes too.

e.g. this would be a invalid statement

```sql
Select Label, Sum(Area)
From document
Group By Tag, IfcRole
```

You can not use the ```Label``` Attribute in the select clause, because it is not referenced in the group by clause.

</details>

## Dependencies
The Workbench does not need any additional software to be installed to be fully functional.

## Support
Found a bug? Have a nice feature request? simply create an issue in this repository or post to this FreeCAD Forum threads

Bug/Help Request: https://forum.freecadweb.org/viewtopic.php?f=3&t=38225
New Features: https://forum.freecadweb.org/viewtopic.php?f=10&t=38224