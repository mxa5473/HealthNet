from django.shortcuts import render, redirect, HttpResponseRedirect
from django.contrib.auth import authenticate, login
from account.models import Doctor, Patient, Nurse, Profile
from meditems.forms import PrescriptionForm, TestForm, MedicalNoteForm
from meditems.models import Prescription, Test, MedicalNote
from django.conf import settings
from django.core.files.storage import FileSystemStorage


def new_prescription(request):

    if request.user.is_authenticated():

        title = "Create Prescription"

        user_id = request.user.id
        isDoctor = (Doctor.objects.filter(profile__user_id=user_id).count() == 1)
        if (isDoctor):
            form = PrescriptionForm(request.POST or None)

            if form.is_valid():
                prescription = form.save(commit=False)
                prescription.doc = Doctor.objects.get(profile__user_id=request.user.id)

                prescription.save()

                return redirect('/viewprescriptions')

            context = {
                "form": form,
                "title": title,
                "usertype": "Doctor"
            }
            return render(request, "meditems/create_prescription.html", context)
        else:
            return redirect('/viewprescriptions')

    else:
        return redirect('/login')


def delete_prescription(request, prescription_id):
    Prescription.objects.filter(id=prescription_id).delete()
    return redirect('/viewprescriptions')


def new_test(request):
    if request.user.is_authenticated():

        title = "Create Test"

        user_id = request.user.id
        isDoctor = (Doctor.objects.filter(profile__user_id=user_id).count() == 1)
        if (isDoctor):
            form = TestForm(request.POST or None, request.FILES or None)

            form.doc = Doctor.objects.get(profile__user_id=request.user.id)

            if form.is_valid():
                test = form.save()
                test.doc = Doctor.objects.get(profile__user_id=request.user.id)
                test.save()

                return redirect('/viewtests')

            context = {
                "form": form,
                "title": title,
                "usertype": "Doctor"
            }
            return render(request, "meditems/create_test.html", context)
        else:
            return redirect('/viewtests')
    else:
        return redirect('/login')


def view_tests(request):
    if request.user.is_authenticated:

        user_id = request.user.id
        userType = ""
        """
        sets user type for the rendered page so only content for the specific user type is displayed
        """
        isPatient = (Patient.objects.filter(profile__user_id=user_id).count() == 1)
        isDoctor = (Doctor.objects.filter(profile__user_id=user_id).count() == 1)
        isNurse = (Nurse.objects.filter(profile__user_id=user_id).count() == 1)

        tests = None

        if isPatient:
            userType = "Patient"
            tests = Test.objects.filter(patient=Patient.objects.filter(profile__user_id=user_id)[0])
        elif isDoctor:
            userType = "Doctor"
            tests = Test.objects.filter(doc=Doctor.objects.filter(profile__user_id=user_id)[0])
        elif isNurse:
            userType = "Nurse"
            nurse = Nurse.objects.filter(profile__user_id=user_id)[0]
            tests = Test.objects.filter(
                patient__profile__hospital_assignment=nurse.profile.hospital_assignment)

        user = Profile.objects.filter(user_id=user_id)[0]

        return render(request, "meditems/viewtests.html", {"usertype": userType, "tests": tests, "user": user})




def view_prescriptions(request):
    if request.user.is_authenticated:

        user_id = request.user.id
        userType = ""
        """
        sets user type for the rendered page so only content for the specific user type is displayed
        """
        isPatient = (Patient.objects.filter(profile__user_id=user_id).count() == 1)
        isDoctor = (Doctor.objects.filter(profile__user_id=user_id).count() == 1)
        isNurse = (Nurse.objects.filter(profile__user_id=user_id).count() == 1)

        prescriptions = None

        if isPatient:
            userType = "Patient"
            prescriptions = Prescription.objects.filter(patient=Patient.objects.filter(profile__user_id=user_id)[0])
        elif isDoctor:
            userType = "Doctor"
            prescriptions = Prescription.objects.filter(doc=Doctor.objects.filter(profile__user_id=user_id)[0])
        elif isNurse:
            userType = "Nurse"
            nurse = Nurse.objects.filter(profile__user_id=user_id)[0]
            prescriptions = Prescription.objects.filter(patient__profile__hospital_assignment=nurse.profile.hospital_assignment)

        user = Profile.objects.filter(user_id=user_id)[0]

        return render(request, "meditems/viewprescriptions.html", {"usertype": userType, "prescriptions": prescriptions, "user": user})


def switch_posted(request, test_id):
    test = Test.objects.filter(id=test_id)[0]

    if (test.released == True):
        test.released = False
    else:
        test.released = True

    test.save()

    return redirect('/viewtests')


def edit_test(request, test_id):
    if request.user.is_authenticated():

        title = "Edit Test"

        user_id = request.user.id

        isPatient = (Patient.objects.filter(profile__user_id=user_id).count() == 1)
        isDoctor = (Doctor.objects.filter(profile__user_id=user_id).count() == 1)
        isNurse = (Nurse.objects.filter(profile__user_id=user_id).count() == 1)

        test_instance = Test.objects.get(id=test_id)

        if isDoctor:

            doc = Doctor.objects.filter(profile__user_id=request.user.id)[0]

            initdata = {'patient': test_instance.patient, "name": test_instance.name,
                        'comments': test_instance.comments,
                        'doc': test_instance.doc, 'released': test_instance.released}

            form = TestForm(request.POST, request.FILES or None, instance=test_instance, initial=initdata)

            if request.POST:
                if form.is_valid():
                    form.save()
                    return redirect('/viewtests')

            else:
                form = TestForm(instance=test_instance, initial=initdata)

            return render(request, 'meditems/edit_test.html', {'form': form, 'usertype': 'Doctor'})

    else:
        return redirect('/login')



def edit_prescription(request, prescription_id):
    if request.user.is_authenticated():

        title = "Edit Prescription"

        user_id = request.user.id

        isPatient = (Patient.objects.filter(profile__user_id=user_id).count() == 1)
        isDoctor = (Doctor.objects.filter(profile__user_id=user_id).count() == 1)
        isNurse = (Nurse.objects.filter(profile__user_id=user_id).count() == 1)

        prescription_instance = Prescription.objects.get(id=prescription_id)

        if isDoctor:

            doc = Doctor.objects.filter(profile__user_id=request.user.id)[0]

            initdata = {'patient': prescription_instance.patient, "name": prescription_instance.name,
                        'dosage': prescription_instance.dosage,
                        'refills': prescription_instance.refills, 'doc': prescription_instance.doc}

            form = PrescriptionForm(request.POST, instance=prescription_instance, initial=initdata)

            if request.POST:
                if form.is_valid():
                    form.save()
                    return redirect('/viewprescriptions')

            else:
                form = PrescriptionForm(instance=prescription_instance, initial=initdata)

            return render(request, 'meditems/edit_prescription.html', {'form': form, 'usertype': 'Doctor'})

    else:
        return redirect('/login')


def delete_test(request, test_id):
    Test.objects.filter(id=test_id).delete()
    return redirect('/viewtests')

def view_notes(request, patient_id):
    if request.user.is_authenticated:

        user_id = request.user.id
        userType = ""
        """
        sets user type for the rendered page so only content for the specific user type is displayed
        """
        isPatient = (Patient.objects.filter(profile__user_id=user_id).count() == 1)
        isDoctor = (Doctor.objects.filter(profile__user_id=user_id).count() == 1)
        isNurse = (Nurse.objects.filter(profile__user_id=user_id).count() == 1)

        if isPatient:
            userType = "Patient"
        elif isDoctor:
            userType = "Doctor"
        elif isNurse:
            userType = "Nurse"

        user = Profile.objects.filter(user_id=user_id)[0]
        notes = MedicalNote.objects.filter(patient=patient_id)

         # new note form stuff
        # note new form
        form = MedicalNoteForm(request.POST or None)

        # if the form is completed, log the action and save the new message
        if form.is_valid():
            note = form.save(commit=False)
            note.doctor = Doctor.objects.filter(profile__user_id=user_id)[0]
            note.patient = Patient.objects.filter(id=patient_id)[0]
            note.save()

            return HttpResponseRedirect("/viewnotes/%s" % patient_id,{"usertype":userType, "notes":notes, "user":user, "form":form})

        #print(userType)
        return render(request, "meditems/viewnotes.html", {"usertype":userType, "notes":notes, "user":user, "form":form})






