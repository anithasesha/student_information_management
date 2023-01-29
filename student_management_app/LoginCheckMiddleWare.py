from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import render, redirect
from django.urls import reverse


class LoginCheckMiddleWare(MiddlewareMixin):
    
    def process_view(self, request, view_func, view_args, view_kwargs):
        modulename = view_func.__module__
        viewname = view_func.__name__
        # print(modulename)
        user = request.user
        default_student_views=['add_student', 'add_student_save', 'logout_user', 'serve']
        student_views=['view_student','edit_student', 'edit_student_save', 'profile', 'profile_update', 'logout_user', 'serve']

        #Check whether the user is logged in or not
        if user.is_authenticated:
            if user.username == "student":
                if viewname in default_student_views:
                    pass
                else:
                    return redirect("add_student")
            
            elif user.is_superuser == False:
                if viewname in student_views:
                    pass
                else:
                    return redirect("view_student", user.username)

            else:
                pass

        else:
            if request.path == reverse("login") or request.path == reverse("doLogin"):
                pass
            else:
                return redirect("login")
