from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.urls import reverse
from django.contrib.staticfiles.storage import staticfiles_storage
import os
# Create your views here.

import pyrebase
from firebase_admin import credentials
import firebase_admin

adminDoctorKey = "j7FEbdLjTsWUtGomO5WkyCYED5t1"

config = {
    "apiKey": "AIzaSyDGD8ewVOBVxl6O1r35Npy2RRw2dlWGdP8",
    "authDomain": "mapuavitalsignsdatabase.firebaseapp.com",
    "databaseURL": "https://mapuavitalsignsdatabase.firebaseio.com",
    "projectId": "mapuavitalsignsdatabase",
    "storageBucket": "mapuavitalsignsdatabase.appspot.com",
    "messagingSenderId": "582213066054",
    "appId": "1:582213066054:web:ab72ca16bf4849166bd947",
    "measurementId": "G-G5FC6W67QF",
    "serviceAccount": str(os.getcwd())+"/vitalsigns/static/vitalsigns/mapuavitalsignsdatabase-firebase-adminsdk-uphv7-0cff4fb849.json"

}

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db = firebase.database()


def index(request):

    try:

        if request.POST.get("login_button"):
            email = request.POST.get("email")
            password = request.POST.get("password")

            user = auth.sign_in_with_email_and_password(email, password)
            auth.refresh(user['refreshToken'])

            sessionID = user['idToken']

            request.session["firebaseLocalId"] = user["localId"]

            print("login uid")
            print(request.session["firebaseLocalId"])

            request.session["uid"] = str(sessionID)

            print("Session created.")

            if db.child("users").child(user["localId"]).child("userinfo").get().val()["isAdmin"]:
                print("Admin Login")
                return HttpResponseRedirect(reverse('vitalsigns_useradmin'))

            else:
                print("Patient Login")

                return HttpResponseRedirect(reverse('vitalsigns_uservitals'))

        elif request.POST.get("register_button"):
            return render(request, "vitalsigns/index.html")
    except ConnectionError:
        error_message = "Please check your internet connection."
        messages.error(request, error_message)
        return HttpResponseRedirect(reverse('vitalsigns_index'))
    except Exception as exp:
        print(str(exp))
        error_message = "Invalid email and/or password."
        messages.error(request, error_message)
        return HttpResponseRedirect(reverse('vitalsigns_index'))

    if request.session.session_key:

        if request.session["firebaseLocalId"] != adminDoctorKey:
            return HttpResponseRedirect(reverse('vitalsigns_uservitals'))
        else:
            return HttpResponseRedirect(reverse('vitalsigns_useradmin'))
    else:
        request.session["firebaseLocalId"] = ""
        request.session.flush()
        return render(request, "vitalsigns/login.html")


def register(request):

    try:

        if request.POST.get("register_button"):
            # auth.create_user_with_email_and_password("romnegrillo@gmail.com", "testing")
            email = request.POST.get("email")

            password = request.POST.get("password")
            confirm_password = request.POST.get("confirm_password")

            full_name = request.POST.get("full_name")
            age = request.POST.get("age")
            gender = request.POST.get("gender_radio")
            address = request.POST.get("address")
            assigned_doctor_number = request.POST.get("doctor_number")

            if password != confirm_password:
                error_message = "Password and confirm password does not match."
                messages.error(request, error_message)
                return HttpResponseRedirect(reverse('vitalsigns_register'))
            else:
                user_data = {
                    "isAdmin": False,
                    "full_name": full_name,
                    "age": age,
                    "gender": gender,
                    "address": address,
                    "assigned_doctor_number": assigned_doctor_number
                }

                user_symptoms = {"flu": 0,
                                 "ear_pain": 0,
                                 "abdominal_pain": 0,
                                 "excessive_sweating": 0,
                                 "arm_pain": 0,
                                 "faintness": 0,
                                 "back_pain": 0,
                                 "fatigue": 0,
                                 "body_aches": 0,
                                 "gas": 0,
                                 "breast_pain": 0,
                                 "genitcal_itching": 0,
                                 "breathing_difficulty": 0,
                                 "headache": 0,
                                 "irregular_periods": 0,
                                 "chest_pain": 0,
                                 "joint_pain": 0,
                                 "congestion": 0,
                                 "leg_pain": 0,
                                 "cough": 0,
                                 "mouth_lesions": 0,
                                 "diarrhea ": 0,
                                 "nausea": 0,
                                 "neck_pain": 0,
                                 "rush": 0,
                                 "rectal_bleeding": 0,
                                 "skin_lump": 0,
                                 "sore_throat": 0,
                                 "vomiting": 0
                                 }

                user = auth.create_user_with_email_and_password(email, password)
                email = email.replace(".", "").replace("@", "")
                db.child("users").child(user["localId"]).child("userinfo").set(user_data)
                db.child("users").child(user["localId"]).child("usersymptoms").set(user_symptoms)
                db.child("users").child(user["localId"]).child("assessment").set("None")

                error_message = "User successfully resgistered"
                messages.error(request, error_message)
                return HttpResponseRedirect(reverse('vitalsigns_register'))

            return render(request, "vitalsigns/register.html")

        elif request.POST.get("login_button"):
            return render(request, "vitalsigns/login.html")

    except ConnectionError:
        error_message = "Please check your internet connection."
        messages.error(request, error_message)
        return HttpResponseRedirect(reverse('vitalsigns_register'))
    except Exception as exp:
        print(str(exp))
        error_message = "Email is already registered."
        messages.error(request, error_message)
        return HttpResponseRedirect(reverse('vitalsigns_register'))

    if request.session.session_key:

        if request.session["firebaseLocalId"] != adminDoctorKey:
            return HttpResponseRedirect(reverse('vitalsigns_uservitals'))
        else:
            return HttpResponseRedirect(reverse('vitalsigns_useradmin'))
    else:
        return render(request, "vitalsigns/register.html")


def useradmin(request):

    if request.session.session_key:
        if request.session["firebaseLocalId"] == adminDoctorKey:
            if request.POST.get("logout"):
                request.session.flush()
                return HttpResponseRedirect(reverse('vitalsigns_index'))

            users = db.child("users").get()
            deviceCoordinates = db.child("coordinates").get().val()
            print(deviceCoordinates)

            return render(request, "vitalsigns/useradmin.html", {"userdata": users.val(), "device_coordinates": deviceCoordinates})
        else:
            return HttpResponseRedirect(reverse('vitalsigns_uservitals'))
    else:
        error_message = "You need to be logged in to view the requested page."
        messages.error(request, error_message)
        return HttpResponseRedirect(reverse('vitalsigns_index'))


def uservitals(request):

    if request.session.session_key:

        if request.session["firebaseLocalId"] != adminDoctorKey:
            print("user logged in uid")
            print(request.session["firebaseLocalId"])

            if request.POST.get("logout"):
                request.session.flush()
                return HttpResponseRedirect(reverse('vitalsigns_index'))

            users = db.child("users").child(
                request.session["firebaseLocalId"]).child("uservitalshistory").get()

            full_name = db.child("users").child(
                request.session["firebaseLocalId"]).child("userinfo").child("full_name").get().val()

            return render(request, "vitalsigns/uservitals.html", {"userdata": users.val(), "full_name": full_name, "isUser": True})

    else:
        error_message = "You need to be logged in to view the requested page."
        messages.error(request, error_message)
        return HttpResponseRedirect(reverse('vitalsigns_index'))


def usersymptoms(request):

    print("user logged in uid")
    print(request.session["firebaseLocalId"])

    if request.session.session_key:
        if request.session["firebaseLocalId"] != adminDoctorKey:
            if request.POST.get("logout"):
                request.session.flush()
                return HttpResponseRedirect(reverse('vitalsigns_index'))

            users = db.child("users").child(
                request.session["firebaseLocalId"]).child("usersymptoms").get()
            full_name = db.child("users").child(
                request.session["firebaseLocalId"]).child("userinfo").child("full_name").get().val()

            return render(request, "vitalsigns/usersymptoms.html", {"userdata": users.val(), "full_name": full_name, "isUser": True})
        else:
            return HttpResponseRedirect(reverse('vitalsigns_useradmin'))

    else:
        error_message = "You need to be logged in to view the requested page."
        messages.error(request, error_message)
        return HttpResponseRedirect(reverse('vitalsigns_index'))


def useradmin_uservitals(request, uid):
    if request.session.session_key:

        if request.session["firebaseLocalId"] == adminDoctorKey:

            if request.POST.get("logout"):
                request.session.flush()
                return HttpResponseRedirect(reverse('vitalsigns_index'))

            users = db.child("users").child(uid).child("uservitalshistory").get()

            full_name = db.child("users").child(uid).child(
                "userinfo").child("full_name").get().val()

            return render(request, "vitalsigns/uservitals.html", {"userdata": users.val(), "full_name": full_name, "uid": uid})

    else:
        error_message = "You need to be logged in to view the requested page."
        messages.error(request, error_message)
        return HttpResponseRedirect(reverse('vitalsigns_index'))


def useradmin_uservitals_clear(request, uid):
    if request.session.session_key:

        if request.session["firebaseLocalId"] == adminDoctorKey:

            if request.POST.get("logout"):
                request.session.flush()
                return HttpResponseRedirect(reverse('vitalsigns_index'))

            db.child("users").child(uid).child("uservitalshistory").remove()
            users = db.child("users").child(uid).child("uservitalshistory").get()

            full_name = db.child("users").child(uid).child(
                "userinfo").child("full_name").get().val()

            error_message = "Vital signs deleted."
            messages.error(request, error_message)

            # return render(request, "vitalsigns/uservitals.html", {"userdata": users.val(), "full_name": full_name, "uid": uid})

            return HttpResponseRedirect(reverse('vitalsigns_useradmin_uservitals', kwargs={'uid': uid}))
    else:
        error_message = "You need to be logged in to view the requested page."
        messages.error(request, error_message)
        return HttpResponseRedirect(reverse('vitalsigns_index'))


def useradmin_usersymptoms(request, uid):

    if request.session.session_key:
        if request.session["firebaseLocalId"] == adminDoctorKey:
            if request.POST.get("logout"):
                request.session.flush()
                return HttpResponseRedirect(reverse('vitalsigns_index'))

            elif request.POST.get("send_assessment_button"):
                users = db.child("users").child(uid).child("usersymptoms").get()
                full_name = db.child("users").child(uid).child(
                    "userinfo").child("full_name").get().val()

                assessment = request.POST.get("assessment_textarea")
                print(assessment)

                db.child("users").child(uid).update(
                    {"assessment": assessment})

                error_message = "Assessment sent to the user!"
                messages.error(request, error_message)

                return render(request, "vitalsigns/usersymptoms.html", {"userdata": users.val(), "full_name": full_name, "isAdmin": True})

            users = db.child("users").child(uid).child("usersymptoms").get()
            full_name = db.child("users").child(uid).child(
                "userinfo").child("full_name").get().val()

            return render(request, "vitalsigns/usersymptoms.html", {"userdata": users.val(), "full_name": full_name, "isAdmin": True})
        else:
            return HttpResponseRedirect(reverse('vitalsigns_useradmin'))

    else:
        error_message = "You need to be logged in to view the requested page."
        messages.error(request, error_message)
        return HttpResponseRedirect(reverse('vitalsigns_index'))


def userprofile(request):

    try:

        if request.POST.get("logout"):
            request.session.flush()
            return HttpResponseRedirect(reverse('vitalsigns_index'))
        if request.POST.get("update_button"):
            # auth.create_user_with_email_and_password("romnegrillo@gmail.com", "testing")

            full_name = request.POST.get("full_name")
            age = request.POST.get("age")
            gender = request.POST.get("gender_radio")
            address = request.POST.get("address")
            assigned_doctor_number = request.POST.get("doctor_number")

            user_data = {
                "isAdmin": False,
                "full_name": full_name,
                "age": age,
                "gender": gender,
                "address": address,
                "assigned_doctor_number": assigned_doctor_number
            }

            # user = auth.create_user_with_email_and_password(email, password)
            # email = email.replace(".", "").replace("@", "")
            # db.child("users").child(user["localId"]).child("userinfo").set(user_data)
            #

            print("To update")

            db.child("users").child(request.session["firebaseLocalId"]).child(
                "userinfo").update(user_data)

            error_message = "Information updated."
            messages.success(request, error_message)
            user_details = db.child("users").child(
                request.session["firebaseLocalId"]).child(
                "userinfo").get().val()
            return render(request, "vitalsigns/userprofile.html", {"user_details": user_details, "isUser": True})
        elif request.POST.get("change_password_button"):
            print("Change password button.")

            password = request.POST.get("password")
            confirm_password = request.POST.get("confirm_password")

            if (password == confirm_password):
                error_message = "Password updated."
                messages.success(request, error_message)
                user_details = db.child("users").child(
                    request.session["firebaseLocalId"]).child(
                    "userinfo").get().val()
                return render(request, "vitalsigns/userprofile.html", {"user_details": user_details, "isUser": True})
            else:
                error_message = "Password and confirm password does not match."
                messages.success(request, error_message)
                user_details = db.child("users").child(
                    request.session["firebaseLocalId"]).child(
                    "userinfo").get().val()
                return render(request, "vitalsigns/userprofile.html", {"user_details": user_details, "isUser": True})

        elif request.POST.get("login_button"):
            return render(request, "vitalsigns/login.html")

    except ConnectionError:
        error_message = "Please check your internet connection."
        messages.error(request, error_message)
        return HttpResponseRedirect(reverse('vitalsigns_register'))
    except Exception as exp:
        print(str(exp))
        error_message = "Email is already registered."
        messages.error(request, error_message)
        return HttpResponseRedirect(reverse('vitalsigns_register'))

    if request.session.session_key:

        if request.session["firebaseLocalId"] != adminDoctorKey:
            users_details = db.child("users").child(
                request.session["firebaseLocalId"]).child(
                "userinfo").get().val()

            print(users_details)
            return render(request, "vitalsigns/userprofile.html", {"user_details": users_details, "isUser": True})
        else:
            return HttpResponseRedirect(reverse('vitalsigns_useradmin'))
    else:
        error_message = "You need to be logged in to view the requested page."
        messages.error(request, error_message)
        return HttpResponseRedirect(reverse('vitalsigns_index'))


def forgotpass(request):
    if request.session.session_key:
        if request.session["firebaseLocalId"] != adminDoctorKey:
            users_details = db.child("users").child(
                request.session["firebaseLocalId"]).child(
                "userinfo").get().val()

            print(users_details)
            return render(request, "vitalsigns/userprofile.html", {"user_details": users_details, "isUser": True})
        else:
            return HttpResponseRedirect(reverse('vitalsigns_useradmin'))
    else:

        if request.POST.get("send_email_button"):

            try:
                print("Send email button clicked")

                print(request.POST.get("email"))

                auth.send_password_reset_email(request.POST.get("email"))

                error_message = "Email sent. Check your email for further instructions."
                messages.error(request, error_message)
                return render(request, "vitalsigns/forgotpass.html")

            except ConnectionError:
                error_message = "Please check your internet connection."
                messages.error(request, error_message)
                return HttpResponseRedirect(reverse('vitalsigns_forgotpass'))
            except Exception as exp:
                print(str(exp))
                error_message = "Email is not registered."
                messages.error(request, error_message)
                return HttpResponseRedirect(reverse('vitalsigns_forgotpass'))

        return render(request, "vitalsigns/forgotpass.html")


def logout(request):

    request.session.flush()

    return HttpResponseRedirect(reverse('vitalsigns_index'))
