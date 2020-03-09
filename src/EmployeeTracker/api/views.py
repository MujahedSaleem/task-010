from django.contrib.auth.models import User
from django.db.models import Sum, Q
from rest_framework.decorators import action
from rest_framework import status
from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from ..models import Attendants, Vacation, Leave
from .serializers import AttendantSerializer, VacationSerializer, LeaveSerializer
from datetime import datetime, timedelta


def subtractTime(inTime, outTime) -> datetime:
    tIn = timedelta(hours=inTime.hour, minutes=inTime.minute)
    return (outTime - tIn)


class ListEmployeeAttendant(ModelViewSet):
    serializer_class = AttendantSerializer
    queryset = Attendants.objects.all()

    @action(['get'], detail=False, url_path="WorkingHour/(?P<t>[^/.]+)")
    def WorkingHour(self, request, *args, **kwargs):
        type = kwargs.get('t')

        try:
            if type == 'w':
                weekDateFromNow = datetime.now().date() - timedelta(days=7)
                xo = [self.makingFunction(user, user.attendant.filter(date__gte=weekDateFromNow), 'Weekly') for user in
                      User.objects.all()]
                return Response(xo)

            elif type == 'q':
                weekDateFromNow = datetime.now().date() - timedelta(days=91)
                xo = [self.makingFunction(user, user.attendant.filter(date__gte=weekDateFromNow), 'quarter') for user in
                      User.objects.all()]
                return Response(xo)
            elif type == 'y':
                weekDateFromNow = datetime.now().date() - timedelta(days=365)
                xo = [self.makingFunction(user, user.attendant.filter(date__gte=weekDateFromNow), 'yearly') for user in
                      User.objects.all()]
                return Response(xo)
            else:
                raise Exception("Determine the period")
        except Exception as ex:
            return Response(str(ex))

    @action(['get'], detail=False)
    def commingToLeavingForHoleTeam(self, request, *args, **kwargs):
        try:
            everyEmpWithWorkingHoure = [self.makingFunction(user, user.attendant, 'yearly') for user in
                                        User.objects.all()]
            everyEmpWithleavingHoure = [self.makingFunction(user, user.leaves, 'yearly') for user in
                                        User.objects.all()]
            sumWorkHour = 0
            for emp in everyEmpWithWorkingHoure:
                sumWorkHour += emp["workingHouresyearly"]
            if sumWorkHour == 0:
                raise Exception("This Team has no work hour ")
            sumLeaveHour = 0
            for emp in everyEmpWithleavingHoure:
                sumLeaveHour += emp["workingHouresyearly"]

            return Response(f"this team has an leaving of percent {sumLeaveHour // sumWorkHour}")

        except Exception as ex:
            return Response(str(ex))

    def makingFunction(self, emp, listAttends, t):
        list = [x for x in listAttends.values('inTime', 'outTime')]
        outtime = ""
        for i in range(len(list)):
            if list[i]['outTime'] != " ":
                outtime = list[i]['outTime']
            else:
                list[i]['outTime'] = outtime
        workingHoures = sum([subtractTime(t['inTime'], t['outTime']).hour for t in list])
        return {"EmpName": emp.username, f"workingHoures{t}": workingHoures}



class CreateAttendantEmployee(CreateAPIView):
    serializer_class = AttendantSerializer
    queryset = Attendants.objects.all()
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        empid = kwargs.get('empId')
        if empid != ' ':
            try:
                user = User.objects.get(pk=empid)
                if user is None:
                    raise Exception("User dose't exist")
                attend = Attendants.objects.filter(Q(emp_id=empid) & Q(date=datetime.now().date()))
                if attend.count() == 0:
                    newAttendant = self.serializer_class(data={'emp': empid})
                    newAttendant.is_valid(raise_exception=True)
                    newAttendant.save()
                    return Response({'message:Thank you'})

                elif attend[0].outTime is None:
                    cloneattend: Attendants = attend.get()
                    cloneattend.outTime = datetime.now()
                    cloneattend.save()
                    return Response({'message:Thank you'})
            except Exception as e:
                return Response({'error': str(e)})
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class CreateEmployeeVacation(CreateAPIView):
    serializer_class = VacationSerializer
    queryset = Vacation.objects.all()
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        empid = kwargs.get('empId')
        if empid != ' ':
            try:
                user = User.objects.get(pk=empid)
                if user is None:
                    raise Exception("User dose't exist")
                if 'date' in request.data:
                    vcationDate = request.data['date']
                    vcation = Vacation.objects.filter(date=vcationDate)
                    if vcation.count() == 0:
                        newVcation = self.serializer_class(data={'emp': empid, 'date': vcationDate})
                        newVcation.is_valid(raise_exception=True)
                        newVcation.save()
                        return Response("Have a good day ")
                    else:
                        raise Exception('You can\'t apply vacation twice in same date')
                else:
                    raise Exception('Vcation Date is required')
            except Exception as e:
                return Response(str(e))
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class CreateLeaveEmployee(CreateAPIView):
    serializer_class = LeaveSerializer
    queryset = Leave.objects.all()
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        empid = kwargs.get('empId')
        if empid != ' ':
            try:
                user = User.objects.get(pk=empid)
                if user is None:
                    raise Exception("User dose't exist")
                leave = Leave.objects.filter(Q(emp_id=empid) & Q(date=datetime.now().date()))
                if leave.count() == 0:
                    newLeave = self.serializer_class(data={'emp': empid})
                    newLeave.is_valid(raise_exception=True)
                    newLeave.save()
                    return Response({'message:Thank you'})

                elif leave[0].outTime is None:
                    cloneattend: Leave = leave.get()
                    cloneattend.outTime = datetime.now()
                    cloneattend.save()
                    return Response({'message:Thank you'})
            except Exception as e:
                return Response({'error': str(e)})
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
