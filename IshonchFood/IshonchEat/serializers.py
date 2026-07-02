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
    # 1. Accepts Primary Key IDs [1, 2, 3] on POST inputs
    categories = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Category.objects.all()
    )
    class Meta:
        model = Restaurant
        fields = ['id','owner_user_id','name','description','address','is_open','created_at','restaurant_img','categories']
        # Highlight: Make this read-only so it's handled automatically
        read_only_fields = ['id','owner_user_id','created_at'] 

    # 2. Automatically converts those IDs into nested objects on GET outputs
    def to_representation(self,instance):
        representation = super().to_representation(instance)
        # We replace the list of IDs with serialized category objects for GET responses
        representation['categories'] = CategorySerializer(instance.categories.all(), many=True).data
        return representation


class CategoryMenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoryMenu
        fields = ['id','restaurant','name']



class MenuItemSerializer(serializers.ModelSerializer):
    category = CategoryMenuSerializer(many=True, read_only=True)
    class Meta:
        model = MenuItem
        fields = [
            'id', 'category',
            'name', 'description',
            'price', 'new_price', 'discount',
            'discount_status', 'promotion',
            'img_product', 'delivery_time'
        ]


class CategoryMenuOfMenuCategorySerializer(serializers.ModelSerializer):
    items=MenuItemSerializer(many=True,read_only=True)
    class Meta:
        model = CategoryMenu
        fields = ['id','restaurant','name','items']



