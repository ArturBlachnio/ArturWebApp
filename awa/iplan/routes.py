from flask import Blueprint, render_template, flash, redirect, url_for, request
from awa import db
from awa.iplan.models import Strategy, Task
from awa.iplan.forms import StrategyForm, TaskForm
from awa.iplan.utils import duration_from_string, string_from_duration, reverse_dict

iplan = Blueprint(name='iplan', import_name=__name__)


@iplan.route('/iplan', methods=['GET', 'POST'])
def home():
    tasks = Task.query.all()
    strategies = Strategy.query.all()
    return render_template('iplan/home.html', tasks=tasks, strategies=strategies)


@iplan.route('/iplan/task', methods=['GET', 'POST'])
def task():
    tasks = Task.query.order_by(Task.order).all()
    strategies = Strategy.query.all()
    return render_template('iplan/task.html', tasks=tasks, strategies=strategies)


@iplan.route('/iplan/task/create', methods=['GET', 'POST'])
def task_create():
    form_task = TaskForm()
    # Dynamic choices
    form_task.strategy.choices = [(item.id, item.name) for item in Strategy.query.order_by(Strategy.order).all()]

    if form_task.validate_on_submit():
        task = Task(name=form_task.name.data, desc=form_task.desc.data,
                plan=duration_from_string(form_task.plan.data),
                actual=duration_from_string(form_task.actual.data),
                frequency=dict(form_task.frequency.choices).get(form_task.frequency.data),
                id_strategy=form_task.strategy.data,
                order=form_task.order.data)
        db.session.add(task)
        db.session.commit()
        return redirect(url_for('iplan.task'))
    elif request.method == 'GET':
        form_task.order.data = 999
        form_task.submit.label.text = 'Create task'
    return render_template('iplan/task_edit.html', form_task=form_task, legend='Create New Task')


@iplan.route('/iplan/task/update/<id_task>', methods=['GET', 'POST'])
def task_update(id_task):
    form_task = TaskForm()
    # Dynamic choices
    form_task.strategy.choices = [(item.id, item.name) for item in Strategy.query.all()]

    task = Task.query.get_or_404(id_task)
    if form_task.validate_on_submit():
        task.name = form_task.name.data
        task.id_strategy = form_task.strategy.data
        task.desc = form_task.desc.data
        task.plan = duration_from_string(form_task.plan.data)
        task.actual = duration_from_string(form_task.actual.data)
        task.frequency = dict(form_task.frequency.choices).get(form_task.frequency.data)
        task.order = form_task.order.data
        db.session.commit()
        return redirect(url_for('iplan.task'))
    elif request.method == 'GET':
        form_task.name.data = task.name
        form_task.strategy.data = task.id_strategy
        form_task.desc.data = task.desc
        form_task.plan.data = string_from_duration(task.plan)
        form_task.actual.data = string_from_duration(task.actual)
        form_task.frequency.data = reverse_dict(form_task.frequency.choices).get(task.frequency, 1)
        form_task.order.data = task.order
        form_task.submit.label.text = 'Update task'
    return render_template('iplan/task_edit.html', form_task=form_task, legend='Update Task')


@iplan.route('/iplan/task/delete/<id_task>', methods=['GET', 'POST'])
def task_delete(id_task):
    task = Task.query.get_or_404(id_task)
    db.session.delete(task)
    db.session.commit()
    flash('Task has been deleted', 'success')
    return redirect(url_for('iplan.task'))


@iplan.route('/iplan/strategy', methods=['GET', 'POST'])
def strategy():
    strategies = Strategy.query.order_by(Strategy.order).all()
    # todo - count using sql
    count_tasks = {item.id: len(Task.query.filter_by(id_strategy=item.id).all()) for item in strategies}
    return render_template('iplan/strategy.html', strategies=strategies, legend='Create New Strategy',
                           count_tasks=count_tasks)


strategy_category_choices = [(1, 'AAAStrategic'), (2, 'Productive'), (3, 'Untracked')]

@iplan.route('/iplan/strategy/create', methods=['GET', 'POST'])
def strategy_create():
    form = StrategyForm()
    form.category.choices = strategy_category_choices

    if form.validate_on_submit():
        item_strategy = Strategy(name=form.name.data, symbol=form.symbol.data, desc=form.desc.data,
                                 color=form.color.data, order=form.order.data,
                                 category=dict(strategy_category_choices).get(form.category.data))
        db.session.add(item_strategy)
        db.session.commit()
        flash('New strategy has been created.', 'success')
        return redirect(url_for('iplan.strategy'))
    elif request.method == 'GET':
        form.order.data = 999
        form.color.data = 'LightSteelBlue'
    return render_template('iplan/strategy_edit.html', form=form, legend='Create New Strategy')


@iplan.route('/iplan/strategy/update/<id_strategy>', methods=['GET', 'POST'])
def strategy_update(id_strategy):
    form = StrategyForm()
    form.category.choices = strategy_category_choices

    item_strategy = Strategy.query.get_or_404(id_strategy)
    if form.validate_on_submit():
        item_strategy.name = form.name.data
        item_strategy.symbol = form.symbol.data
        item_strategy.desc = form.desc.data
        item_strategy.color = form.color.data
        item_strategy.order = form.order.data
        item_strategy.category = dict(strategy_category_choices).get(form.category.data)
        db.session.commit()
        flash('Strategy has been updated.', 'success')
        return redirect(url_for('iplan.strategy'))
    elif request.method == 'GET':
        form.name.data = item_strategy.name
        form.symbol.data = item_strategy.symbol
        form.desc.data = item_strategy.desc
        form.color.data = item_strategy.color
        form.order.data = item_strategy.order
        form.category.data = reverse_dict(strategy_category_choices).get(item_strategy.category, 1)
        form.submit.label.text = 'Update'
    strategies = Strategy.query.all()
    # todo - count using sql
    count_tasks = {item.id: len(Task.query.filter_by(id_strategy=item.id).all()) for item in strategies}
    return render_template('iplan/strategy_edit.html', form=form, strategies=strategies,
                           legend='Update Strategy', count_tasks=count_tasks)


@iplan.route('/iplan/strategy/delete/<id_strategy>', methods=['GET', 'POST'])
def strategy_delete(id_strategy):
    item_strategy = Strategy.query.get_or_404(id_strategy)
    tasks_for_strategy = Task.query.filter_by(id_strategy=id_strategy).all()
    if tasks_for_strategy:
        flash(f'There are still {len(tasks_for_strategy)} task(s) for this category. It can not be removed without'
              f' prior reassignment. There will be automatic solution built later. For now, do that manually.', 'danger')
    else:
        db.session.delete(item_strategy)
        db.session.commit()
        flash('Strategy was deleted', 'success')
    return redirect(url_for('iplan.strategy'))

# todo - strategy: when tasks are there - add to route strategy_delete nr of task
# todo - strategy: when tasks are there - add to route strategy_update nr of task
# todo - strategy: when tasks are there - add to strategy.html on delete button nr tasks
# todo - color picker with bootstrap and JS (it's available on net)
