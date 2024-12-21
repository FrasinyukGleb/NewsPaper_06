from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required

from news.models import Author


class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'protect/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_authors'] = not self.request.user.groups.filter(name = 'authors').exists()
        return context


@login_required
def upgrade_me(request):
    user = request.user
    group = get_object_or_404(Group, name='authors')
    if not user.groups.filter(name=group.name).exists():
        user.groups.add(group)
    if not Author.objects.filter(user=user).exists():
        Author.objects.create(user=user)
    return redirect('/')
