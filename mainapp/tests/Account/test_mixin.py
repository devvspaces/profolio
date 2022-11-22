import pytest
from django.views.generic import TemplateView
from Account.views import ViewMixin


class TestViewMixin:
    def test_valid(self, settings):
        class TestView(ViewMixin, TemplateView):
            title = "Test"

        context = TestView().get_context_data()
        assert context["title"] == "Test"
        assert context["BRAND_NAME"] == settings.BRAND_NAME

    def test_invalid(self):
        class TestView(ViewMixin, TemplateView):
            pass

        with pytest.raises(NotImplementedError):
            TestView().get_context_data()
