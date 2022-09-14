from typing import Any, Optional
import pandas as pd
import csv
from ast import keyword
from contextlib import nullcontext
from re import T
from urllib import request, response
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpRequest
from django.urls import reverse
from itp.models import Publication, Tag, UserProfile, Event, Conference
from itp.forms import ConferenceForm, EventForm, PublicationForm, TagForm, UserForm, UserProfileForm
from django.template import loader
from django.utils.text import slugify
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.models import User
from django.db.models import Q, Count
from django.views.decorators.csrf import csrf_exempt
from django.views import View
from itp.forms import DataForm
from itp.utils import read_file_by_file_extension, show_wordcloud



def index(request):	
	response = render(request, 'itp/index.html', {})
	return response

def about(request):
	return render(request, 'itp/about.html', {})

def sign_up(request):
    registered = False

    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user

            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture'] 

            profile.save()
            registered = True
        else:
            print(user_form.errors, profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()
    
    return render(request, 'itp/sign_up.html', context={'user_form': user_form, 'profile_form': profile_form, 'registered': registered})

def user_login(request):
	if request.method =='POST':
		username = request.POST.get('username')
		password = request.POST.get('password')

		user = authenticate(username=username, password=password)

		if user:
			if user.is_active:
				login(request, user)
				return redirect(reverse('itp:index'))
			else:
				return HttpResponse("Your account is disabled.")

		else:
			print(f"Invalid login details: {username}, {password}")
			return HttpResponse("Invalid login details supplied.")
	else:
		return render(request, 'itp/login.html')

 
@login_required
def user_logout(request):
    logout(request)
    return redirect(reverse('itp:index'))

def publication(request):
	context_dict = {}

	try:
		publication = Publication.objects.all()
		context_dict['publication'] = publication
	except Publication.DoesNotExist:
		context_dict['publication'] = None
	
	return render(request, 'itp/publications.html', context=context_dict)



@login_required
def add_publication(request):
	context_dict={}
	if request.method == 'POST':
		publication_form = PublicationForm(request.POST)

		if publication_form.is_valid():
			publication_form.save(commit=False)
			publication_form.save()
			publication_form.save_m2m()
			return redirect(reverse('itp:publications'))

		else:
			print(publication_form.errors)
	else:
		publication_form = PublicationForm()

	context_dict['publication_form'] = publication_form
	return render(request, 'itp/add_publication.html', context=context_dict)


def all_publications1(request):
	context_dict={}

	try:
		publications = Publication.objects.all()
		context_dict['publications']=publications
	except Publication.DoesNotExist:
		context_dict['publications']=None

	return render(request, 'itp/publications.html', context=context_dict)


def add_event(request):	
	if request.method == 'POST':
		event_form = EventForm(request.POST)

		if event_form.is_valid():
			event_form.save(commit=True)

			return redirect(reverse('itp:events'))

		else:
			print(event_form.errors)
	else:
		event_form = EventForm()
	
	return render(request, 'itp/add_event.html', context={'event_form': event_form})


def all_events(request):
	context_dict = {}
	try:
		events = Event.objects.all()	
		context_dict['events']=events
	except Event.DoesNotExist:
		context_dict['events'] = None

	return render(request, 'itp/events.html', context=context_dict)


def add_conference(request):
	if request.method == 'POST':
		conference_form = ConferenceForm(request.POST)

		if conference_form.is_valid():
			conference_form.save(commit=True)

			return redirect(reverse('itp:add_publication'))

		else:
			print(conference_form.errors)
	else:
		conference_form = ConferenceForm()
	
	return render(request, 'itp/add_conference.html', context={'conference_form': conference_form})

def add_tag(request):
	if request.method == 'POST':
		tag_form = TagForm(request.POST)

		if tag_form.is_valid():
			tag_form.save(commit=True)

			return redirect(reverse('itp:add_publication'))

		else:
			print(tag_form.errors)
	else:
		tag_form = TagForm()
	
	return render(request, 'itp/add_tag.html', context={'tag_form': tag_form})

@login_required
def my_archives(request):
    username = request.user.username
    user=User.objects.get(username=username)

    publications = Publication.objects.filter(author=user)
    context_dict = {}
    context_dict['publications'] = publications

    return render(request, 'itp/my_archives.html', context=context_dict)

def is_valid_q(param):
	return param != '' and param is not None

def all_publications(request):
	context_dict={}

	qs = Publication.objects.all()
	title_query = request.GET.get('title')
	author_query = request.GET.get('author')
	year_min_query = request.GET.get('year_min')
	year_max_query = request.GET.get('year_max')
	magazine_query = request.GET.get('magazine')
	conference_query = request.GET.get('conference')
	doi_query = request.GET.get('doi')
	type_query = request.GET.get('type')
	keyword_query = request.GET.get('keyword')


	if is_valid_q(title_query):
		qs = qs.filter(title__icontains=title_query)

	if is_valid_q(author_query):
		qs = qs.filter(Q(author__first_name__icontains=author_query) | Q(author__last_name__icontains=author_query))

	if is_valid_q(year_min_query):
		qs = qs.filter(year__gte=year_min_query)

	if is_valid_q(year_max_query):
		qs = qs.filter(year__lt=year_max_query)

	if is_valid_q(magazine_query):
		qs = qs.filter(magazine__icontains=magazine_query)
	
	if is_valid_q(conference_query):
		qs = qs.filter(conferenceid__name__icontains=conference_query)

	if is_valid_q(doi_query):
		qs = qs.filter(doi__icontains=doi_query)

	if is_valid_q(type_query) and type_query != 'Choose...':
		qs = qs.filter(type=type_query)

	if is_valid_q(keyword_query):
		qs = qs.filter(tag__name__icontains=keyword_query)


	context_dict['publications']=qs

	return render(request, 'itp/publications.html', context=context_dict)

@staff_member_required
def export(request):
	response = HttpResponse(content_type='text/csv')

	writer = csv.writer(response)


	# for exporting tag_id, (distinct)tag_name, tag_count
	#qs = Publication.objects.all().values('tag').annotate(total=Count('tag'))
	#writer.writerow(['id', 'name','count'])
	#for t in qs.values_list('tag', 'tag__name', 'total'):
	#	writer.writerow(t)

	# for exporting tag_name only
	
	qs = Publication.objects.all()
	writer.writerow(['id', 'name','count'])
	for t in qs.values_list('tag__name'):
		writer.writerow(t)

	response['Content-Disposition'] = 'attachment; filename=tags.csv'
	return response
