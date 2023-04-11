from django.urls import path
from .views import profile, RegisterView
from tracking.views import log_time, chart_view, home

urlpatterns = [
    path("", home, name="users-home"),
    path("register/", RegisterView.as_view(), name="users-register"),
    path("profile/", profile, name="users-profile"),
]
