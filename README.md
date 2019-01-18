# FreeCAD-Reporting
The Reporting Workbench makes it possible to extract informations out of a FreeCAD document pretty easily. It can be used via Python or via the GUI. A bit like the "Arch Schedule" Tool on steroids ;)

## Motivation

I was working on an personal Architecture Project. After there where a lot of walls, windows, doors etc. in the model, I needed an easy way to get the information out of the model. I was not happy with the arch schedule tool, as I think it is not as flexible as it could be. As I work with SQL (Structured Query Language https://en.wikipedia.org/wiki/SQL) a lot during work, I decided to give it a try and create a SQL Module for FreeCAD.

## Getting started

<details>
<summary>
This section gives you a step by step introduction on how to get startet with the workbench. It will guide you through the process of creating a simple report to extract some data out of a FreeCAD Document.

more...
</summary>
    
1. First you should download the Reporting Workbench. It is not in the addon manager right now. So download the ZIP from this repository and copy it to your FreeCAD Addon directory (https://www.freecadweb.org/wiki/How_to_install_additional_workbenches)

![Download Zip](./Documentation/download_zip.png)

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

8. This is pretty good. But I think we can do even better. Double click the Report in the Treeview again. Click on ```Add Statement``` and add "Living Area" in the ```Header``` field and the following in the ```Statement``` field:

```sql
Select Tag, Sum(Area)
From document
Where IfcRole = 'Space'
Group By Tag
```

9. Click ```Add Statement``` once again and leave the ```Header``` field empty and add the following to the ```Statement``` field:

```sql
Select Sum(Area)
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
    
    comming soon...
</details>

## SQL Reference

<details>
<summary>
Check out this section when you want to know something about SQL and what features are supported by this Workbench.

more...
</summary>
    
    comming soon...
</details>

## Dependencies
The Workbench does not need any additional software to be installed to be fully functional.

## Support
Found a bug? Have a nice feature request? simply create an issue in this repository or post to this FreeCAD Forum thread https://forum.freecadweb.org/viewtopic.php?f=9&t=33403.