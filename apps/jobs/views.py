from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.base import TemplateView


class JobsBoardView(LoginRequiredMixin, TemplateView):
    template_name = 'jobs_board.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['latest_jobs'] = list(range(1, 20))
        return context
