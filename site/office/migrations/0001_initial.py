# Generated by Django 2.2.6 on 2019-10-16 16:53

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [("churchcal", "0001_initial")]

    operations = [
        migrations.CreateModel(
            name="OfficeDay",
            fields=[
                ("uuid", models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ("created", models.DateTimeField(auto_now_add=True)),
                ("updated", models.DateTimeField(auto_now=True)),
                ("holy_day_name", models.CharField(blank=True, max_length=255, null=True)),
                ("mp_psalms", models.CharField(max_length=255)),
                ("mp_reading_1", models.CharField(max_length=255)),
                ("mp_reading_1_text", models.TextField(blank=True, null=True)),
                ("mp_reading_1_abbreviated", models.CharField(blank=True, max_length=255, null=True)),
                ("mp_reading_1_abbreviated_text", models.TextField(blank=True, null=True)),
                ("mp_reading_2", models.CharField(max_length=255)),
                ("mp_reading_2_text", models.TextField(blank=True, null=True)),
                ("ep_psalms", models.CharField(max_length=255)),
                ("ep_reading_1", models.CharField(max_length=255)),
                ("ep_reading_1_text", models.TextField(blank=True, null=True)),
                ("ep_reading_1_abbreviated", models.CharField(blank=True, max_length=255, null=True)),
                ("ep_reading_1_abbreviated_text", models.TextField(blank=True, null=True)),
                ("ep_reading_2", models.CharField(max_length=255)),
                ("ep_reading_2_text", models.TextField(blank=True, null=True)),
            ],
            options={"abstract": False},
        ),
        migrations.CreateModel(
            name="StandardOfficeDay",
            fields=[
                (
                    "officeday_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="office.OfficeDay",
                    ),
                ),
                ("month", models.IntegerField()),
                ("day", models.IntegerField()),
            ],
            options={"abstract": False},
            bases=("office.officeday",),
        ),
        migrations.CreateModel(
            name="HolyDayOfficeDay",
            fields=[
                (
                    "officeday_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="office.OfficeDay",
                    ),
                ),
                (
                    "commemoration",
                    models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="churchcal.Commemoration"),
                ),
            ],
            options={"abstract": False},
            bases=("office.officeday",),
        ),
    ]
