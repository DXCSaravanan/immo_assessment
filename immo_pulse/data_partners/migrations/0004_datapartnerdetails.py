# Generated by Django 3.2.9 on 2023-03-28 07:29

import data_partners.models
import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('data_partners', '0003_datapartnerprofiles_is_partner_active'),
    ]

    operations = [
        migrations.CreateModel(
            name='DataPartnerDetails',
            fields=[
                ('partner_data_id', models.AutoField(help_text='Primary id for each partner', primary_key=True, serialize=False)),
                ('source_data_type', models.TextField(choices=[('S3', 'S3'), ('POSTGRESQL', 'POSTGRESQL')], default=data_partners.models.SourceDataType['POSTGRESQL'], help_text='source data type')),
                ('source_details', models.JSONField()),
                ('sink_data_type', models.TextField(choices=[('KAFKA', 'KAFKA'), ('SNOWFLAKE', 'SNOWFLAKE'), ('S3', 'S3')], default=data_partners.models.SinkDataType['KAFKA'], help_text='sink data type')),
                ('sink_details', models.JSONField()),
                ('created_date', models.DateTimeField(default=datetime.datetime.utcnow, help_text='record creation time..')),
                ('updated_date', models.DateTimeField(default=datetime.datetime.utcnow, help_text='record updation time..')),
                ('created_by', models.TextField(help_text='Who created the partner')),
                ('updated_by', models.TextField(help_text='Who updated the partner')),
                ('data_partner_profiles', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='data_partners.datapartnerprofiles')),
            ],
            options={
                'db_table': 'data_partner_details',
            },
        ),
    ]