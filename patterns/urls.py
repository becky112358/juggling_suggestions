from django.urls import path

from . import views

app_name = 'patterns'
urlpatterns = [
    path('', views.index, name='index'),
    path('<int:pattern_id>/', views.detail, name='detail'),
    path('<int:pattern_id>/log_record', views.log_record, name='log_record'),
    path('training_plan', views.training_plan, name='training_plan'),
    path('training_statistics', views.training_statistics, name='training_statistics'),
    path('goals', views.goals, name='goals'),
]
