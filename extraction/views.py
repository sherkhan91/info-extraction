from django.shortcuts import render
from django.http import HttpResponse
from . models import Publication
from . import diffbot_extraction, schedule_trigger
from rest_framework.decorators import api_view
from django.contrib import admin
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.authtoken.views import obtain_auth_token
import schedule
# Create your views here.

def index(request):
    publications = Publication.objects.all()
    return render(request,'view_info.html',{'publications':publications})
    return  HttpResponse("Welcome! to x-cago.")

@api_view(['GET'])
def extract_info(request):
    schedule_trigger.start_scheduler()
    # schedule.every().hour.do(diffbot_extraction.getinformation)
    # schedule.every(5).minutes.do(diffbot_extraction.getinformation)
    
    return HttpResponse('Information extraction job has been called.')

