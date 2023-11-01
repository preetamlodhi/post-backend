from rest_framework import serializers
from api.models import Post
from api.models import User


class PostSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source="user.username")
    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'post_date', 'user']

class UserSerializer(serializers.ModelSerializer):
    posts = serializers.HyperlinkedRelatedField(many=True, view_name="post-detail", read_only=True)

    class Meta:
        model = User
        fields = ['url', 'id', 'name', 'posts']

class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields=['email', 'name', 'password']
        extra_kwargs={
            'password':{'write_only':True}
        }

    def create(self, validate_data):
        return User.objects.create_user(**validate_data)

class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=100)
    class Meta:
        model = User
        fields = ['email', 'password']
