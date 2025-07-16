from django.urls import path
from timer import views

app_name = 'timer'

urlpatterns = [
    path(
        '',
        views.TimerListCreateAPIView.as_view(),
        name='timer-list-create'
    ),
    path(
        '<int:pk>/media-upload',
        views.TimerImageCreateAPIView.as_view(),
        name='timer-media-upload'
    ),
    path(
        '<int:pk>',
        views.TimerDetailAPIView.as_view(),
        name='timer-detail'
    ),
    path(
        'types',
        views.TypeListCreateAPIView.as_view(),
        name='timer-type-list-create'
    ),
    path(
        'types/<int:pk>',
        views.TypeDetailsAPIView.as_view(),
        name='timer-type-update'
    )
]
