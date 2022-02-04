#!/bin/bash

# 1. Delete the saltbox_dependencies directory (locally)
workon employeefinder
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver