# from channels.auth import login, logout
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from student_management_app.EmailBackEnd import EmailBackEnd


def loginPage(request):
    user = request.user
    if user.is_authenticated:
        return redirect("students")
    
    return render(request, 'login.html')



def doLogin(request):
    if request.method != "POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        user = EmailBackEnd.authenticate(request, username=request.POST.get('email'), password=request.POST.get('password'))
        if user != None:
            login(request, user)
            return redirect('students')
        else:
            messages.error(request, "Invalid Login Credentials!")
            #return HttpResponseRedirect("/")
            return redirect('login')



def get_user_details(request):
    if request.user != None:
        return HttpResponse("User: "+request.user.email+" User Type: "+request.user.user_type)
    else:
        return HttpResponse("Please Login First")



def logout_user(request):
    logout(request)
    return HttpResponseRedirect('/')



def profile(request):
    user = User.objects.get(id=request.user.id)

    context={
        "user": user
    }
    return render(request, 'profile.html', context)


def profile_update(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method!")
        return redirect('profile')
    else:
        password = request.POST.get('password')

        try:
            customuser = User.objects.get(id=request.user.id)
            if request.user.is_superuser == True:
                customuser.email = request.POST.get('email')
                customuser.first_name = request.POST.get('first_name')
                customuser.last_name = request.POST.get('last_name')
            if password != None and password != "":
                customuser.set_password(password)
            customuser.save()
            messages.success(request, "Profile Updated Successfully")
            return redirect('profile')
        except:
            messages.error(request, "Failed to Update Profile")
            return redirect('profile')
    

