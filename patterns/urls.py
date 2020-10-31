from django.urls import path

from . import views

app_name = 'patterns'
urlpatterns = [
    path('', views.index, name='index'),
    path('<int:pattern_id>/', views.detail, name='detail'),
    path('<int:pattern_id>/log_record', views.log_record, name='log_record'),
]
