from django.urls import path
from . import views

urlpatterns = [

    # Get All MenuItems
    path('menu-items',views.get_all_menuitems,name='get_all_menuitems'),

    # Get Single MenuItem
    path('single-menu-item/<int:id>',views.get_single_menuitem, name='get_single_menuitem'),

    # GET Popular Menu items
    path('menu-items/popular', views.popular_menu_items, name="popular-menu-items"),

    # GET ALL Categories
    path('categories',views.get_all_categories, name='get_all_categories'),

    # GET Single Category
    path('category/<int:id>',views.get_single_category, name='get_single_category'),

    # GET ALL Restaurant
    path('restaurants',views.get_all_restaurants, name='get_all_restaurants'),

    # GET Single Restaurant
    path('restaurant/<uuid:uuid>', views.get_single_restaurant, name='get_single_restaurant'),

    # GET Restaurant menu all items by restaurant_id
    path('restaurants/<uuid:restaurant_id>/menu', views.restaurant_menu, name='restaurant-menu'),

    # Get Restaurants itself by category id
    path('categories/<str:category_name>/restaurants',views.restaurants_by_category, name='restaurant-by-category') 

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