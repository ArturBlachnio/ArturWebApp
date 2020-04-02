from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField, IntegerField
from wtforms.validators import DataRequired, Length


class TaskForm(FlaskForm):
    name = StringField(label='Name', validators=[DataRequired(), Length(min=2, max=40)])
    strategy = SelectField(label='Strategy', coerce=int)  # Dynamically determined in route
    desc = StringField(label='Description')
    plan = StringField(label='Planned')  # Is converted to Interval with duration_from_string
    actual = StringField(label='Actual')
    # Coerce=int is essential here if choices are (int, str)
    frequency = SelectField(label='Frequency', coerce=int, choices=[(1, 'OneTime'), (2, 'Continues')])
    order = IntegerField(label='Order')
    submit = SubmitField(label='Add Task')

    # todo: validation of plan and actual duration input - to be consistent with duration_from_string


class StrategyForm(FlaskForm):
    name = StringField(label='Name', validators=[DataRequired(), Length(max=30)])
    category = SelectField(label='Category', coerce=int)
    symbol = StringField(label='Symbol', validators=[Length(max=3)])
    desc = StringField(label='Description')
    color = StringField(label='Color Hex')
    order = IntegerField(label='Order')
    submit = SubmitField(label='Submit')

