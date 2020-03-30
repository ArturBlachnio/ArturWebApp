from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField, IntegerField
from wtforms.validators import DataRequired, Length


class TaskForm(FlaskForm):
    title = StringField(label='Title', validators=[DataRequired(), Length(min=2, max=40)])
    category = SelectField(label='Category', coerce=int)
    description = StringField(label='Extra Description')
    plan = StringField(label='Planned')  # Is converted to Interval with duration_from_string
    actual = StringField(label='Actual')
    # Coerce=int is essential here if choices are (int, str)
    frequency = SelectField(label='Frequency', coerce=int, choices=[(1, 'OneTime'), (2, 'Repeatable')])
    submit = SubmitField(label='Add Task')

    # todo: validation of plan and actual duration input - to be consistent with duration_from_string


class TaskCategoryForm(FlaskForm):
    name = StringField(label='Category Name', validators=[DataRequired(), Length(max=30)])
    cat3 = StringField(label='Category 3-digit Symbol', validators=[DataRequired(), Length(max=30)])
    color = StringField(label='Color', validators=[DataRequired(), Length(max=30)])
    submit = SubmitField(label='Add Category')
