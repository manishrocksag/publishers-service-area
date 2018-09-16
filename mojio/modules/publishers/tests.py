from unittest import TestCase

from datetime import timedelta

from django.contrib.auth import get_user_model
from django.utils.timezone import now

from apps.organizations.models import Institution
from apps.user_management.models import SiteUserData

from ..models import Campaign, Invitation
from ..campaign_services import CampaignService


class CampaignServiceTest(TestCase):
    def setUp(self):
        Campaign.objects.all().delete()
        Invitation.objects.all().delete()
        get_user_model().objects.all().delete()
        self.institution = Institution.objects.create(
            institution_id=1,
            location='Kharagpur',
            label='IIT Kharagpur',
            website='www.iitkgp.ernet.in'
        )
        self.campaign = Campaign.objects.create(
            name='Test Campaign',
            start_date_time=now(),
            slots=10,
            institution=self.institution
        )

        self.campaign_service = CampaignService(self.campaign)

    def tearDown(self):
        self.campaign.delete()
        self.institution.delete()
        Campaign.objects.all().delete()
        Invitation.objects.all().delete()
        get_user_model().objects.all().delete()

    def _setup_invitations_and_users(self):
        """Create 2 invitations and 3 users for self.campaign"""
        user1 = get_user_model().objects.create_user(email='user1@test.com')
        user2 = get_user_model().objects.create_user(email='user2@test.com')
        user3 = get_user_model().objects.create_user(email='user3@test.com')

        invitation1 = Invitation.create(
            invited_email='',
            invitation_type=2,
            campaign=self.campaign
        )
        invitation2 = Invitation.create(
            invited_email='', invitation_type=2, campaign=self.campaign
        )

        for user in [user1, user2]:
            SiteUserData.objects.create(user=user, via_invitation=invitation1)
        SiteUserData.objects.create(user=user3, via_invitation=invitation2)

    def test_is_active(self):
        self.campaign.is_active = True
        self.campaign.save()

        self.assertEqual(self.campaign.is_active, True)

    def test_get_vacant_slots(self):
        """Test to check if get_vacant_slots gets the correct number of vacant slots"""
        total_slots = 10
        # Creating an invitation with some signed up users

        self.campaign.slots = total_slots
        self.campaign.save()

        self._setup_invitations_and_users()

        vacant_slots = self.campaign_service.get_vacant_slots()

        # HARD CODED - assuming 3 users have been created
        # TODO - remove this hardcoding
        self.assertEqual(vacant_slots, (total_slots - 3))

    def test_update_campaign_status(self):
        """
        Test to check if campaign status is updated on expiry

        Expiry of campaign occurs if either all slots get filled up
        or the end_date_time is reached
        """

        # HARD CODED - assuming 3 users have been created
        # TODO - remove this hardcoding
        self._setup_invitations_and_users()

        # Checking expiry on basis of only slots
        # Keeping total slots at 3
        self.campaign.slots = 3
        self.campaign.end_date_time = None
        self.campaign.is_active = True
        self.campaign.save()

        self.campaign_service.update_campaign_status()
        self.assertEqual(self.campaign_service.is_campaign_active(), False)

        # Checking expiry on basis of time
        self.campaign.slots = 10
        self.campaign.is_active = True
        self.campaign.end_date_time = now() - timedelta(days=2)
        self.campaign.save()

        self.campaign_service.update_campaign_status()
        self.assertEqual(self.campaign_service.is_campaign_active(), False)

        # Checking non expiry
        self.campaign.slots = 10
        self.campaign.end_date_time = None
        self.campaign.is_active = True
        self.campaign.save()

        self.campaign_service.update_campaign_status()
        self.assertEqual(self.campaign_service.is_campaign_active(), True)
