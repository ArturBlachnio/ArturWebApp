from awa import db
from datetime import timedelta

# Errors solution:
# Table 'xx' is already defined for this MetaData instance.  Specify 'extend_existing=True'
# A. Use: db.metadata.clear() before any class is defined to start from scratch and clear meta
# B. Use: __table_args__ = {'extend_existing': True} after class definition to extend current model
db.metadata.clear()


class Strategy(db.Model):
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    symbol = db.Column(db.String(3))
    desc = db.Column(db.Text)
    color = db.Column(db.String(7))
    order = db.Column(db.Integer)
    artur = db.Column(db.String(10), default='artur')
    br_task = db.relationship('Task', backref='strategy')  # todo: lazy=True - test that later

    def __repr__(self):
        return f"TaskCategory(id='{self.id}', name='{self.name}', symbol='{self.symbol}', desc='{self.desc}'," \
               f" color='{self.color}, order='{self.order}')"


class Project(db.Model):
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)


class Task(db.Model):
    __table_args__ = {'extend_existing': True}
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


def init_db():
    db.drop_all()
    db.create_all()

if __name__ == '__main__':
    init_db()

