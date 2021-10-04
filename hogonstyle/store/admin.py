from django.contrib import admin
from .models import Item, Slide, Color, UserProfile, Address, Order, OrderItem, Refund, Coupon, Size, Set


@admin.register(Color)
class ColorAdmin(admin.ModelAdmin):
    pass


@admin.register(Size)
class SizeAdmin(admin.ModelAdmin):
    pass


@admin.register(Slide)
class SlideAdmin(admin.ModelAdmin):
    pass


# @admin.register(UserProfile)
# class CategoryAdmin(admin.ModelAdmin):
#     pass
#
#
# @admin.register(Order)
# class CategoryAdmin(admin.ModelAdmin):
#     pass
#
#
# @admin.register(Address)
# class CategoryAdmin(admin.ModelAdmin):
#     pass
#
#
# @admin.register(OrderItem)
# class CategoryAdmin(admin.ModelAdmin):
#     pass
#
#
# @admin.register(Refund)
# class CategoryAdmin(admin.ModelAdmin):
#     pass
#
#
# @admin.register(Coupon)
# class CategoryAdmin(admin.ModelAdmin):
#     pass


admin.site.register(Item)
admin.site.register(UserProfile)
admin.site.register(Set)
admin.site.register(Address)
admin.site.register(Order)
admin.site.register(OrderItem)