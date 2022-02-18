from django.shortcuts import render

# Create your views here.
def mainSite(request):
    return render(request, "index.html")
