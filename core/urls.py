from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('login/', auth_views.LoginView.as_view(template_name='core/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path('register/', views.register, name='register'),
    path('dodaj-tepih/', views.dodaj_tepih, name='dodaj-tepih'),
    path('moji-tepisi/', views.moji_tepisi, name='moji-tepisi'),
    path('tepih/<int:tepih_id>/', views.detalji_tepih, name='detalji-tepih'),
    path('tepih/<int:tepih_id>/ukloni/', views.ukloni_tepih, name='ukloni-tepih'),
    path('zakazivanje/', views.zakazi_tepih_view, name='zakazivanje'),
    path('moji-termini/', views.moja_zakazivanja, name='moji-termini'),
    path('ajax/dodaj-tepih/', views.ajax_dodaj_tepih, name='ajax-dodaj-tepih'),
    path('zakazivanje/<int:zakazivanje_id>/otkazi/', views.otkazi_zakazivanje, name='otkazi-zakazivanje'),




]
