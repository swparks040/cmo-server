#!/bin/bash

# rm db.sqlite3
# rm -rf ./cmoapi/migrations
# python3 manage.py migrate
# python3 manage.py makemigrations cmoapi
# python3 manage.py migrate cmoapi
python3 manage.py loaddata categories
python3 manage.py loaddata pto
python3 manage.py loaddata family_member_relationships
python3 manage.py loaddata family_members
python3 manage.py loaddata messages
python3 manage.py loaddata responses