from django.urls import path
from . import views

urlpatterns = [
    path('', views.render_home_page, name='home'),
    path('about/', views.render_about_page, name='about'),
    path('contacts/', views.render_contacts_page, name='contacts'),
    path('faq/', views.render_faq_page, name='faq'),
    path('products/', views.render_articles_page, name='products'),
    path('register/', views.render_register_page, name='register'),
    path('login/', views.render_login_page, name='login'),
    path('profile/',views.render_profile_page,name='profile'),
    path('products/<slug:slug>/',views.render_product_detail_page,name='product_detail'),
    path('products/<int:product_id>/<str:action>/',views.handle_product_action, name='add_action'),
    path('products/<slug:slug>/update/',views.UpdateProduct.as_view(),name='update'),
    path('products/<slug:slug>/delete/',views.DeleteProduct.as_view(),name='delete'),
    path('product/image/<int:pk>/delete/', views.delete_image, name='delete_image'),
    path('basket/',views.render_basket_page,name='basket'),
    path('favourites/',views.render_favourites_page,name='favourite'),
    path('delete/<str:action>/<int:item_id>/', views.delete_item, name='delete_item'),
    path('basket/increase/<int:item_id>/', views.increase_quantity, name='increase_quantity'),
    path('basket/decrease/<int:item_id>/', views.decrease_quantity, name='decrease_quantity'),
    path('contact/', views.contact_view, name='contact'),
    path('buy/', views.render_buy_page, name='buy'),
    path('logout/', views.user_logout, name='logout'),
    path('search/', views.search, name='search'),
]