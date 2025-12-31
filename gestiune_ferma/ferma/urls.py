from django.urls import path 
from . import views
urlpatterns=[
    path('', views.acasa_view, name='acasa'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('animale/', views.animale_view, name='animale'),
    path('parcele/', views.parcele_view, name='parcele'),
    path('resurse/', views.resurse_view, name='resurse'),
    path('animale/adauga/', views.adauga_animal_view, name='adauga_animal'),
    path('animale/modifica/<int:id_animal>/', views.modifica_animal_view, name='modifica_animal'),
    path('animale/sterge/<int:id_animal>/', views.sterge_animal_view, name='sterge_animal'),
    path('utilizatori/', views.utilizatori_view, name='utilizatori'),
    path('utilizatori/sterge/<int:id_utilizator>/', views.sterge_utilizator_view, name='sterge_utilizator'),
]