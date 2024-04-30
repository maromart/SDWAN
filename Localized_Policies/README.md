# SD-WAN Localized Policies 
In Cisco SD-WAN, a Localized Policy is attached to one or many Device Templates and a Device Template is attached to one or many devices.

Also, a Localized Policy may content:
- QoS Map Scheduler
- ACL/Access Device List
- Route Policies
  
This script generates an interactive treemap diagram with D3.js in HTML/JS to visualize the relationships.

Also, you can view the static information in a spreadsheet.

Note: The python script collects:
-  Localized Policies information if they were created through vManager wizard
-  Device Templates and Devices information if they are in vManage mode


## Installation
- Install requirements.txt
- Clone or download the repository
- Internet connection to connect to D3.js source script

## Usage
Run locpol.py
```
Please enter vManager url without https:// <IP or URL with port(optional)>
username:<Enter username>
Password:<Enter password>
Getting session cookie...
OK...
Getting token...
Token OK...
Getting device templates...
```

Once the script finishes, you can open the generated spreadsheet and/or HTML file

- On spreadsheet, go to Localized Policies tab.

- On HTML, click on Localized Policies square (node) to expand or collapse.

  Color convention:

  - Purple: Localized Policies
  - Green: Device Templates
  - Blue: Devices

  If the name of the node  is positioned on the left side, this means it has descendants.


## Built With
- [Python](https://www.python.org/)
- [D3.js](https://d3js.org/)
- [Javascript](https://www.javascript.com/)

## Autors
- Mario Uriel Romero

Initiative and ideas in conjuntion with
- Lei Tian

## Acknowledgment
This script was tested with 20 and 120 devices.

For a greater number of devices it is advisable to use the spreadsheet file.

The HTML window size is adjusted to display all the information, nevertheless the navigation experience can be affected and you may apply zoom in/out.






