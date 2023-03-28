from django.contrib import admin

from data_partners.models import (
    DataPartnerProfiles,
    DataPartnerDetails
)

# Register your models here.
admin.site.register(DataPartnerProfiles)
admin.site.register(DataPartnerDetails)
