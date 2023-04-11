from django.urls import path, include
from . import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register(prefix="employee", viewset=views.EmployeeViewSet, basename="employee")
router.register(prefix="log-time", viewset=views.LogtimeViewSet, basename="log-time")

urlpatterns = [
    path("logtime/", views.log_time, name="logtime-user"),
    path("chart-view/", views.chart_view, name="chart-logs-view"),
]
urlpatterns += [path("", include(router.urls))]
