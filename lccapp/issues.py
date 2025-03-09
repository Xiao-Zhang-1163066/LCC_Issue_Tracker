from lccapp import app, db
from flask import redirect, render_template, request, session, url_for, flash
from .user import role_required

@app.route('/my_issues')
@role_required()
def my_issues():
    """My Issues page endpoint."""

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
@role_required()
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
@role_required()
def add_comment(issue_id):
    user_id = session['user_id']
    role = session['role']
    content = request.form['content']
    source_page = request.form.get('source_page', 'issue_detail')
    with db.get_cursor() as cursor:
        cursor.execute("""
            insert into comments (issue_id, user_id, content)
            values (%s, %s, %s)
            ;""", (issue_id, user_id, content))
        db.get_db().commit()
    
    # If the user is a Helper or Admin, update the issue status to "open"
    if role in ['helper', 'admin']:
        with db.get_cursor() as cursor:
            cursor.execute("""
                UPDATE issues
                SET issue_status = 'open'
                WHERE issue_id = %s AND issue_status IN ('new', 'stalled', 'resolved');
            """, (issue_id,))
            db.get_db().commit()

    flash('You commented successfully!', 'success')
    
    if source_page == "my_issues":
        return redirect(url_for('my_issues'))

    return redirect(url_for('issue_detail', issue_id=issue_id))

@app.route('/user_issues')
@role_required(['admin', 'helper'])
def user_issues():
    """display the issues reported by all the users"""
    with db.get_cursor() as cursor:
        # Fetch ongoing issues (status: new, open, stalled)
        cursor.execute("""
            SELECT i.issue_id, i.summary, i.description, i.created_at, i.issue_status, u.user_id, u.first_name, u.last_name, u.profile_image
            FROM issues i
            JOIN users u ON i.user_id = u.user_id
            WHERE i.issue_status IN ('new', 'open', 'stalled')
            ;""")
        ongoing_issues = cursor.fetchall()
        # Fetch resolved issues (status: resolved)
        cursor.execute("""
            SELECT i.issue_id, i.summary, i.description, i.created_at, i.issue_status, u.user_id, u.first_name, u.last_name, u.profile_image
            FROM issues i
            JOIN users u ON i.user_id = u.user_id
            WHERE i.issue_status = 'resolved'
            ;""")
        resolved_issues = cursor.fetchall()
    # Fetch resolved issues (status: resolved)

    return render_template('user_issues.html', ongoing_issues=ongoing_issues, resolved_issues=resolved_issues)

@app.route('/issue_detail/<int:issue_id>')
@role_required(['admin', 'helper'])
def issue_detail(issue_id):
    """display details of the chosen issue"""
    if 'loggedin' not in session:
        return redirect(url_for('login'))   

    with db.get_cursor() as cursor:
        # Fetch issue detail
            cursor.execute("""
                select i.issue_id, i.user_id, i.summary, i.description, i.created_at, i.issue_status, u.username, u.first_name, u.profile_image
                from issues i
                join users u on i.user_id = u.user_id
                where i.issue_id = %s
                order by i.created_at DESC
                ;""", (issue_id,))
            issue = cursor.fetchone()
            # fetch comments
            cursor.execute("""
                select c.comment_id, c.content, c.created_at, u.user_id, u.first_name, u.last_name, u.profile_image, u.role
                from comments c
                join users u on c.user_id = u.user_id
                where c.issue_id = %s
                order by c.created_at
                ;""", (issue_id,))
            comments = cursor.fetchall()

    return render_template('issue_detail.html', issue=issue, comments=comments)


@app.route('/update_issue_status/<int:issue_id>', methods=['POST'])
@role_required(['admin', 'helper'])
def update_issue_status(issue_id):
    """change issue status"""
    new_status = request.form.get('issue_status')  
    source_page = request.form.get('source_page', 'my_issues')
    # update issue status
    with db.get_cursor() as cursor:
            cursor.execute("""
                UPDATE issues
                SET issue_status = %s
                WHERE issue_id = %s
                ;""", (new_status, issue_id,))
            db.get_db().commit()
    flash('Issue status updated successfully!', 'success')
    if source_page == "my_issues":
        return redirect(url_for('my_issues'))
    return redirect(url_for('issue_detail', issue_id=issue_id))
 

