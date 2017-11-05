# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-11-05 22:27
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('houses', '0003_auto_20171025_2241'),
    ]

    operations = [
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
            options={
                'verbose_name_plural': 'cities',
            },
        ),
        migrations.CreateModel(
            name='District',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
                ('city', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='houses.City')),
            ],
        ),
        migrations.CreateModel(
            name='Neighborhood',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
                ('district', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='houses.District')),
            ],
        ),
        migrations.AddField(
            model_name='starturl',
            name='type',
            field=models.CharField(choices=[('R', 'Rent'), ('B', 'Buy')], default='R', max_length=1),
        ),
        migrations.AlterField(
            model_name='house',
            name='start_url',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='houses.StartURL'),
        ),
        migrations.AlterField(
            model_name='starturl',
            name='city',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='houses.City'),
        ),
        migrations.AlterField(
            model_name='starturl',
            name='neighborhood',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='houses.Neighborhood'),
        ),
        migrations.AddField(
            model_name='starturl',
            name='district',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='houses.District'),
        ),
    ]
