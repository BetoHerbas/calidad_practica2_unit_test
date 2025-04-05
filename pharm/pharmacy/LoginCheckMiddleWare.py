from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import admin
import datetime


from django.core.cache import cache
from django.conf import settings


#Check whether the user is logged in or not

class LoginCheckMiddleWare(MiddlewareMixin):
   
    
    USER_VIEWS = {
        "1": "pharmacy.HODViews",
        "2": "pharmacy.pharmacistViews",
        "3": "pharmacy.DoctorViews",
        "4": "pharmacy.clerkViews",
        "5": "pharmacy.patient_view",
    }

    REDIRECTS = {
        "2": "pharmacist_home",
        "3": "doctor_home",
        "4": "clerk_home",
        "5": "patient_home",
    }

    ALLOWED_MODULES = {"pharmacy.views", "django.views.static", ""}

    def process_view(self, request, view_func, view_args, view_kwargs):
        user = request.user
        modulename = view_func.__module__

        if not user.is_authenticated:
            return None if request.path == reverse("login") else redirect("login")

        user_type = user.user_type
        if user_type in self.USER_VIEWS:
            if modulename in (self.USER_VIEWS[user_type], *self.ALLOWED_MODULES):
                return None
            return redirect(self.REDIRECTS.get(user_type, "login"))

        return redirect("login")


     #NB: Email confirmation will not occur       
    #  or request.path == reverse("reset_password") or request.path == reverse("password_reset_done") or request.path == reverse("password_reset_complete")