from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin


class FrontEndView(LoginRequiredMixin, TemplateView):
    """View react frontend"""
    template_name = 'frontend/index.html'
