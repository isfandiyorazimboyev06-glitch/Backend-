from rest_framework import serializers
from .models import Advertisement, Category, CategoryMenu, Restaurant, MenuItem 



class AdvertisementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Advertisement
        fields = ['id', 'restaurant','image_ads','promotion']  

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id','name']
        
class RestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = ['id','owner_user_id','name','description','address','is_open','created_at','restaurant_img','categories']
        read_only_fields = ['id','created_at','owner_user_id']
        # owner_user_id ni requestdan emas, tokendan olamiz!


class CategoryMenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoryMenu
        fields = ['id','restaurant','name']



class MenuItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuItem
        fields = [
            'id',
            'restaurant', 'category',
            'name', 'description',
            'price', 'new_price', 'discount',
            'discount_status', 'promotion',
            'img_product', 'delivery_time'
        ]


