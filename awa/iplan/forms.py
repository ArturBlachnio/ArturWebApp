from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField
from wtforms.fields.html5 import DateField, TimeField, IntegerField
from wtforms.validators import DataRequired, Length


class TaskForm(FlaskForm):
    name = StringField(label='Name', validators=[DataRequired(), Length(min=1, max=140)])
    desc = StringField(label='Description')
    duration_plan = StringField(label='Duration Plan')  # Is converted to Interval with duration_from_string
    duration_real = StringField(label='Duration Real')
    category = SelectField(label='Category', coerce=int)
    time_line = SelectField(label='Timeline')
    time_due_date = DateField(label='Due Date')
    time_due_time = TimeField(label='Due Time')
    # Coerce=int - browser sends data in str format so function is needed to transform it
    frequency = SelectField(label='Frequency', coerce=int)
    frequency_days = IntegerField(label='Days till next repeat')
    order = IntegerField(label='Order')
    id_strategy = SelectField(label='Strategy', coerce=int)
    id_project = SelectField(label='Project', coerce=int)
    submit = SubmitField(label='Add Task')

    # todo: validation of plan and actual duration input - to be consistent with duration_from_string


class StrategyForm(FlaskForm):
    name = StringField(label='Name', validators=[DataRequired(), Length(max=40)])
    category = SelectField(label='Category', coerce=int)
    symbol = StringField(label='Symbol', validators=[Length(max=3)])
    desc = StringField(label='Description')
    color = StringField(label='Color Hex')
    order = IntegerField(label='Order')
    submit = SubmitField(label='Submit')


class ProjectForm(FlaskForm):
    name = StringField(label='Name', validators=[DataRequired(), Length(max=40)])
    symbol = StringField(label='Symbol', validators=[Length(max=20)])
    desc = StringField(label='Description')
    category = SelectField(label='Category', coerce=int)
    time_due_date = DateField(label='Due Date')
    time_due_time = TimeField(label='Due Time')
    duration_plan = StringField(label='Duration Plan')
    color = StringField(label='Color Hex')
    order = IntegerField(label='Order')
    submit = SubmitField(label='Submit')
