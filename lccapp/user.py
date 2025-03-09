from lccapp import app
from lccapp import db
from flask import redirect, render_template, request, session, url_for, flash
from flask_bcrypt import Bcrypt
import re
from functools import wraps

# Create an instance of the Bcrypt class, which we'll be using to hash user
# passwords during login and registration.
flask_bcrypt = Bcrypt(app)

# Default role assigned to new users upon registration.
DEFAULT_USER_ROLE = 'visitor'


def role_required(allowed_roles=['admin', 'helper', 'visitor']):
    """
    Custom decorator to restrict access based on user roles.
     allowed_roles: List of roles allowed to access the function. Defaults to ['admin', 'helper', 'visitor'].
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if 'loggedin' not in session:
                return redirect(url_for('login'))
            if session.get('role') not in allowed_roles:
                return render_template('access_denied.html'), 403
            return func(*args, **kwargs)
        return wrapper
    return decorator


def user_home_url():
    """Generates a URL to the homepage for the currently logged-in user.
    
    If the user is not logged in, or the role stored in their session cookie is
    invalid, this returns the URL for the login page instead."""
    role = session.get('role', None)
    if role=='visitor':
        home_endpoint='visitor_home'
    elif role=='helper':
        home_endpoint='helper_home'
    elif role=='admin':
        home_endpoint='admin_home'
    else:
        home_endpoint = 'login'
    
    return url_for(home_endpoint)


@app.route('/')
def root():
    """Root endpoint (/)
    
    Methods:
    - get: Redirects guests to the login page, and redirects logged-in users to
        their own role-specific homepage.
    """
    return redirect(user_home_url())


@app.route('/admin/home')
@role_required(['admin'])
def admin_home():
     """Admin Homepage endpoint.
     """
     return render_template('admin_home.html')


@app.route('/helper/home')
@role_required(['helper'])
def helper_home():
     """Helper Homepage endpoint.
     """
     return render_template('helper_home.html')


@app.route('/visitor/home')
@role_required(['visitor'])
def visitor_home():
     """Visitor Homepage endpoint.
     """
     return render_template('visitor_home.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    """Login page endpoint.

    Methods:
    - get: Renders the login page.
    - post: Attempts to log the user in using the credentials supplied via the
        login form, and either:
        - Redirects the user to their role-specific homepage (if successful)
        - Renders the login page again with an error message (if unsuccessful).
    
    If the user is already logged in, both get and post requests will redirect
    to their role-specific homepage.
    """
    if 'loggedin' in session:
         return redirect(user_home_url())

    if request.method=='POST' and 'username' in request.form and 'password' in request.form:
        # Get the login details submitted by the user.
        username = request.form['username']
        password = request.form['password']

        # Attempt to validate the login details against the database.
        with db.get_cursor() as cursor:
            cursor.execute('''
                           SELECT user_id, username, password_hash, role, status, first_name
                           FROM users
                           WHERE username = %s;
                           ''', (username,))
            account = cursor.fetchone()
            
            if account is not None:
                # We found a matching account: now we need to check whether the
                # password they supplied matches the hash in our database.
                password_hash = account['password_hash']
                
                if flask_bcrypt.check_password_hash(password_hash, password):
                    # Password is correct. Save the user's ID, username, and role
                    # as session data, which we can access from other routes to
                    # determine who's currently logged in.
                    # 
                    # Users can potentially see and edit these details using their
                    # web browser. However, the session cookie is signed with our
                    # app's secret key. That means if they try to edit the cookie
                    # to impersonate another user, the signature will no longer
                    # match and Flask will know the session data is invalid.
                    if account['status'] == 'inactive':
                        flash("Your account is inactive. Please contact support.", "warning")
                        return render_template('login.html', username=username)
                    else:
                        session['loggedin'] = True
                        session['user_id'] = account['user_id']
                        session['username'] = account['username']
                        session['role'] = account['role']
                        session['first_name'] = account['first_name']
                        session['status'] = account['status']
                        return redirect(user_home_url())
                else:
                    # Password is incorrect. Re-display the login form, keeping
                    # the username provided by the user so they don't need to
                    # re-enter it. We also set a `password_invalid` flag that
                    # the template uses to display a validation message.
                    return render_template('login.html',
                                           username=username,
                                           password_invalid=True)
            else:
                # We didn't find an account in the database with this username.
                # Re-display the login form, keeping the username so the user
                # can see what they entered (otherwise, they might just keep
                # trying the same thing). We also set a `username_invalid` flag
                # that tells the template to display an appropriate message.
                #
                # Note: In this example app, we tell the user if the user
                # account doesn't exist. Many websites (e.g. Google, Microsoft)
                # do this, but other sites display a single "Invalid username
                # or password" message to prevent an attacker from determining
                # whether a username exists or not. Here, we accept that risk
                # to provide more useful feedback to the user.
                return render_template('login.html', 
                                       username=username,
                                       username_invalid=True)

    # This was a GET request, or an invalid POST (no username and/or password),
    # so we just render the login form with no pre-populated details or flags.
    return render_template('login.html')


@app.route('/signup', methods=['GET','POST'])
def signup():
    """Signup (registration) page endpoint.

    Methods:
    - get: Renders the signup page.
    - post: Attempts to create a new user account using the details supplied
        via the signup form, then renders the signup page again with a welcome
        message (if successful) or one or more error message(s) explaining why
        signup could not be completed.

    If the user is already logged in, both get and post requests will redirect
    to their role-specific homepage.
    """
    if 'loggedin' in session:
         return redirect(user_home_url())
    
    if request.method == 'POST' and 'username' in request.form and 'email' in request.form and 'password' in request.form:
        # Get the details submitted via the form on the signup page, and store
        # the values in temporary local variables for ease of access.
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        location = request.form['location']
        # We start by assuming that everything is okay. If we encounter any
        # errors during validation, we'll store an error message in one or more
        # of these variables so we can pass them through to the template.
        username_error = None
        email_error = None
        password_error = None

        # Check whether there's an account with this username in the database.
        with db.get_cursor() as cursor:
            cursor.execute('SELECT user_id FROM users WHERE username = %s;',
                           (username,))
            account_already_exists = cursor.fetchone() is not None
        
        # Validate the username, ensuring that it's unique (as we just checked
        # above) and meets the naming constraints of our web app.
        if account_already_exists:
            username_error = 'An account already exists with this username.'
        elif len(username) > 20:
            # The user should never see this error during normal conditions,
            # because we set a maximum length of 20 on the input field in the
            # template. However, a user or attacker could easily override that
            # and submit a longer value, so we need to handle that case.
            username_error = 'Your username cannot exceed 20 characters.'
        elif not re.match(r'[A-Za-z0-9]+', username):
            username_error = 'Your username can only contain letters and numbers.'            

        # Validate the new user's email address. Note: The regular expression
        # we use here isn't a perfect check for a valid address, but is
        # sufficient for this example.
        if len(email) > 320:
            # As above, the user should never see this error under normal
            # conditions because we set a maximum input length in the template.
            email_error = 'Your email address cannot exceed 320 characters.'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            email_error = 'Invalid email address.'
                
        # Validate password. Think about what other constraints might be useful
        # here for security (e.g. requiring a certain mix of character types,
        # or avoiding overly-common passwords). Make sure that you clearly
        # communicate any rules to the user, either through hints on the signup
        # page or with clear error messages here.
        #
        # Note: Unlike the username and email address, we don't enforce a
        # maximum password length. Because we'll be storing a hash of the
        # password in our database, and not the password itself, it doesn't
        # matter how long a password the user chooses. Whether it's 8 or 800
        # characters, the hash will always be the same length.
        # Validate the password
        if password != confirm_password:
            password_error = 'Passwords do not match.'
        elif not is_password_valid(password):
            password_error = 'Password must be at least 8 characters long and include a mix of letters and numbers.'
                
        if (username_error or email_error or password_error):
            # One or more errors were encountered, so send the user back to the
            # signup page with their username and email address pre-populated.
            # For security reasons, we never send back the password they chose.
            return render_template('signup.html',
                                   username=username,
                                   email=email,
                                   first_name = first_name,
                                   last_name = last_name,
                                   location = location,
                                   username_error = username_error,
                                   email_error = email_error,
                                   password_error = password_error)
        else:
            # The new account details are valid. Hash the user's new password
            # and create their account in the database.
            password_hash = flask_bcrypt.generate_password_hash(password)
            
            # Note: In this example, we just assume the SQL INSERT statement
            # below will run successfully. But what if it doesn't?
            #
            # If the INSERT fails for any reason, MySQL Connector will throw an
            # exception and the user will receive a generic error page. We
            # should implement our own error handling here to deal with that
            # possibility, and display a more useful message to the user.
            with db.get_cursor() as cursor:
                cursor.execute('''
                               INSERT INTO users (username, password_hash, email, first_name, last_name, location, role)
                               VALUES (%s, %s, %s, %s, %s, %s, %s);
                               ''',
                               (username, password_hash, email, first_name, last_name, location, DEFAULT_USER_ROLE,))
            flash('You have signed up successfully!', 'success')
            
            # Now that registration is complete, send the user back to the
            # signup page. We set the `signup_successful` flag to display a
            # post-signup message.
            return render_template('login.html')            

    # This was a GET request, or an invalid POST (no username, email, and/or
    # password). Render the signup page with no pre-populated form fields or
    # error messages.
    return render_template('signup.html')


@app.route('/logout')
def logout():
    """Logout endpoint.

    Methods:
    - get: Logs the current user out (if they were logged in to begin with),
        and redirects them to the login page.
    """
    # Note that nothing actually happens on the server when a user logs out: we
    # just remove the cookie from their web browser. They could technically log
    # back in by manually restoring the cookie we've just deleted. In a high-
    # security web app, you may need additional protections against this (e.g.
    # keeping a record of active sessions on the server side).
    session.pop('loggedin', None)
    session.pop('user_id', None)
    session.pop('username', None)
    session.pop('role', None)
    
    return redirect(url_for('login'))


def is_password_valid(password):
    """
    Check if the password meets complexity requirements.
    """
    if len(password) < 8:
        return False
    if not re.search(r"[a-zA-Z]", password):  # At least one letter 
        return False
    if not re.search(r"[0-9]", password):  # At least one digit
        return False
    return True


@app.route('/reset_password', methods=['GET', 'POST'])
@role_required()
def reset_password():
    """Reset password endpoint."""

    user_id = session['user_id']

    if request.method == 'POST':
        current_password = request.form.get('current_password')
        new_password = request.form.get('new_password')
        confirm_password = request.form.get('confirm_password')

        # Fetch the user's current password hash from the database
        with db.get_cursor() as cursor:
            cursor.execute("SELECT password_hash FROM users WHERE user_id = %s;", (user_id,))
            user = cursor.fetchone()

        if not user:
            flash('User not found.', 'danger')
            return redirect(url_for('reset_password'))

        # Verify the current password
        if not flask_bcrypt.check_password_hash(user['password_hash'], current_password):
            flash('Current password is incorrect.', 'danger')
            return redirect(url_for('reset_password'))

        # Check if the new password matches the confirm password
        if new_password != confirm_password:
            flash('New password and confirm password do not match.', 'danger')
            return redirect(url_for('reset_password'))

        # Check password complexity
        if not is_password_valid(new_password):
            flash('Password must be at least 8 characters long and include a mix of uppercase, lowercase, numbers, and special characters.', 'danger')
            return redirect(url_for('reset_password'))

        # Hash the new password and update the database
        hashed_password = flask_bcrypt.generate_password_hash(new_password)
        with db.get_cursor() as cursor:
            cursor.execute("UPDATE users SET password_hash = %s WHERE user_id = %s;", (hashed_password, user_id))
            db.get_db().commit()

        flash('Password updated successfully!', 'success')
        return redirect(user_home_url())

    return render_template('reset_password.html')