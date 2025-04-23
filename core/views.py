from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from core.forms import CustomUserCreationForm
from core.models import Tepih, UserProfile, User, Zakazivanje
from django.contrib.auth.decorators import login_required
from .forms import TepihForm, ZakazivanjeForm
from django.http import JsonResponse
from django.views.decorators.http import require_POST

def home(request):
    return render(request, 'core/home.html')

def about(request):
    return render(request, 'core/about.html')

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            ime = form.cleaned_data['ime']
            prezime = form.cleaned_data['prezime']
            email = form.cleaned_data['email']
            broj_telefona = form.cleaned_data['broj_telefona']
            lokacija = form.cleaned_data['lokacija']
            
            username = ime.lower().replace(' ', '')

            user = User.objects.create_user(
                username=username,
                email=email,
                password=form.cleaned_data['password1']
            )

            # Nadoveži se na profil koji je kreirao signal
            profile = user.userprofile
            profile.ime = ime
            profile.prezime = prezime
            profile.broj_telefona = broj_telefona
            profile.lokacija = lokacija
            profile.save()

            login(request, user)
            messages.success(request, 'Uspješno ste se registrovali.')
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'core/register.html', {'form': form})


@login_required
def dodaj_tepih(request):
    profile = request.user.userprofile
    if request.method == 'POST':
        form = TepihForm(request.POST)
        if form.is_valid():
            tepih = form.save(commit=False)
            tepih.korisnik = profile
            tepih.save()
            messages.success(request, 'Tepih je dodat!')
            return redirect('moji-tepisi')
    else:
        form = TepihForm()
    return render(request, 'core/dodaj_tepih.html', {'form': form})


@login_required
def moji_tepisi(request):
    profile = request.user.userprofile
    cena_po_m2 = 2
    tepisi = Tepih.objects.filter(korisnik=profile)

    for t in tepisi:
        t.cena = t.velicina_m2 * cena_po_m2

    return render(request, 'core/moji_tepisi.html', {
        'tepisi': tepisi,
        'cena_po_m2': cena_po_m2
    })



@login_required
def detalji_tepih(request, tepih_id):
    profile = request.user.userprofile
    tepih = Tepih.objects.get(id=tepih_id, korisnik=profile)
    zakazano = Zakazivanje.objects.filter(tepih=tepih)

    if request.method == 'POST':
        form = ZakazivanjeForm(request.POST)
        if form.is_valid():
            zakazivanje = form.save(commit=False)
            zakazivanje.tepih = tepih
            zakazivanje.save()
            messages.success(request, 'Termin je uspešno zakazan.')
            return redirect('moji-tepisi')
    else:
        form = ZakazivanjeForm()

    return render(request, 'core/detalji_tepih.html', {
        'tepih': tepih,
        'form': form,
        'zakazano': zakazano
    })

@login_required
def ukloni_tepih(request, tepih_id):
    profile = request.user.userprofile
    tepih = Tepih.objects.get(id=tepih_id, korisnik=profile)
    tepih.delete()
    messages.success(request, "Tepih je uspešno uklonjen.")
    return redirect('moji-tepisi')

@login_required
def zakazi_tepih_view(request):
    profile = request.user.userprofile
    cena_po_m2 = 2  # EUR po m²
    tepisi = Tepih.objects.filter(korisnik=profile)

    # Dodeli svakom tepihu cenu
    for tepih in tepisi:
        tepih.cena = round(tepih.velicina_m2 * cena_po_m2, 2)

    if request.method == 'POST':
        izabrani_id = request.POST.getlist('tepisi')
        datum = request.POST.get('datum')

        if not izabrani_id:
            messages.error(request, "Morate izabrati bar jedan tepih.")
            return redirect('zakazivanje')

        zakazivanje = Zakazivanje.objects.create(
            datum=datum,
            status='na čekanju'
        )
        for t_id in izabrani_id:
            tepih = Tepih.objects.get(id=t_id, korisnik=profile)
            zakazivanje.tepisi.add(tepih)

        zakazivanje.save()
        messages.success(request, "Uspješno ste zakazali termin za izabrane tepihe.")
        return redirect('moji-termini')

    return render(request, 'core/zakazivanje.html', {
        'tepisi': tepisi,
        'cena_po_m2': cena_po_m2
    })


@login_required
def moja_zakazivanja(request):
    profile = request.user.userprofile
    zakazi = Zakazivanje.objects.filter(tepisi__korisnik=profile).distinct().order_by('-datum')

    cena_po_m2 = 2  # Cena po m², možeš ovo kasnije staviti u settings ako hoćeš

    for zakazivanje in zakazi:
        ukupna_povrsina = sum(t.velicina_m2 for t in zakazivanje.tepisi.all())
        zakazivanje.ukupna_povrsina = ukupna_povrsina
        zakazivanje.cena = round(ukupna_povrsina * cena_po_m2)

    return render(request, 'core/moja_zakazivanja.html', {
        'zakazi': zakazi
    })

from django.http import JsonResponse

@login_required
def ajax_dodaj_tepih(request):
    if request.method == 'POST':
        form = TepihForm(request.POST)
        if form.is_valid():
            tepih = form.save(commit=False)
            tepih.korisnik = request.user.userprofile
            tepih.save()

            return JsonResponse({
                'id': tepih.id,
                'vrsta': tepih.vrsta,
                'velicina': tepih.velicina_m2,
                'napomena': tepih.napomena or '',
            }, status=200)

        return JsonResponse({'errors': form.errors}, status=400)

    return JsonResponse({'error': 'Invalid request'}, status=400)


@require_POST
@login_required
def otkazi_zakazivanje(request, zakazivanje_id):
    zakazivanje = Zakazivanje.objects.get(id=zakazivanje_id, tepih__korisnik=request.user.userprofile)
    zakazivanje.delete()
    messages.success(request, "Termin je uspešno otkazan.")
    return redirect('moji-termini')
