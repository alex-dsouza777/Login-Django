from django.shortcuts import render, HttpResponseRedirect
from . forms import SignupForm
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash


def sign_up(request):
    if request.method == 'POST':
        fm = SignupForm(request.POST)
        if(fm.is_valid()):
            fm.save()
            messages.success(request,"Account Created Successfully")
    else:
         fm = SignupForm()
    return render(request,"loginapp/signup.html",{"form":fm})


#login
def user_login(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            fm = AuthenticationForm(request,request.POST)
            if fm.is_valid():
                uname = fm.cleaned_data['username']
                upass = fm.cleaned_data['password']
                user = authenticate(username = uname, password = upass)
                if user is not None:
                    login(request,user)
                    messages.success(request,"Logged Successfully")
                    return HttpResponseRedirect('/profile/')

        else:
            fm = AuthenticationForm()
        return render(request,"loginapp/userlogin.html",{"form":fm})
    else:
        return HttpResponseRedirect("/profile/")


#profile view
def user_profile(request):
    if request.user.is_authenticated:
        return render(request,"loginapp/profile.html",{'name':request.user})
    else:
        return HttpResponseRedirect('/login/')


#logout
def user_logout(request):
    logout(request)
    return HttpResponseRedirect("/login/")

#change password
def user_change_pass(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            fm = PasswordChangeForm(user=request.user,data=request.POST)
            if fm.is_valid():
                fm.save()
                update_session_auth_hash(request,fm.user)
                messages.success(request,"Password Changed Succesfully")
                return HttpResponseRedirect("/profile/")
        else:
            fm = PasswordChangeForm(user=request.user)
        return render(request,"loginapp/changepass.html",{'form':fm})
    else:
        return HttpResponseRedirect("/login/")


