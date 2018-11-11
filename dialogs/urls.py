from django.urls import path
from rest_framework import routers

from dialogs import views

router = routers.DefaultRouter()
router.register(r'messages', views.MessageViewSet)

urlpatterns = [
    path('thread/', views.ThreadList.as_view()),
    path('thread/<int:pk>', views.ThreadDetail.as_view()),
] + router.urls