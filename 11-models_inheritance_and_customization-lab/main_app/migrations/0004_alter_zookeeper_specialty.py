# Generated by Django 4.2.4 on 2023-10-24 11:00

from django.db import migrations, models
import main_app.models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0003_zoodisplayanimal'),
    ]

    operations = [
        migrations.AlterField(
            model_name='zookeeper',
            name='specialty',
            field=models.CharField(choices=[('Mammals', 'Mammals'), ('Birds', 'Birds'), ('Reptiles', 'Reptiles'), ('Others', 'Others')], max_length=10, validators=[main_app.models.validate_specialties]),
        ),
    ]
