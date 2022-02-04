Requirements:
- Python version >= 3.6 [https://www.python.org/ftp/python/3.10.2/python-3.10.2-amd64.exe]

- PIP:
	Download the script, from https://bootstrap.pypa.io/get-pip.py.
	Open a terminal/command prompt, cd to the folder containing the get-pip.py file and run:

	```python get-pip.py```

- Virtualenv:
	In your Command Prompt enter:

	```pip install virtualenv```

- Virtualenv Wrapper:
	In your Command Prompt enter:
	
	```pip install virtualenvwrapper-win```

Setup:

1. After all requirements are installed, Create a python virtual environment

	```mkvirtualenv -p python3 employeefinder```

2. Activate the virtual environment
	
	```workon employeefinder```

3. Once the virtual environment is active, Install all python package dependencies.

	```pip install -r requirements.txt```

4. Initialize the database. CD inside the Django Project where you will see the `manage.py` file then run:
	
	```python manage.py migrate```

5. populate necessary initial data via fixtures

	```sh load_fixtures.sh```

6. Create super user account. Follow on-screen instructions

	```python manage.py createsuperuser```

7. run the django server.

	```python manage.py runserver```

