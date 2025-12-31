from django.shortcuts import render, redirect
from django.db.models import Count
from .models import Utilizatori, Specii, Parcele, Resurse, Animale, Culturi, Insamantari, Tratamente
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.contrib.auth.hashers import make_password, check_password

from functools import wraps


def user_autentificat(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if 'user_id' not in request.session:
            return redirect('login') # Trimite-l la login dacă nu are sesiune
        return view_func(request, *args, **kwargs)
    return _wrapped_view

#LOGIN
def login_view(request):
    error_message = None
    if request.method == 'POST':
        email_formular = request.POST.get('email')
        parola_formular = request.POST.get('parola')

        try:
            user = Utilizatori.objects.get(email=email_formular)

            if (parola_formular==user.parola):
                request.session['user_id'] = user.id_utilizator
                request.session['user_nume'] = user.nume
                request.session['user_prenume'] = user.prenume
                request.session['user_cnp'] = user.cnp
                request.session['user_rol'] = user.rol
                request.session['user_status'] = user.stare_cont
                return redirect('acasa')
            else:
                error_message = "Parola gresita"
        
        except Utilizatori.DoesNotExist:
            error_message = "Utilizatorul nu exista."
    return render(request, 'login.html', {'error': error_message})


def logout_view(request):
    request.session.flush()
    return redirect('login')

#ACASA
@user_autentificat
def acasa_view(request):
    specii = Specii.objects.annotate(numar_animale=Count('animale')).order_by('nume')
    parcele = Parcele.objects.all().order_by('suprafata')[:3]
    resurse = Resurse.objects.all().order_by('tip')[:3]

    if 'user_id' in request.session:
        nume_user = request.session.get('user_nume')
        prenume_user = request.session.get('user_prenume')
        cnp_user = request.session.get('user_cnp')
        rol_user = request.session.get('user_rol')
        status_user = request.session.get('user_status')

        context = {
            'nume': nume_user,
            'prenume': prenume_user,
            'rol': rol_user,
            'cnp': cnp_user,
            'status': status_user,
            'specii': specii,
            'parcele': parcele,
            'resurse': resurse
        }
        return render(request, 'acasa.html', context)
    else:
        return redirect('login')

@user_autentificat
def animale_view(request):

    animale = Animale.objects.all()
    specii = Specii.objects.all()
    tratamente = Tratamente.objects.all()
    insamantari = Insamantari.objects.all()
    rol_user = request.session.get('user_rol')
    context = {
        'specii': specii,
        'animale': animale,
        'tratamente': tratamente,
        'insamantari': insamantari,
        'rol': rol_user,
    }    
    return render(request, 'animale.html',context)

@user_autentificat
def parcele_view(request):
    parcele = Parcele.objects.all()
    culturi = Culturi.objects.all()
    rol_user = request.session.get('user_rol')
    context = {
        'parcele': parcele,
        'culturi': culturi,
        'rol': rol_user,
    } 
    return render(request, 'parcele.html', context)

@user_autentificat
def resurse_view(request):
    resurse = Resurse.objects.all()
    rol_user = request.session.get('user_rol')
    context = {
        'resurse': resurse,
        'rol': rol_user,
    }
    return render(request, 'resurse.html', context)

@user_autentificat
def adauga_animal_view(request):
    if request.method == 'POST':
        crotaliu = request.POST.get('crotaliu')
        id_specie = request.POST.get('specie')
        data_nastere = request.POST.get('data_nastere')
        sex = request.POST.get('sex')
        sanatate = request.POST.get('sanatate')
        status = request.POST.get('status')

        specie_obj = Specii.objects.get(id_specie=id_specie)
        Animale.objects.create(
            id_specie=specie_obj,
            crotaliu=crotaliu,
            data_nastere=data_nastere,
            sex=sex,
            sanatate=sanatate,
            status=status
        )
        return redirect('animale')

    specii = Specii.objects.all()
    return render(request, 'adauga_animal.html', {'specii': specii})

@user_autentificat
def modifica_animal_view(request, id_animal):
    animal = Animale.objects.get(id_animal=id_animal)
    
    if request.method == 'POST':
        animal.sanatate = request.POST.get('sanatate')
        animal.status = request.POST.get('status')
        animal.save()

        medicament = request.POST.get('medicament')
        if medicament:
            Tratamente.objects.create(
                id_animal=animal,
                data=request.POST.get('data_tratament'),
                medicament=medicament
            )

        data_ins = request.POST.get('data_ins')
        if data_ins:
            Insamantari.objects.create(
                id_animal=animal,
                data_ins=data_ins,
                data_fatare=request.POST.get('data_fatare')
            )
        
        return redirect('animale')

    return render(request, 'modifica_animal.html', {'animal': animal})


@user_autentificat
def sterge_animal_view(request, id_animal):
    if request.session.get('user_rol') != 'admin':
        return redirect('animale')

    animal = Animale.objects.get(id_animal=id_animal)
    animal.delete()
    return redirect('animale')


@user_autentificat
def utilizatori_view(request):
    if request.session.get('user_rol') != 'admin':
        return redirect('acasa') # Angajatii nu au voie sa vada lista de useri

    lista_utilizatori = Utilizatori.objects.all().order_by('nume')

    context = {
        'utilizatori': lista_utilizatori,
        'rol': request.session.get('user_rol')
    }
    return render(request, 'utilizatori.html', context)


@user_autentificat
def sterge_utilizator_view(request, id_utilizator):
    if request.session.get('user_rol') == 'admin':
        try:
            utilizator = Utilizatori.objects.get(id_utilizator=id_utilizator)
            utilizator.delete()
            print(f"DEBUG: Utilizatorul {id_utilizator} a fost sters!")
        except Utilizatori.DoesNotExist:
            print("DEBUG: Utilizatorul nu a fost gasit!")
    
    return redirect('utilizatori')