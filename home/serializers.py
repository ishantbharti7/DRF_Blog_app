from rest_framework import serializers
from .models import Blog
from   django.contrib.auth.models import User


class BlogSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    class Meta:
        model = Blog
        fields = ('id', 'title', 'user','blog_text', 'main_image', 'created_at', 'updated_at')
    

    def get_user(self, obj):
        user =None

        if obj:
            user =  obj.user.username
            print(user)
        
        return user