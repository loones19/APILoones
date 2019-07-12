from django.shortcuts import render
from django.contrib.auth.models import User, Group
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Category, DataPrice, SubCategory
from .serializers import UserSerializer, GroupSerializer, CategorySerializer, SubCategorySerializer, DataPriceSerializer

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class SubCategoryViewSet(viewsets.ModelViewSet):
    queryset = SubCategory.objects.all()
    serializer_class = SubCategorySerializer

    @action(detail=True, methods=['get'])
    def dataprice_by_subcategory(self, request, pk=None):
        """ Return DataPrices to generate Charts in Front-End """
        subcategory = get_object_or_404(SubCategory, pk=pk)

        return Response(
            [
                {'name': subcategory.name,
                 'price': dataprice.price, 
                 'date': dataprice.date
                } for dataprice in DataPrice.objects.filter(subcategory=subcategory).order_by('date')
            ],
        status=status.HTTP_200_OK)


class DataPriceViewSet(viewsets.ModelViewSet):
    queryset = DataPrice.objects.all()
    serializer_class = DataPriceSerializer

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer

class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer