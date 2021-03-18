from rest_framework import serializers

from ratings.models import Rating


class CreateRatingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Rating
        fields = ('star','post','email')

    def create(self, validated_data):
        request = self.context.get('request')
        print(request)
        user_id = request.user.id
        validated_data['email_id'] = user_id
        rating = Rating.objects.update_or_create(
            email=validated_data.get('email_id', None),
            post=validated_data.get('post', None),
            defaults={'star': validated_data.get('star')}
        )
        return rating

