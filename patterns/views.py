from django.shortcuts import get_object_or_404, render

from .models import Pattern, PropType


def index(request):
    pattern_list = Pattern.objects.all()
    return render(request, 'patterns/index.html',
                  {'pattern_list': pattern_list,
                   'PropType': PropType})


def detail(request, pattern_id):
    pattern = get_object_or_404(Pattern, pk=pattern_id)
    return render(request, 'patterns/detail.html', {'pattern': pattern})
