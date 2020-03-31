from flask import Blueprint, render_template, flash, redirect, url_for, request
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


@iplan.route('/iplan/categories', methods=['GET', 'POST'])
def categories():
    form = TaskCategoryForm()
    if form.validate_on_submit():
        task_category = TaskCategory(name = form.name.data, cat3 = form.cat3.data, color = form.color.data)
        db.session.add(task_category)
        db.session.commit()
        flash('New category for tasks was created', 'success')
        return redirect(url_for('iplan.categories'))
    categories = TaskCategory.query.all()
    # todo - count using sql
    count_tasks = {cat.id: len(Task.query.filter_by(category_id=cat.id).all()) for cat in categories}
    return render_template('iplan/categories.html', form=form, categories=categories, count_tasks=count_tasks)


@iplan.route('/iplan/categories/update/<category_id>', methods=['GET', 'POST'])
def category_update(category_id):
    form = TaskCategoryForm()
    task_category = TaskCategory.query.get_or_404(category_id)
    print(task_category)
    if form.validate_on_submit():
        task_category.name = form.name.data
        task_category.cat3 = form.cat3.data
        task_category.color = form.color.data
        db.session.commit()
        flash('Category for tasks has been updated created', 'success')
        return redirect(url_for('iplan.categories'))
    elif request.method == 'GET':
        form.name.data = task_category.name
        form.cat3.data = task_category.cat3
        form.color.data = task_category.color
    categories = TaskCategory.query.all()
    # todo - count using sql
    count_tasks = {cat.id: len(Task.query.filter_by(category_id=cat.id).all()) for cat in categories}
    return render_template('iplan/categories_update.html', form=form, categories=categories, count_tasks=count_tasks)

@iplan.route('/iplan/categories/delete/<category_id>', methods=['GET', 'POST'])
def category_delete(category_id):
    task_category = TaskCategory.query.get_or_404(category_id)
    tasks_for_category = Task.query.filter_by(category_id=category_id).all()
    if tasks_for_category:
        flash(f'There are still {len(tasks_for_category)} task(s) for this category. It can not be removed without'
              f' prior reassignment. There will be automatic solution built later. For now, do that manually.', 'danger')
    else:
        db.session.delete(task_category)
        db.session.commit()
        flash('Category was deleted', 'success')
    return redirect(url_for('iplan.categories'))
