from django.shortcuts import render, redirect, HttpResponseRedirect
from messenger.forms import ThreadForm, MessageForm
from account.models import Profile, Patient, Nurse, Doctor
from messenger.models import Thread, Message
from administration.models import Log
from django.contrib.auth.models import User



def new_thread(request):
    """
    this view manages the request of a new thread
    """

    if request.user.is_authenticated():

        title = "New Thread"

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

        # create new form
        form = ThreadForm(request.POST or None)

        # if the form is completed, log the action and save the new thread
        if form.is_valid():
            thread = form.save(commit=False)
            thread.user1 = Profile.objects.get(user_id=request.user.id)
            thread.save()

            log = Log(username=thread.user1.user.username, action =" created a new thread")
            log.save()


            return redirect('/messenger')

        context = {
            "form": form,
            "title" : title,
            "usertype": userType
        }

        return render(request,"messenger/createthread.html", context)

    else:
        return redirect('/login')


def view_messages(request):

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
        threads = Thread.objects.filter(user1=user) | Thread.objects.filter(user2=user)

        print(userType)
        return render(request, "messenger/viewmessages.html", {"usertype":userType, "threads":threads, "user":user})

def view_thread(request, thread_id):

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
        thread = Thread.objects.filter(id=thread_id)[0]

        messages = Message.objects.filter(thread_id=thread_id)



        # new message form stuff
        # create new form
        form = MessageForm(request.POST or None)

        # if the form is completed, log the action and save the new message
        if form.is_valid():
            message = form.save(commit=False)
            message.author = Profile.objects.get(user_id=user_id)
            message.thread = thread
            message.save()

            log = Log(username=message.author.user.username, action=" sent a message")
            log.save()

            return HttpResponseRedirect("/viewthread/%s" % thread_id)

        print(userType)
        return render(request, "messenger/viewthread.html", {"usertype":userType, "thread":thread, "messages":messages, "user":user, "form":form})


def delete_thread(request, thread_id):
    """
    this function deletes a thread and all messages associated with it
    """
    messages = Message.objects.filter(thread_id=thread_id)

    for message in messages:
        message.delete()

    Thread.objects.filter(id=thread_id).delete()
    return redirect('/messenger')





