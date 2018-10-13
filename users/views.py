from django.shortcuts import render

# Create your views here.
def signup(request):
    return render(request, "users/user_signup.html")

def signin(request):
    return render(request, "users/user_login.html")