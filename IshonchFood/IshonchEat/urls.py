from django.urls import path
from . import views

urlpatterns = [

    #1. GET, POST and DELETE Popular Menu items
    path("ads", views.popular_menu_items),
    path("ads/<int:ad_id>",views.delete_advertisement),

    #2. GET, POST General Category of Restaurant
    path("general-category", views.general_category, name='general-category'),
    path("general-category/<int:id>",views.general_category_detail, name='general-category-detail'),

    #3. GET ALL Restaurants
    path('restaurants',views.all_restaurants, name='all-restaurants'),
    path('restaurant/<uuid:uuid>', views.single_restaurant, name='single-restaurant'), # GET Single Restaurant


    #4. GET ALL Menu Categories of Restaurnat
    path('menu-category',views.all_categories_menu, name='all-categories-menu'),
    path('menu-category/<int:id>',views.category_menu_detail, name='category-menu-detail'),

    #5. Get All MenuItems of Restaurant
    path('menu-items',views.menuitems,name='all-menuitems'),
    path('menu-items/<int:id>',views.menuitem_detail,name='menuitem-detail'),

    #6. GET Restaurant menu all items by restaurant-id
    path('restaurants/<uuid:restaurant_id>/menu', views.restaurant_menu, name='restaurant-menu'),

    #7. Get Restaurants itself by category id
    path('category/restaurants/<str:category_name>',views.restaurants_by_category, name='restaurant-by-category'),

    #8. Get Menu items filtered by restaurant id and menu category
    path('restaurants/<uuid:restaurant_id>/menu_categories/<str:category_menu_name>/items',views.menu_items_by_category,
    name='restaurant-menu-items-by-category'), 

    #9
    path("restaurants/<uuid:restaurant_id>/menu-items",views.restaurant_menu_detail),










    # Get Single MenuItem
    # path('single-menu-item/<int:id>',views.get-single-menuitem, name='get-single-menuitem'),

 



    

    # GET Single Category
   # path('category/<int:id>',views.get-single-category, name='get-single-category'),





    # # Restoranlar
    # path('restaurants/', views.restaurant-list-create, name='restaurant-list-create'),
    # path('restaurants/<uuid:id>/', views.restaurant-detail, name='restaurant-detail'),
    # path('restaurants/<uuid:id>/menu', views.restaurant-menu, name='restaurant-menu'),

    # # Kategoriyalar (Yangi qo'shildi)
    # path('categories/', views.category-list-create, name='category-list-create'),
    
    # # Taomlar / Menu Items (Yangi qo'shildi)
    # path('menu-items/', views.menu-item-create, name='menu-item-create'),
    # path('menu-items/<int:id>/', views.menu-item-detail, name='menu-item-detail'),

    # # Ichki API (Order servis uchun)
    # path('internal/menu-items/<int:id>', views.internal-menu-item-check, name='internal-item-check'),
]