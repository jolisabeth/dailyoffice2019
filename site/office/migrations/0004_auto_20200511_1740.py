# Generated by Django 3.0.6 on 2020-05-11 21:40

import ckeditor.fields
from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('office', '0003_aboutitem'),
    ]

    operations = [
        migrations.CreateModel(
            name='UpdateNotice',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('notice', ckeditor.fields.RichTextField()),
                ('app_mode', models.BooleanField(default=True)),
                ('web_mode', models.BooleanField(default=True)),
                ('version', models.FloatField()),
            ],
            options={
                'ordering': ['-version'],
            },
        ),
        migrations.AlterModelOptions(
            name='aboutitem',
            options={'ordering': ['order']},
        ),
    ]
