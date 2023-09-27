from django.urls import path
from robots import views

urlpatterns = [path("robot/", views.RobotCreateView.as_view(), name="robot")]
