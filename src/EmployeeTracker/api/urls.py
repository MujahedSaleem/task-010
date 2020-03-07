from django.urls import path,include

from .views import ListEmployeeAttendant, CreateAttendantEmployee, CreateEmployeeVacation

urlpatterns=[
    path('<t>', ListEmployeeAttendant.as_view()),
    path('check/<empId>', CreateAttendantEmployee.as_view()),
    path('vacation/<empId>',CreateEmployeeVacation.as_view())
]