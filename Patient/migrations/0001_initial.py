# Generated by Django 3.2 on 2024-02-22 15:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('main', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Patient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('facial_image', models.ImageField(default='main\\static\\images\\profile.png', upload_to='images')),
                ('contact', models.CharField(max_length=13, null=True, unique=True)),
                ('gender', models.CharField(max_length=6, null=True)),
                ('dob', models.DateField(null=True)),
                ('care', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='main.caretaker')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50, null=True)),
                ('dob', models.DateField(null=True)),
                ('gender', models.CharField(max_length=6, null=True)),
                ('relation', models.CharField(max_length=30, null=True)),
                ('description', models.TextField(null=True)),
                ('facial_image', models.ImageField(default='main\\static\\images\\profile.png', upload_to='images')),
                ('facial_embedding', models.BinaryField(null=True, unique=True)),
                ('patient', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Patient.patient')),
            ],
        ),
    ]
