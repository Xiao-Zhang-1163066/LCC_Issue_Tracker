from lccapp import app, db
from flask import redirect, render_template, request, session, url_for, flash
import os
from werkzeug.utils import secure_filename 
from .user import role_required

# Get the absolute path of the current file
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, "static/uploads")
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER  
#  Set allowed pic extentions
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}

def allowed_file(filename):
    """Check if the uploaded file has an allowed extension"""
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/profile', methods=['GET', 'POST'])
@role_required()
def profile():
    """User Profile page endpoint."""

    user_id = session['user_id']

    if request.method == 'POST':
        # Get form data
        username = request.form.get('username')
        email = request.form.get('email')
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        location = request.form.get('location')

        # Update user profile in database
        with db.get_cursor() as cursor:
            cursor.execute("""
                UPDATE users 
                SET username = %s, email = %s, first_name = %s, last_name = %s, location = %s 
                WHERE user_id = %s;
            """, (username, email, first_name, last_name, location, user_id))
            db.get_db().commit()
        flash('Save successfully', 'success')
        return redirect(url_for('profile'))  
    # Fetch user data
    with db.get_cursor() as cursor:
        cursor.execute('SELECT username, first_name, last_name, email, location, role, profile_image FROM users WHERE user_id = %s;', (user_id,))
        profile = cursor.fetchone()

    return render_template('profile.html', profile=profile, username=session.get('username'))


@app.route('/upload_image', methods=['POST'])
@role_required()
def upload_image():
    if 'profile_image' not in request.files:
        flash('No file uploaded.', 'danger')
        return redirect(url_for('profile'))

    file = request.files['profile_image']
    if file.filename == '':
        flash('No file selected.', 'warning')
        return redirect(url_for('profile'))

    if file and allowed_file(file.filename):
        filename = f"user_{session['user_id']}.png"  # Rename file
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)

        # Ensure the folder exists
        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

        # Save the new file
        file.save(filepath)

        # Update database with new file path
        with db.get_cursor() as cursor:
            cursor.execute("""
                UPDATE users SET profile_image = %s WHERE user_id = %s;
            """, (f"/static/uploads/{filename}", session['user_id']))
            db.get_db().commit()

        flash('Profile image updated successfully!', 'success')
    else:
        flash('Invalid file type. Only PNG, JPG, JPEG, and GIF are allowed.', 'danger')

    return redirect(url_for('profile'))

if __name__ == '__main__':
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    app.run(debug=True)


