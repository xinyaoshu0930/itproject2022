from django.urls import path
from itp import views

app_name = 'itp'

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
#    path('sign_up/', views.sign_up, name='sign_up'),
#    path('login/', views.user_login, name='login'),
#    path('login_check',views.login_check, name='login_check'),
#    path('logout/', views.user_logout, name='logout'),
#    path('search', views.search, name='search'),
]