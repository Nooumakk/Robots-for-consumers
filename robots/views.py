import json
import openpyxl
from datetime import datetime, timedelta
from openpyxl.writer.excel import save_virtual_workbook
from .models import Robot
from django.http import JsonResponse, HttpResponse
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


class RobotDetailView(View):
    def get(self, request):
        current_date = datetime.now()
        one_week_ago = current_date - timedelta(weeks=1)
        robots = Robot.objects.filter(created__gte=one_week_ago).order_by("model").values("model", "version")
        models = set([model["model"] for model in robots])
        workbook = openpyxl.Workbook()
        for model in models:
            sheet = workbook.create_sheet(model)

            sheet["A1"] = "Model"
            sheet["B1"] = "Version"
            sheet["C1"] = "Quantity per week"

            # created = timezone.make_aware(one_week_ago, timezone=timezone.get_current_timezone())
            count = 0
            for robot in robots:
                if robot["model"] == model:
                    count += 1
                    continue
            sheet.append([model, robot["version"], count])

        file_name = "example.xlsx"

        excel_data = save_virtual_workbook(workbook)

        response = HttpResponse(
            excel_data, content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
        response["Content-Disposition"] = f'attachment; filename="{file_name}"'

        return response
