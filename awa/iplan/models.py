from awa import db
from datetime import datetime, timedelta

# To initiate db:
# (0) make sure you have env-vars: set FLASK_APP=run.py | set FLASK_ENV=development
# If there is no database: cmd> flask db init
# (1) cmd> flask db migrate
# (2) cmd> flask db upgrade


class Strategy(db.Model):
    # __table_args__ = {'extend_existing': True}
    # __tablename__ = strategy
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), nullable=False)
    symbol = db.Column(db.String(3))
    desc = db.Column(db.Text)
    color = db.Column(db.String(7))
    order = db.Column(db.Integer)
    time_creation = db.Column(db.DateTime, default=datetime.now)
    time_completion = db.Column(db.DateTime)
    show_timeline = db.Column(db.Boolean, default=True, nullable=False)
    category = db.Column(db.String(20), nullable=True)
    br_task = db.relationship('Task', backref='strategy')  # todo: lazy=True - test that later

    def __repr__(self):
        return f"Strategy(id='{self.id}', name='{self.name}', symbol='{self.symbol}', desc='{self.desc}'," \
               f" color='{self.color}', order='{self.order}', time_creation='{self.time_creation}'," \
               f" time_completion='{self.time_completion}', show_timeline='{self.show_timeline}'," \
               f" category='{self.category}')"


class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), nullable=False)
    symbol = db.Column(db.String(3))
    desc = db.Column(db.Text)
    category = db.Column(db.String(20))
    color = db.Column(db.String(7))
    order = db.Column(db.Integer)
    time_creation = db.Column(db.DateTime, default=datetime.now)
    time_completion = db.Column(db.DateTime)
    time_due = db.Column(db.DateTime)
    duration_plan = db.Column(db.Interval, nullable=False, default=timedelta(0))
    show_timeline = db.Column(db.Boolean, default=True, nullable=False)
    br_task = db.relationship('Task', backref='project')  # todo: lazy=True - test that later

    def __repr__(self):
        return f"Project(id='{self.id}', name='{self.name}', symbol='{self.symbol}', desc='{self.desc}'," \
               f" category='{self.category}', color='{self.color}', order='{self.order}'," \
               f" time_creation='{self.time_creation}', time_completion='{self.time_completion}'," \
               f" time_due='{self.time_due}', duration_plan='{self.duration_plan}'," \
               f" show_timeline='{self.show_timeline}')"


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(140), nullable=False)
    desc = db.Column(db.Text)
    category = db.Column(db.String(20))
    frequency = db.Column(db.String(10))
    frequency_days = db.Column(db.Integer)
    time_creation = db.Column(db.DateTime, default=datetime.now)
    time_completion = db.Column(db.DateTime)
    time_due = db.Column(db.DateTime)
    time_line = db.Column(db.String(20))
    duration_plan = db.Column(db.Interval, nullable=False, default=timedelta(0))
    duration_real = db.Column(db.Interval, nullable=False, default=timedelta(0))
    timer_start = db.Column(db.DateTime)
    order = db.Column(db.Integer)
    show_menu = db.Column(db.Boolean, default=True, nullable=False)
    id_strategy = db.Column(db.Integer, db.ForeignKey('strategy.id'), nullable=False)
    id_project = db.Column(db.Integer, db.ForeignKey('project.id'))

    def __repr__(self):
        return f"Task(id='{self.id}', name='{self.name}', desc='{self.desc}', category='{self.category}'," \
               f" frequency='{self.frequency}', frequency_days='{self.frequency_days}'," \
               f" time_creation='{self.time_creation}', time_completion='{self.time_completion}'," \
               f" time_due='{self.time_due}', time_line='{self.time_line}', duration_plan='{self.duration_plan}'," \
               f" duration_real='{self.duration_real}', timer_start='{self.timer_start}', order='{self.order}'," \
               f" show_menu='{self.show_menu}', id_strategy='{self.id_strategy}', id_project='{self.id_project}')"
