from django.shortcuts import render, redirect
from django.contrib import messages

from account.models import Doctor, Patient, Nurse

from administration.models import Log
from administration.models import Stat
from appointments.models import Appointment
from meditems.models import Prescription
from administration.models import Hospital
from django.template import loader

from django.contrib.auth import (
    authenticate,
    get_user_model,
    login,
    logout,
)

import administration

from account.models import Profile, Nurse, Doctor

from account.forms import ProfileForm

from login.forms import UserRegisterForm
from administration.forms import HospitalForm


def landing(request, message=""):
    """
    landing page for an admin
    """
    if request.user.is_superuser:

        patients = Patient.objects.all()
        nurses = Nurse.objects.all()
        doctors = Doctor.objects.all()

        logs = Log.objects.all()

        #Counts hospitals in system
        if (Stat.objects.filter(name="Hospitals").count() == 1):
            Stat.objects.filter(name="Hospitals")[0].delete()
        stats = Stat(name="Hospitals", value=Hospital.objects.all().count())
        # Save the object
        stats.save()

        #Counts doctors in system
        if (Stat.objects.filter(name="Doctors").count() == 1):
            Stat.objects.filter(name="Doctors")[0].delete()
        stats = Stat(name="Doctors", value=Doctor.objects.all().count())
        # Save the object
        stats.save()


        # Counts nurses in system
        if (Stat.objects.filter(name="Nurses").count() == 1):
            Stat.objects.filter(name="Nurses")[0].delete()
        stats = Stat(name="Nurses", value=Nurse.objects.all().count())
        # Save the object
        stats.save()


        # Counts patients in system
        if (Stat.objects.filter(name="Patients").count() == 1):
            Stat.objects.filter(name="Patients")[0].delete()
        stats = Stat(name="Patients", value=Patient.objects.all().count())
        # Save the object
        stats.save()


        #If the Apointment Counter object is created then delete it
        if(Stat.objects.filter(name="Appointment Counter").count() == 1):
            Stat.objects.filter(name="Appointment Counter")[0].delete()
        #Initialize the Apointment Counter object
        stats = Stat(name = "Appointment Counter", value  = Appointment.objects.all().count())
        #Save the object
        stats.save()


        # If the Average Visits Per Patient object is created then delete it
        if (Stat.objects.filter(name="Average Visits Per Patient").count() == 1):
            Stat.objects.filter(name="Average Visits Per Patient")[0].delete()
        # Initialize the Average Visits Per Patient object
        if (Patient.objects.all().count() == 0 ):
            stats = Stat(name="Average Visits Per Patient", value=(0))
        else:
            stats = Stat(name="Average Visits Per Patient", value= (Appointment.objects.all().count() / Patient.objects.all().count()))
        #Save the objects
        stats.save()


        #number of admited patients
        if (Stat.objects.filter(name="Patients Currently Admitted").count() == 1):
            Stat.objects.filter(name="Patients Currently Admitted")[0].delete()
        cntr = 0
        patCount = Patient.objects.all().count()
        if patCount != 0:
            for pat in Patient.objects.all():
                if pat.isAdmitted == "YES":
                    cntr = cntr + 1

        stats1 = Stat(name="Patients Currently Admitted", value=cntr)
        stats1.save()


        #total number of precsriptions
        if (Stat.objects.filter(name="Issued Prescriptions").count() == 1):
            Stat.objects.filter(name="Issued Prescriptions")[0].delete()

        presCnt = Stat(name= "Issued Prescriptions", value= Prescription.objects.all().count())
        presCnt.save()


        #average number of prescripions per patient
        if (Stat.objects.filter(name="Average Prescriptions Per Patient").count() == 1):
            Stat.objects.filter(name="Average Prescriptions Per Patient")[0].delete()
        if (Patient.objects.all().count() == 0):
            avgPresCnt = Stat(name="Average Prescriptions Per Patient", value=0)
        else:
            avgPresCnt = Stat(name= "Average Prescriptions Per Patient", value= Prescription.objects.all().count())

        avgPresCnt.save()

        statistics = Stat.objects.filter()


        return render(request,'administration/landing.html',{"patients":patients, "nurses":nurses, "doctors":doctors,
                                                             "logs":logs, "statistics" : statistics,"message":message})


    return redirect('/')


def register_new_nurse(request):

    # this view provides an admin with the ability to register other users
    if request.user.is_superuser:

        title = "Register Nurse"
        form = UserRegisterForm(request.POST or None)

        if form.is_valid():
            user = form.save(commit=False)
            password = form.cleaned_data.get('password')
            user.set_password(password)
            user.save()

            profile = Profile()
            profile.user = user
            profile.save()

            nurse = Nurse()
            nurse.profile = profile
            nurse.save()

            log = Log(username="admin", action=" registered "+ nurse.profile.user.username + " as a nurse ")
            log.save()
            msg = "Nurse %s was successfully created" % nurse

            return landing(request,msg)

        context = {
            "form":form,
            "title":title
        }
        return render(request,'administration/create_user.html',context)
    else:
        return redirect('/')


def register_new_doctor(request):

    # # this view provides an admin with the ability to register other users
    if request.user.is_superuser:

        title = "Register Doctor"
        form = UserRegisterForm(request.POST or None)
        profile_form = ProfileForm(request.POST or None)

        if form.is_valid() and profile_form.is_valid():
            user = form.save(commit=False)
            password = form.cleaned_data.get('password')
            user.set_password(password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()

            doctor = Doctor()
            doctor.profile = profile
            doctor.save()

            messages.success(request, 'Form submission successful')

            log = Log(username="admin", action=" registered "+ doctor.profile.user.username + " as a doctor ")
            log.save()

            msg = "Doctor %s was successfully created" % doctor

            return landing(request,msg)

        context = {
            "form":form,
            "title":title,
            "prof":profile_form,
        }
        return render(request,'administration/create_user.html',context)
    else:
        return redirect('/')

def register_new_hospital(request):

    # # this view provides an admin with the ability to register other users
    if request.user.is_superuser:

        title = "Register Hospital"
        form = HospitalForm(request.POST or None)

        if form.is_valid():
            hospital = form.save(commit=False)
            hospital.save()

            messages.success(request, 'Form submission successful')

            log = Log(username="admin", action=" created "+ hospital.name + " hospital ")
            log.save()

            msg = "%s was registered as a new hospital" % hospital

            return landing(request,msg)

        context = {
            "form":form,
            "title":title
        }
        return render(request,'administration/create_user.html',context)
    else:
        return redirect('/')
