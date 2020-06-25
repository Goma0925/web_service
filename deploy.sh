git add --all
git commit -m "Deployed to heroku by command line"
git push heroku master
heroku run python manage.py makemigrations users
heroku run python manage.py makemigrations taggit
heroku run python manage.py makemigrations
heroku run python manage.py migrate users
heroku run python manage.py migrate events
heroku run python manage.py migrate
