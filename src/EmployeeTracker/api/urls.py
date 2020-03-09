from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ListEmployeeAttendant, CreateAttendantEmployee, CreateEmployeeVacation, CreateLeaveEmployee

router = DefaultRouter()
router.register('work', ListEmployeeAttendant, basename='Leave')
urlpatterns = [
    path('check/<empId>', CreateAttendantEmployee.as_view()),
    path('vacation/<empId>', CreateEmployeeVacation.as_view()),
    path('leave/<empId>', CreateLeaveEmployee.as_view())
]
urlpatterns += router.urls
