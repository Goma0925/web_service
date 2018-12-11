from django.shortcuts import render
from django.contrib import auth
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required

# Create your views here.
def signup(request):

    return render(request, "users/user_signup.html", {})

def login(request, **kwargs):
    redirect_to = request.GET.get('next', "events:retrieve_eventboard")
    if request.method == 'POST':
        # First get the username and password supplied
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Django's built-in authentication function:
        user = auth.authenticate(email=email, password=password)
        # If we have a user
        if user:
            # Check if the account is active
            if user.is_active:
                # Log in the user.
                auth.login(request, user)
                # Send the user back to some page.
                #print("Login success")
                return HttpResponseRedirect(reverse(redirect_to))
            else:
                # If account is not active:
                return HttpResponseRedirect(reverse("users:login"))
        else:
            #print("Someone tried to login and failed.")
            #print("They used email: {} and password: {}".format(email, password))
            return HttpResponseRedirect(reverse("users:login"))
    else:
        # Nothing has been provided for username or password.
        return render(request, "users/user_login.html")


def logout(request):
    auth.logout(request)