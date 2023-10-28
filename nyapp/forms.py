from django import forms
from django.contrib.auth.models import User
from .models import CustomUser
from .models import Egitim

from django import forms
from .models import Egitim

class EgitimYayinla(forms.ModelForm):
    egitmen = forms.CharField(max_length=100, required=False)  # egitmen alanını burada tanımlayın

    class Meta:
        model = Egitim
        fields = ['baslik', 'egitim_icerigi', 'sure', 'fiyat', 'profile_picture']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(EgitimYayinla, self).__init__(*args, **kwargs)
        if user:
            self.fields['egitmen'].initial = user.username
            self.fields['egitmen'].widget.attrs['readonly'] = True



class RegistrationForm(forms.ModelForm):
    password1 = forms.CharField(widget=forms.PasswordInput, label='Şifre')
    password2 = forms.CharField(widget=forms.PasswordInput, label='Şifre (Tekrar)')

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2','profile_picture','first_name','last_name']

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if CustomUser.objects.filter(username=username).exists():
            raise forms.ValidationError("Bu kullanıcı adı zaten kullanılıyor.")
        return username

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Şifreler eşleşmiyor.")
        return password2

