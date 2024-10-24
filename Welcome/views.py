from django.shortcuts import render, redirect

def welcome(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

def languages_selection(request):
    return render(request, 'languages_selection.html')