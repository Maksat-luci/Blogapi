from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework.routers import DefaultRouter

from main.views import *
from ratings.views import AddStarRatingView

router = DefaultRouter()
router.register('posts',PostViewSet)
router.register('comments',CommentViewSet)
router.register('favorites',FavoriteViewSet)

schema_view = get_schema_view(
    openapi.Info(
        title="Blog API",
        default_version='v1',
        description="Test description",
    ),
    public=True
)

urlpatterns = [

    path('admin/', admin.site.urls),
    path('v1/api/docs/',schema_view.with_ui()),
    path('api-auth/',include('rest_framework.urls')),
    path('v1/api/categories/',CategoryListView.as_view()),
    path('v1/api/rating/', AddStarRatingView.as_view()),
    path('v1/api/account/',include('account.urls')),
    path('v1/api/news/',NewsView.as_view()),
    path('auth/',include('rest_framework_social_oauth2.urls')),
    path('v1/api/',include(router.urls)),



]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)