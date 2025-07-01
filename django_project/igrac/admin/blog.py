from django.contrib import admin

from igrac.models.blog import BlogPage


@admin.register(BlogPage)
class BlogPageAdmin(admin.ModelAdmin):
    pass
