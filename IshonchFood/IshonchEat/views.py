from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

from .models import Advertisement, Category, Restaurant, CategoryMenu, MenuItem
from .serializers import AdvertisementSerializer, CategorySerializer,  RestaurantSerializer,CategoryMenuSerializer, MenuItemSerializer 

from drf_spectacular.utils import extend_schema


#1. Advertisement Api end points GET, POST, DELETE
@extend_schema(
    methods=['GET'],
    responses={200: AdvertisementSerializer(many=True)},
    description = "Get popular menu items",
    tags = ["Popular Ads"]
)

@extend_schema(
    methods=['POST'],
    request = AdvertisementSerializer,
    responses={201: AdvertisementSerializer()},
    description="Post popular menu items",
    tags = ["Popular Ads"]
)

# Get and Post All Popular Products
@api_view(['GET','POST'])
def popular_menu_items(request):
    if request.method == 'GET':
        ads = Advertisement.objects.filter(is_active=True).select_related('restaurant')
        serializer = AdvertisementSerializer(ads,many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'POST':
        deserializer = AdvertisementSerializer(data=request.data)
        deserializer.is_valid(raise_exception=True)
        deserializer.save()
        return Response(deserializer.data, status=status.HTTP_201_CREATED)


from drf_spectacular.utils import extend_schema, OpenApiParameter
@extend_schema(
    methods=['DELETE'],
    parameters=[
        OpenApiParameter(
            name="ad_id",
            type=int,
            location=OpenApiParameter.PATH,
            description="Advertisement ID to delete"
        )
    ],
    responses={204:None},
    description="Delete an advertisement",
    tags=["Popular Ads"]
)
@api_view(["DELETE"]) # Add Put method
def delete_advertisement(request,ad_id):
    ads = get_object_or_404(Advertisement, id=ad_id)
    ads.delete()

    return Response(status=status.HTTP_204_NO_CONTENT)



#2. Get and Post General Category
@extend_schema(
    methods=['GET'],
    responses={200: CategorySerializer(many=True)},
    description="Get All General Category",
    tags=['General Category']
)
@extend_schema(
    methods=['POST'],
    request=CategorySerializer,
    responses={201:CategorySerializer()},
    description = "Post A New General Category",
    tags=['General Category']
)

@api_view(['GET','POST'])
def general_category(request):
    if request.method == 'GET':
        categories = Category.objects.values('id','name','sort_order') # auto parse will recieve dict
        serializer = CategorySerializer(categories,many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'POST':
        deserializer = CategorySerializer(data=request.data)
        deserializer.is_valid(raise_exception=True)
        deserializer.save()
        return Response(deserializer.data, status=status.HTTP_201_CREATED)


# Delete and Put General Category





#3. GET ALL Restaurants Swagger
@extend_schema(
    methods=['GET'],
    responses={200: RestaurantSerializer(many=True)},
    description="Retrieve a list of all restaurants.",
    tags=['Restaurants']
)
@extend_schema(
    methods=['POST'],
    request=RestaurantSerializer,
    responses={201: RestaurantSerializer()},
    description="Register a new restaurant.",
    tags=['Restaurants']
)

# GET ALL Restaurants
@api_view(['GET','POST'])
def all_restaurants(request):
    if request.method == 'GET':
        restaurant = Restaurant.objects.select_related('categories').only('id','owner_user_id','categories','name','description','address','restaurant_img',' is_open','created_at','phone_number')
        serializer = RestaurantSerializer(restaurant, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    elif request.method == 'POST':
        deserializer = RestaurantSerializer(data=request.data)
        deserializer.is_valid()
        deserializer.save()
        return Response(deserializer.data, status = status.HTTP_201_CREATED)

# Get Single Restaurant Swagger
@extend_schema(
    methods=['GET'],
    responses={200: RestaurantSerializer},
    description="Retrieve a single restaurant by its UUID.",
    tags=['Restaurants']
)
# Get Single Restaurant
@api_view(['GET']) # add delete, put
def single_restaurant(request, uuid):
    restaurant = get_object_or_404(Restaurant, id=uuid)
    serializer = RestaurantSerializer(restaurant)
    return Response(serializer.data, status=status.HTTP_200_OK)









#4. Get and Post ALL Menu Categories of Restaurant Swagger
@extend_schema(
    methods=['GET'],
    responses={200: CategoryMenuSerializer(many=True)},
    description="Retrieve a list of all categories.",
    tags=['Category Menu of Restaurant']
)
@extend_schema(
    methods=['POST'],
    request=CategoryMenuSerializer,
    responses={201: CategoryMenuSerializer()},
    description="Create a new category.",
    tags=['Category Menu of Restaurant']
)

# Get and Post ALL Menu Categories of Restaurant
@api_view(['GET','POST'])
def all_categories_menu(request):
    if request.method == 'GET':
        categories = CategoryMenu.objects.select_related('restaurant').only(
            # Fields from CategoryMenu
            'id','restaurant','name','sort_order',
            # Fields from the joined Restaurant table (using __)
            'restaurant__id', 'restaurant__owner_user_id','restaurant__categories','restaurant__name',
            'restaurant__description', 'restaurant__address', 'restaurant__restaurant_img', 'restaurant__is_open',
            'restaurant__created_at', 'restaurant__phone_number',
            )
        serializer = CategoryMenuSerializer(categories,many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        deserializer = CategoryMenuSerializer(data=request.data)
        deserializer.is_valid(raise_exception=True)
        deserializer.save()
        return Response(deserializer.data,status=status.HTTP_201_CREATED)




#5. Get and Post ALL MenuItems Swagger
@extend_schema(
    methods=['GET'],
    responses={200: MenuItemSerializer(many=True)},
    description="Retrieve a list of all menu items.",
    tags=['Menu Items']
)
@extend_schema(
    methods=['POST'],
    request=MenuItemSerializer,
    responses={201: MenuItemSerializer()},
    description="Create a new menu item.",
    tags=['Menu Items']
)
# Get and Post ALL MenuItems
@api_view(['GET','POST'])
def menuitems(request):
    if request.method == 'GET':
        menu_items = MenuItem.objects.select_related('restaurant','category')
        serializer = MenuItemSerializer(menu_items,many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    elif request.method == 'POST':
        deserializer = MenuItemSerializer(data=request.data)
        deserializer.is_valid(raise_exception=True)
        deserializer.save()
        return Response(deserializer.data, status=status.HTTP_201_CREATED)







# # GET Restaurant menu all items by restaurant_id
# @extend_schema(
#     methods = ['GET'],
#     responses={200: MenuItemSerializer(many=True)},
#     description="Get all menu items for a restaurant",
#     tags=["Find menu all items by restaurant_id"]
# )

# @api_view(['GET'])
# def restaurant_menu(request, restaurant_id):
#     restaurant = get_object_or_404(Restaurant, id=restaurant_id)

#     menu_items = MenuItem.objects.filter(
#         restaurant = restaurant
#     ).select_related("category")

#     serializer = MenuItemSerializer(menu_items, many=True)
#     return Response(serializer.data, status=status.HTTP_200_OK)


# # Get Restaurants itself by category id
# @extend_schema(
#     methods=['GET'],
#     responses={200:RestaurantSerializer(many=True)},
#     description="Get Restaurants by category_id",
#     tags=["Filter by Category"],
# )
# @api_view(["GET"])
# def restaurants_by_category(request, category_name):
#     restaurants = Restaurant.objects.filter(
#         categories__name__iexact = category_name
#     ).distinct()

#     serializer = RestaurantSerializer(
#         restaurants, many=True
#     )

#     return Response(serializer.data, status=status.HTTP_200_OK)










        




























# --- YORDAMCHI FUNKSIYALAR (Xavfsizlikni tekshirish) ---


# def check_menu_manage_permission(request):
#     """Token ichida 'menu.manage' huquqi borligini tekshiradi"""
#     token_permissions = request.auth.get('permissions',[])
#     return 'menu.manage' in token_permissions

# def check_ownership(request, restaurant_obj):
#     """Token egasi shu restoranning egasi ekanligini tekshiradi"""
#     token_user_id = str(request.auth.get('user_id'))
#     return restaurant_obj.owner_user_id == token_user_id




# @extend_schema(
#     summary="Get all restaurants or create a new one",
#     request=RestaurantSerializer,
#     responses={200: RestaurantSerializer(many=True), 201: RestaurantSerializer}
# )
# # --- API ENDPOINTLAR ---
# @api_view(['GET','POST'])
# # @permission_classes([IsAuthenticated]) # Faqat login qilganlar kira oladi
# def restaurant_list_create(request):
#     """
#     GET  /api/restaurants/     -> Hamma restoranlarni ko'rish (restaurant.read o'rnida)
#     POST /api/restaurants/     -> Yangi restoran yaratish (Faqat 'menu.manage' bilan)
#     """

#     # --- GET: Restoranlar ro'yxatini olish ---
#     if request.method == 'GET':
#         restaurants = Restaurant.objects.all()
#         serializer = RestaurantSerializer(restaurant, many=True)
#         return Response(serializer.data, status= status.HTTP_200_OK)

#     # --- POST: Yangi restoran qo'shish ---
#     elif request.method == "POST":
#         # 1. Huquqni tekshiramiz
#         # if not check_menu_manage_permission(request):
#         #     return Response(
#         #         {"error": "Sizda restoran yaratish uchun 'menu.manage' huquqi yo'q!"}, 
#         #         status=status.HTTP_403_FORBIDDEN
#         #     )
        

#         # 2. Kelgan ma'lumotni validatsiya qilamiz (Pydantic kabi)
#         serializer = RestaurantSerializer(data=request.data)
#         if serializer.is_valid():
#             # Tokendan foydalanuvchi ID sini olib, egasi (owner) qilib saqlaymiz
#             token_user_id = str(request.auth.get('user_id'))
#             serializer.save(owner_user_id=token_user_id)
#             return Response(serializer.data, status=status.HTTP_201_CREATED)

#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# @extend_schema(
#     summary="Get, update or delete a specific restaurant",
#     request=RestaurantSerializer,
#     responses={200: RestaurantSerializer}
# )
# @api_view(['GET','PUT','PATCH','DELETE'])
# # @permission_classes([IsAuthenticated])
# def restaurant_detail(request, id):
#     """
#     Bitta restoran ustida amallar (O'qish hamma uchun, tahrirlash faqat egasiga)
#     """
#     # Bazadan restoranni ID bo'yicha qidiramiz, topilmasa avtomat 404 qaytaradi
#     restaurant = get_object_or_404(Restaurant, id=id)

#     # --- GET: Bitta restoranni o'qish ---
#     if request.method == 'GET':
#             serializer = RestaurantSerializer(restaurant)
#             return Response(serializer.data, status=status.HTTP_200_OK)

#     # --- PUT / PATCH / DELETE: Faqat egasi tahrirlay oladi ---
#     # Birinchi navbatda 'menu.manage' bormi va bu o'sha restoranning egasimi?
#     # if not check_menu_manage_permission(request) or not check_ownership(request, restaurant):
#     #     return Response(
#     #         {"error": "Siz bu restoranning egasi emassiz yoki sizda 'menu.manage' huquqi yo'q!"}, 
#     #         status=status.HTTP_403_FORBIDDEN
#     #     )
    
#     if request.method in ['PUT','PATCH']:
#         # partial=True bu PATCH so'rovi uchun (faqat bitta-ikkita maydonni o'zgartirishga ruxsat beradi)
#         partial = (request.method == 'PATCH')
#         serializer = RestaurantSerializer(restaurant, data=request.data, partial=partial)

#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_200_OK)

#         return Response(serializer.error, status=status.HTTP_400_BAD_REQUEST)

#     elif request.method in ['DELETE']:
#         restaurant.delete()
#         return Response({"message": "Restoran muvaffaqiyatli o'chirildi"}, status=status.HTTP_204_NO_CONTENT)


# @extend_schema(
#     summary="Get the active menu of a restaurant",
#     responses={200: MenuItemSerializer(many=True)}
# )
# @api_view(['GET'])
# # @permission_classes([IsAuthenticated])
# def restaurant_menu(request, id):
#     """
#     GET /api/restaurants/{id}/menu -> Restoranning faqat sotuvda bor taomlarini olish
#     """
#     # Restoran borligini tekshiramiz
#     restaurant = get_object_or_404(Restaurant, id=id)

#     # Shu restaurant tegishli va is_available=True bo'lgan taomlarni olamiz
#     menu_items = MenuItem.objects.filter(restaurant=restaurant, is_available=True)
#     serializer = MenuItemSerializer(menu_items, many=True)
#     return Response(serializer.data, status=status.HTTP_200_OK)



# @extend_schema(
#     summary="Internal endpoint for Order Service validation",
#     responses={200: MenuItemSerializer} # Or construct a custom inline serializer if preferred
# )
# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# def internal_menu_item_check(request, id):
#     """
#     GET /api/internal/menu-items/{id} -> Order servis uchun ichki tekshiruv endpointi
#     """
#     try:
#         item = MenuItem.objects.get(id=id)
#         return Response({
#             "id": item.id,
#             "name": item.name,
#             "price": float(item.price),
#             "currency": item.currency,
#             "is_available": item.is_available # Order servis shu maydon orqali buyurtmani rad etadi
#         }, status=status.HTTP_200_OK)
#     except MenuItem.DoesNotExist:
#         return Response({"error": "Taom topilmadi"}, status=status.HTTP_404_NOT_FOUND)


# # ==========================================
# # 1. KATEGORIYALAR (CATEGORIES) ENDPOINTLARI
# # ==========================================

# @extend_schema(
#     summary="Get all categories",
#     responses={200: CategorySerializer(many=True)}
# )
# @api_view(['GET', 'POST'])
# @permission_classes([IsAuthenticated])
# def category_list_create(request):
#     """
#     GET  /api/categories -> Barcha kategoriyalarni olish
#     POST /api/categories -> Yangi kategoriya yaratish (menu.manage huquqi bilan)
#     """
#     if request.method == 'GET':
#         categories = Category.objects.all()
#         serializer = CategorySerializer(categories, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)

#     elif request.method == 'POST':
#         # if not check_menu_manage_permission(request):
#         #     return Response({"error": "Sizda 'menu.manage' huquqi yo'q!"}, status=status.HTTP_403_FORBIDDEN)
        
#         serializer = CategorySerializer(data=request.data)
#         if serializer.is_valid():
#             # Biznes qoida: Foydalanuvchi faqat o'ziga tegishli restoranga kategoriya qo'sha oladi
#             restaurant = serializer.validated_data['restaurant']
#             if not check_ownership(request, restaurant):
#                 return Response({"error": "Siz faqat o'zingizga tegishli restoranga kategoriya qo'sha olasiz!"}, status=status.HTTP_403_FORBIDDEN)
            
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# # ==========================================
# # 2. TAOMLAR (MENU ITEMS) ENDPOINTLARI
# # ==========================================

# @extend_schema(
#     summary="Create a new menu item",
#     request=MenuItemSerializer,
#     responses={201: MenuItemSerializer}
# )
# @api_view(['POST'])
# @permission_classes([IsAuthenticated])
# def menu_item_create(request):
#     """
#     POST /api/menu-items -> Yangi taom qo'shish (menu.manage)
#     """
#     # if not check_menu_manage_permission(request):
#     #     return Response({"error": "Sizda 'menu.manage' huquqi yo'q!"}, status=status.HTTP_403_FORBIDDEN)

#     serializer = MenuItemSerializer(data=request.data)
#     if serializer.is_valid():
#         restaurant = serializer.validated_data['restaurant']
#         # Xavfsizlik: Boshqa birovning restoraniga taom qo'shib yubormasligini tekshiramiz
#         # if not check_ownership(request, restaurant):
#         #     return Response({"error": "Siz faqat o'zingizga tegishli restoranga taom qo'sha olasiz!"}, status=status.HTTP_403_FORBIDDEN)
        
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_201_CREATED)
#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# @extend_schema(
#     summary="Update a specific menu item",
#     request=MenuItemSerializer,
#     responses={200: MenuItemSerializer}
# )
# @api_view(['PATCH'])
# @permission_classes([IsAuthenticated])
# def menu_item_detail(request, id):
#     """
#     PATCH /api/menu-items/{id} -> Taomni qisman yangilash (menu.manage)
#     """
#     # if not check_menu_manage_permission(request):
#     #     return Response({"error": "Sizda 'menu.manage' huquqi yo'q!"}, status=status.HTTP_403_FORBIDDEN)

#     item = get_object_or_404(MenuItem, id=id)
    
#     # Ownership tekshiruvi: Taom tegishli bo'lgan restoranning egasimi?
#     # if not check_ownership(request, item.restaurant):
#     #     return Response({"error": "Siz bu restoranning egasi emassiz!"}, status=status.HTTP_403_FORBIDDEN)

#     serializer = MenuItemSerializer(item, data=request.data, partial=True)
#     if serializer.is_valid():
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_200_OK)
#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


