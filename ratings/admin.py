from django.contrib import admin

from ratings.models import RatingStar, Rating


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    """Рейтинг"""
    list_display = ("star", "post",'email')

admin.site.register(RatingStar)