from django.shortcuts import render, get_object_or_404
from .models import Icerik
from django.shortcuts import render, redirect
from django.contrib import auth
from .forms import RegistrationForm, EgitimYayinla  # EgitimYayinla formunu ekledik
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password
from .models import CustomUser, UserProfile, Egitim  # Egitim modelini ekledik
from django.http import HttpResponseRedirect


def anasayfa(request):
    return render(request, 'anasayfa.html')

@csrf_protect


@csrf_protect
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            user.set_password(form.cleaned_data['password1'])
            user.save()

            # Kullanıcı profili oluştur
            user_profile, created = UserProfile.objects.get_or_create(user=user)
            
            if 'profile_picture' in request.FILES:
                user_profile.profile_picture = request.FILES['profile_picture']
            else:
                # Kullanıcı bir resim seçmediyse veya yüklemediyse varsayılan resmi kullanın
                # 'default_profile.png' burada varsayılan resmin dosya adını ve yolunu temsil eder
                user_profile.profile_picture = 'avatar.jpg'

            user_profile.save()

            login(request, user)  # Kullanıcıyı oturum açık hale getir

            return HttpResponseRedirect('/')  # HttpResponse nesnesi döndür

    else:
        form = RegistrationForm()
        # Kullanıcı bir resim seçmediyse veya yüklemediyse varsayılan resmi ayarlayın
        default_profile_picture = 'avatar.jpg'
        return render(request, 'registration/register.html', {'form': form, 'default_profile_picture': default_profile_picture})


@csrf_protect
def giris(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('anasayfa')
        else:
            error_message = "Kullanıcı adı veya şifre hatalı."
            return render(request, 'giris.html', {'error_message': error_message})
    return render(request, 'giris.html')

def cikis_yap(request):
    logout(request)
    return redirect('giris')

def egitim_ekle(request):
    if request.method == 'POST':
        form = EgitimYayinla(request.POST, request.FILES)
        if form.is_valid():
            egitim = form.save(commit=False)
            egitim.egitmen = request.user  # request.user'ı egitmen olarak atayın
            egitim.egitim_sahibi = request.user  # request.user'ı egitim_sahibi olarak atayın
            egitim.save()
            return redirect('egitimler')
    else:
        form = EgitimYayinla(user=request.user)  # formu request.user ile başlatın
    return render(request, 'egitim_ekle.html', {'form': form})




def hesap(request):
    if request.user.is_authenticated:
        # Kullanıcı giriş yaptıysa, eğitimlerini getir
        egitimler = Egitim.objects.filter(egitim_sahibi=request.user)

        if request.method == 'POST':
            # Kullanıcı bir POST isteği gönderdiğinde, profil resmini kontrol et
            form = EgitimYayinla(request.POST, request.FILES)
            if form.is_valid():
                egitim = form.save(commit=False)
                egitim.egitmen = request.user
                egitim.egitim_sahibi = request.user
                if 'profile_picture' in request.FILES:
                    egitim.profile_picture = request.FILES['profile_picture']
                else:
                    egitim.profile_picture = 'avatar.jpg'
                egitim.save()
                return redirect('egitimler')
        else:
            form = EgitimYayinla()

        # Kullanıcı bir GET isteği gönderdiğinde, profil resmini kontrol etmeyin
        return render(request, 'hesap.html', {'form': form, 'egitimler': egitimler})
    else:
        # Kullanıcı giriş yapmamışsa, eğitimleri listeleme
        return render(request, 'hesap.html')



def egitimler(request):
    # Tüm eklenen eğitimleri listele
    egitimler = Egitim.objects.all()
    return render(request, 'egitimler.html', {'egitimler': egitimler})

def egitim_detay(request, slug):
    egitim = get_object_or_404(Egitim, slug=slug)
    return render(request, 'egitim_detay.html', {'egitim': egitim})


def kullanici_bilgileri(request, kullanici_adi):
    # Kullanıcı adına göre ilgili kullanıcıyı çekin
    try:
        kullanici = CustomUser.objects.get(username=kullanici_adi)
    except CustomUser.DoesNotExist:
        # Kullanıcı bulunamadıysa ilgili işlemi yapın veya hata mesajını gösterin
        kullanici = None

    # Kullanıcıyı kullanarak gerekli işlemleri yapın ve template'e veri gönderin
    return render(request, 'kullanici_bilgileri.html', {'kullanici': kullanici})




@login_required
def egitim_duzenle(request, slug):
    # Eğitimi getir veya 404 hatası göster
    egitim = get_object_or_404(Egitim, slug=slug)

    # Kullanıcının bu eğitimi düzenleme izni kontrol et
    if egitim.egitmen != request.user:
        return redirect('anasayfa')  # Eğitimi düzenleme izni yoksa ana sayfaya yönlendir

    if request.method == 'POST':
        form = EgitimYayinla(request.POST, request.FILES, instance=egitim)
        if form.is_valid():
            form.save()
            return redirect('egitim_detay', slug=egitim.slug)  # Düzenleme işlemi başarılıysa eğitim detayına yönlendir
    else:
        form = EgitimYayinla(instance=egitim)

    return render(request, 'egitim_duzenle.html', {'form': form, 'egitim': egitim})


from django.shortcuts import render, redirect, get_object_or_404
from .models import Egitim

def egitim_sil(request, egitim_id):
    egitim = get_object_or_404(Egitim, id=egitim_id)
    if request.method == 'POST':
        egitim.delete()
        return redirect('anasayfa')  # Eğitim silindikten sonra anasayfaya yönlendirme
    return render(request, 'egitim_sil.html', {'egitim': egitim})
