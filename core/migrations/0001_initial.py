# Generated by Django 5.2 on 2025-04-23 08:56

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ime', models.CharField(max_length=50)),
                ('prezime', models.CharField(max_length=50)),
                ('broj_telefona', models.CharField(max_length=20)),
                ('lokacija', models.CharField(blank=True, max_length=100)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Tepih',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vrsta', models.CharField(choices=[('vuna', 'Vuna'), ('pamuk', 'Pamuk'), ('sintetika', 'Sintetika'), ('orijentalni', 'Orijentalni'), ('antialergijski', 'Antialergijski'), ('tepison', 'Tepison'), ('obican', 'Obican tepih')], max_length=50)),
                ('velicina_m2', models.FloatField()),
                ('datum_unosa', models.DateTimeField(auto_now_add=True)),
                ('napomena', models.TextField(blank=True)),
                ('korisnik', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.userprofile')),
            ],
        ),
        migrations.CreateModel(
            name='Zakazivanje',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('na čekanju', 'Na čekanju'), ('primljen', 'Primljen'), ('u pranju', 'U pranju'), ('završeno', 'Završeno')], default='na čekanju', max_length=20)),
                ('datum', models.DateTimeField(blank=True)),
                ('tepisi', models.ManyToManyField(to='core.tepih')),
            ],
        ),
    ]
