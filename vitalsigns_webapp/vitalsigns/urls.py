from . import views
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("", views.index, name="vitalsigns_index"),
    path("register", views.register, name="vitalsigns_register"),
    path("useradmin", views.useradmin, name="vitalsigns_useradmin"),
    path("logout", views.logout, name="vitalsigns_logout"),
    path("uservitals", views.uservitals, name="vitalsigns_uservitals"),
    path("usersymptoms", views.usersymptoms, name="vitalsigns_usersymptoms"),
    path("useradmin/uservitals/<str:uid>",
         views.useradmin_uservitals,
         name="vitalsigns_useradmin_uservitals"),
    path("useradmin/usersymptoms/<str:uid>",
         views.useradmin_usersymptoms,
         name="vitalsigns_useradmin_usersymptoms"),
    path("userprofile", views.userprofile, name="vitalsigns_userprofile"),
    path("forgotpass", views.forgotpass, name="vitalsigns_forgotpass"),

    path("useradmin/uservitals/<str:uid>/clear",
         views.useradmin_uservitals_clear,
         name="vitalsigns_useradmin_usersymptoms"),


]
