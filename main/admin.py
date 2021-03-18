# Register your models here.
from django.contrib import admin
from modeltranslation.admin import TranslationAdmin

from main.models import *


class PostImageInline(admin.TabularInline):
    model = PostImage
    max_num = 10
    min_num = 1



@admin.register(Post)
class PostAdmin(TranslationAdmin):

    # inlines = [PostImageInline, ]
    list_filter = ('created_at',)
    list_display = ('title', )
    # search_fields = ('title','description','email')


admin.site.register(Category)
