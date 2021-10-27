from django.contrib import admin
from .models import Item, Color, UserProfile, Address, Order, OrderItem, Refund, Coupon, Size, Set, SiteSettings


@admin.register(Color)
class ColorAdmin(admin.ModelAdmin):
    pass


@admin.register(Size)
class SizeAdmin(admin.ModelAdmin):
    pass

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = (
    'id', 'title', 'category', 'sub_category', 'price', 'discount_price', 'timestamp', 'is_active')
    list_display_links = ('id', 'title')
    list_filter = ('category', 'sub_category')
    list_editable = ('is_active',)
    search_fields = ('title', 'price', 'discount_price', 'category', 'sub_category')
    list_per_page = 25


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
    'id', 'user', 'code', 'order_date', 'deliver_method', 'payment_method', 'do_factor', 'payment', 'desc', 'state', 'ordered', 'get_total_discounted', 'get_final_payment')
    list_display_links = ('id', 'code')
    list_filter = ('state', 'ordered')
    list_editable = ('state',)
    search_fields = ('id', 'user', 'code', 'order_date', 'state')
    list_per_page = 50


admin.site.register(SiteSettings)
admin.site.register(UserProfile)
admin.site.register(Set)
admin.site.register(Address)
admin.site.register(OrderItem)
