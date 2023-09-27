import json
from .models import Robot
from django.http import JsonResponse
from django.views import View
from django.core.exceptions import ValidationError


class RobotCreateView(View):
    def post(self, request, *args, **kwargs):
        try:
            content_type = request.headers.get("Content-Type", "")
            if content_type != "application/json":
                return JsonResponse({"error": "Invalid content type"}, status=400)

            data = json.loads(request.body.decode("utf-8"))
            robot = Robot(**data)
            robot.full_clean()
            robot.save()
            return JsonResponse({"message": f"Robot {robot.serial} created successfully"})

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON data"}, status=400)

        except ValidationError as exc:
            return JsonResponse({"error": exc.message_dict}, status=400)
