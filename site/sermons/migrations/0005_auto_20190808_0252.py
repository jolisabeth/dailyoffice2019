# Generated by Django 2.2.3 on 2019-08-08 02:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("sermons", "0004_auto_20190808_0251")]

    operations = [
        migrations.AlterField(
            model_name="sermon",
            name="primary_date_and_time_given",
            field=models.DateTimeField(
                blank=True,
                help_text="The primary date given (used for sorting).  More than one date and time can be added on the date and time tab",
                null=True,
                verbose_name="Date and Time Given",
            ),
        )
    ]
