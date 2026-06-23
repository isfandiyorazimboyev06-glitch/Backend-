from rest_framework import serializers
from .models import Restaurant, Category, MenuItem

class RestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = ['id','owner_user_id','name','description','address','is_open','created_at']
        read_only_fields = ['id','created_at','owner_user_id']
        # owner_user_id ni requestdan emas, tokendan olamiz!




class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id','restaurant','name','sort_order']

class MenuItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuItem
        fields = [
            'id',
            'restaurant', 'category',
            'name', 'description',
            'price', 'new_price', 'discount',
            'status', 'promotion',
            'image_url', 'delivery_time'
        ]

class PopularPromotionSerializer(serailizers.ModelSerializer):
    class Meta:
        model = MenuItem
        fields = ['id', 'restaurant','name','image_url','promotion']