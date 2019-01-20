from django.shortcuts import render
from django.contrib import auth
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from applications.users import forms
from applications.users.models import User
from django.utils import timezone
import pytz #time zone lib. Might not be needed?
from applications.events.models import Event
from django.contrib.auth.decorators import login_required


def signup(request):
    registered = False
    if request.method == "POST":
        #print("POST:")
        #print(request.POST)
        account_form = forms.CustomUserCreationForm(data=request.POST)
        if account_form.is_valid():
            user = account_form.save(commit=False)
            #print("User created:", user, type(user))
            user.date_joined = timezone.now()
            user.is_staff = False
            user.is_superuser = False
            user.is_active = True
            user.save()
            #print("User saved:", user, type(user))
            #user = auth.authenticate(username=user.email, password=user.password)
            #print(auth.authenticate(username=user.email, password=user.password))
            auth.login(request, user)
            registered = True
            return render(request, "users/user_signup.html", {"account_form": account_form, "registered": registered})
        else:
            return render(request, "users/user_signup.html", {"account_form": account_form, "registered": registered})
    #CSFR token update
    account_form = forms.CustomUserCreationForm()
    return render(request, "users/user_signup.html", {"account_form": account_form, "registered": registered})

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


@login_required
def retrieve_my_hangouts(request):
    join_list = request.user.hangouts_to_join
    events = list()
    for event_id in join_list:
        events += Event.objects.filter(event_id=event_id)
    context = {"events": events}
    return render(request, "users/my_hangouts.html", context=context)


@login_required
def retrieve_my_watchlist(request):
    watch_list = request.user.watch_list
    events = list()
    for event_id in watch_list:
        events += Event.objects.filter(event_id=event_id)
    context = {"events": events}
    return render(request, "users/my_watchlist.html", context=context)


@login_required
def edit_profile(request):
    profile_form = forms.ProfileForm()
    user = request.user
    print("Profile:", profile_form)
    context = {"profile_form": profile_form, "user":user}
    return render(request, "users/edit_profile.html", context=context)