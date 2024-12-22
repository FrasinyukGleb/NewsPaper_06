from django.core.mail import EmailMultiAlternatives
from django.shortcuts import get_object_or_404, redirect
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from .models import Post, PostCategory, Category
from .filters import PostFilter
from .forms import PostForm
# from .signals import send_post_notification
from .tasks import send_post_notification

class PostList(ListView):
    model = Post
    ordering = '-date_add'
    template_name = 'news.html'
    context_object_name = 'news'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs


class PostDetail(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'

class NewsFilter(ListView):
    model = Post
    ordering = '-date_add'
    template_name = 'news_search.html'
    context_object_name = 'news'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class PostCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = ('news.add_post')

    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        if self.request.path == '/news/articles/create/':
            post.type = 'articles'
        else:
            post.type = 'news'
        post.save()
        send_post_notification.delay(post.pk)

        return super().form_valid(form)


class PostUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = ('news.change_post')

    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'
    success_url = reverse_lazy('news_list')


class PostDelete(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    permission_required = ('news.delete_post')

    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('news_list')


class SubscribeToCategory(LoginRequiredMixin, View):
    def post(self, request, category_id):
        category = get_object_or_404(Category, id=category_id)
        category.subscribers.add(request.user)
        return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))

