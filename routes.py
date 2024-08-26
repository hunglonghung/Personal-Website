from collections import defaultdict
from datetime import datetime
from flask import flash, render_template, request, redirect, url_for
from app import db
from models import Issue, Project, Rule, Schedule, Diary, Setting, StudyTimeRecord, Subtask, UsefulLink
from flask import current_app as app

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/schedule', methods=['GET', 'POST'])
def schedule():
    if request.method == 'POST':
        task = request.form['task']
        date = request.form['date']
        new_task = Schedule(task=task, date=date)
        db.session.add(new_task)
        db.session.commit()
        return redirect(url_for('schedule'))
    schedules = Schedule.query.all()
    return render_template('schedule.html', schedules=schedules)

@app.route('/schedule/delete/<int:id>', methods=['POST'])
def delete_schedule(id):
    password = request.form['password']
    setting = Setting.query.first()
    if setting and password == setting.password:
        task_to_delete = Schedule.query.get_or_404(id)
        db.session.delete(task_to_delete)
        db.session.commit()
    else:
        flash('Incorrect password')
    return redirect(url_for('schedule'))

@app.route('/diary', methods=['GET', 'POST'])
def diary():
    if request.method == 'POST':
        content = request.form['content']
        date = request.form['date']
        new_entry = Diary(content=content, date=date)
        db.session.add(new_entry)
        db.session.commit()
        return redirect(url_for('diary'))
    diaries = Diary.query.all()
    return render_template('diary.html', diaries=diaries)

@app.route('/diary/delete/<int:id>', methods=['POST'])
def delete_diary(id):
    password = request.form['password']
    setting = Setting.query.first()
    if setting and password == setting.password:
        entry_to_delete = Diary.query.get_or_404(id)
        db.session.delete(entry_to_delete)
        db.session.commit()
    else:
        flash('Incorrect password')
    return redirect(url_for('diary'))

@app.route('/settings', methods=['GET', 'POST'])
def settings():
    if request.method == 'POST':
        password = request.form['password']
        setting = Setting.query.first()
        if setting:
            setting.password = password
        else:
            setting = Setting(password=password)
            db.session.add(setting)
        db.session.commit()
        flash('Password updated successfully')
        return redirect(url_for('settings'))
    return render_template('settings.html')

@app.route('/issues', methods=['GET', 'POST'])
def issues():
    if request.method == 'POST':
        issue = request.form['issue']
        # cause = request.form['cause']
        solution = request.form['solution']
        date = request.form['date']
        new_issue = Issue(issue=issue, solution=solution, date=date)
        db.session.add(new_issue)
        db.session.commit()
        return redirect(url_for('issues'))
    issues = Issue.query.all()
    return render_template('issues.html', issues=issues)

@app.route('/issues/delete/<int:id>', methods=['POST'])
def delete_issue(id):
    password = request.form['password']
    setting = Setting.query.first()
    if setting and password == setting.password:
        issue_to_delete = Issue.query.get_or_404(id)
        db.session.delete(issue_to_delete)
        db.session.commit()
    else:
        flash('Incorrect password')
    return redirect(url_for('issues'))
@app.route('/projects', methods=['GET', 'POST'])
def projects():
    if request.method == 'POST':
        name = request.form['name']
        link = request.form.get('link')
        new_project = Project(name=name, link=link)
        db.session.add(new_project)
        db.session.commit()
        return redirect(url_for('projects'))
    projects = Project.query.all()
    return render_template('projects.html', projects=projects)
@app.route('/project/<int:id>/update_subtask/<int:subtask_id>', methods=['POST'])
def update_subtask(id, subtask_id):
    subtask = Subtask.query.get_or_404(subtask_id)
    subtask.name = request.form['name']
    subtask.state = request.form['state']
    db.session.commit()
    return redirect(url_for('project', id=id))

@app.route('/project/<int:id>/delete_subtask/<int:subtask_id>', methods=['POST'])
def delete_subtask(id, subtask_id):
    subtask = Subtask.query.get_or_404(subtask_id)
    db.session.delete(subtask)
    db.session.commit()
    return redirect(url_for('project', id=id))
@app.route('/project/<int:id>', methods=['GET', 'POST'])
def project(id):
    project = Project.query.get_or_404(id)
    if request.method == 'POST':
        # Handle adding subtask
        name = request.form['name']
        state = request.form.get('state', 'Not yet')
        parent_id = request.form.get('parent_id')
        subtask = Subtask(name=name, state=state, project_id=id, parent_id=parent_id)
        db.session.add(subtask)
        db.session.commit()
        return redirect(url_for('project', id=id))
    
    subtasks = Subtask.query.filter_by(project_id=id).all()
    total_subtasks = len(subtasks)
    completed_subtasks = sum(1 for subtask in subtasks if subtask.state == 'Done')
    
    if total_subtasks > 0:
        project.progress = (completed_subtasks / total_subtasks) * 100
    else:
        project.progress = 0
    db.session.commit()

    return render_template('project.html', project=project, subtasks=subtasks)
# Route for Rules
@app.route('/rules', methods=['GET', 'POST'])
def rules():
    if request.method == 'POST':
        content = request.form['content']
        category = request.form['category']
        new_rule = Rule(content=content, category=category)
        db.session.add(new_rule)
        db.session.commit()
        return redirect(url_for('rules'))
    rules = Rule.query.all()
    return render_template('rules.html', rules=rules)

# Route for Useful Links
@app.route('/useful_links', methods=['GET', 'POST'])
def useful_links():
    if request.method == 'POST':
        link = request.form['link']
        comment = request.form.get('comment')
        new_link = UsefulLink(link=link, comment=comment)
        db.session.add(new_link)
        db.session.commit()
        return redirect(url_for('useful_links'))
    links = UsefulLink.query.all()
    return render_template('useful_links.html', links=links)



@app.route('/rules/delete/<int:id>', methods=['POST'])
def delete_rule(id):
    password = request.form['password']
    setting = Setting.query.first()
    if setting and password == setting.password:
        rule_to_delete = Rule.query.get_or_404(id)
        db.session.delete(rule_to_delete)
        db.session.commit()
    else:
        flash('Incorrect password')
    return redirect(url_for('rules'))
@app.route('/useful_links/delete/<int:id>', methods=['POST'])
def delete_link(id):
    password = request.form['password']
    setting = Setting.query.first()
    if setting and password == setting.password:
        link_to_delete = UsefulLink.query.get_or_404(id)
        db.session.delete(link_to_delete)
        db.session.commit()
    else:
        flash('Incorrect password')
    return redirect(url_for('useful_links'))

@app.route('/study_time', methods=['GET', 'POST'])
def study_time():
    if request.method == 'POST':
        start_time_str = request.form['start_time']
        end_time_str = request.form['end_time']
        
        # Chuyển đổi chuỗi thành datetime
        start_time = datetime.fromisoformat(start_time_str)
        end_time = datetime.fromisoformat(end_time_str)
        
        category = request.form['category']
        description = request.form.get('description')
        
        new_record = StudyTimeRecord(
            start_time=start_time, 
            end_time=end_time, 
            category=category, 
            description=description
        )
        
        db.session.add(new_record)
        db.session.commit()
        
        return redirect(url_for('study_time'))
    
    # Lấy tất cả các bản ghi và nhóm chúng theo ngày
    records = StudyTimeRecord.query.order_by(StudyTimeRecord.start_time.desc()).all()
    records_by_date = defaultdict(list)
    
    for record in records:
        date = record.start_time.date()
        records_by_date[date].append(record)
    
    return render_template('study_time.html', records_by_date=records_by_date)
@app.route('/study_time/delete/<int:id>', methods=['POST'])
def delete_record(id):
    password = request.form['password']
    setting = Setting.query.first()
    if setting and password == setting.password:
        record_to_delete = StudyTimeRecord.query.get_or_404(id)
        db.session.delete(record_to_delete)
        db.session.commit()
    else:
        flash('Incorrect password')
    return redirect(url_for('study_time'))