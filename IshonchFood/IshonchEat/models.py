from django.db import models
import uuid

class Restaurant(models.Model):
    # ID ni UUID formatida o'rnatamiz
    id = models.UUIDField(primary_key=True, default = uuid.uuid4, editable=False)

    # Auth servisdagi userId uchun maydon (FK emas, shunchaki Integer yoki UUID bo'lishi mumkin)
    # Agar u yoqda ham UUID bo'lsa, UUIDField qiling, agar oddiy raqam bo'lsa IntegerField
    owner_user_id = models.IntegerField() # db_index qidiruvni tezlashtiradi


    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    address = models.URLField(max_length=500)
    restaurant_img = models.ImageField(upload_to='restaurant/', blank=True, null=True)
    is_open = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.name

class Category(models.Model):
    # Manually defining the default Django behavior
    id = models.BigAutoField(primary_key=True) 
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='categories')
    name = models.CharField(max_length=100)
    sort_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['sort_order']

        # Bir restoranda bir xil nomli kategoriya takrorlanmasligi uchun:
        unique_together = ('restaurant', 'name')

    def __str__(self):
        return f"{self.restaurant.name} - {self.name}"

class MenuItem(models.Model):
    # Manually defining the default Django behavior
    id = models.BigAutoField(primary_key=True) 
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='menu_items')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='items')
    name = models.CharField(max_length=255)
    description = models.TextField(blank = True, null = True)

    # Pul miqdori uchun har doim DecimalField ishlatiladi
    price = models.DecimalField(max_digits=10, decimal_places=2)
    new_price = models.DecimalField(max_digits=10, decimal_places=2,blank=True, null=True)
    discount = models.DecimalField(max_digits=10, decimal_places=2,blank=True, null=True)
    discount_status = models.BooleanField(default=True)
    promotion = models.CharField(max_length=255)

    img_product = models.ImageField(upload_to='products/', blank=True, null=True)
    delivery_time=models.CharField(max_length=255,blank=True,null=True)

    def __str__(self):
        return self.name + "-----" + self.category.name


class Advertisement(models.Model):
    id = models.BigAutoField(primary_key=True)

    restaurant = models.ForeignKey(
        Restaurant, on_delete=models.CASCADE, related_name="advertisements"
    )
    image_ads = models.ImageField(upload_to="ads/")
    promotion = models.CharField(max_length=255)

    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.restaurant.name} - {self.promotion}"


