import json
from .models import Order
from customers.models import Customer
from django.http import JsonResponse
from django.views import View
from django.core.exceptions import ValidationError


class OrderCreateView(View):
    def post(self, request):
        try:
            content_type = request.headers.get("Content-Type", "")
            if content_type != "application/json":
                return JsonResponse({"error": "Invalid content type"}, status=400)
            data = json.loads(request.body.decode("utf-8"))

            customer, created = Customer.objects.get_or_create(email=data["email"])

            order = Order(customer=customer, robot_serial=data["robot_serial"])
            order.full_clean()
            order.save()

            return JsonResponse({"status": "OK"})
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON data"}, status=400)
        except ValidationError as exc:
            return JsonResponse({"error": exc.message_dict}, status=400)
