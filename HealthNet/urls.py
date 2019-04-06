from django.conf.urls import include, url
from django.contrib import admin
import login.views
import appointments.views
import account.views
import administration.views
import messenger.views
import meditems.views
from django.views.generic import RedirectView
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^profile/', include('account.urls')),

    url(r'^login/', login.views.login_view, name="login"),
    url(r'^logout/',login.views.logout_view, name="logout"),
    url(r'^register/', login.views.register_view, name="register"),
    url(r'^newapp/(?P<date_id>[0-9]+)$', appointments.views.new_appointment_w_date, name="newappwd" ),
    url(r'^newapp/', appointments.views.new_appointment, name="newapp" ),
    url(r'^calendar/', appointments.views.calendar, name="calendar"),
    url(r'^patientedit/',account.views.view_patients, name="patientedit"),
    url(r'^edit_pat/(?P<patient_id>[0-9]+)$', account.views.edit_patient, name='edit_pat'),
    url(r'^edit_app/(?P<appointment_id>[0-9]+)$', appointments.views.edit_appointment, name='edit_app'),
    url(r'^edit_app/delete/(?P<appointment_id>[0-9]+)$', appointments.views.delete_appointment, name='delete_app'),
    url(r'^ad/', administration.views.landing, name="adminland" ),
    url(r'^newnurse/', administration.views.register_new_nurse, name="newnurse" ),
    url(r'^newdoctor/', administration.views.register_new_doctor, name="newdoctor" ),
    url(r'^newhospital/', administration.views.register_new_hospital, name="newhospital"),
    url(r'^messenger/', messenger.views.view_messages, name="viewmessages" ),
    url(r'^newthread/', messenger.views.new_thread, name="newthread"),
    url(r'^viewthread/(?P<thread_id>[0-9]+)$', messenger.views.view_thread, name="viewthread"),
    url(r'^viewnotes/(?P<patient_id>[0-9]+)$', meditems.views.view_notes, name="viewnotes"),
    url(r'^deletethread/(?P<thread_id>[0-9]+)$', messenger.views.delete_thread, name="deletethread"),
    url(r'^viewtests/',meditems.views.view_tests, name="viewtests"),
    url(r'^newtest/', meditems.views.new_test, name="newtest"),
    url(r'^switch_posted/(?P<test_id>[0-9]+)$', meditems.views.switch_posted, name="switchposted"),
    url(r'^toggle_admittance/(?P<patient_id>[0-9]+)$', account.views.toggle_admittance, name="toggleadmittance"),
    url(r'^delete_test/(?P<test_id>[0-9]+)$', meditems.views.delete_test, name="deletetest"),
    url(r'^edit_test/(?P<test_id>[0-9]+)$', meditems.views.edit_test, name="edittest"),
    url(r'^newprescription/', meditems.views.new_prescription, name="newprescription"),
    url(r'^viewprescriptions/',meditems.views.view_prescriptions, name="viewprescriptions"),
    url(r'^delete_prescription/(?P<prescription_id>[0-9]+)$', meditems.views.delete_prescription, name="deleteprescription"),
    url(r'^edit_prescription/(?P<prescription_id>[0-9]+)$', meditems.views.edit_prescription, name="editprescription"),
    url(r'^transfer_patient/(?P<patient_id>[0-9]+)/(?P<hospital_id>[0-9]+)$', account.views.transfer_patient, name="transferpatient"),
    url(r'^$',RedirectView.as_view(url='/login'), name="accountview"),


]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
