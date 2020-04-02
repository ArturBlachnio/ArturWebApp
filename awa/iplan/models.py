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
    time_creation = db.Column(db.DateTime, default=datetime.utcnow)
    time_completion = db.Column(db.DateTime)
    category = db.Column(db.String(20), nullable=True)
    br_task = db.relationship('Task', backref='strategy')  # todo: lazy=True - test that later

    def __repr__(self):
        return f"Strategy(id='{self.id}', name='{self.name}', symbol='{self.symbol}', desc='{self.desc}'," \
               f" color='{self.color}, order='{self.order}', time_creation='{self.time_creation}'," \
               f" time_completion='{self.time_completion}', category='{self.category}')"


class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), nullable=False)


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), nullable=False)
    desc = db.Column(db.Text)
    plan = db.Column(db.Interval, nullable=False, default=timedelta(0))
    actual = db.Column(db.Interval, nullable=False, default=timedelta(0))
    start = db.Column(db.DateTime)
    end = db.Column(db.DateTime)
    complete = db.Column(db.Boolean, nullable=False, default=False)
    frequency = db.Column(db.String(10), nullable=False, default='OneTime')  # Onetime or repeatable
    order = db.Column(db.Integer)
    id_strategy = db.Column(db.Integer, db.ForeignKey('strategy.id'), nullable=False)
    # categories = db.relationship('TaskCategory', back_populates='task_category')

    def __repr__(self):
        return f"Task(id='{self.id}', name='{self.name}', desc='{self.desc}', plan='{self.plan}'" \
               f" actual='{self.actual}', start='{self.start}', end='{self.end}', " \
               f" complete='{self.complete}', freq='{self.frequency}', order='{self.order}', id_strategy='{self.id_strategy}')"

