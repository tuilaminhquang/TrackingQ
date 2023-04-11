from django.shortcuts import render
from django.http import HttpResponse
from datetime import datetime
import calendar
from datetime import timedelta
from django.db.models import Count, Q, Sum
from django.views.decorators.csrf import csrf_exempt
from tracking.models import LogTime, Employee
from django.contrib.auth.models import User
from django.db.models import Count, F, Max, Q, Sum
from django.contrib.auth.decorators import login_required
from rest_framework import viewsets, generics, status, permissions, mixins
from tracking.serializers import EmployeeSerializer, LogtimeSerializer
from rest_framework.decorators import action
import xlsxwriter
import io

@login_required()
def home(request):
    if request.method == "GET":
        search = request.GET.get("search", None)
        if search:
            employee = Employee.objects.filter(name__icontains=search)
        else:
            employee = Employee.objects.all()

        context = {
            "employee": employee,
        }
        return render(request, "tracking/employees.html", context)


class EmployeeViewSet(
    viewsets.ViewSet, generics.ListCreateAPIView, generics.RetrieveUpdateAPIView, generics.DestroyAPIView
):
    queryset = Employee.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = EmployeeSerializer

    @action(methods=["get"], url_path="create", detail=False)
    def get(self, request):
        return render(request, "tracking/create_employee.html")

    @action(methods=["get"], url_path="log-times", detail=True)
    def get_log(self, request, pk):
        employee = self.get_object()
        logs = employee.logs.all().order_by("-date")
        context = {"logs": logs, "employee": employee}
        return render(request, "tracking/detail_employee.html", context=context)


@csrf_exempt
def log_time(request):
    if request.method == "POST":
        date = request.POST.get("date")
        string_time = request.POST.get("hour")
        employee_id = request.POST.get("employee_id")
        from_hour = request.POST.get("from_hour")
        to_hour = request.POST.get("to_hour")
            
    employee = Employee.objects.get(pk=employee_id)
    date = datetime.strptime(date, "%Y-%m-%d")
    t1 = datetime.strptime(from_hour, "%H:%M")
    t2 = datetime.strptime(to_hour, "%H:%M")
    delta = t2 - t1
    total_hour = abs(delta.total_seconds() / (60 * 60))
    # split_time = string_time.split()
    # hour = split_time[0].split("h")[0]
    # if string_time.find("m") != -1:
    #     min_hour = round(float(split_time[1].split("m")[0]) / 60, 2)
    # else:
    #     min_hour = 0
    # total_hour = round(float(hour) + float(min_hour), 2)
    log = LogTime.objects.create(
        employee=employee, date=date, hour=total_hour, from_hour=t1, to_hour=t2
    )
    log.save()
    return HttpResponse(200)


def et_days_of_week(date):
    start = date - timedelta(days=date.weekday())
    end = start + timedelta(days=6)
    return {"start": start, "end": end}


def chart_view(request):
    date_from = request.POST.get("date")
    template_name = "tracking/char_view.html"
    start_end_date = request.GET.get("start_date", None)
    export_excel = request.GET.get("export_excel", None)
    if start_end_date:
        start_end_date = datetime.strptime(start_end_date, "%Y-%m-%d")
        start_end_date = et_days_of_week(start_end_date)
    else:
        start_end_date = et_days_of_week(datetime.today())
    start = datetime.strptime(start_end_date["start"].strftime("%Y-%m-%d"), "%Y-%m-%d")
    end = datetime.strptime(start_end_date["end"].strftime("%Y-%m-%d"), "%Y-%m-%d")

    user_logs = (
        LogTime.objects.select_related("employee")
        .values("employee")
        .filter(date__range=[start, end])
        .annotate(
            sum_hour=Sum("hour"),
            full_name=F("employee__name"),
            salary=F("employee__salary"),
            sum_salary=F("employee__salary") * F("sum_hour"),
        )
    )
    if export_excel:
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output)
        header = [
            "Tên nhân viên",
            "Số giờ làm",
            "Lương theo giờ",
            "Tổng tiền",
        ]
        work_sheet = workbook.add_worksheet()
        title_format = workbook.add_format({'bold': True, 'font_size': 20})
        bold = workbook.add_format({"bold": True, 'font_size': 13})
        normal = workbook.add_format({ 'font_size': 13})
        work_sheet.write(0, 2, "BẢNG LƯƠNG NHÂN VIÊN - HIÊN NHÀ COFFEE", title_format)


        work_sheet.write(1, 1, "Thoi gian", bold)
        work_sheet.write(1, 2, f"From {start} / To {end}", normal)
        for col_num, data in enumerate(header):
            work_sheet.write(3, col_num+1, data, bold)
        row = 4
        for user_log in user_logs:
            work_sheet.write(row, 1, user_log.get('full_name'), normal)
            work_sheet.write(row, 2, user_log.get('sum_hour'), normal)
            work_sheet.write(row, 3, user_log.get('salary'), normal)
            work_sheet.write(row, 4, user_log.get('sum_salary'), normal)
            row += 1
        #Set width of column
        work_sheet.set_column(1, 4, 30)

        workbook.close()
        output.seek(0)

        response = HttpResponse(
            output.read(),
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )
        response[
            "Content-Disposition"
        ] = "attachment; filename=HienNha-Payslip.xlsx"
        output.close()
        return response

    context = {
        "user_logs": user_logs,
        "start": start.strftime("%B %d, %Y"),
        "end": end.strftime("%B %d, %Y"),
    }
    
    return render(request, template_name, context=context)

class LogtimeViewSet(
    viewsets.ViewSet, generics.ListCreateAPIView, generics.RetrieveUpdateAPIView, generics.DestroyAPIView
):
    queryset = LogTime.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = LogtimeSerializer

