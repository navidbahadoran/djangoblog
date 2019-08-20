from django.shortcuts import get_object_or_404
from django.contrib.syndication.views import Feed
from django.contrib.auth.models import User
from django.views.generic import ListView, DetailView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from extra_views import CreateWithInlinesView, UpdateWithInlinesView
from blogging.models import Post, Category
from blogging.forms import PostUpdateForm, CategoryInline


class LatestEntriesFeed(Feed):
    # title = "Police beat site news"
    # link = "/sitenews/"
    # description = "Updates on changes and additions to police beat central."

    def items(self):
        return Post.objects.order_by('-published_date')[:5]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.text


class PostListView(ListView):
    model = Post
    template_name = 'blogging/post_list.html'
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        if self.request.user.is_authenticated:
            query_login_user = Post.objects.filter(author=self.request.user)
            query_not_login_user = Post.objects.exclude(author__exact=self.request.user).exclude(
                published_date__exact=None)
            query_user = query_login_user.union(query_not_login_user)
            return query_user.order_by('-published_date')
        else:
            return Post.objects.exclude(published_date__exact=None).order_by('-published_date')


class PostDetailView(DetailView):
    model = Post
    template_name = 'blogging/post_detail.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super(PostDetailView, self).get_context_data(**kwargs)
        context['category_list'] = Category.objects.filter(posts=self.get_object())
        return context


class UserPostListView(ListView):
    model = Post
    template_name = 'blogging/user_posts.html'
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        user_for_list = get_object_or_404(User, username=self.kwargs.get('username'))
        if self.request.user == user_for_list:
            query_for_user = Post.objects.filter(author=user_for_list)
        else:
            query_for_user = Post.objects.filter(author=user_for_list).exclude(published_date__exact=None)

        return query_for_user.order_by('-published_date')


class PostCreateView(LoginRequiredMixin, CreateWithInlinesView):
    model = Post
    inlines = [CategoryInline]
    CategoryInline.factory_kwargs['can_delete'] = False
    template_name = 'blogging/post_form.html'
    form_class = PostUpdateForm

    def forms_valid(self, form, inlines):
        form.instance.author = self.request.user
        for formset in inlines:
            formset.instance.post_name = form.instance
        return super().forms_valid(form, inlines)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateWithInlinesView):
    model = Post
    inlines = [CategoryInline]
    template_name = 'blogging/post_update.html'
    form_class = PostUpdateForm

    def forms_valid(self, form, inlines):
        form.instance.author = self.request.user
        for formset in inlines:
            formset.instance.post_name = form.instance
        return super().forms_valid(form, inlines)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    context_object_name = 'post'
    success_url = '/'
    template_name = 'blogging/post_confirm_delete.html'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False
