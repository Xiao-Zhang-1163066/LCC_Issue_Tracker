from lccapp import app, db
from flask import redirect, render_template, request, session, url_for, flash

@app.route('/my_issues')
def my_issues():
    """My Issues page endpoint."""
    if 'loggedin' not in session:
        return redirect(url_for('login'))

    user_id = session['user_id']

    with db.get_cursor() as cursor:
        cursor.execute("""
            select i.issue_id, i.user_id, i.summary, i.description, i.created_at, i.issue_status, u.username, u.first_name, u.profile_image
            from issues i
            join users u on i.user_id = u.user_id
            where i.user_id = %s
            order by i.created_at DESC
            ;""", (user_id,))
        issues = cursor.fetchall()

    for issue in issues:
        with db.get_cursor() as cursor:
            cursor.execute("""
                select c.comment_id, c.content, c.created_at, u.user_id, u.first_name, u.last_name, u.profile_image, u.role
                from comments c
                join users u on c.user_id = u.user_id
                where c.issue_id = %s
                order by c.created_at
                ;""", (issue['issue_id'],))
            issue["comments"] = cursor.fetchall()

    return render_template('my_issues.html', issues=issues, username=session.get('username'))

@app.route('/add_issue', methods=['POST'])
def add_issue():
    user_id = session['user_id']
    formvals = request.form 
    summary = formvals['summary']
    description = formvals['description']
    with db.get_cursor() as cursor:
        cursor.execute("""
            insert into issues (user_id, summary, description)
            values (%s, %s, %s)
            ;""", (user_id, summary, description, ))
        db.get_db().commit()
    flash('A issue added successfully!', 'success')
    return redirect(url_for('my_issues'))  

@app.route('/add_comment/<int:issue_id>', methods=['POST'])
def add_comment(issue_id):
    user_id = session['user_id']
    content = request.form['content']
    with db.get_cursor() as cursor:
        cursor.execute("""
            insert into comments (issue_id, user_id, content)
            values (%s, %s, %s)
            ;""", (issue_id, user_id, content))
        db.get_db().commit()
    flash('You commented successfully!', 'success')
    
    return redirect(url_for('my_issues'))  


