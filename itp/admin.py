from multiprocessing import Event
from django.contrib import admin
from django.db import models
from django.contrib.auth.models import User
from itp.models import Conference, Publication, Tag, UserProfile, Event


admin.site.register(Publication)
admin.site.register(UserProfile)
admin.site.register(Event)
admin.site.register(Conference)
admin.site.register(Tag)