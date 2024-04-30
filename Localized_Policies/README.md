# SD-WAN Localized Policies 
In Cisco SD-WAN, a Localized Policy is attached to Device Templates and a Device Template is attached to one or many devices.

This script generates an interactive treemap diagram in HTML/JS and an spreadsheet containing the relationships.

Note: The script collects:
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
username:<Enter username>https://github.com/maromart/SDWAN/pulls
Password:<Enter password>
Getting session cookie...
OK...
Getting token...
Token OK...
Getting device templates...
```
## Built With
- [Python](https://www.python.org/)
- [D3.js](https://d3js.org/)

## Autors
- Mario Uriel Romero

## Acknowledgment

Initiative and ideas in conjuntion with
- Lei Tian



