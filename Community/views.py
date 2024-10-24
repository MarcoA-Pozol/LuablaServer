from django.shortcuts import render, HttpResponse

def community_home(request):
    return HttpResponse("Welcome to Community")