# Generated by Django 3.2.9 on 2023-03-27 15:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data_partners', '0002_auto_20230327_2050'),
    ]

    operations = [
        migrations.AddField(
            model_name='datapartnerprofiles',
            name='is_partner_active',
            field=models.BooleanField(default=True, help_text='Partner is active or not..'),
        ),
    ]