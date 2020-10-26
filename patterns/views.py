from django.shortcuts import get_object_or_404, render

from .models import Modifier, Pattern


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
    return render(request, 'patterns/detail.html',
                  {'pattern': pattern,
                   'pattern_list': pattern_list,
                   'modifier_list': Modifier})
