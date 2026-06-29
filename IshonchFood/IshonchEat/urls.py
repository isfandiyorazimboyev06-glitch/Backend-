from django.urls import path
from . import views

urlpatterns = [

    #1. GET, POST and DELETE Popular Menu items
    path("ads", views.popular_menu_items),
    path("ads/<int:ad_id>",views.delete_advertisement),

    #2. GET, POST General Category of Restaurant
    path("general-category", views.general_category, name='general_category'),

    #3. GET ALL Restaurants
    path('restaurants',views.all_restaurants, name='all_restaurants'),
    path('restaurant/<uuid:uuid>', views.single_restaurant, name='single_restaurant'), # GET Single Restaurant


    #4. GET ALL Menu Categories of Restaurnat
    path('menu-category',views.all_categories_menu, name='all_categories_menu'),

    #5. Get All MenuItems of Restaurant
    path('menu-items',views.menuitems,name='all_menuitems'),











    # Get Single MenuItem
    # path('single-menu-item/<int:id>',views.get_single_menuitem, name='get_single_menuitem'),

 



    

    # GET Single Category
   # path('category/<int:id>',views.get_single_category, name='get_single_category'),



    # GET Restaurant menu all items by restaurant_id
   path('restaurants/<uuid:restaurant_id>/menu', views.restaurant_menu, name='restaurant-menu'),

    # Get Restaurants itself by category id
   path('categories/<str:category_name>/restaurants',views.restaurants_by_category, name='restaurant-by-category'),

   # Get Menu items filtered by restaurant id and menu category
   path('restaurants/<uuid:restaurant_id>/menu-categories/<str:category_menu_name>/items',views.menu_items_by_category,
   name='restaurant-menu-items-by-category'), 

    # # Restoranlar
    # path('restaurants/', views.restaurant_list_create, name='restaurant-list-create'),
    # path('restaurants/<uuid:id>/', views.restaurant_detail, name='restaurant-detail'),
    # path('restaurants/<uuid:id>/menu', views.restaurant_menu, name='restaurant-menu'),

    # # Kategoriyalar (Yangi qo'shildi)
    # path('categories/', views.category_list_create, name='category-list-create'),
    
    # # Taomlar / Menu Items (Yangi qo'shildi)
    # path('menu-items/', views.menu_item_create, name='menu-item-create'),
    # path('menu-items/<int:id>/', views.menu_item_detail, name='menu-item-detail'),

    # # Ichki API (Order servis uchun)
    # path('internal/menu-items/<int:id>', views.internal_menu_item_check, name='internal-item-check'),
]