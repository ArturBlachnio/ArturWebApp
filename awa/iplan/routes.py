from flask import Blueprint, render_template, flash, redirect, url_for
from awa import db
from awa.iplan.models import Task, TaskCategory
from awa.iplan.forms import TaskForm, TaskCategoryForm
from awa.iplan.utils import duration_from_string

iplan = Blueprint(name='iplan', import_name=__name__)


@iplan.route('/iplan', methods=['GET', 'POST'])
def home():
    formcat = TaskCategoryForm()
    form = TaskForm()

    form.category.choices = [(cat.id, cat.name) for cat in TaskCategory.query.all()]

    if formcat.validate_on_submit():
        flash('Task category added', 'info')
        category = TaskCategory(name=formcat.name.data, cat3=formcat.cat3.data, color=formcat.color.data)
        db.session.add(category)
        db.session.commit()
        return redirect(url_for('iplan.home'))

    if form.validate_on_submit():
        flash('Task added to Task-List', 'success')
        task = Task(title=form.title.data, description=form.description.data,
                    plan=duration_from_string(form.plan.data),
                    actual=duration_from_string(form.actual.data),
                    frequency=dict(form.frequency.choices).get(form.frequency.data),
                    category_id=form.category.data)
        db.session.add(task)
        db.session.commit()
        return redirect(url_for('iplan.home'))
    tasks = Task.query.all()
    categories = TaskCategory.query.all()
    return render_template('iplan/home.html', tasks=tasks, form=form, categories=categories, formcat=formcat)


@iplan.route('/iplan/tasks/<task_id>/delete', methods=['GET', 'POST'])
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    db.session.delete(task)
    db.session.commit()
    flash('Task was deleted', 'warning')
    return redirect(url_for('iplan.home'))
