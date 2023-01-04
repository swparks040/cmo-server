rm db.sqlite3
rm -rf ./cmoapi/migrations
python3 manage.py makemigrations cmoapi
python3 manage.py migrate
python3 manage.py loaddata users
python3 manage.py loaddata tokens
python3 manage.py loaddata cmousers
python3 manage.py loaddata family_member_relationships
python3 manage.py loaddata family_members
python3 manage.py loaddata categories
python3 manage.py loaddata pto
python3 manage.py loaddata pto_requests
python3 manage.py loaddata messages
python3 manage.py loaddata comments