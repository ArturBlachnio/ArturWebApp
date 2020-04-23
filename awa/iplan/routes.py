from flask import Blueprint, render_template, flash, redirect, url_for, request
from awa import db
from awa.iplan.models import Strategy, Task
from awa.iplan.forms import StrategyForm, TaskForm
from awa.iplan._initial_setup import *
from datetime import timedelta, date, datetime
from awa.iplan.utils import (TimeLine, duration_from_string, string_from_duration, reverse_dict, reorder_tasks)


iplan = Blueprint(name='iplan', import_name=__name__)


@iplan.route('/iplan', methods=['GET', 'POST'])
def home():
    tasks = Task.query.all()
    strategies = Strategy.query.all()
    return render_template('iplan/home.html', tasks=tasks, strategies=strategies)


@iplan.route('/iplan/timeline', methods=['GET', 'POST'])
def timeline():
    tasks = Task.query.filter(Task.time_completion.is_(None)).order_by(Task.order).all()
    strategies = Strategy.query.all()
    # todo - count using sql
    count_tasks = dict(zip([strategy.id for strategy in strategies], [0 for _ in range(len(strategies))]))
    for task in tasks:
        if task.strategy.id in count_tasks:
            count_tasks[task.strategy.id] += 1

    return render_template('iplan/timeline.html', tasks=tasks, TimeLine=TimeLine, strategies=strategies, count_tasks=count_tasks,
                           string_from_duration=string_from_duration, now=datetime.now())




@iplan.route('/iplan/task', methods=['GET', 'POST'])
def task():
    tasks = Task.query.order_by(Task.order).all()
    strategies = Strategy.query.all()
    return render_template('iplan/task.html', tasks=tasks, strategies=strategies,
                           string_from_duration=string_from_duration, now=datetime.now())

@iplan.route('/iplan/task/donetoday', methods=['GET', 'POST'])
def task_donetoday():
    tasks = Task.query.filter(Task.time_completion>=date.today()).order_by(Task.order).all()
    return render_template('iplan/task.html', tasks=tasks, string_from_duration=string_from_duration, now=datetime.now())


@iplan.route('/iplan/task/completed', methods=['GET', 'POST'])
def task_completed():
    tasks = Task.query.filter(Task.time_completion.isnot(None)).order_by(Task.order).all()
    strategies = Strategy.query.all()
    return render_template('iplan/task.html', tasks=tasks, strategies=strategies,
                           string_from_duration=string_from_duration, now=datetime.now())


@iplan.route('/iplan/task/open', methods=['GET', 'POST'])
def task_open():
    tasks = Task.query.filter(Task.time_completion.is_(None)).order_by(Task.order).all()
    strategies = Strategy.query.all()
    return render_template('iplan/task.html', tasks=tasks, strategies=strategies,
                           string_from_duration=string_from_duration, now=datetime.now())


@iplan.route('/iplan/task/create/timeline_catgory_<timeline_category>', methods=['GET', 'POST'])
def task_create(timeline_category='This Week'):
    form_task = TaskForm()
    # Dynamic choices
    form_task.id_strategy.choices = [(item.id, item.name) for item in Strategy.query.order_by(Strategy.order).all()]
    form_task.category.choices = TASK_CATEGORY_CHOICES
    form_task.frequency.choices = TASK_FREQUENCY_CHOICES
    form_task.time_line.choices = TimeLine.selectfield_choices()
    if form_task.validate_on_submit():
        task = Task(name=form_task.name.data, desc=form_task.desc.data,
                duration_plan=duration_from_string(form_task.duration_plan.data),
                duration_real=duration_from_string(form_task.duration_real.data),
                category=dict(TASK_CATEGORY_CHOICES).get(form_task.category.data),
                frequency=dict(TASK_FREQUENCY_CHOICES).get(form_task.frequency.data),
                id_strategy=form_task.id_strategy.data,
                order=form_task.order.data,
                time_line=form_task.time_line.data,
                time_due=form_task.time_due.data)
        db.session.add(task)
        db.session.commit()
        return redirect(url_for('iplan.timeline'))
    elif request.method == 'GET':
        form_task.order.data = 0
        form_task.submit.label.text = 'Create task'
        form_task.time_line.data = timeline_category
        form_task.time_due.data = datetime.now() + timedelta(days=DUE_DATE_INITIAL_DAYS)
    return render_template('iplan/task_edit.html', form_task=form_task, legend='Create New Task')


@iplan.route('/iplan/task/update/<id_task>', methods=['GET', 'POST'])
def task_update(id_task):
    form_task = TaskForm()
    # Dynamic choices
    form_task.id_strategy.choices = [(item.id, item.name) for item in Strategy.query.all()]
    form_task.category.choices = TASK_CATEGORY_CHOICES
    form_task.frequency.choices = TASK_FREQUENCY_CHOICES
    form_task.time_line.choices = TimeLine.selectfield_choices()

    task = Task.query.get_or_404(id_task)
    if form_task.validate_on_submit():
        task.name = form_task.name.data
        task.id_strategy = form_task.id_strategy.data
        task.desc = form_task.desc.data
        task.category = dict(TASK_CATEGORY_CHOICES).get(form_task.category.data)
        task.frequency = dict(TASK_FREQUENCY_CHOICES).get(form_task.frequency.data)
        task.duration_plan = duration_from_string(form_task.duration_plan.data)
        task.duration_real = duration_from_string(form_task.duration_real.data)
        task.time_line = form_task.time_line.data
        task.time_due = form_task.time_due.data
        task.order = form_task.order.data
        db.session.commit()
        return redirect(url_for('iplan.timeline'))
    elif request.method == 'GET':
        form_task.name.data = task.name
        form_task.id_strategy.data = task.id_strategy
        form_task.desc.data = task.desc
        form_task.category.data = reverse_dict(TASK_CATEGORY_CHOICES).get(task.category, 1)
        form_task.frequency.data = reverse_dict(TASK_FREQUENCY_CHOICES).get(task.frequency, 1)
        form_task.duration_plan.data = string_from_duration(task.duration_plan)
        form_task.duration_real.data = string_from_duration(task.duration_real)
        form_task.order.data = task.order
        form_task.time_line.data = task.time_line
        form_task.time_due.data = task.time_due
        form_task.submit.label.text = 'Update task'
    return render_template('iplan/task_edit.html', form_task=form_task, legend='Update Task')


@iplan.route('/iplan/task/complete/<id_task>', methods=['GET', 'POST'])
def task_complete(id_task):
    task = Task.query.get_or_404(id_task)
    task.time_completion = datetime.now()
    # Add new task if task was repeatable
    if task.frequency == 'Continues':
        new_task = Task(name=task.name, desc=task.desc,
                        duration_plan=task.duration_plan, duration_real=timedelta(0),
                        category=task.category, frequency=task.frequency,
                        id_strategy=task.id_strategy, order=task.order,
                        time_line='This Week',
                        time_creation=datetime.now() + timedelta(days=1))
        db.session.add(new_task)
    db.session.commit()
    return redirect(url_for('iplan.timeline'))


@iplan.route('/iplan/task/restore/<id_task>', methods=['GET', 'POST'])
def task_restore(id_task):
    task = Task.query.get_or_404(id_task)
    task.time_completion = None
    db.session.commit()
    return redirect(request.referrer)


@iplan.route('/iplan/task/move_<direction>/<id_task>', methods=['GET', 'POST'])
def task_move(id_task, direction):
    task = Task.query.get_or_404(id_task)
    tasks = Task.query.filter(Task.time_completion.is_(None)).order_by(Task.order).all()
    new_orders_of_ids = reorder_tasks(direction=direction, task_id=task.id,
                                      current_order_of_ids=[task.id for task in tasks])
    for i, task in enumerate(tasks):
        task.order = new_orders_of_ids[i] + TimeLine.get_timeline_index(task.time_line) * 100
    db.session.commit()
    return redirect(url_for('iplan.timeline'))


@iplan.route('/iplan/task/move_timeline_to_<direction>/<id_task>', methods=['GET', 'POST'])
def task_move_timeline(id_task, direction):
    task = Task.query.get_or_404(id_task)
    task.time_line = TimeLine.move_in_timeline(current_timeline=task.time_line, direction=direction)
    db.session.commit()
    return redirect(url_for('iplan.timeline'))


# 'iplan.task_timeline_move', id_task=task.id, direction='right')

@iplan.route('/iplan/task/timer_start/<id_task>')
def task_timer_start(id_task):
    task = Task.query.get_or_404(id_task)
    task.timer_start = datetime.now()
    db.session.commit()
    return redirect(request.referrer)


@iplan.route('/iplan/task/timer_end/<id_task>')
def task_timer_end(id_task):
    task = Task.query.get_or_404(id_task)
    task.duration_real += datetime.now() - task.timer_start
    task.timer_start = None
    # todo remove timer_end from database - its not needed
    db.session.commit()
    return redirect(request.referrer)


@iplan.route('/iplan/task/delete/<id_task>', methods=['GET', 'POST'])
def task_delete(id_task):
    task = Task.query.get_or_404(id_task)
    db.session.delete(task)
    db.session.commit()
    return redirect(request.referrer)


@iplan.route('/iplan/task/show_menu_<state>/<id_task>', methods=['GET', 'POST'])
def show_menu(id_task, state):
    task = Task.query.get_or_404(id_task)
    if state == 'on':
        task.show_menu = True
    elif state == 'off':
        task.show_menu = False
    db.session.commit()
    return redirect(request.referrer)


@iplan.route('/iplan/task/show_menu_all_<state>', methods=['GET', 'POST'])
def show_menu_all(state):
    tasks = Task.query.filter(Task.time_completion.is_(None)).all()
    if state == 'on':
        for task in tasks:
            task.show_menu = True
    elif state == 'off':
        for task in tasks:
            task.show_menu = False
    db.session.commit()
    return redirect(request.referrer)


@iplan.route('/iplan/task/show_strategy_timeline_<id_strategy>', methods=['GET', 'POST'])
def show_strategy_timeline(id_strategy):
    strategy = Strategy.query.get_or_404(id_strategy)
    strategy.show_timeline = not strategy.show_timeline
    db.session.commit()
    return redirect(request.referrer)


@iplan.route('/iplan/strategy', methods=['GET', 'POST'])
def strategy():
    strategies = Strategy.query.order_by(Strategy.order).all()
    # todo - count using sql
    count_tasks = {item.id: len(Task.query.filter_by(id_strategy=item.id).all()) for item in strategies}
    return render_template('iplan/strategy.html', strategies=strategies, legend='Create New Strategy',
                           count_tasks=count_tasks)


@iplan.route('/iplan/strategy/create', methods=['GET', 'POST'])
def strategy_create():
    form = StrategyForm()
    form.category.choices = STRATEGY_CATEGORY_CHOICES

    if form.validate_on_submit():
        item_strategy = Strategy(name=form.name.data, symbol=form.symbol.data, desc=form.desc.data,
                                 color=form.color.data, order=form.order.data,
                                 category=dict(STRATEGY_CATEGORY_CHOICES).get(form.category.data))
        db.session.add(item_strategy)
        db.session.commit()
        return redirect(url_for('iplan.strategy'))
    elif request.method == 'GET':
        form.order.data = 0
        form.color.data = 'LightSteelBlue'
    return render_template('iplan/strategy_edit.html', form=form, legend='Create New Strategy')


@iplan.route('/iplan/strategy/update/<id_strategy>', methods=['GET', 'POST'])
def strategy_update(id_strategy):
    form = StrategyForm()
    form.category.choices = STRATEGY_CATEGORY_CHOICES

    item_strategy = Strategy.query.get_or_404(id_strategy)
    if form.validate_on_submit():
        item_strategy.name = form.name.data
        item_strategy.symbol = form.symbol.data
        item_strategy.desc = form.desc.data
        item_strategy.color = form.color.data
        item_strategy.order = form.order.data
        item_strategy.category = dict(STRATEGY_CATEGORY_CHOICES).get(form.category.data)
        db.session.commit()
        return redirect(url_for('iplan.strategy'))
    elif request.method == 'GET':
        form.name.data = item_strategy.name
        form.symbol.data = item_strategy.symbol
        form.desc.data = item_strategy.desc
        form.color.data = item_strategy.color
        form.order.data = item_strategy.order
        form.category.data = reverse_dict(STRATEGY_CATEGORY_CHOICES).get(item_strategy.category, 1)
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
# todo - Far Future change time to utc level. Currently it's local time only
