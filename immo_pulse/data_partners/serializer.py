from dataclasses import fields
from pyexpat import model
from rest_framework import serializers

from data_partners.models import (
    DataPartnerProfiles,
    DataPartnerDetails
)


class DataPartnerProfilesCreateListSerializer(serializers.ModelSerializer):
    partner_name = serializers.CharField(max_length=1000, allow_blank=False, allow_null=False)
    partner_country = serializers.CharField(max_length=100, allow_blank=False, allow_null=False)
    partner_type = serializers.CharField(max_length=500, allow_blank=False, allow_null=False)
    is_partner_active = serializers.BooleanField()
    created_by = serializers.CharField(max_length=200, allow_blank=False, allow_null=False)
    updated_by = serializers.CharField(max_length=200, allow_blank=False, allow_null=False)

    class Meta:
        model = DataPartnerProfiles
        fields = '__all__'


class DataPartnerDetailsCreateListSerializer(serializers.ModelSerializer):
    data_partner_profiles = serializers.PrimaryKeyRelatedField(queryset=DataPartnerProfiles.objects.all(), many=True)
    source_data_type = serializers.CharField(max_length=100, allow_blank=False, allow_null=False)
    source_details = serializers.JSONField()
    sink_data_type = serializers.CharField(max_length=100, allow_blank=False, allow_null=False)
    sink_details = serializers.JSONField()
    created_by = serializers.CharField(max_length=200, allow_blank=False, allow_null=False)
    updated_by = serializers.CharField(max_length=200, allow_blank=False, allow_null=False)

    class Meta:
        model = DataPartnerDetails
        fields = '__all__'
