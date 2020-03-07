from django.db import models
from django.contrib.auth.models import User


class baseAttendLeaveClass(models.Model):
    inTime = models.DateTimeField(auto_now=True, editable=True)
    outTime = models.DateTimeField(null=True, blank=True)
    date = models.DateField(auto_now_add=True, editable=True)

    class Meta:
        abstract = True


class Attendants(baseAttendLeaveClass):
    emp = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name="attendant")


class Vacation(models.Model):
    emp = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name="vacations")
    date = models.DateField()


class Leave(baseAttendLeaveClass):
    emp = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name="leaves")

