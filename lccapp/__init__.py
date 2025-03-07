# This script runs automatically when our `loginapp` module is first loaded,
# and handles all the setup for our Flask app.
from flask import Flask

app = Flask(__name__)

# Set the "secret key" that our app will use to sign session cookies. This can
# be anything.
# 
# Anyone with access to this key can pretend to be signed in as any user. In a
# real-world project, you wouldn't store this key in your source code. To learn
# about how to manage "secrets" like this in production code, check out
# https://blog.gitguardian.com/how-to-handle-secrets-in-python/
#
# For the purpose of your assignments, you DON'T need to use any of those more
# advanced and secure methods: it's fine to store your secret key in your
# source code like we do here.
app.secret_key = 'COMP 639'

# Set up database connection.
from lccapp import db
from lccapp import connect
db.init_db(app, connect.dbuser, connect.dbpass, connect.dbhost, connect.dbname)

# Include all modules that define our Flask route-handling functions.
from lccapp import user
from lccapp import admin
from lccapp import profile
from lccapp import my_issues
from lccapp import user_issues
from lccapp import user_management
