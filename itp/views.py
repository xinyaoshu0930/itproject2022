from contextlib import nullcontext
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect,  JsonResponse
from django.urls import reverse
from django.template import loader
from django.db.models import Avg
from django.utils.text import slugify
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt

#from itp.models import 
#from itp.forms import


def index(request):	
	response = render(request, 'itp/index.html', {})
	return response

def about(request):
	return render(request, 'itp/about.html', {})
