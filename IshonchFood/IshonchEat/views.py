from rest_framework.decorators import api_view, permission_classes, authentication_classes
from .authentication import JWTSharedSecretAuthentication
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

from .models import Advertisement, Category, Restaurant, CategoryMenu, MenuItem
from .serializers import AdvertisementSerializer, CategorySerializer,  RestaurantSerializer,CategoryMenuSerializer, MenuItemSerializer,CategoryMenuOfMenuCategorySerializer

from drf_spectacular.utils import extend_schema,extend_schema_view,OpenApiParameter
#from rest_framework.views import APIView

from drf_spectacular.types import OpenApiTypes

from django.db.models import Q



# ==========================================
# 1. ADVERTISEMENT ENDPOINTS
# ==========================================

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
@authentication_classes([JWTSharedSecretAuthentication])
def popular_menu_items(request):
    if request.method == 'GET':
        ads = Advertisement.objects.filter(is_active=True).select_related('restaurant')
        serializer = AdvertisementSerializer(ads,many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        # Guard: Explicit check if user has role.manage or admin access
        if not request.user.is_authenticated or not request.user.has_perm('role.manage'):
            return Response({"detail":"Permission denied."}, status.HTTP_403_FORBIDDEN)

        deserializer = AdvertisementSerializer(data=request.data)
        deserializer.is_valid(raise_exception=True)
        deserializer.save()
        return Response(deserializer.data, status=status.HTTP_201_CREATED)

#class PopularMenuItemsView(APIView):



@extend_schema_view(
    patch=extend_schema(
        description="Update an advertisement completely (Admin Only)",
        parameters=[
            OpenApiParameter(
                name="ad_id",
                type=int,
                location=OpenApiParameter.PATH,
                description="ID of the advertisement to update"
            )
        ],
        request=AdvertisementSerializer,
        responses={200:AdvertisementSerializer},
        tags=['Popular Ads']
    ),
    delete=extend_schema(
        description="Permanently remove an ad from the system (Admin Only).",
        parameters=[
            OpenApiParameter(
                name="ad_id",
                type=int,
                location=OpenApiParameter.PATH,
                description="Advertisement ID to delete"
            )
        ],
        responses={204:None},
        tags=["Popular Ads"]
    )
)

@api_view(["PATCH","DELETE"]) 
@authentication_classes([JWTSharedSecretAuthentication])
def delete_advertisement(request,ad_id):
    # Guard: Only system admins can alter advertising slots
    if not request.user.is_authenticated or not request.user.has_perm('role.manage'):
        return Response({'detail':'Permission denied.'}, status=status.HTTP_403_FORBIDDEN)

    ads = get_object_or_404(Advertisement, id=ad_id)

    if request.method == "PATCH":
        serializer = AdvertisementSerializer(ads,data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == "DELETE":
        ads.delete()
        return Response({"detail":"Ads successfully deleted."},status=status.HTTP_204_NO_CONTENT)


# ==========================================
# 2. GENERAL CATEGORY ENDPOINTS
# ==========================================

#2. Get and Post General Category
@extend_schema(
    methods=['GET'],
    responses={200: CategorySerializer(many=True)},
    description="Get All General Categories (Public)",
    tags=['General Category']
)
@extend_schema(
    methods=['POST'],
    request=CategorySerializer,
    responses={201:CategorySerializer()},
    description = "Post A New General Category (Admin Only)",
    tags=['General Category']
)

@api_view(['GET','POST'])
@authentication_classes([JWTSharedSecretAuthentication])
def general_category(request):
    if request.method == 'GET':
        categories = Category.objects.values('id','name','sort_order') # auto parse will recieve dict
        serializer = CategorySerializer(categories,many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        if not request.user.is_authenticated or not request.user.has_perm('user.manage'):
            return Response({"detail":"Permission denied."},status=status.HTTP_403_FORBIDDEN)

        deserializer = CategorySerializer(data=request.data)
        deserializer.is_valid(raise_exception=True)
        deserializer.save()
        return Response(deserializer.data, status=status.HTTP_201_CREATED)

@extend_schema(
    methods=['PATCH'],
    request=CategorySerializer,
    responses={200:CategorySerializer},
    description="Update A General Category (Admin Only)",
    tags=['General Category']
)
@extend_schema(
    methods =['DELETE'],
    responses={204:None},
    description="DELETE A General Category (Admin Only)",
    tags=['General Category']
)
@api_view(['PATCH','DELETE'])
@authentication_classes([JWTSharedSecretAuthentication])
def general_category_detail(request,id):

    if not request.user.is_authenticated or not request.user.has_perm('user.manage'):
        return Response({"detail":"Permission denied."}, status=status.HTTP_403_FORBIDDEN)
    # Fetch the category or raise a 404 error if it doesn't exist
    category = get_object_or_404(Category, id=id)

    # 1 HANDLE UPDATE (PATCH)
    if request.method == 'PATCH':
        serializer = CategorySerializer(category,data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data,status=status.HTTP_200_OK)

    elif request.method == 'DELETE':
        category.delete()
        return Response({"detail":"A General Category successfully deleted."},status=status.HTTP_204_NO_CONTENT)


# ==========================================
# 3. RESTAURANT PROFILE ENDPOINTS
# ==========================================


#3. GET ALL Restaurants Swagger
@extend_schema(
    methods=['GET'],
    responses={200: RestaurantSerializer(many=True)},
    description="Retrieve a list of all restaurants. (Public)",
    tags=['Restaurants']
)
@extend_schema(
    methods=['POST'],
    request=RestaurantSerializer,
    responses={201: RestaurantSerializer()},
    description="Register a new restaurant. (Admin Only)",
    tags=['Restaurants']
)

# GET ALL Restaurants
@api_view(['GET','POST'])
@authentication_classes([JWTSharedSecretAuthentication])
def all_restaurants(request):
    if request.method == 'GET':
        restaurant = Restaurant.objects.prefetch_related('categories').all().only(
            'id',
            'owner_user_id',
            'name',
            'description',
            'address',
            'restaurant_img',
            'is_open',
            'created_at',
            'phone_number'
        )
        serializer = RestaurantSerializer(restaurant, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    elif request.method == 'POST':
        # Only admin infrastructure assigns new root restaurants
        if not request.user.is_authenticated or not request.user.has_perm('user.manage'):
            return Response({"detail":"Permission denied."}, status=status.HTTP_403_FORBIDDEN)

        deserializer = RestaurantSerializer(data=request.data)
        deserializer.is_valid(raise_exception=True)
        deserializer.save()
        return Response(deserializer.data, status = status.HTTP_201_CREATED)


# Get Single Restaurant Swagger 
@extend_schema_view(
    get=extend_schema(
            description="Fetch a restaurant's full profile details (Authenticated)",
            responses={200: RestaurantSerializer},
            tags=['Restaurants']
    ),
    patch=extend_schema(
        description="Modify an existing restaurant profile (Owner or Admin)",
        request=RestaurantSerializer,
        responses={200:RestaurantSerializer},
        tags=['Restaurants']
    ),
    delete=extend_schema(
        description="Permanently remove a restaurant profile (Admin Only)",
        responses={204:None},
        tags=['Restaurants']
    )

)
# Get Single Restaurant
@api_view(['GET','PATCH','DELETE']) 
@authentication_classes([JWTSharedSecretAuthentication])
def single_restaurant(request, uuid):
    # 1. HANDLE RETRIEVAL (GET) - Highly optimized with prefetching
    if request.method == 'GET':
        # restaurant.read permission allows check profile records
        # if not request.user.is_authenticated or not request.user.has_perm('restaurant.read'):
        #     return Response({"detail":"Permission denied."},status=status.HTTP_403_FORBIDDEN)

        restaurant = get_object_or_404(Restaurant.objects.prefetch_related('categories_menu__items'), id=uuid)
        serializer = RestaurantSerializer(restaurant)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # Fetch the flat record for mutations (PATCH/DELETE)
    restaurant = get_object_or_404(Restaurant,id=uuid)


    # # Ownership guard context validation for mutations
    is_owner = str(restaurant.owner_user_id) == str(request.user.id)
    is_admin = getattr(request.user, 'role', None) == 'ADMIN'


    # 2. HANDLE UPDATE (PATCH)
    if request.method == 'PATCH':

        if not request.user.is_authenticated or not (is_owner or is_admin):
            return Response({"detail":"You do not own this restaurant profile resource."}, status=status.HTTP_403_FORBIDDEN)

        serializer = RestaurantSerializer(restaurant,data=request.data,partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data,status=status.HTTP_200_OK)

    # 3. HANDLE DELETION (DELETE)
    elif request.method == 'DELETE':
        if not request.user.is_authenticated or not is_admin:   
            return Response({"detail": "Only system administrators can drop full restaurants."},status=status.HTTP_403_FORBIDDEN)
        restaurant.delete()
        return Response({"detail":"Restaurant successfully deleted."},status=status.HTTP_204_NO_CONTENT)
    
    

# ==========================================
# 4. MENU CATEGORY TAB ENDPOINTS
# ==========================================

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
    description="Create a new category tab (Restaurant Owner / Admin).",
    tags=['Category Menu of Restaurant']
)


# Get and Post ALL Menu Categories of Restaurant
@api_view(['GET','POST'])
@authentication_classes([JWTSharedSecretAuthentication])
def all_categories_menu(request):
    if request.method == 'GET':
        categories = CategoryMenu.objects.all().select_related('restaurant')
        serializer = CategoryMenuSerializer(categories,many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        # # Ownership validation check for RESTAURANT role
        if request.user.role == "RESTAURANT_OWNER":
            target_restaurant_id = request.data.get('restaurant')
            #  Check if 'owner_user_id' is the correct field name on your Restaurant model!
            restaurant_profile = get_object_or_404(Restaurant, id=target_restaurant_id)
            if str(restaurant_profile.owner_user_id) != str(request.user.id):
                return Response({"detail":"You do not own this target restaurant location."},status=status.HTTP_403_FORBIDDEN)

        deserializer = CategoryMenuSerializer(data=request.data)
        deserializer.is_valid(raise_exception=True)
        deserializer.save()
        return Response(deserializer.data,status=status.HTTP_201_CREATED)


@extend_schema_view(
    get=extend_schema(
        description='get menu category by its id',
        responses={200:CategoryMenuSerializer},
        tags=['Category Menu of Restaurant']
    ),
    patch=extend_schema(
        request=CategoryMenuSerializer,
        responses={200:CategoryMenuSerializer},
        tags=['Category Menu of Restaurant']
    ),
    delete=extend_schema(
        responses={204:None},
        tags=['Category Menu of Restaurant']
    )
)
# DELETE and PATCH Single Menu Categories of Restaurant
@api_view(['GET','PATCH','DELETE'])
@authentication_classes([JWTSharedSecretAuthentication])
def category_menu_detail(request,id):

    category_menu = get_object_or_404(CategoryMenu, id=id) 
    if request.method == 'GET':
        serializer = CategoryMenuSerializer(category_menu)
        return Response(serializer.data,status=status.HTTP_200_OK)
    if not request.user.is_authenticated or not request.user.has_perm('menu.manage'):
        return Response({"detail":"Permission denied."}, status=status.HTTP_403_FORBIDDEN)

     

    # Check ownership
    is_owner=str(category_menu.restaurant.owner_user_id) == str(request.user.id)
    is_admin = request.user.role == "ADMIN"

    if not (is_owner or is_admin):
         return Response({"detail":"You do not have access to alter this restaurant layout."},status=status.HTTP_403_FORBIDDEN)

    if request.method == 'PATCH':
        serializer = CategoryMenuSerializer(category_menu,data=request.data,partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data,status=status.HTTP_200_OK)

    elif request.method == 'DELETE':
        category_menu.delete()

        return Response({"detail":"Category Menu successfully deleted."},status=status.HTTP_204_NO_CONTENT)





# ==========================================
# 5. MENU ITEM (FOOD) ENDPOINTS
# ==========================================

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
@authentication_classes([JWTSharedSecretAuthentication])
def menuitems(request):
    if request.method == 'GET':
        menu_items = MenuItem.objects.prefetch_related('category')
        serializer = MenuItemSerializer(menu_items,many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    elif request.method == 'POST':
        if not request.user.is_authenticated or not request.user.has_perm('menu_manage'):
            return Response({"detail":"Permission denied."}, status=status.HTTP_403_FORBIDDEN)

        if request.user.role == "RESTAURANT_OWNER":
            category_id = request.data.get('category')
            category_menu = get_object_or_404(CategoryMenu,id=category_id)
            if str(category_menu.restaurant.owner_user_id) != str(request.user.id):
                return Response({"detail":"You do not own this category's restaurant menu."},status=status.HTTP_403_FORBIDDEN)

        deserializer = MenuItemSerializer(data=request.data)
        deserializer.is_valid(raise_exception=True)
        deserializer.save()
        return Response(deserializer.data, status=status.HTTP_201_CREATED)

@extend_schema_view(
    get=extend_schema(
        description='Get menuitem by its id',
        responses=MenuItemSerializer(),
        tags=['Menu Items']
    ),
    patch=extend_schema(
        description='Update menu item by its id',
        request=MenuItemSerializer,
        responses=MenuItemSerializer(),
        tags=['Menu Items']
    ),
    delete=extend_schema(
        description='Delete menu item by its id',
        responses={204:None},
        tags=['Menu Items']
    )
)
@api_view(['GET','PATCH','DELETE'])
@authentication_classes([JWTSharedSecretAuthentication])
def menuitem_detail(request,id):

    menuitem = get_object_or_404(MenuItem.objects.prefetch_related('category__restaurant'), id=id)

    if request.method == 'GET':
        serializer = MenuItemSerializer(menuitem)
        return Response(serializer.data,status=status.HTTP_200_OK)

    if not request.user.is_authenticated or not request.user.has_perm('menu.manage'):
        return Response({"detail":"Permission denied."}, status=status.HTTP_403_FORBIDDEN)

    is_owner = str(menuitem.category.restaurant.owner_user_id) == str(request.user.id)
    is_admin = request.user.role == 'ADMIN'

    if not (is_owner or is_admin):
        return Response({"detail":"You do not own the restaurant providing this food item."},status=status.HTTP_403_FORBIDDEN)

    
    if request.method == 'PATCH':
        serializer = MenuItemSerializer(menuitem,data=request.data,partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data,status=status.HTTP_200_OK)

    elif request.method == 'DELETE':
        menuitem.delete()
        return Response({'message':"Delete Menuite successfully"},status=status.HTTP_204_NO_CONTENT)




# ===============================================
# 6, 7, 8, 9 PUBLIC FILTER CHANNELS (Open Access)
# ===============================================

#6. GET Restaurant menu all items by restaurant_id
@extend_schema(
    methods = ['GET'],
    responses={200: MenuItemSerializer(many=True)},
    description="Get all menu items for a specific restaurant by filtering through its menu categories.",
    tags=["Find menu all items by restaurant_id"]
)

@api_view(['GET'])
#@authentication_classes([JWTSharedSecretAuthentication])
def restaurant_menu(request, restaurant_id):
    # 1. Verify that the restaurant exists
    restaurant = get_object_or_404(Restaurant, id=restaurant_id)

    # 2. Filter menu items by spanning across tables:
    # Look at MenuItem -> menu category -> restaurant
    menu_items = MenuItem.objects.filter(
        category__restaurant = restaurant
    ).distinct().prefetch_related("category")

    # 3. Serialize and return the records
    serializer = MenuItemSerializer(menu_items, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@extend_schema(
    methods=['GET'],
    responses={200:CategoryMenuSerializer(many=True)},
    description="get menu category by restaurant_id",
    tags=["Find menu category by restaurant_id"]
)
@api_view(['GET'])
#@authentication_classes([JWTSharedSecretAuthentication])
def restaurant_menu_category(request,restaurant_id):
     # 1. Verify that the restaurant exists
    restaurant = get_object_or_404(Restaurant,id=restaurant_id)

    # 2. Filter menu items by spanning across tables:
    # Look at restaurant -> menu category
    menu_category = CategoryMenu.objects.filter(
        restaurant=restaurant
    ).select_related('restaurant')

    # 3. Serializer and return the records
    serializer = CategoryMenuSerializer(menu_category,many=True)

    return Response(serializer.data, status=status.HTTP_200_OK)






#7. Get Restaurants itself by category id
@extend_schema(
    methods=['GET'],
    # parameters = [
    #     OpenApiParameter(
    #         name='category_name',
    #         type=OpenApiTypes.STR,
    #         location=OpenApiParameter.QUERY,
    #         required = True,
    #         description="The name of the category to filter restaurants by (e.g., FastFood)"
    #     )
    # ],
    responses={200:RestaurantSerializer(many=True)},
    description="Get Restaurants by category_id",
    tags=["Filter restaurants by General Category"],
)
@api_view(["GET"])
#@authentication_classes([JWTSharedSecretAuthentication])
def restaurants_by_category(request,category_name):
    # category_name=request.query_params.get('category_name',None)

    # if not category_name:
    #     return Response({"detail":"category_name query parameter is required."},
    #     status=status.HTTP_400_BAD_REQUEST)

    restaurants = Restaurant.objects.filter(
        categories__name__iexact = category_name
    ).distinct()

    serializer = RestaurantSerializer(
        restaurants, many=True
    )
    return Response(serializer.data, status=status.HTTP_200_OK)


#8. Get all menu items for a specific restaurant under a specific menu category section (e.g., Only Burgers from KFC).
@extend_schema(
    methods=['GET'],
    responses={200:MenuItemSerializer(many=True)},
    description="Get all menu items for a specific restaurant under a specific menu category section (e.g., Only Burgers from KFC).",
    tags=["Get all menu items of restaurant with specific menu category"]
)
@api_view(['GET'])
#@authentication_classes([JWTSharedSecretAuthentication])
def menu_items_by_category(request,restaurant_id,category_menu_name):
    # 1. Safety Check: Verify the restaurant exists
    restaurant = get_object_or_404(Restaurant, id=restaurant_id)
    
    # 2. Safety Check: Verify the category menu exists using the correct field name ('name')
    category_menu = get_object_or_404(
        CategoryMenu, 
        name__iexact=category_menu_name, 
        restaurant=restaurant
    )
    
    # 3. Fetch the menu items belonging to this verified category tab
    # select_related("category") is used here to avoid N+1 query lookup costs
    menu_items = MenuItem.objects.filter(category=category_menu).distinct().prefetch_related("category")
    
    # 4. Serialize and return the response array
    serializer = MenuItemSerializer(menu_items, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

# 9
@extend_schema(
    methods=['GET'],
    responses={200:CategoryMenuOfMenuCategorySerializer(many=True)},
    description="Provide nested category menu -> menu items inside.",
    tags=['Resturant Category Menu -> Menu Items']
)
@api_view()
#@authentication_classes([JWTSharedSecretAuthentication])
def restaurant_menu_detail(request,restaurant_id):
    categories = (
        CategoryMenu.objects.filter(restaurant_id=restaurant_id)
    ).prefetch_related("items")

    serializer = CategoryMenuOfMenuCategorySerializer(categories, many=True)

    return Response(serializer.data, status=status.HTTP_200_OK)



# 10 Searching bar for frontend
# ==========================================
# PUBLIC GLOBAL SEARCH ENDPOINT
# ==========================================

@extend_schema(
    methods=['GET'],
    parameters=[
        OpenApiParameter(
            name='query',
            type=OpenApiTypes.STR,
            location=OpenApiParameter.QUERY,
            required=True,
            description="Search keyword for restaurant names or menu items (e.g., 'lavash')"
        )
    ],
    responses={
        200: OpenApiTypes.OBJECT
    },
    description="Global search across restaurants and menu items.",
    tags=['Search']
)
@api_view(['GET'])
#@authentication_classes([JWTSharedSecretAuthentication])
def global_search(request):
    query = request.query_params.get('query', '').strip()
    
    if not query:
        return Response({
            "restaurants": [],
            "items": []
        }, status=status.HTTP_200_OK)

    # We use Q directly here, completely removing "models.Q"
    restaurants = Restaurant.objects.filter(
        Q(name__icontains=query) | Q(description__icontains=query)
    ).distinct().prefetch_related('categories')

    items = MenuItem.objects.filter(
        Q(name__icontains=query) | Q(description__icontains=query)
    ).distinct().prefetch_related('category')

    restaurant_serializer = RestaurantSerializer(restaurants, many=True)
    item_serializer = MenuItemSerializer(items, many=True)

    return Response({
        "restaurants": restaurant_serializer.data,
        "items": item_serializer.data
    }, status=status.HTTP_200_OK)
