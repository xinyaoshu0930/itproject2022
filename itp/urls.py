from django.urls import path
from itp import views

app_name = 'itp'

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('sign_up/', views.sign_up, name='sign_up'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('publications/', views.all_publications, name='publications'),
    path('add_publication/', views.add_publication, name='add_publication'),
    path('events/', views.all_events, name='events'),
    path('add_event/', views.add_event, name='add_event'),
    path('add_publication/add_conference/', views.add_conference, name='add_conference'),
    path('add_publication/add_tag/', views.add_tag, name='add_tag'),
    path('my_archives.html', views.my_archives, name='my_archives')
]