from awa import db
from datetime import datetime, timedelta

# To initiate db:
# (0) make sure you have env-vars: set FLASK_APP=run.py | set FLASK_ENV=development
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
    category = db.Column(db.String(20), nullable=True)
    br_task = db.relationship('Task', backref='strategy')  # todo: lazy=True - test that later
    br_project = db.relationship('Project', backref='strategy')  # todo: lazy=True - test that later

    def __repr__(self):
        return f"Strategy(id='{self.id}', name='{self.name}', symbol='{self.symbol}', desc='{self.desc}'," \
               f" color='{self.color}, order='{self.order}', time_creation='{self.time_creation}'," \
               f" time_completion='{self.time_completion}', category='{self.category}')"


class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), nullable=False)
    id_strategy = db.Column(db.Integer, db.ForeignKey('strategy.id'), nullable=False)


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(140), nullable=False)
    desc = db.Column(db.Text)
    category = db.Column(db.String(20))
    frequency = db.Column(db.String(10))
    time_creation = db.Column(db.DateTime, default=datetime.now)
    time_completion = db.Column(db.DateTime)
    time_due = db.Column(db.DateTime)  # THis is not used now, it was used for old timeline concept
    time_line = db.Column(db.String(20))
    duration_plan = db.Column(db.Interval, nullable=False, default=timedelta(0))
    duration_real = db.Column(db.Interval, nullable=False, default=timedelta(0))
    timer_start = db.Column(db.DateTime)
    order = db.Column(db.Integer)
    show_menu = db.Column(db.Boolean, default=True, nullable=False)
    id_strategy = db.Column(db.Integer, db.ForeignKey('strategy.id'), nullable=False)
    id_project = db.Column(db.Integer, db.ForeignKey('project.id'))

    def __repr__(self):
        return f"Task(id='{self.id}', name='{self.name}', desc='{self.desc}', category='{self.category}', " \
               f"frequency='{self.frequency}', time_creation='{self.time_creation}', " \
               f"time_completion='{self.time_completion}', time_due='{self.time_due}', time_line='{self.time_line}', " \
               f"duration_plan='{self.duration_plan}', duration_real='{self.duration_real}', " \
               f"timer_start='{self.timer_start}', order='{self.order}', show_menu='{self.show_menu}', " \
               f"id_strategy='{self.id_strategy}', id_project='{self.id_project}')"
