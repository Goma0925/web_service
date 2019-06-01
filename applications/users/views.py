#Django libs
from django.shortcuts import render, redirect
from django.contrib import auth
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.contrib.auth.decorators import login_required
import pytz #time zone lib. Might not be needed?
#Django modules
from applications.users import forms
from applications.users.models import User
from applications.events.models import Event
#Additional Django libs



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
    if request.method == 'POST':
        profile_form = forms.ProfileForm(request.POST)
        if profile_form.is_valid():
            user = request.user
            user.profile.first_name = profile_form.cleaned_data["first_name"]
            user.profile.last_name = profile_form.cleaned_data["last_name"]
            user.profile.middle_name = profile_form.cleaned_data["middle_name"]
            user.profile.birthday = profile_form.cleaned_data["birthday"]
            user.profile.where_you_live = profile_form.cleaned_data["where_you_live"]
            user.profile.introduction = profile_form.cleaned_data["introduction"]
            user.save()
            user.profile.save()
            return redirect(reverse("users:retrieve_profile"))
        else:
            print(profile_form.errors)
            print(profile_image_form.errors)
            print("Failed")

    profile = request.user.profile
    #Fill in the profile_form with the current profile data
    profile_form = forms.ProfileForm(
        initial= {
            "first_name": profile.first_name,
            "last_name": profile.last_name,
            "middle_name": profile.middle_name,
            "birthday": profile.birthday,
            "where_you_live": profile.where_you_live,
            "introduction": profile.introduction,
        }
    )

    user_birthday = str(profile.birthday).split("-")
    context = {"profile_form": profile_form, "profile":profile, "birthday_year": user_birthday[0],
               "birthday_month": user_birthday[1], "birthday_day": user_birthday[2],}
    return render(request, "users/edit_profile.html", context=context)

def retrieve_profile(request):
    profile = request.user.profile
    context = {"profile": profile}
    return render(request, "users/my_profile.html", context=context)

def edit_my_images(request):
    if request.method == 'POST':
        profile_image_form = forms.ProfileImageForm(request.POST, request.FILES)

        #test
        #from pprint import pprint
        print(vars(profile_image_form))
        if profile_image_form.is_valid():
            user = request.user
            user.profile.profile_image_storage_url = profile_image_form.save_image_of(user)
            #print("user.profile.profile_image_storage_url: ", user.profile.profile_image_storage_url)
            user.profile.save()
            #print("image saved")
        else:
            print(profile_image_form.errors)

    profile_image_form = forms.ProfileImageForm()
    profile_image_storage_url = request.user.profile.profile_image_storage_url
    #print("profile_image_storage_url: ", profile_image_storage_url)
    context = {"profile_image_form": profile_image_form, "profile_image_storage_url": profile_image_storage_url}
    return render(request, "users/edit_images.html", context=context)
