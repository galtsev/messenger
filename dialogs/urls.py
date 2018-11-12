from django.urls import path
from rest_framework import routers

from dialogs import views


urlpatterns = [
    path('thread/', views.ThreadList.as_view()),
    path('thread/<int:pk>', views.get_thread_view),
    path('thread/<int:thread_id>/participants', views.add_participant),
    path('thread/<int:thread_id>/participants/<int:user_id>', views.remove_participant),
    path('thread/<int:thread_id>/remove_participant', views.remove_participant),
    path('thread/<int:thread_id>/messages', views.MessageView.as_view()),
]