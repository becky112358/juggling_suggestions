from django.shortcuts import get_object_or_404, render

from .models import Pattern


def index(request):
    pattern_list = Pattern.objects.all()
    return render(request, 'patterns/index.html',
                  {'pattern_list': pattern_list,
                   'prop_type_list': Pattern.PropType})


def detail(request, pattern_id):
    pattern_list = Pattern.objects.all()
    pattern = get_object_or_404(Pattern, pk=pattern_id)
    return render(request, 'patterns/detail.html',
                  {'pattern': pattern,
                   'pattern_list': pattern_list})
