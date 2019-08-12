from django.shortcuts import get_object_or_404, reverse
from django.contrib.syndication.views import Feed
from django.contrib.auth.models import User
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from blogging.models import Post, Category
from blogging.forms import PostUpdateForm, CategoryFormset, CategoryInline

from extra_views import CreateWithInlinesView, UpdateWithInlinesView


class PostCategoryInlineCreateView(CreateWithInlinesView):
    model = Post
    # form_class = PostUpdateForm
    inlines = [CategoryInline]
    fields = ['title', 'text', 'published_date']
    template_name = 'blogging/post_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


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
            return query_user.order_by('published_date')
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


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    template_name = 'blogging/post_form.html'
    fields = ['title', 'text', 'published_date']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    # def get_success_url(self):
    #     return reverse_lazy('post-detail', args=(self.object.id,))


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    template_name = 'blogging/post_update.html'
    form_class = PostUpdateForm
    formset_class = CategoryFormset

    def form_valid(self, form):
        form.instance.author = self.request.user
        context = self.get_context_data()
        context['formset'] = self.formset_class(self.request.POST)
        formset = context['formset']
        print(formset)
        for cat in formset:
            # cat_name = 'Dogs'
            # cat_dic = cat.fields['name']
            print(cat)
            cat_name = cat['name']
            print(cat_name)
            if cat_name:
                # category_sample = Category.objects.filter(name=cat_name).first()
                # category_sample.posts.add(self.object)
                cat_name.posts.add(self.object)

        #     # category_sample.save()
        #     category_sample.posts.add(self.get_object())
        # category_sample.save()

        # if formset.is_valid():
        #     category_form = formset.save(commit=False)
        #     category_form.posts.add(self.get_object())
        #     category_form.save()
        #     formset.save()

        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.get_object()
        # if self.request.POST:
        #     context['formset'] = self.formset_class(self.request.POST)
        # else:
        #     initial_value = []
        #     for c in post.categories.all():
        #         initial_value.append({'name': c})
        #     context['formset'] = self.formset_class(initial=initial_value)
        initial_value = []
        for c in post.categories.all():
            initial_value.append({'name': c})
        context['formset'] = self.formset_class(initial=initial_value)
        return context


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
