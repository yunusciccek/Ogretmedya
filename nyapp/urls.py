from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.anasayfa, name='anasayfa'),
    path('giris/', views.giris, name='giris'),
    path('kayit/', views.register, name='register'),
    path('cikis/', views.cikis_yap, name='cikis'),
    path('egitim_ekle/', views.egitim_ekle, name='egitim_ekle'),
    path('hesap/', views.hesap, name='hesap'),
    path('egitimler/', views.egitimler, name='egitimler'),
    path('egitimler/<slug:slug>/', views.egitim_detay, name='egitim_detay'),
    path('kullanici/<str:kullanici_adi>/', views.kullanici_bilgileri, name='kullanici_bilgileri'),
    path('hesap/egitim_duzenle/<slug:slug>/', views.egitim_duzenle, name='egitim_duzenle'),
    path('egitim/sil/<int:egitim_id>/', views.egitim_sil, name='egitim_sil'),
]



