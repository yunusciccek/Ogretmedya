from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django import forms
from django.utils.text import slugify

class CustomUser(AbstractUser):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    user_profile = models.OneToOneField('UserProfile', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.username

class Icerik(models.Model):
    baslik = models.CharField(max_length=200)
    metin = models.TextField()
    resim = models.ImageField(upload_to='icerik_resimler/')

    def __str__(self):
        return self.baslik

class Egitim(models.Model):
    slug = models.SlugField(unique=True, blank=True, null=True)
    baslik = models.CharField(max_length=100)
    egitim_icerigi = models.TextField()
    egitmen = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    sure = models.PositiveIntegerField(help_text="Lütfen süreyi dakika cinsinden giriniz.")
    fiyat = models.DecimalField(max_digits=10, decimal_places=2)
    profile_picture = models.ImageField(upload_to='profile_pictures/')
    egitim_sahibi = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='egitimleri', null=True, blank=True)
    
    def save(self, *args, **kwargs):
        # Eğitim başlığından slug oluşturun
        if not self.slug:
            self.slug = slugify(self.baslik)
        super(Egitim, self).save(*args, **kwargs)

    def get_absolute_url(self):
        # Eğitim nesnesinin URL'sini oluşturun
        return f'/egitimler/{self.slug}/'

    def __str__(self):
        return self.baslik
        
    class Meta:
        unique_together = ('baslik', 'slug')
    

class UserProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)

    def __str__(self):
        return self.user.username
