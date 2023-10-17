# Generated by Django 4.2.4 on 2023-10-17 14:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0014_migrate_smartphone'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_name', models.CharField(max_length=30)),
                ('customer_name', models.CharField(max_length=100)),
                ('order_date', models.DateField()),
                ('status', models.CharField(choices=[('Pending', 'Pending'), ('Completed', 'Completed'), ('Cancelled', 'Cancelled')], max_length=30)),
                ('amount', models.PositiveIntegerField(default=0)),
                ('product_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('total_price', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('warranty', models.CharField(default='No warranty')),
                ('delivery', models.DateField(blank=True, null=True)),
            ],
        ),
    ]
