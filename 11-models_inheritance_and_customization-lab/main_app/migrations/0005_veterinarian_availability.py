# Generated by Django 4.2.4 on 2023-10-24 12:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0004_alter_zookeeper_specialty'),
    ]

    operations = [
        migrations.AddField(
            model_name='veterinarian',
            name='availability',
            field=models.BooleanField(choices=[('Available', True), ('Not Available', False)], default=True),
        ),
    ]
