from django.urls import path

from . import views
from .my_skill import skill
from django_ask_sdk.skill_adapter import SkillAdapter

my_skill_view = SkillAdapter.as_view(
    skill=skill)

urlpatterns = [
    path('', my_skill_view, name='index'),
    path('doctorappointment', views.DoctorAppointment.as_view(), name="doctorappointment"),
    path('createUser', views.createUser.as_view(), name="createUser"),
        path('listappointments', views.ListAppointment.as_view(), name="listappointments"),
        path('listappointments/<str:listall>/<str:next>', views.ListAppointment.as_view(), name="listappointments"),
]
