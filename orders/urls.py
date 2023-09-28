from django.urls import path
from orders import views

urlpatterns = [path("order/", views.OrderCreateView.as_view(), name="order")]
