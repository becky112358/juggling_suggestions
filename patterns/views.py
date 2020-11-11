from django.contrib.auth import get_user_model
from django.db.models import Q
from django.shortcuts import get_object_or_404, HttpResponseRedirect, render
from django.urls import reverse

from .forms import GoalForm, RecordForm, RecordFormTwoJugglers
from .models import Goal, Modifier, Pattern, Record


def index(request):
    pattern_list = Pattern.objects.all()

    n_jugglers_list = []
    for pattern in pattern_list:
        if pattern.n_jugglers not in n_jugglers_list:
            n_jugglers_list.append(pattern.n_jugglers)

    return render(request, 'patterns/index.html',
                  {'pattern_list': pattern_list,
                   'prop_type_list': Pattern.PropType,
                   'n_jugglers_list': n_jugglers_list})


def detail(request, pattern_id):
    pattern_list = Pattern.objects.all()
    pattern = get_object_or_404(Pattern, pk=pattern_id)

    current_user = request.user

    goal = Goal.objects.filter(pattern=pattern).filter(user=current_user)
    if goal:
        if request.method == 'POST':
            form = GoalForm(request.POST, instance=goal[0])
            if form.is_valid():
                goal.delete()
                return HttpResponseRedirect(reverse('patterns:detail', args=(pattern.id,)))
        else:
            form = GoalForm()

        goal_text = "Remove this pattern from my goals"

    else:
        if request.method == 'POST':
            goal_list = Goal.objects.filter(user=request.user)
            max_row = goals_max_row(goal_list)
            goal = Goal(user=current_user, pattern=pattern, row=max_row + 1)
            form = GoalForm(request.POST, request.FILES, instance=goal)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect(reverse('patterns:detail', args=(pattern.id,)))
        else:
            form = GoalForm()

        goal_text = "Add this pattern to my goals"

    record_list = user_get_records(current_user).filter(pattern=pattern)

    return render(request, 'patterns/detail.html',
                  {'pattern': pattern,
                   'pattern_list': pattern_list,
                   'modifier_list': Modifier,
                   'form': form,
                   'goal_text': goal_text,
                   'record_list': record_list})


# TODO fix this tangle!
def log_record(request, pattern_id):
    pattern = get_object_or_404(Pattern, pk=pattern_id)
    n_jugglers = pattern.n_jugglers
    current_user = request.user
    other_users = get_user_model().objects.exclude(id=current_user.id)
    if request.method == 'POST':
        record = Record(pattern=pattern)
        if n_jugglers == 1:
            form = RecordForm(request.POST, request.FILES, instance=record)
        else:
            form = RecordFormTwoJugglers(request.POST, request.FILES, instance=record,
                                         other_users=other_users)
        if form.is_valid():
            record = form.save(commit=False)
            record.user1 = current_user
            record.save()
            return HttpResponseRedirect(reverse('patterns:detail', args=(pattern.id,)))
    else:
        if n_jugglers == 1:
            form = RecordForm()
        else:
            form = RecordFormTwoJugglers(other_users=other_users)
    return render(request, 'patterns/log_record.html',
                  {'pattern': pattern,
                   'form': form})


def training_statistics(request):
    record_list = user_get_records(request.user)
    return render(request, 'patterns/training_statistics.html',
                  {'record_list': record_list})


def goals(request):
    goal_list = Goal.objects.filter(user=request.user)
    max_row = goals_max_row(goal_list)
    return render(request, 'patterns/goals.html',
                  {'goal_list': goal_list,
                   'row_list': range(max_row+1)})


def user_get_records(user):
    record_list = Record.objects \
        .filter(Q(user1=user) | Q(user2=user)) \
        .order_by('-date')
    return record_list


def goals_max_row(goal_list):
    max_row = 0
    for goal in goal_list:
        max_row = max(max_row, goal.row)
    return max_row
