# Database Syncing Project
---
Authors: Nick Boukis & Sami Shahin  

### Python Version
2.7.10

### Installation
```sh
$ pip install bitarray
```  

### Running Demonstration
1. Connect computers via ethernet
2. Run ```ipconfig``` on the Windows computer to find the IP address of the ethernet port, this will be considered the "DB2 IP Address"
3. Get IP address of Mac's ethernet port by going to settings, pass this as a variable in ip_from

ON WINDOWS:

4. Change IP address in ```db2.py```
5. Run
```sh
$ F:
$ cd /path/to/db2.py
$ activate snakes
$ set PYTHONPATH=/path/to/EC504-Final-Project
$ python db2.py
``` 

ON MAC:

6. Open two tabs in terminal, left is ```db1_gui``` and right is ```db3```

IN ```db3``` TAB:

7. Run
```sh
$ cd /path/to/db3.py
$ export PYTHONPATH=/path/to/EC504-Final-Project
$ python db3.py
``` 

IN ```db1_gui``` TAB:

8. Run
```sh
$ cd /path/to/EC504-Final-Project
$ python db1_gui.py
``` 