from pathlib import Path

from rest_framework import (
    generics,
    status
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from data_partners.models import (
    DataPartnerDetails,
    DataPartnerProfiles
)
from data_partners.serializer import (
    DataPartnerProfilesCreateListSerializer,
    DataPartnerDetailsCreateListSerializer
)

PARTNER_PROFILE_MANDATORY_FIELDS = ['partner_name', 'partner_country', 'partner_type', 'is_partner_active']
S3_MANDATORY_FIELDS = ['aws_access_key_id', 'aws_secret_access_key']
SNOWFLAKE_FIELDS = ['sf_username', 'sf_password', 'sf_host', 'sf_database', 'sf_schema', 'sf_table_list']
KAFKA_FIELDS = [
    'bootstrap_servers', 'security_protocol',
    'sasl_mechanisms', 'sasl_username',
    'sasl_password', 'topic'
]
POSTGRES_FIELDS = ['pg_username', 'pg_password', 'pg_host', 'pg_port', 'pg_database', 'pg_table_list']

class DataPartnerProfilesCreateListView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = DataPartnerProfiles.objects.all()
    serializer_class = DataPartnerProfilesCreateListSerializer

    def check_for_mandatory_fields(self, source_input_keys: list):
        return True if(all(x in source_input_keys for x in PARTNER_PROFILE_MANDATORY_FIELDS)) else False

    def post(self, request):
        try:
            data_partner_profiles_serializer = DataPartnerProfilesCreateListSerializer(request.data)
            if data_partner_profiles_serializer:
                input_data = request.data
                partner_name = input_data['partner_name']
                is_passed = self.check_for_mandatory_fields(list(input_data.keys()))
                if not is_passed:
                    message = f'Mandatory fields for the partner is not present'
                    return Response(message, status.HTTP_400_BAD_REQUEST)
                DataPartnerProfiles.objects.create(**input_data)
                message = f'Successfully registered the partner {partner_name}'
                return Response(message, status.HTTP_201_CREATED)
            else:
                message = 'Serialization error'
                return Response(message, status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            message = f'Error occured while creating the partner - {str(e)}'
            print(message)
            return Response(message, status.HTTP_400_BAD_REQUEST)


class DataPartnerDetailsCreateListView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = DataPartnerDetails.objects.all()
    serializer_class = DataPartnerDetailsCreateListSerializer

    def check_for_mandatory_fields(self, source_type: str, source_input_keys: list):
        if source_type == 'S3':
            return True if (all(x in source_input_keys for x in S3_MANDATORY_FIELDS)) else False
        if source_type == 'SNOWFLAKE':
            return True if (all(x in source_input_keys for x in SNOWFLAKE_FIELDS)) else False
        if source_type == 'KAFKA':
            return True if (all(x in source_input_keys for x in KAFKA_FIELDS)) else False
        if source_type == 'POSTGRESQL':
            return True if (all(x in source_input_keys for x in POSTGRES_FIELDS)) else False
    
    def check_partner_exist(self, partner_profile_id):
        try:
            return DataPartnerProfiles.objects.get(partner_id=partner_profile_id)
        except DataPartnerProfiles.DoesNotExist:
            return None

    def post(self, request):
        try:
            data_partner_details_serializer = DataPartnerDetailsCreateListSerializer(request.data)
            if data_partner_details_serializer:
                input_data = request.data
                source_data_type = input_data['source_data_type']
                sink_data_type = input_data['sink_data_type']
                source_details = input_data['source_details']
                sink_details = input_data['sink_details']
                partner_profile_id = input_data['data_partner_profiles']
                get_partner_details = self.check_partner_exist(partner_profile_id)
                if not get_partner_details:
                    message = f'partner profile {partner_profile_id} does not exist'
                    return Response(message, status.HTTP_400_BAD_REQUEST)
                input_data['data_partner_profiles'] = get_partner_details
                is_source_details_passed = self.check_for_mandatory_fields(source_data_type, list(source_details.keys()))
                if not is_source_details_passed:
                    message = f'Mandatory fields for the source {source_data_type} is not present'
                    return Response(message, status.HTTP_400_BAD_REQUEST)
                is_sink_details_passed = self.check_for_mandatory_fields(sink_data_type, list(sink_details.keys()))
                if not is_sink_details_passed:
                    message = f'Mandatory fields for the sink {sink_data_type} is not present'
                    return Response(message, status.HTTP_400_BAD_REQUEST)
                DataPartnerDetails.objects.create(**input_data)
                message = f'Successfully created the partner details'
                return Response(message, status.HTTP_201_CREATED)
            else:
                message = 'Serialization error'
                return Response(message, status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            message = f'Error occured while creating the partner details - {str(e)}'
            print(message)
            return Response(message, status.HTTP_400_BAD_REQUEST)
    
    def list(self, request, pk=None):
        try:
            final_results = []
            data_details = DataPartnerDetails.objects.all()
            for data_detail in data_details:
                detail = {}
                profile = {}
                data_partner_profile_id = data_detail.data_partner_profiles_id
                partner_profiles = self.check_partner_exist(data_partner_profile_id)
                profile['partner_id'] = partner_profiles.partner_id
                profile['partner_name'] = partner_profiles.partner_name
                profile['partner_country'] = partner_profiles.partner_country
                profile['partner_type'] = partner_profiles.partner_type
                profile['is_partner_active'] = partner_profiles.is_partner_active
                profile['created_by'] = partner_profiles.created_by
                profile['updated_by'] = partner_profiles.updated_by
                profile['created_date'] = partner_profiles.created_date
                profile['updated_date'] = partner_profiles.updated_date
                detail['partner_profile'] = profile
                detail['source_data_type'] = data_detail.source_data_type
                detail['source_details'] = data_detail.source_details
                detail['sink_data_type'] = data_detail.sink_data_type
                detail['sink_details'] = data_detail.sink_details
                detail['created_by'] = data_detail.created_by
                detail['updated_by'] = data_detail.updated_by
                final_results.append(detail)
            return Response(final_results, status.HTTP_200_OK)
        except Exception as e:
            message = f'Error occured while fetching data partner details - {str(e)}'
            return Response(message, status.HTTP_400_BAD_REQUEST)
