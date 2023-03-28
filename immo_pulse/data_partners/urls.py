from django.urls import path
from data_partners.views import (
    DataPartnerProfilesCreateListView,
    DataPartnerDetailsCreateListView
)

urlpatterns = [
    path(
        'data_partner_profile/',
        DataPartnerProfilesCreateListView.as_view(),
        name='profile_list_create_view'
    ),
    path(
        'data_partner_details/',
        DataPartnerDetailsCreateListView.as_view(),
        name='details_list_create_view'
    )
]