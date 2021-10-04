from django.urls import path

from . import views
from .views import add_to_cart, remove_single_item_from_cart

urlpatterns = [
    path('', views.index, name='index'),
    # path('products', views.products, name='products'),
    path('register', views.register, name='register'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('products/street', views.products_street, name='products-street'),
    path('products/<category>/<subcategory>', views.products, name='products'),
    path('products/<int:item_id>', views.product_detail, name='product-detail'),
    path('sets', views.sets, name='sets'),
    path('sets/<int:set_id>', views.sets_details, name='sets-details'),
    path('add-to-cart/<int:id>>', add_to_cart, name='add-to-cart'),
    # path('remove-from-cart/<int:id>', remove_from_cart, name='remove-from-cart'),
    path('remove-item-from-cart/<int:id>', remove_single_item_from_cart,
         name='remove-single-item-from-cart'),
    path('add-to-set/<int:id>>', views.add_to_set, name='add-to-set'),
    path('remove-from-set/<int:id>>', views.remove_from_set, name='remove_from_set'),
    path('add-all-to-order/<int:id>>', views.add_all_to_order, name='add-all-to-order'),
    path('add-address', views.add_address, name='add-address'),
    path('update-address', views.update_address, name='update-address'),
    path('checkout', views.checkout, name='checkout'),
    path('cart', views.cart, name='cart'),
    path('profile', views.profile, name='profile'),
    path('profile-update', views.update_profile, name='profile-update'),
    path('profile/address', views.profile_address, name='profile-address'),
    path('profile/orders', views.profile_orders, name='profile-orders'),
    path('profile/change-password', views.profile_password, name='profile-password'),
    path('about', views.about, name='about'),
    path('contact', views.contact, name='contact'),
    path('faq', views.faq, name='faq'),
    path('delivery', views.delivery, name='delivery'),
    path('in-person-store', views.in_person_store, name='in-person-store'),
    path('payment', views.payment, name='payment'),
    path('privacy', views.privacy, name='privacy'),
    path('refunding', views.refunding, name='refunding'),
    path('size-guide', views.size_guide, name='size-guide'),
]
