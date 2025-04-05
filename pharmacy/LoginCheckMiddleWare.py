from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import admin
import datetime


from django.core.cache import cache
from django.conf import settings


#Check whether the user is logged in or not

class LoginCheckMiddleWare(MiddlewareMixin):
    # Define a mapping for user types and their corresponding view modules and redirection views
    USER_TYPE_VIEWS = {
        "1": ["pharmacy.HODViews"],
        "2": ["pharmacy.pharmacistViews", "pharmacist_home"],
        "3": ["pharmacy.DoctorViews", "doctor_home"],
        "4": ["pharmacy.clerkViews", "clerk_home"],
        "5": ["pharmacy.patient_view", "patient_home"],
    }

    def process_view(self, request, view_func, view_args, view_kwargs):
        modulename = view_func.__module__
        user = request.user

        # Check if the user is authenticated
        if user.is_authenticated:
            user_type = user.user_type
            # Default allowed modules
            allowed_modules = ["pharmacy.views", "django.views.static"]

            if user_type in self.USER_TYPE_VIEWS:
                # Add allowed modules for user type
                allowed_modules.append(self.USER_TYPE_VIEWS[user_type][0])
                redirect_view = self.USER_TYPE_VIEWS[user_type][1] if len(self.USER_TYPE_VIEWS[user_type]) > 1 else None

                # Check if the current module is allowed
                if modulename not in allowed_modules and redirect_view:
                    return redirect(redirect_view)
            else:
                return redirect("login")
        elif request.path != reverse("login"):
            # If the user is not authenticated, redirect to login unless already on the login page
            return redirect("login")

        return None



     #NB: Email confirmation will not occur       
    #  or request.path == reverse("reset_password") or request.path == reverse("password_reset_done") or request.path == reverse("password_reset_complete")