from django.urls import path
from robots import views

urlpatterns = [
    path("robot/", views.RobotCreateView.as_view(), name="robot"),
    path("robot/detail", views.RobotDetailView.as_view(), name="robot_detail"),
]
