from django.shortcuts import render, redirect


def dashboard(request):
    return render(request,'dashboard.html')

def keshav(request):
    return render(request,'test/keshav.html')

def success(request):
    return render(request,'sucess.html')