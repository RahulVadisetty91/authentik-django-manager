"""miscellaneous flow tests"""
from django.test import TestCase

from passbook.flows.api import StageSerializer, StageViewSet
from passbook.flows.models import Stage
from passbook.stages.dummy.models import DummyStage


class TestFlowsMisc(TestCase):
    """miscellaneous tests"""

    def test_models(self):
        """Test that ui_user_settings returns none"""
        self.assertIsNone(Stage().ui_user_settings)

    def test_api_serializer(self):
        """Test that stage serializer returns the correct type"""
        obj = DummyStage()
        self.assertEqual(StageSerializer().get_type(obj), "dummy")

    def test_api_viewset(self):
        """Test that stage serializer returns the correct type"""
        dummy = DummyStage.objects.create()
        self.assertIn(dummy, StageViewSet().get_queryset())
