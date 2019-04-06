from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.template import loader
from account.forms import UserForm, PatientForm, ProfileForm, DoctorForm, NurseForm
from django.contrib.auth.models import User
from account.models import Patient
from account.models import Profile
from account.models import Doctor
from account.models import Nurse
from administration.models import Log
from meditems.models import Test, Prescription, MedicalNote
from administration.models import Hospital
from meditems.forms import MedicalNoteForm

from appointments.models import Appointment

from django.conf import settings


def index(request, message=""):
    if request.user.is_superuser:
        return redirect('/ad')

    if request.user.is_authenticated():

        # gets the user id based on the request
        user_id = request.user.id
        # gets the user instance based on the id
        user_instance = User.objects.get(id=user_id)

        isPatient = (Patient.objects.filter(profile__user_id=user_id).count() == 1)
        isDoctor = (Doctor.objects.filter(profile__user_id=user_id).count() == 1)
        isNurse = (Nurse.objects.filter(profile__user_id=user_id).count() == 1)

        if isPatient:
            # get the profile instance based on the id
            profile_instance = Profile.objects.get(user_id=user_id)

            # get the patient instance based on the id
            patient_instance = Patient.objects.get(profile__user_id=user_id)

            appointments = Appointment.objects.filter(patient=patient_instance)

            tests = Test.objects.filter(patient=patient_instance, released=True)
            prescriptions = Prescription.objects.filter(patient=patient_instance)

            return render(request, "account/userinfo.html", {"user": request.user, "profile": profile_instance,
                                                             "patient": patient_instance, "usertype": "Patient",
                                                             "appointments": appointments, "tests": tests,
                                                             "prescriptions": prescriptions,"message":message})

        elif (isDoctor):

            # get the profile instance based on the id
            profile_instance = Profile.objects.get(user_id=user_id)

            # get the doctor instance based on the id
            doctor_instance = Doctor.objects.get(profile__user_id=user_id)

            appointments = Appointment.objects.filter(doctor=doctor_instance).order_by('-date').reverse()

            return render(request, "account/userinfo.html", {"user": request.user, "profile": profile_instance,
                                                             "doctor": doctor_instance, "usertype": "Doctor",
                                                             "appointments": appointments,"message":message})

        elif (isNurse):

            # get the profile instance based on the id
            profile_instance = Profile.objects.get(user_id=user_id)

            # get the nurse instance based on the id
            nurse_instance = Nurse.objects.get(profile__user_id=user_id)

            appointments = Appointment.objects.filter(hospital=profile_instance.hospital_assignment).order_by(
                '-date').reverse()

            return render(request, "account/userinfo.html", {"user": request.user, "profile": profile_instance,
                                                             "nurse": nurse_instance, "usertype": "Nurse",
                                                             "appointments": appointments,"message":message})

    else:
        return redirect('/login')


def edit_info(request):
    if request.user.is_authenticated:
        # gets the user id based on the request
        user_id = request.user.id
        # gets the user instance based on the id
        user_instance = User.objects.get(id=user_id)

        isPatient = (Patient.objects.filter(profile__user_id=user_id).count() == 1)
        isDoctor = (Doctor.objects.filter(profile__user_id=user_id).count() == 1)
        isNurse = (Nurse.objects.filter(profile__user_id=user_id).count() == 1)

        if isPatient:

            # if there is data that exists on the user, the forms will be prefilled
            user_init_data = {'first_name': user_instance.first_name, 'last_name': user_instance.last_name,
                              'email': user_instance.email,
                              'username': user_instance.username}

            # create a new user form that is tied to the current instance and is prefilled with current data
            user_form = UserForm(instance=user_instance, initial=user_init_data)

            # get the profile instance based on the id
            profile_instance = Profile.objects.get(user_id=user_id)

            # if there is data that exists on the profile, the forms will be prefilled
            profile_init_data = {'streetAddress': profile_instance.streetAddress, 'town': profile_instance.town,
                                 'zipCode': profile_instance.zipCode, 'state': profile_instance.state,
                                 'phoneNumber': profile_instance.phoneNumber,'hospital_assignment':profile_instance.hospital_assignment}

            profile_form = ProfileForm(instance=profile_instance, initial=profile_init_data)

            # get the patient instance based on the id
            patient_instance = Patient.objects.get(profile__user_id=user_id)
            # if there is data that exists on the patient, the forms will be prefilled
            patient_init_data = {'height': patient_instance.height, 'weight': patient_instance.weight,
                                 'age': patient_instance.age, 'hospital_preferred':patient_instance.hospital_preferred}

            # create a new patient form that is tied to the current instance and is prefilled with current data



            # if the user is submitting a form, save it if it is valid
            if request.POST:
                patient_form = PatientForm(request.POST, instance=patient_instance)
                profile_form = ProfileForm(request.POST, instance=profile_instance)
                user_form = UserForm(request.POST, instance=user_instance)

                if user_form.is_valid() and patient_form.is_valid() and profile_form.is_valid():
                    user_form.save()
                    patient_form.save()
                    profile_form.save()

                    log = Log(username=patient_instance.profile.user.username, action=" made profile changes ")
                    log.save()

                    return redirect('/profile')
                else:
                    print("error")
            else:
                patient_form = PatientForm(instance=patient_instance, initial=patient_init_data)
                profile_form = ProfileForm(instance=profile_instance, initial=profile_init_data)
                user_form = UserForm(instance=user_instance, initial=user_init_data)

            appointments = Appointment.objects.filter(patient=patient_instance)

            return render(request, "account/useredit.html", {"user": request.user, "profile": profile_instance,
                                                             "patient": patient_instance, "userform": user_form,
                                                             "patientform": patient_form, "profileform": profile_form,
                                                             "usertype": "Patient", "appointments": appointments})

        elif isDoctor:

            # if there is data that exists on the user, the forms will be prefilled
            user_init_data = {'first_name': user_instance.first_name, 'last_name': user_instance.last_name,
                              'email': user_instance.email,
                              'username': user_instance.username}

            # create a new user form that is tied to the current instance and is prefilled with current data
            user_form = UserForm(instance=user_instance, initial=user_init_data)

            # get the profile instance based on the id
            profile_instance = Profile.objects.get(user_id=user_id)

            # if there is data that exists on the profile, the forms will be prefilled
            profile_init_data = {'streetAddress': profile_instance.streetAddress, 'town': profile_instance.town,
                                 'zipCode': profile_instance.zipCode, 'state': profile_instance.state,
                                 'phoneNumber': profile_instance.phoneNumber,
                                 'hospital_assignment': profile_instance.hospital_assignment}

            profile_form = ProfileForm(instance=profile_instance, initial=profile_init_data)

            # get the doctor instance based on the id
            doctor_instance = Doctor.objects.get(profile__user_id=user_id)
            # if there is data that exists on the patient, the forms will be prefilled

            doctor_init_data = {'type': doctor_instance.type}

            # create a new patient form that is tied to the current instance and is prefilled with current data
            doctor_form = DoctorForm(instance=doctor_instance, initial=doctor_init_data)

            # if the user is submitting a form, save it if it is valid
            if request.POST:
                doctor_form = DoctorForm(request.POST, instance=doctor_instance, initial=doctor_init_data)
                profile_form = ProfileForm(request.POST, instance=profile_instance, initial=profile_init_data)
                user_form = UserForm(request.POST, instance=user_instance, initial=user_init_data)

                if user_form.is_valid() and profile_form.is_valid():
                    user_form.save()
                    doctor_form.save()
                    profile_form.save()

                    log = Log(username=doctor_instance.profile.user.username, action=" made profile changes ")
                    log.save()

                    return redirect('/profile')
                else:
                    print("error")

            appointments = Appointment.objects.filter(doctor=doctor_instance).order_by('-date').reverse()

            return render(request, "account/useredit.html", {"user": request.user, "profile": profile_instance,
                                                             "doctor": doctor_instance, "userform": user_form,
                                                             "doctorform": doctor_form, "profileform": profile_form,
                                                             "usertype": "Doctor", "appointments": appointments})




        elif isNurse:

            # if there is data that exists on the user, the forms will be prefilled
            user_init_data = {'first_name': user_instance.first_name, 'last_name': user_instance.last_name,
                              'email': user_instance.email,
                              'username': user_instance.username}

            # create a new user form that is tied to the current instance and is prefilled with current data
            user_form = UserForm(instance=user_instance, initial=user_init_data)

            # get the profile instance based on the id
            profile_instance = Profile.objects.get(user_id=user_id)

            # if there is data that exists on the profile, the forms will be prefilled
            profile_init_data = {'streetAddress': profile_instance.streetAddress, 'town': profile_instance.town,
                                 'zipCode': profile_instance.zipCode, 'state': profile_instance.state,
                                 'phoneNumber': profile_instance.phoneNumber}

            profile_form = ProfileForm(instance=profile_instance, initial=profile_init_data)

            # get the nurse instance based on the id
            nurse_instance = Nurse.objects.get(profile__user_id=user_id)
            # if there is data that exists on the patient, the forms will be prefilled

            nurse_init_data = {'type': nurse_instance.type}

            # create a new nurse form that is tied to the current instance and is prefilled with current data
            nurse_form = NurseForm(instance=nurse_instance, initial=nurse_init_data)

            # if the user is submitting a form, save it if it is valid
            if request.POST:
                nurse_form = NurseForm(request.POST, instance=nurse_instance, initial=nurse_init_data)
                profile_form = ProfileForm(request.POST, instance=profile_instance, initial=profile_init_data)
                user_form = UserForm(request.POST, instance=user_instance, initial=user_init_data)

                if user_form.is_valid():
                    user_form.save()
                    nurse_form.save()
                    profile_form.save()

                    log = Log(username=nurse_instance.profile.user.username, action=" made profile changes ")
                    log.save()

                    return redirect('/profile')
                else:
                    print("error")

            appointments = Appointment.objects.filter(hospital=profile_instance.hospital_assignment).order_by(
                '-date').reverse()

            return render(request, "account/useredit.html", {"user": request.user, "profile": profile_instance,
                                                             "nurse": nurse_instance, "userform": user_form,
                                                             "nurseform": nurse_form, "profileform": profile_form,
                                                             "usertype": "Nurse", "appointments": appointments})
    else:
        return redirect('/login')


def view_patients(request, message=""):
    """
    This view is used for doctors to view patients medical information and make changes
    """

    # gets the user id based on the request
    user_id = request.user.id

    # if the user is not authorized
    isNotValid = (Patient.objects.filter(profile__user_id=user_id).count() == 1)

    if isNotValid:
        return redirect('/')
    # gets the user instance based on the id
    user_instance = User.objects.get(id=user_id)

    isDoctor = (Doctor.objects.filter(profile__user_id=user_id).count() == 1)

    if isDoctor:
        userType = "Doctor"
        patients = Patient.objects.all()
    else:
        userType = "Nurse"
        nurse_inst = Nurse.objects.filter(profile__user_id=user_id)[0]
        hospital_id = nurse_inst.profile.hospital_assignment
        #print(hospital_id)
        patients = Patient.objects.filter(profile__hospital_assignment=hospital_id)

    return render(request, "account/patientedit.html",
                  {"user": request.user, "patients": patients, "usertype": userType,"message":message})


def edit_patient(request, patient_id):
    """
    This view is used for doctors wishing to edit a patients profile
    """

    if request.user.is_authenticated():

        title = "Edit Patient"
        user_id = request.user.id
        if (Doctor.objects.filter(profile__user_id=user_id).count() == 1):
            doc = Doctor.objects.filter(profile__user_id=request.user.id)[0]
            usertype = "Doctor"
        else:
            doc = None
            usertype = "Nurse"

        pat_instance = Patient.objects.get(id=patient_id)

        initdata = {'patient': pat_instance, "height": pat_instance.height, "weight": pat_instance.weight,
                    "doctor": pat_instance.doctor, "allergies": pat_instance.allergies}

        form = PatientForm(request.POST, instance=pat_instance, initial=initdata)

        if request.POST:

            if form.is_valid():
                if (Doctor.objects.filter(profile__user_id=user_id).count() == 1):
                    log = Log(username=doc.profile.user.username, action=" edited a patient ")
                    log.save()
                form.save()

                fullname = Patient.objects.filter(id=patient_id)[0].profile.user.first_name + " " + \
                           Patient.objects.filter(id=patient_id)[0].profile.user.last_name

                return redirect('/patientedit')

        else:
            form = PatientForm(instance=pat_instance, initial=initdata)

        fullname = Patient.objects.filter(id=patient_id)[0].profile.user.first_name + " " + \
                   Patient.objects.filter(id=patient_id)[0].profile.user.last_name

        return render(request, 'account/patientmodify.html',
                      {'form': form, 'usertype': usertype, 'patname': fullname, 'patient':patient_id,
                       'doc':doc,'patinst':pat_instance})


def toggle_admittance(request, patient_id):
    patient = Patient.objects.filter(id=patient_id)[0]

    if (patient.isAdmitted == "YES"):
        patient.isAdmitted = "NO"
        log = Log(username=patient.profile.user.username, action="has been discharged")
    else:
        patient.isAdmitted = "YES"
        log = Log(username=patient.profile.user.username, action="has been admitted")

    patient.save()
    log.save()

    return redirect('/patientedit')


def transfer_patient(request, patient_id, hospital_id):
    patient = Patient.objects.filter(id=patient_id)[0]

    hospital = Hospital.objects.filter(id=hospital_id)[0]

    patient.profile.hospital_assignment = hospital

    patient.profile.save()

    msg = "Patient %s was transferred to %s hospital" % (patient, hospital)

    return view_patients(request,msg)






