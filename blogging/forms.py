from django import forms
from blogging.models import Post, Category, PostCategory
from extra_views import InlineFormSetFactory


class DateInput(forms.DateTimeInput):
    """ widget for date picker"""
    input_type = 'date'


class PostUpdateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'text', 'published_date']
        widgets = {'published_date': DateInput()}


class CategoryInline(InlineFormSetFactory):
    model = PostCategory
    fields = ['category_name']
    factory_kwargs = {'extra': 1, 'max_num': None, 'can_delete': False}

    class Meta:
        labels = {'category_name': 'Category'}
        help_texts = {'category_name': 'Choose category for your post'}


# ('', 'Choose from the list')
#
# CATEGORY_CHOICES = []
# for c in Category.objects.all():
#     CATEGORY_CHOICES.append((c.name, c.name))


# class CategoryUpdateForm(forms.ModelForm):
#     name = forms.ModelChoiceField(queryset=Category.objects.all(), to_field_name="name")

    # name = forms.ChoiceField(choices=CATEGORY_CHOICES)

    # class Meta:
    #     model = Category
    #     fields = ['name']
    #     labels = {'name': 'Category'}
    #     help_texts = {'name': 'Choose category for your post'}
        # widgets = {
        #     'name': forms.Select(choices=CATEGORY_CHOICES)
        # }


# CategoryUpdateFormset = forms.formset_factory(CategoryUpdateForm, extra=1, max_num=3, can_delete=True)
# CategoryUpdateInlineFormset = forms.inlineformset_factory(Post, PostCategory, fields=['category_name'], extra=1,
#                                                           max_num=3, formset=CategoryUpdateFormset)




