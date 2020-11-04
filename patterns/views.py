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

    if Goal.objects.filter(pattern=pattern).filter(user=current_user):
        is_goal = True
    else:
        is_goal = False

    if request.method == 'POST':
        goal = Goal(user=current_user, pattern=pattern, row=0)
        form = GoalForm(request.POST, request.FILES, instance=goal)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('patterns:detail', args=(pattern.id,)))
    else:
        form = GoalForm()

    record_list = Record.objects.filter(pattern=pattern)\
        .filter(Q(user1=current_user) | Q(user2=current_user))\
        .order_by('-date')

    return render(request, 'patterns/detail.html',
                  {'pattern': pattern,
                   'pattern_list': pattern_list,
                   'modifier_list': Modifier,
                   'is_goal': is_goal,
                   'form': form,
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
