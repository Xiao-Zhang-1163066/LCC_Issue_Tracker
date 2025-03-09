from lccapp import app, db
from flask import redirect, render_template, request, session, url_for, flash
from .user import role_required

@app.route('/user_management')
@role_required(['admin'])
def user_management():
    """ display the list of all the users """
    search_query = request.args.get('search', '').strip()
    with db.get_cursor() as cursor:
        if search_query:
            search_param = f"%{search_query}%"
            cursor.execute("""
                SELECT user_id, username, first_name, last_name, role, email, location, status
                FROM users
                WHERE username LIKE %s OR first_name LIKE %s OR last_name LIKE %s
                ORDER BY username ASC
            ;""",(search_param ,search_param ,search_param ))
            
        else:
            cursor.execute("""
                SELECT user_id, username, first_name, last_name, role, email, location, status
                FROM users
                ORDER BY 
                CASE 
                    WHEN role = 'admin' THEN 1
                    WHEN role = 'helper' THEN 2
                    WHEN role = 'visitor' THEN 3
                    ELSE 4
                END,
                username ASC
                ;""")
        users = cursor.fetchall()
        
    return render_template('user_management.html', users=users, search_query=search_query)


@app.route('/user_profile/<int:user_id>', methods=['GET', 'POST'])
@role_required(['admin'])
def user_profile(user_id):
    """display the chosen user's information and allow admin to edit role and user st"""
    
    if request.method == 'POST':
        role = request.form.get('role')
        status = request.form.get('status')

        if not role or not status:
            flash('Role and status cannot be empty.', 'danger')
            return redirect(url_for('user_profile', user_id=user_id))

        with db.get_cursor() as cursor:
            cursor.execute('''
                UPDATE users
                SET role = %s, status = %s
                WHERE user_id = %s;
            ''', (role, status, user_id))
            db.get_db().commit()
            flash('Updated successfully!', 'success')       
        return redirect(url_for('user_profile', user_id=user_id))

    with db.get_cursor() as cursor:
        cursor.execute('''
            SELECT user_id, username, first_name, last_name, role, status, email, location, profile_image
            FROM users
            WHERE user_id = %s;
        ''', (user_id,))
        user = cursor.fetchone()

    return render_template('user_profile.html', user=user)