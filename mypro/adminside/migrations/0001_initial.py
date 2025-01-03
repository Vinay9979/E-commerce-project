# Generated by Django 5.0.4 on 2024-06-17 05:18

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('client', '0017_contact'),
    ]

    operations = [
        migrations.CreateModel(
            name='Categoryphotos',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('imgUrl', models.URLField()),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='client.category')),
            ],
            options={
                'db_table': 'categoryphotos',
            },
        ),
    ]