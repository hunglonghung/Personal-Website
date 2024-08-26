from app import db

class Schedule(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(200), nullable=False)
    date = db.Column(db.String(10), nullable=False)

class Diary(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    date = db.Column(db.String(10), nullable=False)

class Setting(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    password = db.Column(db.String(200), nullable=False)

class Issue(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    issue = db.Column(db.Text, nullable=False)
    # cause = db.Column(db.Text, nullable=False)
    solution = db.Column(db.Text, nullable=False)
    date = db.Column(db.String(10), nullable=False)
class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    link = db.Column(db.String(200), nullable=True)
    progress = db.Column(db.Float, default=0.0)
    subtasks = db.relationship('Subtask', backref='project', lazy=True)

class Subtask(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    state = db.Column(db.String(20), default='Not yet')
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)
    parent_id = db.Column(db.Integer, db.ForeignKey('subtask.id'), nullable=True)
    subtasks = db.relationship('Subtask', backref=db.backref('parent', remote_side=[id]), lazy=True)
class Rule(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(50), nullable=False)

class UsefulLink(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    link = db.Column(db.String(200), nullable=False)
    comment = db.Column(db.Text, nullable=True)

class StudyTimeRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)
    category = db.Column(db.String(20), nullable=False)
    description = db.Column(db.Text, nullable=True)
