from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

from .models import Restaurant, MenuItem, Category
from .serializers import RestaurantSerializer, MenuItemSerializer, CategorySerializer

from drf_spectacular.utils import extend_schema


# Get ALL MenuItems
@api_view(['GET','POST'])
def get_all_menuitems(request):
    if request.method == 'GET':
        menu_items = MenuItem.objects.select_related('restaurant','category').all()
        serializer = MenuItemSerializer(menu_items,many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    elif request.method == 'POST':
        deserializer = MenuItemSerializer(data=request.data)
        deserializer.is_valid(raise_excaption=True)
        deserializer.save()
        return Response(deserializer.data, status=status.HTTP_201_CREATED)


# Get Single MenuItem
@api_view(['GET'])
def get_single_menuitem(request, id):
    menu_item = get_object_or_404(MenuItem, id=id)
    serializer = MenuItemSerializer(menu_item)
    return Response(serializer.data,status=status.HTTP_200_OK)



# Get ALL Categories
@api_view(['GET','POST'])
def get_all_categories(request):
    if request.method == 'GET':
        categories = Category.objects.select_related('restaurant').all()
        serializer = CategorySerializer(categories,many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        deserializer = CategorySerializer(data=request.data)
        deserializer.is_valid(raise_excaption=True)
        deserializer.save()
        return Response(deserializer.data,status=status.HTTP_201_CREATED)

# Get Single Category
@api_view(['GET'])
def get_single_category(request,id):
    category = get_object_or_404(Category, id=id)
    serializer = CategorySerializer(category)
    return Response(serializer.data, status=status.HTTP_200_OK)


# GET ALL Restaurants
@api_view(['GET','POST'])
def get_all_restaurants(request):
    if request.method == 'GET':
        restaurant = Restaurant.objects.all()
        serializer = RestaurantSerializer(restaurant, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    elif request.method == 'POST':
        deserializer = RestaurantSerializer(data=request.data)
        deserializer.is_valid()
        deserializer.save()
        return Response(deserializer.data, status = status.HTTP_201_CREATED)

# Get Single Restaurant
@api_view(['GET'])
def get_single_restaurant(request, uuid):
    restaurant = get_object_or_404(Restaurant, id=uuid)
    serializer = RestaurantSerializer(restaurant)
    return Response(serializer.data, status=status.HTTP_200_OK)
        




























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


