from django.shortcuts import render

def DeliveryView(request):
    return render(request,"delivery/index.html")
