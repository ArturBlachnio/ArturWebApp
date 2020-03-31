from awa import db
from datetime import timedelta

# !!! USE THIS WHEN ERROR IN CREATION HAPPEN
# db.metadata.clear()


class TaskCategory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    cat3 = db.Column(db.String(3), nullable=False)
    color = db.Column(db.String(7), nullable=False)
    tasks = db.relationship('Task', backref='category')  # , lazy=True

    def __repr__(self):
        return f"TaskCategory(id='{self.id}', name='{self.name}', cat3='{self.cat3}', color='{self.color}')"


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(40), nullable=False)
    description = db.Column(db.Text)
    plan = db.Column(db.Interval, nullable=False, default=timedelta(0))  # Interval could potentially make issues on some platforms (tdb)
    actual = db.Column(db.Interval, nullable=False, default=timedelta(0))
    start = db.Column(db.DateTime)
    end = db.Column(db.DateTime)
    complete = db.Column(db.Boolean, nullable=False, default=False)
    frequency = db.Column(db.String(10), nullable=False, default='OneTime')  # Onetime or repeatable
    category_id = db.Column(db.Integer, db.ForeignKey('task_category.id'), nullable=False)
    # categories = db.relationship('TaskCategory', back_populates='task_category')

    def __repr__(self):
        return f"Task(id='{self.id}', title='{self.title}', desc='{self.description}', plan='{self.plan}'" \
               f" actual='{self.actual}', start='{self.start}', end='{self.end}', " \
               f" complete='{self.complete}', freq='{self.frequency}', category_id='{self.category_id}')"


def init_db():
    """ Database must be created in a way that db is aware of models. That's why it's here. """
    db.drop_all()
    db.create_all()

    # # Create fixed categories
    # cat1 = TaskCategory(category='Not Tracked', cat3='NOT', color='#ced2d6')
    # cat2 = TaskCategory(category='Gentlemen Explorer', cat3='GXP', color='#66b381')
    # cat3 = TaskCategory(category='Data Science', cat3='DSC', color='#827499')
    # cat4 = TaskCategory(category='Developer', cat3='DEV', color='#66b3a7')
    # cat5 = TaskCategory(category='Polyglot', cat3='PGT', color='#dba65c')
    # cat6 = TaskCategory(category='Create Read Think', cat3='CRT', color='#cadb5c')
    # cat7 = TaskCategory(category='Home And Son', cat3='HAS', color='#f59a9a')
    # cat8 = TaskCategory(category='Negative', cat3='NEG', color='#802e2e')
    # for cat in [cat1, cat2, cat3, cat4, cat5, cat6, cat7, cat8]:
    #     db.session.add(cat)
    #     db.session.commit()
    #
    # # Create an exemplary tasks
    # for i in range(1,9):
    #     task = Task(title=f'Task nr {i}', description=f'Desc {i}', category_id=i)
    #     # plan = timedelta(hours=i, minutes=2, seconds=3),
    #     # actual = timedelta(hours=i, minutes=2, seconds=3), start = datetime.utcnow(), end = datetime.utcnow()
    #     db.session.add(task)
    #     db.session.commit()


if __name__ == '__main__':
    init_db()

