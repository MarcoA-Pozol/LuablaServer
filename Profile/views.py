from django.shortcuts import render, HttpResponse

def profile_home(request):
    return HttpResponse("Welcome to profile")