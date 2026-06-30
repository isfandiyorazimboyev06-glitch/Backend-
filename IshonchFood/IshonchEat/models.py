from django.db import models
import uuid







# General Category (Global categories like Fast Food, Sweets, Sushe, etc.)
class Category(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=100,unique=True)
    sort_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['sort_order']

    def __str__(self):
        return self.name


    


# Restaurants
class Restaurant(models.Model):
    # Set UUID format
    id = models.UUIDField(primary_key=True, default = uuid.uuid4, editable=False)

    owner_user_id = models.IntegerField(db_index=True) # db_index qidiruvni tezlashtiradi
    categories = models.ManyToManyField(
        Category,
        related_name='restaurants',
        blank=True
    )


    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    address = models.URLField(max_length=500)
    restaurant_img = models.ImageField(upload_to='restaurant/', blank=True, null=True)
    is_open = models.BooleanField(default=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    phone_number = models.CharField(max_length=20,default="+998971234567")


    def __str__(self):
        return self.name

# Advertisement Banner
class Advertisement(models.Model):
    id = models.BigAutoField(primary_key=True)

    restaurant = models.ForeignKey(
        Restaurant, on_delete=models.CASCADE, related_name="advertisements"
    )
    image_ads = models.ImageField(upload_to="ads/")
    promotion = models.CharField(max_length=255)

    is_active = models.BooleanField(default=True, db_index=True)

    def __str__(self):
        return f"{self.restaurant.name} - {self.promotion}"
        

# Category Menu of Restaurant (Internal categories like "Burgers", "Drinks")
class CategoryMenu(models.Model):
    # Manually defining the default Django behavior
    id = models.BigAutoField(primary_key=True) 
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='categories_menu')
    name = models.CharField(max_length=100)
    sort_order = models.PositiveIntegerField(default=0)

    class Meta: 
        ordering = ['sort_order']

        # Prevents duplicate local categories in the same restaurant
        unique_together = ('restaurant', 'name')

    def __str__(self):
        return f"{self.restaurant.name} -> {self.name}"




# Restaurants MenuItem
class MenuItem(models.Model):
    # Manually defining the default Django behavior
    id = models.BigAutoField(primary_key=True) 
    #restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='menu_items')
    category = models.ManyToManyField(CategoryMenu, related_name='items')
    name = models.CharField(max_length=255)
    description = models.TextField(blank = True, null = True)

    
    price = models.DecimalField(max_digits=10, decimal_places=2)
    new_price = models.DecimalField(max_digits=10, decimal_places=2,blank=True, null=True)
    discount = models.DecimalField(max_digits=10, decimal_places=2,blank=True, null=True)
    discount_status = models.BooleanField(default=False)
    promotion = models.CharField(max_length=255, blank=True, null=True)

    img_product = models.ImageField(upload_to='products/', blank=True, null=True)
    delivery_time=models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.name} (ID: {self.id})"





