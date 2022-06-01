from django.shortcuts import render

from rest_framework import viewsets
from rest_framework import permissions

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics

from rest_framework.decorators import api_view
from rest_framework.reverse import reverse

from .serializers import ValueSerializer, SkillSerializer, ExperienceSerializer, UserCreateSerializer, UserDetailSerializer
from .models import Value, Skill, Experience
from .permissions import OwnerOnly, UserOnly, UnauthenticatedOnly
from django.contrib.auth.models import User

from django.shortcuts import redirect

# Create your views here.
class ValueViewset(viewsets.ModelViewSet):
    queryset = Value.objects.all()
    serializer_class = ValueSerializer
    permission_classes = [permissions.IsAuthenticated, OwnerOnly]
    
    def get_queryset(self):
        queryset = self.queryset
        queryset = queryset.filter(owner__exact=self.request.user)
        
        valueFilterName = self.request.query_params.get('valueFilterName', False)
        if (valueFilterName):
            queryset = queryset.filter(name__icontains = valueFilterName)
        
        return queryset
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, many=isinstance(request.data,list))
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
    def perform_create(self, serializer):
        item = serializer.save(owner = self.request.user)
        if (type(item) is not list):
            old_exp_array = item.experiences.all()
            new_exp_array = []
            for exp in old_exp_array:
                if exp.owner == self.request.user:
                    new_exp_array.append(exp)

            item.experiences.set(new_exp_array)
            item.save()
        else :
            for instance in item:
                instance.save()
            

        
    def perform_update(self, serializer):
        instance = serializer.save(owner = self.request.user)
        old_exp_array = instance.experiences.all()
        new_exp_array = []
        for exp in old_exp_array:
            if exp.owner == self.request.user:
                new_exp_array.append(exp)
                
        serializer.save(experiences=new_exp_array)
    
class SkillViewset(viewsets.ModelViewSet):
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer
    permission_classes = [permissions.IsAuthenticated, OwnerOnly]
    
    def get_queryset(self):
        queryset = self.queryset
        queryset = queryset.filter(owner__exact=self.request.user)
        
        skillFilterName = self.request.query_params.get('skillFilterName', False)
        if (skillFilterName):
            queryset = queryset.filter(name__icontains = skillFilterName)
        
        return queryset
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, many=isinstance(request.data,list))
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
    def perform_create(self, serializer):
        item = serializer.save(owner = self.request.user)
        if (type(item) is not list):
            old_exp_array = item.experiences.all()
            new_exp_array = []
            for exp in old_exp_array:
                if exp.owner == self.request.user:
                    new_exp_array.append(exp)

            item.experiences.set(new_exp_array)
            item.save()
        else :
            for instance in item:
                instance.save()
        
    def perform_update(self, serializer):
        instance = serializer.save(owner = self.request.user)
        old_exp_array = instance.experiences.all()
        new_exp_array = []
        for exp in old_exp_array:
            if exp.owner == self.request.user:
                new_exp_array.append(exp)
                
        serializer.save(experiences=new_exp_array)
    
class ExperienceViewset(viewsets.ModelViewSet):
    queryset = Experience.objects.all()
    serializer_class = ExperienceSerializer
    permission_classes = [permissions.IsAuthenticated, OwnerOnly]
    
    def get_queryset(self):
        queryset = self.queryset
        queryset = queryset.filter(owner__exact=self.request.user)
        return queryset
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, many=isinstance(request.data,list))
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
    def perform_create(self, serializer):
        item = serializer.save(owner = self.request.user)
        if (type(item) is not list):
            old_value_array = item.value_set.all()
            new_value_array = []
            for value in old_value_array:
                if value.owner == self.request.user:
                    new_value_array.append(value)
            
            old_skill_array = item.skill_set.all()
            new_skill_array = []
            for skill in old_skill_array:
                if skill.owner == self.request.user:
                    new_skill_array.append(skill)
                    
            item.skill_set.set(new_skill_array)
            item.value_set.set(new_value_array)
            item.save()
        else:
            for instance in item:
                instance.save()
        
    def perform_update(self, serializer):
        instance = serializer.save(owner = self.request.user)
        
        old_value_array = instance.value_set.all()
        new_value_array = []
        for value in old_value_array:
            if value.owner == self.request.user:
                new_value_array.append(value)
        
        old_skill_array = instance.skill_set.all()
        new_skill_array = []
        for skill in old_skill_array:
            if skill.owner == self.request.user:
                new_skill_array.append(skill)

        serializer.save(skill_set=new_skill_array, value_set=new_value_array)

class CurrentUser(APIView):
    def get(self, request):
        if (request.user.is_authenticated):
            return redirect('user-detail', pk=request.user.id)
    
        return redirect('signup')

class UserSignup(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer
    permission_classes = [permissions.AllowAny, UnauthenticatedOnly]

class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserDetailSerializer
    permission_classes = [permissions.IsAuthenticated, UserOnly]
    
    def get_queryset(self):
        return self.queryset.filter(username__exact=str(self.request.user))
        
class Home(APIView):
    def get(self, request):
        return Response({
            'VSE': reverse('api-root', request=request),
            'User': reverse('current-user', request=request),
            'Signup': reverse('signup', request=request),
        })