from datetime import datetime
from enum import Enum

from django.db import models
from django.db.models import JSONField
from rest_framework.compat import coreapi, coreschema

class Countries(Enum):
    UK = "UK"
    SPAIN = "SPAIN"
    GERMANY = "GERMANY"

    @classmethod
    def choices(cls):
        return tuple((i.name, i.value) for i in cls)


class SourceType(Enum):
    RESIDENT = "RESIDENT"
    INVESTOR = "INVESTOR"
    PROPERTY = "PROPERTY"

    @classmethod
    def choices(cls):
        return tuple((i.name, i.value) for i in cls)

class SourceDataType(Enum):
    S3 = "S3"
    POSTGRESQL = "POSTGRESQL"

    @classmethod
    def choices(cls):
        return tuple((i.name, i.value) for i in cls)

class SinkDataType(Enum):
    KAFKA = "KAFKA"
    SNOWFLAKE = "SNOWFLAKE"
    S3 = "S3"

    @classmethod
    def choices(cls):
        return tuple((i.name, i.value) for i in cls)


class DataPartnerProfiles(models.Model):
    partner_id = models.AutoField(primary_key=True, help_text='Primary id for each partner')
    partner_name = models.TextField(null=False, blank=False, help_text='Name of the partner')
    partner_description = models.TextField(null=True, blank=True, help_text='Simple description about the partner')
    partner_country = models.TextField(
        null=False, blank=False,
        choices=Countries.choices(),
        default=Countries.UK,
        help_text='To which country partner belongs to'
    )
    partner_type = models.TextField(
        null=False, blank=False,
        choices=SourceType.choices(),
        default=SourceType.RESIDENT,
        help_text='partner type'
    )
    is_partner_active = models.BooleanField(default=True, help_text='Partner is active or not..')
    created_date = models.DateTimeField(default=datetime.utcnow, help_text='record creation time..')
    updated_date = models.DateTimeField(default=datetime.utcnow, help_text='record updation time..')
    created_by = models.TextField(null=False, blank=False, help_text='Who created the partner')
    updated_by = models.TextField(null=False, blank=False, help_text='Who updated the partner')

    class Meta:
        db_table = 'data_partner_profiles'


class DataPartnerDetails(models.Model):
    partner_data_id = models.AutoField(primary_key=True, help_text='Primary id for each partner')
    data_partner_profiles = models.ForeignKey(DataPartnerProfiles, on_delete=models.RESTRICT)
    source_data_type = models.TextField(
        null=False, blank=False,
        choices=SourceDataType.choices(),
        default=SourceDataType.POSTGRESQL,
        help_text='source data type'
    )
    source_details = JSONField()
    sink_data_type = models.TextField(
        null=False, blank=False,
        choices=SinkDataType.choices(),
        default=SinkDataType.KAFKA,
        help_text='sink data type'
    )
    sink_details = JSONField()
    created_date = models.DateTimeField(default=datetime.utcnow, help_text='record creation time..')
    updated_date = models.DateTimeField(default=datetime.utcnow, help_text='record updation time..')
    created_by = models.TextField(null=False, blank=False, help_text='Who created the partner')
    updated_by = models.TextField(null=False, blank=False, help_text='Who updated the partner')

    class Meta:
        db_table = 'data_partner_details'
