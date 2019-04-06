from django.shortcuts import render, redirect
from appointments.forms import AppointmentForm
from appointments.forms import AppointmentFormDoctor, AppointmentFormNurse
from account.models import Patient
from account.models import Doctor
from account.models import Nurse
from appointments.models import Appointment
from administration.models import Log
from administration.models import Stat
import account.views



def new_appointment(request):
    """
    This view manages the creation of a new appointment
    """

    if request.user.is_authenticated():

        title = "Create Appointment"

        user_id = request.user.id

        # used to check which type of user is creating a new appointment

        isPatient = (Patient.objects.filter(profile__user_id=user_id).count() == 1)
        isDoctor = (Doctor.objects.filter(profile__user_id=user_id).count() == 1)
        isNurse = (Nurse.objects.filter(profile__user_id=user_id).count() == 1)

        userType = ""

        if isPatient:
            userType = "Patient"

            # create a new form
            form = AppointmentForm(request.POST or None)

            # if the form is completed, log the action and save the new appointment
            if form.is_valid():
                appointment = form.save(commit=False)
                appointment.patient = Patient.objects.get(profile__user_id=request.user.id)
                appointment.save()

                log = Log(username=appointment.patient.profile.user.username, action=" created a new appointment ")
                log.save()


                msg = "Appointment with %s successfully created on %s" % (appointment.doctor, appointment.date)

                return account.views.index(request, msg)

        elif isDoctor:

            userType = "Doctor"

            form = AppointmentFormDoctor(request.POST or None)
            if form.is_valid():
                appointment = form.save(commit=False)
                appointment.doctor = Doctor.objects.get(profile__user_id=request.user.id)
                appointment.save()

                log = Log(username=appointment.doctor.profile.user.username, action=" created a new appointment ")
                log.save()

                msg = "Appointment with patient %s successfully created on %s" % (appointment.patient, appointment.date)



                return account.views.index(request, msg)

        elif isNurse:

            userType = "Nurse"

            nurse = (Nurse.objects.filter(profile__user_id=user_id))[0]

            form = AppointmentFormNurse(request.POST or None)
            if form.is_valid():
                appointment = form.save(commit=False)
                appointment.save()

                log = Log(username=nurse.profile.user.username, action=" created a new appointment ")
                log.save()


                msg = "Appointment successfully created with patient %s seeing %s on %s" % (appointment.patient, appointment.doctor, appointment.date)

                return account.views.index(request, msg)

        context = {
            "form": form,
            "title": title,
            "usertype": userType
        }
        return render(request, "appointments/create_appointment.html", context)

    else:
        return redirect('/login')


def edit_appointment(request, appointment_id):
    # this view is used for editing appointments with the appointmentform

    if request.user.is_authenticated():

        title = "Edit Appointment"

        user_id = request.user.id

        isPatient = (Patient.objects.filter(profile__user_id=user_id).count() == 1)
        isDoctor = (Doctor.objects.filter(profile__user_id=user_id).count() == 1)
        isNurse = (Nurse.objects.filter(profile__user_id=user_id).count() == 1)

        app_instance = Appointment.objects.get(id=appointment_id)

        if isPatient:

            # get the patient instance
            pat = Patient.objects.filter(profile__user_id=request.user.id)[0]

            # tests if the patient is viewing only their appointments
            isValid = (Appointment.objects.filter(id=appointment_id, patient=pat))

            # redirect if trying to access others appointments
            if not isValid:
                return redirect('/profile')

            # used to fill form with current values
            initdata = {'doctor': app_instance.doctor, "date": app_instance.date, 'time': app_instance.time,
                        'reason': app_instance.reason, 'short_reason': app_instance.short_reason}

            # create the form
            form = AppointmentForm(request.POST, instance=app_instance, initial=initdata)

            if request.POST:

                """
                modifications to appointments is completed in a bit of a messy way. The issue is that appointments
                should not be able to be edited to be during the same time of another if the doctor is the same.
                This test is done by getting a list of all appointments and checking if any match the current form
                submission. The problem with this is when an appointment is under edit, it already exists, and the
                checker flags the operation as illegal.

                The way around this was to save all the instance's current fields, and delete it. If the form fails,
                a new instance is created with the old forms and the user can try again. If the form is successful
                a new instance is created with the new values and the user is redirected.
                """

                # these are the appointment fields being saved
                pk = Appointment.objects.filter(id=appointment_id)[0].id
                date = Appointment.objects.filter(id=appointment_id)[0].date
                time = Appointment.objects.filter(id=appointment_id)[0].time
                doc = Appointment.objects.filter(id=appointment_id)[0].doctor
                reason = Appointment.objects.filter(id=appointment_id)[0].reason
                s_reason = Appointment.objects.filter(id=appointment_id)[0].short_reason

                # deletes the current appointment instance
                Appointment.objects.filter(id=appointment_id)[0].delete()


                # if the form is valid, log it and save the new data
                if form.is_valid():
                    log = Log(username=pat.profile.user.username, action=" edited an appointment ")
                    log.save()
                    form.save()
                    msg = "Appointment with %s on %s successfully modified" % (doc, date)

                    return account.views.index(request,msg)

                # if the form fails, create a new appointment instance and save it and send a new form
                else:
                    app = Appointment(id=pk, patient=pat, date=date, time=time, doctor=doc, reason=reason, short_reason=s_reason)
                    app.save()

            else:

                form = AppointmentForm(instance=app_instance, initial=initdata)

            return render(request, 'appointments/edit_appointment.html', {'form': form, 'usertype': 'patient'})

        elif isDoctor:

            doc = Doctor.objects.filter(profile__user_id=request.user.id)[0]

            # tests if the doctor is viewing only their appointments
            isValid = (Appointment.objects.filter(id=appointment_id, doctor=doc))

            if not isValid:
                return redirect('/profile')

            initdata = {'patient': app_instance.patient, "date": app_instance.date, 'time': app_instance.time,
                        'reason': app_instance.reason, 'short_reason': app_instance.short_reason}

            form = AppointmentFormDoctor(request.POST, instance=app_instance, initial=initdata)

            if request.POST:

                date = Appointment.objects.filter(id=appointment_id)[0].date
                time = Appointment.objects.filter(id=appointment_id)[0].time
                pat = Appointment.objects.filter(id=appointment_id)[0].patient
                reason = Appointment.objects.filter(id=appointment_id)[0].reason
                s_reason = Appointment.objects.filter(id=appointment_id)[0].short_reason
                pk = Appointment.objects.filter(id=appointment_id)[0].id

                Appointment.objects.filter(id=appointment_id)[0].delete()

                if form.is_valid():

                    log = Log(username=doc.profile.user.username, action=" edited an appointment ")
                    log.save()
                    form.save()

                    return redirect('/')
                else:

                    app = Appointment(id=pk, patient=pat, date=date, time=time, doctor=doc, reason=reason,
                                      short_reason=s_reason)
                    app.save()
            else:
                form = AppointmentFormDoctor(instance=app_instance, initial=initdata)

            return render(request, 'appointments/edit_appointment.html', {'form': form, 'usertype': 'Doctor'})


        elif isNurse:

            nurse = Nurse.objects.filter(profile__user_id=request.user.id)

            initdata = {'patient': app_instance.patient, "doctor": app_instance.doctor, "date": app_instance.date,
                        'time': app_instance.time, 'reason': app_instance.reason,
                        'short_reason': app_instance.short_reason}

            form = AppointmentFormNurse(request.POST, instance=app_instance, initial=initdata)

            if request.POST:
                pk = Appointment.objects.filter(id=appointment_id)[0].id
                date = Appointment.objects.filter(id=appointment_id)[0].date
                time = Appointment.objects.filter(id=appointment_id)[0].time
                pat = Appointment.objects.filter(id=appointment_id)[0].patient
                doc = Appointment.objects.filter(id=appointment_id)[0].doctor
                reason = Appointment.objects.filter(id=appointment_id)[0].reason
                s_reason = Appointment.objects.filter(id=appointment_id)[0].short_reason

                Appointment.objects.filter(id=appointment_id)[0].delete()

                if form.is_valid():
                    form.save()
                    log = Log(username=nurse[0].profile.user.username, action=" edited an appointment ")
                    log.save()
                    return redirect('/')
                else:
                    app = Appointment(id=pk, patient=pat, date=date, time=time, doctor=doc, reason=reason,
                                      short_reason=s_reason)
                    app.save()

            else:

                form = AppointmentFormNurse(instance=app_instance, initial=initdata)

            return render(request, 'appointments/edit_appointment.html', {'form': form, 'usertype': 'Nurse'})

    else:
        return redirect('/login')


def delete_appointment(request, appointment_id):
    Appointment.objects.filter(id=appointment_id).delete()
    return redirect('/')


def calendar(request):
    """
    generates the calendar view
    """
    if request.user.is_authenticated():

        appointments = {}

        user_id = request.user.id

        userType = ''

        isPatient = (Patient.objects.filter(profile__user_id=user_id).count() == 1)
        isDoctor = (Doctor.objects.filter(profile__user_id=user_id).count() == 1)
        isNurse = (Nurse.objects.filter(profile__user_id=user_id).count() == 1)


        if isPatient:

            # get the patient instance
            pat = Patient.objects.filter(profile__user_id=request.user.id)[0]

            appointments = Appointment.objects.filter(patient=pat)

            userType = "Patient"


        if isDoctor:

            # get the patient instance
            doc = Doctor.objects.filter(profile__user_id=request.user.id)[0]

            appointments = Appointment.objects.filter(doctor=doc)

            userType = "Doctor"


        if isNurse:
            nurse = Nurse.objects.filter(profile__user_id=request.user.id)[0]
            appointments = Appointment.objects.filter(hospital=nurse.profile.hospital_assignment)

            userType = "Nurse"


        #print(appointments)

        #for appointment in appointments:
           # print(appointment.datetimeToString())

        return render(request, 'appointments/calendar.html', {'appts': appointments,'usertype':userType})

#-------------------------------------------------------------------------------------------------------
def new_appointment_w_date(request, date_id):
    """
     This view manages the creation of a new appointment
     """

    if request.user.is_authenticated():

        title = "Create Appointment"

        user_id = request.user.id

        # used to check which type of user is creating a new appointment

        isPatient = (Patient.objects.filter(profile__user_id=user_id).count() == 1)
        isDoctor = (Doctor.objects.filter(profile__user_id=user_id).count() == 1)
        isNurse = (Nurse.objects.filter(profile__user_id=user_id).count() == 1)

        year =  date_id[0:4]
        month = date_id[4:6]
        day = date_id[6:8]
        date_string = year + "-" + month + "-" + day


        userType = ""

        if isPatient:
            userType = "Patient"

            #initialize the from the the passed in date
            initdata = {"date": date_string}

            # create a new form
            form = AppointmentForm(request.POST or None, initial=initdata)



            # if the form is completed, log the action and save the new appointment
            if form.is_valid():
                appointment = form.save(commit=False)
                appointment.patient = Patient.objects.get(profile__user_id=request.user.id)
                #appointment.date = date_string
                appointment.save()

                log = Log(username=appointment.patient.profile.user.username, action=" created a new appointment ")
                log.save()





                return redirect('/calendar')

        elif isDoctor:

            userType = "Doctor"

            # initialize the from the the passed in date
            initdata = {"date": date_string}

            # create a new form

            form = AppointmentForm(request.POST or None, initial=initdata)
            if form.is_valid():
                appointment = form.save(commit=False)
                appointment.doctor = Doctor.objects.get(profile__user_id=request.user.id)
                #appointment.date = date_string
                appointment.save()

                log = Log(username=appointment.doctor.profile.user.username, action=" created a new appointment ")
                log.save()

                return redirect('/calendar')

        elif isNurse:

            userType = "Nurse"

            nurse = (Nurse.objects.filter(profile__user_id=user_id))[0]

            # initialize the from the the passed in date
            initdata = {"date": date_string}

            # create a new form
            form = AppointmentForm(request.POST or None, initial=initdata)
            if form.is_valid():
                appointment = form.save(commit=False)
                #appointment.date = date_string
                appointment.save()

                log = Log(username=nurse.profile.user.username, action=" created a new appointment ")
                log.save()

                return redirect('/calendar')

        context = {
            "form": form,
            "title": title,
            "usertype": userType
        }
        return render(request, "appointments/create_appointment.html", context)

    else:
        return redirect('/login')
#-------------------------------------------------------------------------------------------------------