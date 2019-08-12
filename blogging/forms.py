from django import forms
from blogging.models import Post, Category, PostCategory
from extra_views import InlineFormSetFactory


class PostUpdateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'text', 'published_date']


# ('', 'Choose from the list')

CATEGORY_CHOICES = []
for c in Category.objects.all():
    CATEGORY_CHOICES.append((c.name, c.name))


class CategoryUpdateForm(forms.ModelForm):
    # def __init__(self, *args, **kwargs):
    #     super(CategoryUpdateForm, self).__init__(*args, **kwargs)
    #     self.fields['name'].widget.attrs['placeholder'] = "-----------"

    name = forms.ModelChoiceField(queryset=Category.objects.all(), to_field_name="name")
    # name = forms.ChoiceField(choices=CATEGORY_CHOICES)

    class Meta:
        model = Category
        fields = ['name']
        labels = {'name': 'Category'}
        help_texts = {'name': 'Choose category for your post'}
        # widgets = {
        #     'name': forms.Select(choices=CATEGORY_CHOICES)
        # }


CategoryFormset = forms.formset_factory(CategoryUpdateForm, extra=1, max_num=3, can_delete=True)


class CategoryInline(InlineFormSetFactory):
    model = PostCategory
    exclude = ['post_name']
    # formset_class = CategoryFormset
