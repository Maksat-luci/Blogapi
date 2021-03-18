from datetime import timedelta
from django.db.models import Q
from django.utils import timezone
from rest_framework.decorators import  action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from rest_framework import generics, viewsets, status, mixins
from rest_framework.views import APIView

from main import services
from main.parsing import main
from main.permissions import IsAuthorPermission
from main.serializers import *
from django.db import models

class PermissionMixin:

    def get_permissions(self):
        if self.action == 'create':
            permissions = [IsAuthenticated,]
        elif self.action in ['update' , 'partial_update' , 'destroy']:
            permissions = [IsAuthorPermission, ]
        else:
            permissions = []
        return [perm() for perm in permissions]



class LikedMixin:
    @action(detail=True, methods=['post'])
    def like(self, request, pk=None):
        """Лайкает obj.
        """
        obj = self.get_object()
        services.add_like(obj, request.user)
        return Response('successfully liked')

    @action(detail=True, methods=['post'])
    def unlike(self, request, pk=None):
        """Удаляет лайк с obj.
        """
        obj = self.get_object()
        services.remove_like(obj, request.user)
        return Response('successfully unliked')


class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [AllowAny, ]


class PostViewSet(PermissionMixin,LikedMixin,viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


    def get_queryset(self):
        queryset = super().get_queryset()
        days_count = int(self.request.query_params.get('days', 0))
        if days_count > 0:
            start_date = timezone.now() - timedelta(days=days_count)
            queryset = queryset.filter(created_at__gte=start_date)
        return queryset


    @action(detail=False, methods=['GET'])
    def ratings(self, request):
        post = Post.objects.filter(draft=False).annotate(
            rating_user=models.Count('ratings', filter=models.Q(ratings__email = request.user))
        ).annotate(
            middle_star=models.Sum(models.F('ratings__star')) / models.Count(models.F('ratings'))
        )

        serializer = PostSerializer(post,many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def my_posts(self,request,pk=None):
        queryset = self.get_queryset()
        queryset = queryset.filter(author=request.user)
        serializer = PostSerializer(queryset, many=True, context={'request':request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['GET'])
    def search(self, request, pk=None):
        q = request.query_params.get('q')
        queryset = self.get_queryset().filter(Q(title__icontains=q) | Q(text__icontains=q))
        serializer = PostSerializer(queryset, many=True,context={'request':request})
        return Response(serializer.data, status=status.HTTP_200_OK)



class PostImageView(generics.ListCreateAPIView):
    queryset = PostImage.objects.all()
    serializer_class = PostImageSerializer

    def get_serializer_context(self):
        return {'request':self.request}


class CommentViewSet(PermissionMixin,viewsets.ModelViewSet):
    queryset = Comments.objects.all()
    serializer_class = CommentSerializer



class NewsView(APIView):
    def get(self, request):
        dict_ = main()
        serializer = NewsSerializer(instance=dict_, many=True)
        return Response(serializer.data)

class FavoriteViewSet(mixins.ListModelMixin, mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer
    permission_classes = [IsAuthenticated, ]

    def get_serializer_context(self):
        return {'request': self.request, 'action': self.action}


#регистрация v1/api/register/
#заходим на почту и активируем аккаунт
#создаём пост редактируем оставляем коммент http://localhost:8000/v1/api/comments/ передаём пост и боди
# и удаляем пост
#пагиннацию показываем
#поискhttp://localhost:8000/v1/api/posts/search/?q=ежовик
#показывавем permission модифицируя посты других пользователей
#фильрация по своим постам http://localhost:8000/v1/api/posts/my_posts/
#фильтрация по дням http://localhost:8000/v1/api/posts/?days=5
#райтинг чтобы добаввить рейтинг посту //localhost:8000/v1/api/rating/ post,email,star
#для вывода нужно коментить getfields
#вывод ://localhost:8000/v1/api/posts/ratings/
#поставить лайк http://localhost:8000/v1/api/posts/4/like/
#убрать лайк http://localhost:8000/v1/api/posts/4/unlike/
#перейти в свагер http://localhost:8000/v1/api/docs/
#парсинг http://localhost:8000/v1/api/news/

#фавориты  http://localhost:8000/v1/api/favorites/ GET получаем список фаворитов
#фавориты  http://localhost:8000/v1/api/favorites/ POst добавляем в фавориты
