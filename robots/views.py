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
        robots = Robot.objects.filter(created__gte=one_week_ago).values("model", "version")
        models = set([robot["model"] for robot in robots])
        workbook = openpyxl.Workbook()
        for model in models:
            sheet = workbook.create_sheet(model)

            sheet["A1"] = "Модель"
            sheet["B1"] = "Версия"
            sheet["C1"] = "Количество за неделю"

            model_robots = robots.filter(model=model)
            version_counts = {}

            for robot in model_robots:
                version = robot["version"]
                if version in version_counts:
                    version_counts[version] += 1
                else:
                    version_counts[version] = 1

            data_to_append = [[model, version, count] for version, count in version_counts.items()]
            for row_data in data_to_append:
                sheet.append(row_data)

        file_name = "example.xlsx"

        excel_data = save_virtual_workbook(workbook)

        response = HttpResponse(
            excel_data, content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
        response["Content-Disposition"] = f'attachment; filename="{file_name}"'

        return response
