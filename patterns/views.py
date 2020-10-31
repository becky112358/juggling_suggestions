from django.shortcuts import get_object_or_404, HttpResponseRedirect, render
from django.urls import reverse

from .forms import RecordForm
from .models import Modifier, Pattern, Record


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

    record_list = Record.objects.filter(pattern=pattern).order_by('-date')

    return render(request, 'patterns/detail.html',
                  {'pattern': pattern,
                   'pattern_list': pattern_list,
                   'modifier_list': Modifier,
                   'record_list': record_list})


def log_record(request, pattern_id):
    pattern = get_object_or_404(Pattern, pk=pattern_id)
    if request.method == 'POST':
        record = Record(pattern=pattern)
        formset = RecordForm(request.POST, request.FILES, instance=record)
        if formset.is_valid():
            formset.save()
            return HttpResponseRedirect(reverse('patterns:detail', args=(pattern.id,)))
    else:
        formset = RecordForm()
    return render(request, 'patterns/log_record.html',
                  {'pattern': pattern,
                   'formset': formset})
