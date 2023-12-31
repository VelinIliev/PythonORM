# Generated by Django 4.2.4 on 2023-10-26 10:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0005_regularrestaurantreview_foodcriticrestaurantreview'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='regularrestaurantreview',
            options={'ordering': ['-rating'], 'verbose_name': 'Regular Restaurant Review', 'verbose_name_plural': 'Regular Restaurant Reviews'},
        ),
        migrations.AlterUniqueTogether(
            name='regularrestaurantreview',
            unique_together={('reviewer_name', 'restaurant')},
        ),
    ]
