from lccapp import app, db
from flask import redirect, render_template, request, session, url_for, flash

@app.route('/user_issues')
def user_issues():
    """display the issues reported by all the users"""
    if 'loggedin' not in session:
        return redirect(url_for('login'))   

    user_id = session['user_id']

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
            WHERE i.issue_status IN ('new', 'open', 'stalled')
            ;""")
        resolved_issues = cursor.fetchall()
    # Fetch resolved issues (status: resolved)

    return render_template('user_issues.html', ongoing_issues=ongoing_issues, resolved_issues=resolved_issues)

@app.route('/issue_detail/<int:issue_id>')
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
def update_issue_status(issue_id):
    """change issue status"""
    new_status = request.form.get('issue_status')  
    source_page = request.form.get('source_page', 'my_issues')
    with db.get_cursor() as cursor:
        # update issue status
            cursor.execute("""
                UPDATE issues
                SET issue_status = %s
                WHERE issue_id = %s
                ;""", (new_status, issue_id,))
            db.get_db().commit()
    if source_page == "my_issues":
        return redirect(url_for('my_issues'))
    elif source_page == "issue_detail":
        return redirect(url_for('issue_detail', issue_id=issue_id))
    else:
        return redirect(url_for('my_issues'))

