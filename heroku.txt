git init                                         # Only necessary if this is not already a 
                                                   # git repository
$ heroku create
$ heroku config:set SECRET_KEY=KjJPe35tQKY2YLRzm7vhm3aJdqqh8YHR
$ pip install gunicorn psycopg2-binary
$ pip freeze > requirements.txt
$ echo "web: gunicorn main:app" > Procfile
$ git add .; git commit -a -m "Initial commit"     # Only necessary because this is a new git repo.
$ git push heroku master                           # If you have any changes or files to add,
                                                   # commit them before you push. 
$ heroku addons:create heroku-postgresql:hobby-dev
$ heroku run python setup.py
$ heroku open