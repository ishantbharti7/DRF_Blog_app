from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import BlogSerializer
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import Blog
from django.db.models import Q


class BlogView(APIView):
    # For authentication Purpose
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    def get(self,request):
        # Filtering data on the basis of the user show data to user which he/she has posted
        blogs = Blog.objects.filter(user=request.user)
        if request.GET.get('search'):
            search = request.GET.get('search')
            blogs  = blogs.filter(Q(title__icontains=search)| Q(blog_text__icontains=search))
        serializer = BlogSerializer(blogs,many=True)
        return Response({
                'data': serializer.data,
                'message': 'Blog Fetched successfully'
            }, status=status.HTTP_201_CREATED)


    def post(self, request):
        try:
            data = request.data
            data['user'] = request.user.id
            user =  request.user
            serializer = BlogSerializer(data=data)
            serializer.is_valid(raise_exception  = True)
            serializer.validated_data['user']  = user
            serializer.save()
            return Response({
                'data': serializer.data,
                'message': 'Blog Created successfully'
            }, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({
                'data': str(e),
                'message': 'Something went wrong'
            }, status=status.HTTP_400_BAD_REQUEST)


    def patch(self,request):
        try:
            data  = request.data
            blog = Blog.objects.filter(id=data.get('id'))
            if not blog.exists():
                return Response("Invalid ")
            if request.user  != blog[0].user:
                return Response("You are not authorized to this")
            serializer = BlogSerializer(blog[0],data=data,partial=True)

            if not serializer.is_valid():
                return  Response("Somehing Went Wrong")
            serializer.save()

            return Response({
                'data':serializer.data,
                'meassage':"Blog Updated succesfully"
            })
        
        except Exception as e:
            return Response({
                'data': str(e),
                'message': 'Something went wrong'
            }, status=status.HTTP_400_BAD_REQUEST)
