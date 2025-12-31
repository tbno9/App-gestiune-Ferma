from django.db import models

class Specii(models.Model):
    id_specie = models.AutoField(primary_key=True)
    nume = models.CharField(max_length=100)

    class Meta:
        db_table = 'specii'

    def __str__(self):
        return self.nume


class Animale(models.Model):
    id_animal = models.AutoField(primary_key=True)
    id_specie = models.ForeignKey(Specii, on_delete=models.DO_NOTHING, db_column='id_specie')
    crotaliu = models.CharField(max_length=50, blank=True, null=True)
    data_nastere = models.DateField(blank=True, null=True)
    sex = models.CharField(max_length=1, blank=True, null=True)
    sanatate = models.CharField(max_length=100, blank=True, null=True)
    status = models.CharField(max_length=6, blank=True, null=True)

    class Meta:
        db_table = 'animale'

    def __str__(self):
        return f"{self.crotaliu} ({self.id_animal})"


class Parcele(models.Model):
    id_parcela = models.AutoField(primary_key=True)
    suprafata = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    locatie = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        db_table = 'parcele'

    def __str__(self):
        return self.locatie or str(self.id_parcela)


class Culturi(models.Model):
    id_cultura = models.AutoField(primary_key=True)
    id_parcela = models.ForeignKey(Parcele, on_delete=models.DO_NOTHING, db_column='id_parcela')
    tip = models.CharField(max_length=100, blank=True, null=True)
    data = models.DateField(blank=True, null=True)
    cantitate = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    class Meta:
        db_table = 'culturi'

    def __str__(self):
        return self.tip or str(self.id_cultura)


class Insamantari(models.Model):
    id_ins = models.AutoField(primary_key=True)
    id_animal = models.ForeignKey(Animale, on_delete=models.DO_NOTHING, db_column='id_animal')
    data_ins = models.DateField(blank=True, null=True)
    data_est = models.DateField(blank=True, null=True)
    data_fatare = models.DateField(blank=True, null=True)

    class Meta:
        db_table = 'insamantari'


class Tratamente(models.Model):
    id_tratament = models.AutoField(primary_key=True)
    id_animal = models.ForeignKey(Animale, on_delete=models.DO_NOTHING, db_column='id_animal')
    data = models.DateField()
    medicament = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        db_table = 'tratamente'


class Utilizatori(models.Model):
    id_utilizator = models.AutoField(primary_key=True)
    nume = models.CharField(max_length=100)
    prenume = models.CharField(max_length=100)
    parola = models.CharField(max_length=255)
    email = models.CharField(unique=True, max_length=100)
    cnp = models.CharField(db_column='CNP', unique=True, max_length=13, blank=True, null=True)
    rol = models.CharField(max_length=50, blank=True, null=True)
    stare_cont = models.CharField(max_length=9, blank=True, null=True, default='activ')

    class Meta:
        db_table = 'utilizatori'

    def __str__(self):
        return f"{self.nume} {self.prenume}"


class Rapoarte(models.Model):
    id_raport = models.AutoField(primary_key=True)
    id_utilizator = models.ForeignKey(Utilizatori, on_delete=models.DO_NOTHING, db_column='id_utilizator')
    tip = models.CharField(max_length=100, blank=True, null=True)
    data = models.DateField(blank=True, null=True)
    start_per = models.DateField(blank=True, null=True)
    stop_per = models.DateField(blank=True, null=True)

    class Meta:
        db_table = 'rapoarte'


class Resurse(models.Model):
    id_resursa = models.AutoField(primary_key=True)
    tip = models.CharField(max_length=100, blank=True, null=True)
    cantitate = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    class Meta:
        db_table = 'resurse'
