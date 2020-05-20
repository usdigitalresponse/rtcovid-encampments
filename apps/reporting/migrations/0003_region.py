# Generated by Django 3.0.6 on 2020-05-19 19:45

import django.contrib.gis.db.models.fields
from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('reporting', '0002_auto_20200513_1818'),
    ]

    operations = [
        migrations.CreateModel(
            name='Region',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=50)),
                ('geom', django.contrib.gis.db.models.fields.MultiPolygonField(srid=4326)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='encampment',
            name='region',
            field=models.ForeignKey(default='', null=True, on_delete=django.db.models.deletion.PROTECT, to='reporting.Region'),
            preserve_default=False,
        ),
    ]
