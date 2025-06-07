from django.urls import path
from timer import views

app_name = 'timer'

urlpatterns = [
    path(
        'timers/',
        views.TimerListCreateAPIView.as_view(),
        name='timer-list-create'
    ),
    path(
        'timers/<int:pk>/',
        views.TimerDetailAPIView.as_view(),
        name='timer-detail'
    ),
]
