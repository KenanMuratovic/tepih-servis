from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    ime = models.CharField(max_length=50)
    prezime = models.CharField(max_length=50)
    broj_telefona = models.CharField(max_length=20)
    lokacija = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"{self.ime} {self.prezime}"
    
    
class Tepih(models.Model):
    VRSTE_TEPIS = [
        ('vuna', 'Vuna'),
        ('pamuk', 'Pamuk'),
        ('sintetika', 'Sintetika'),
        ('orijentalni', 'Orijentalni'),
        ('antialergijski', 'Antialergijski'),
        ('tepison', 'Tepison'),
        ('obican' , 'Obican tepih')
    ]

    korisnik = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    vrsta = models.CharField(max_length=50, choices=VRSTE_TEPIS)
    velicina_m2 = models.FloatField()
    datum_unosa = models.DateTimeField(auto_now_add=True)
    napomena = models.TextField(blank=True)

    def __str__(self):
        return f"{self.vrsta} ({self.velicina_m2} m²)"



class Zakazivanje(models.Model):
    STATUSI = [
        ('na čekanju', 'Na čekanju'),
        ('primljen', 'Primljen'),
        ('u pranju', 'U pranju'),
        ('završeno', 'Završeno'),
    ]

    tepisi = models.ManyToManyField(Tepih)

    datum = models.DateTimeField()
    status = models.CharField(max_length=20, choices=STATUSI, default='na čekanju')
    datum = models.DateTimeField(blank=True)
    def __str__(self):
        return f"{self.tepih} | {self.datum.strftime('%d.%m.%Y %H:%M')} | {self.status}"

@receiver(post_save, sender=User)
def kreiraj_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

