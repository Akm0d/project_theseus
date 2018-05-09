# Project Theseus
This project is forked from the private repo of the OpenWest Defusal Station project. It is named "Project Theseus" after the paradox of the Ship of Theseus; a thought experiment that raises the question of whether an object that has had all of its components replaced remains fundamentally the same object.

# Contribution Guidelines
1. Create a branch for your code and merge it to master once the changes are stable
2. Keep the file structure as organized as possible
3. Never commit binaries, hidden files created by your IDE, or Windows-style line endings.
4. Keep detailed comments of what each function is meant to do
5. Follow the PEP-8 standard when writing python https://www.python.org/dev/peps/pep-0008/
6. Use comments starting with TODO to mark a feature that needs to be implemented and FIXME to mark features that need to be improved
7. If you are stuck, then it is absolutely OK to ask for help

# Getting Started
```bash
$ sudo apt-get update
$ sudo apt-get install python3 git python3-pip
$ git clone https://github.com/jtylers/project_theseus.git
$ cd project_theseus/python
$ pip3 install -r requirements.txt
$ ./serve.py
$ firefox 127.0.0.1:5000
```
I highly suggest using PyCharm if you are working with Flask and Python
```bash
$ sudo apt-get update
$ sudo apt-get install snapd
$ snap install pycharm-community
```

## Where are variables stored?
### Stored in the database
ID
Name
Laser
Code
Color
Time    -- Stored as a datetime object but written at end of game
Success
