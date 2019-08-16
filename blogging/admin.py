from django.contrib import admin
from blogging.models import Post, Category, PostCategory


class CategoryInline(admin.TabularInline):
    model = Category.posts.through
    extra = 1


class PostAdmin(admin.ModelAdmin):
    model = Post
    inlines = [CategoryInline]


class CategoryAdmin(admin.ModelAdmin):
    model = Category
    exclude = ['posts']


admin.site.register(Post, PostAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(PostCategory)
