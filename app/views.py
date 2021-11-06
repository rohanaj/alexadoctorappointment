from django.shortcuts import render, redirect
from django.views import View
from django.http import JsonResponse
# Create your views here.
from .models import Doctor, Patient, User1, Appointment
from datetime import datetime
from django.utils import timezone
from django.utils.decorators import method_decorator

from django.views.decorators.csrf import csrf_exempt




class createUser(View):
    def get(self, request):
        
        return render(request, "usercreate.html")
    def post(self, request):
        data = request.POST
        
        user = User1(first_name=data.get("first_name"),last_name=data.get("last_name"),user_type=data.get("user_type"))
        user.save()
        return redirect('createUser')
        
class DoctorAppointment(View):
    def get(self, request):
        doctors = Doctor.objects.all()
        patients = Patient.objects.all()
        return render(request, "appointment.html",{"doctors":doctors, "patients":patients})
    def post(self, request):
        data = request.POST
        timeslot = data.get("datetime");print("timeslot",timeslot)
         
        timeslot = datetime.strptime(timeslot,"%Y-%m-%dT%H:%M");print(timeslot)
        doctor = data.get("doctor")
        patient = data.get("patient")
        doctorname = doctor.split(" ")
        UserDoctor = User1.objects.get(first_name=doctorname[0],last_name=doctorname[1],user_type="doctor")
        userdoctor = Doctor.objects.get(user=UserDoctor)
        
        patientname = patient.split(" ")
        UserPatient = User1.objects.get(first_name=patientname[0],last_name=patientname[1],user_type="patient")
        userpatient = Patient.objects.get(user=UserPatient)
        
        appointment = Appointment(time=timeslot, doctor=userdoctor, patient=userpatient)
        appointment.save()
        
        return redirect('doctorappointment')
        
class ListAppointment(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(ListAppointment, self).dispatch(request, *args, **kwargs)
    def post(self,request):
        next = request.POST.get("next");print(next)
        listall = request.POST.get("listall");print(listall)
        listappointments = [] 
        appointments = list()
        if listall=="today":
           appointments = list(Appointment.objects.filter(time=datetime.datetime.now().date()).values())
        if listall is None and next is None:
            print("I am inside first condition")
            appointments = list(Appointment.objects.all().values())
        #elif next:
        #    appointments = list(Appointment.objects.filter(time__gt = datetime.now()).values())
        #    print("I am inside second condition")    
        elif listall:
            appointments = list(Appointment.objects.filter().values())
            print("I am inside thrid condition") 
                
                            
           
        print(appointments) 
        for ap in appointments:
            for k, v in ap.items():
                if k == "time":
                    ap[k] = timezone.localtime(v).isoformat()
                elif k == "doctor_id":
                    doctor_obj = Doctor.objects.get(id=v)
                    ap[k] = doctor_obj.user.first_name +" "+ doctor_obj.user.last_name
                elif k == "patient_id":
                    patient_obj = Patient.objects.get(id=v)
                    ap[k] = patient_obj.user.first_name +" "+ patient_obj.user.last_name
            listappointments.append(ap)
        
        return JsonResponse({"listappointment":listappointments})

        
        
            
                    


