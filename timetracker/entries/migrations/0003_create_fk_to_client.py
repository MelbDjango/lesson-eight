# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


def move_client_name_to_temporary_field(apps, schema_editor):
    Project = apps.get_model("entries", "Project")

    for p in Project.objects.all():
        p.client_name = p.client
        p.save()

def create_clients(apps, schema_editor):
    Client = apps.get_model("entries", "Client")
    Project = apps.get_model("entries", "Project")

    for p in Project.objects.all():
        if p.client_name:
            c, _ = Client.objects.get_or_create(name=p.client_name)
            p.client = c
            p.save()


class Migration(migrations.Migration):

    dependencies = [
        ('entries', '0002_auto_20150723_0819'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='entry',
            options={'verbose_name_plural': 'entries'},
        ),
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
            ],
        ),
        migrations.AddField(
            model_name='project',
            name='client_name',
            field=models.CharField(max_length=200, default=''),
        ),
        migrations.RunPython(move_client_name_to_temporary_field),
        migrations.AlterField(
            model_name='project',
            name='client',
            field=models.ForeignKey(to='entries.Client', blank=True, null=True),
        ),
        migrations.RunPython(create_clients),
        migrations.RemoveField(
            model_name='project',
            name='client_name',
        ),

    ]
