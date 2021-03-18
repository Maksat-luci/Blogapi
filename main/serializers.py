from rest_framework import serializers
from .models import *

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields= '__all__'


class PostSerializer(serializers.ModelSerializer):
    rating_user = serializers.BooleanField(default=False)
    created_at = serializers.DateTimeField(format='%d/%m/%Y %H:%M:%S',read_only=True)
    middle_star = serializers.IntegerField(default=0)

    class Meta:
        model = Post
        fields = ('id', 'title','title_ru','title_en',
                  'title_ky','text_ru','text_ky','text_en',
                  'category', 'created_at', 'text','telegram_bot',
                  'rating_user','middle_star','total_likes')

    # def get_fields(self):
    #     fields = super().get_fields()
    #     request = self.context.get('request')
    #     if request.method == 'POST':
    #         fields.pop('rating_user')
    #         fields.pop('middle_star')
    #
    #     return fields

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['author'] = instance.author.email
        representation['comments'] = CommentSerializer(instance.replies.all(), many=True).data
        representation['images'] = PostImageSerializer(instance.images.all(),
                                                       many=True, context=self.context).data
        return representation

    def create(self, validated_data):
        request = self.context.get('request')
        images_data = request.FILES
        user_id = request.user.id
        validated_data['author_id'] = user_id
        post = Post.objects.create(**validated_data)
        for image in images_data.getlist('images'):
            PostImage.objects.create(post=post, image=image)
        return post

    def update(self, instance, validated_data):
        request = self.context.get('request')
        for k, v in validated_data.items():
            setattr(instance, k, v)
        instance.save()
        instance.images.all().delete()
        images_data = request.FILES
        for image in images_data.getlist('images'):
            PostImage.objects.create(post=instance, image=image)
        return instance


class PostImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostImage
        fields = '__all__'

    def _get_image_url(self,obj):
        if obj.image:
            url = obj.image.url
            request = self.context.get('request')
            if request is not None:
                url = request.build_absolute_uri(url)
        else:
            url = ''
        return url



class CommentSerializer(serializers.ModelSerializer):
    created = serializers.DateTimeField(format='%d/%m/%Y %H:%M:%S',read_only=True)

    class Meta:
        model = Comments
        fields = ('post','body','created',)

    def create(self, validated_data):
        request = self.context.get('request')
        user_id = request.user.id
        validated_data['author_id'] = user_id
        comment = Comments.objects.create(**validated_data)
        return comment

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['author'] = instance.author.email
        return representation

class NewsSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=255)
    description = serializers.CharField(max_length=255)

class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorite
        fields = ('id', 'post', 'user', 'favorite')

    def get_fields(self):
        action = self.context.get('action')
        fields = super().get_fields()
        if action == 'create':
            fields.pop('user')
            fields.pop('favorite')
        return fields

    def create(self, validated_data):
        request = self.context.get('request')
        user = request.user
        post = validated_data.get('post')
        favorite = Favorite.objects.get_or_create(user=user, post=post)[0]
        favorite.favorite = True if favorite.favorite == False else False
        favorite.save()
        return favorite