import shortuuid

from django.conf import settings
from django.contrib import auth
from django.contrib.auth.models import AbstractUser
from django.db import models
from colorful.fields import RGBColorField
from django.urls import reverse

LABEL_CHOICES = (
    ('S', 'معمولی'),
    ('N', 'جدید'),
    ('F', 'مشخص شده')
)

CATEGORY_CHOICES = (
    ('MA', 'مردانه'),
    ('WO', 'زنانه'),
    ('AC', 'اکسسوری'),
    ('ST', 'استریت'),
)

SUBCATEGORY_CHOICES = (
    ('TS', 'تی شرت'),
    ('PS', 'پولوشرت'),
    ('SH', 'پیراهن'),
    ('HO', 'سویشرت و هودی'),
    ('PA', 'کاپشن و پالتو'),
    ('BA', 'بافت'),
    ('DO', 'دورس'),
    ('JE', 'شلوار جین'),
    ('SP', 'شلوار پارچه ای'),
    ('SK', 'شلوار کتان'),
    ('SS', 'شلوارک'),
    ('KK', 'کفش کتانی'),
    ('SN', 'صندل'),
    ('RS', 'کفش رسمی'),
    ('MB', 'کیف پول و جاکارتی'),
    ('BS', 'کیف کمری'),
    ('SC', 'شال'),
    ('CA', 'کلاه و کپ'),
    ('BE', 'کمربند'),
    ('SO', 'جوراب'),
    ('LA', 'لندیارد'),
    ('FA', 'فندک'),
    ('DE', 'دکوری'),
    ('MA', 'مانتو'),
    ('TP', 'تاپ'),
    ('BL', 'بلوز و شومیز'),
    ('BB', 'کیف دستی و دوشی'),
    ('BP', 'کوله پشتی'),
)

SHIRT_SIZE_CHOICES = (
    ('S', 'S'),
    ('M', 'M'),
    ('L', 'L'),
    ('XL', 'XL'),
    ('2XL', '2XL'),
    ('3XL', '3XL'),
    ('4XL', '4XL'),
    ('FS', 'FS'),
)

ORDER_STATE = (
    ('در حال بررسی', 'در حال بررسی'),
    ('در حال آماده سازی', 'در حال آماده سازی'),
    ('ارسال شده', 'ارسال شده'),
    ('تحویل گرفته شده', 'تحویل گرفته شده'),
)


def get_upload_path(instance, filename):
    model = instance.__class__._meta
    name = model.verbose_name_plural.replace(' ', '_')
    title = instance.title.replace(' ', '_')

    return f'images/{name}/{title}/{filename}'


class UserProfile(AbstractUser):
    # user = models.OneToOneField(
    #     settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    user_code = models.CharField(verbose_name="کد مشتری", default=shortuuid.random(length=8), editable=False,
                                 max_length=8, blank=False)
    phone = models.CharField("شماره موبایل", max_length=12, blank=True)
    full_name_bank = models.CharField("نام صاحب حساب", max_length=100, blank=True)
    bank_name = models.CharField("نام بانک", max_length=50, blank=True)
    sheba = models.CharField("شماره شبا", max_length=26, blank=True)

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = "کاربر"
        verbose_name_plural = "کاربرها"


class SiteSettings(models.Model):
    pass


class Slide(models.Model):
    settgs = models.ForeignKey(SiteSettings, verbose_name="تنظیمات", on_delete=models.DO_NOTHING)
    link = models.CharField("لینک", max_length=100, blank=True)
    image = models.ImageField("عکس", help_text="Size: 1920x570")
    is_active = models.BooleanField("فعال بودن", default=True)

    def __str__(self):
        return "{} - {}".format(self.caption1, self.caption2)

    class Meta:
        verbose_name = "اسلاید"
        verbose_name_plural = "اسلایدها"


class Color(models.Model):
    tag = models.CharField(max_length=200)
    color = RGBColorField(colors=['#FF0000', '#00FF00', '#0000FF'])

    def __str__(self):
        return self.tag

    class Meta:
        verbose_name = "رنگ"
        verbose_name_plural = "رنگها"


#
# class Category(models.Model):
#     title = models.CharField("عنوان", max_length=200)
#     slug = models.SlugField("کد دسته بندی")
#     description = models.TextField("توضیحات")
#     image = models.ImageField("عکس")
#     is_active = models.BooleanField("فعالیت", default=True)
#
#     def __str__(self):
#         return self.title
#
#     def get_absolute_url(self):
#         return reverse("core:category", kwargs={
#             'slug': self.slug
#         })
#
#     class Meta:
#         verbose_name = "دسته بندی"
#         verbose_name_plural = "دسته بندیها"


class Size(models.Model):
    name = models.CharField("نام", max_length=10)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "سایز"
        verbose_name_plural = "سایزها"


class Item(models.Model):
    title = models.CharField("عنوان", max_length=200)
    price = models.IntegerField("قیمت اصلی")
    discount_price = models.IntegerField("قیمت با تخفیف", blank=True, null=True)
    colors = models.ManyToManyField(Color, verbose_name="رنگ ها")
    sizes = models.ManyToManyField(Size, verbose_name="سایزها")
    category = models.CharField("دسته بندی", choices=CATEGORY_CHOICES, max_length=2)
    sub_category = models.CharField("زیر دسته", choices=SUBCATEGORY_CHOICES, max_length=2)
    # label = models.CharField("برچسب", choices=LABEL_CHOICES, max_length=1)
    description = models.TextField("توضیحات")
    is_active = models.BooleanField("موجود است؟", default=True)
    timestamp = models.DateTimeField("تاریخ و زمان ایجاد", auto_now_add=True)
    image_1 = models.ImageField("عکس 1", upload_to=get_upload_path)
    image_2 = models.ImageField("عکس 2", upload_to=get_upload_path)
    image_3 = models.ImageField("عکس 3", upload_to=get_upload_path)
    image_4 = models.ImageField("عکس 4", upload_to=get_upload_path)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("core:product", kwargs={
            'id': self.id
        })

    def get_price(self):
        if self.discount_price:
            return self.discount_price
        else:
            return self.price

    def get_add_to_cart_url(self):
        return reverse("core:add-to-cart", kwargs={
            'id': self.id,
            'size': self.size,

        })

    def get_remove_from_cart_url(self):
        return reverse("core:remove-from-cart", kwargs={
            'id': self.id
        })

    class Meta:
        verbose_name = "آیتم"
        verbose_name_plural = "آیتمها"


class Set(models.Model):
    items = models.ManyToManyField(Item, verbose_name="آیتم ها")
    title = models.CharField("عنوان", max_length=200)
    is_active = models.BooleanField("موجود است؟", default=True)
    timestamp = models.DateTimeField("تاریخ و زمان ایجاد", auto_now_add=True)
    image = models.ImageField("عکس 1", upload_to=get_upload_path)

    class Meta:
        verbose_name = "ست"
        verbose_name_plural = "ستها"


class OrderItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE, verbose_name="کاربر")
    ordered = models.BooleanField("سفارش داده شده", default=False)
    size = models.CharField("سایز", max_length=3)
    color = models.CharField("رنگ", max_length=50)
    item = models.ForeignKey(Item, on_delete=models.CASCADE, verbose_name="آیتم")
    quantity = models.IntegerField("تعداد", default=1)
    is_refunded = models.BooleanField("برگشت داده شده", default=False)


    def __str__(self):
        return f"{self.quantity} of {self.item.title}"

    def get_total_item_price(self):
        return self.quantity * self.item.get_price()

    def get_total_discount_item_price(self):
        return self.quantity * self.item.discount_price

    def get_amount_saved(self):
        return self.get_total_item_price() - self.get_total_discount_item_price()

    def get_final_price(self):
        return self.item.get_price()

    class Meta:
        verbose_name = "آیتم سفارش"
        verbose_name_plural = "آیتم سفارشها"


class SetOrderItems(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE, verbose_name="کاربر")
    items = models.ManyToManyField(OrderItem, verbose_name="آیتم ها")
    set = models.ForeignKey(Set, verbose_name="ست", on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)

    def get_total_discounted(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_final_price()
        return total

    class Meta:
        verbose_name = "ست آیتم"
        verbose_name_plural = "ست آیتم ها"


class Address(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    receiver_name = models.CharField("نام و نام خانوادگی تحویل گیرنده", max_length=200)
    phone = models.CharField("شماره موبایل", max_length=13)
    postal_code = models.CharField("کد پستی", max_length=20)
    distinct = models.CharField("استان", max_length=50)
    city = models.CharField("شهر", max_length=50)
    address = models.TextField("آدرس")

    default = models.BooleanField(default=False)

    def __str__(self):
        return self.address

    class Meta:
        verbose_name = "آدرس"
        verbose_name_plural = "آدرسها"


class Payment(models.Model):
    # type = models.
    stripe_charge_id = models.CharField(max_length=50)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.SET_NULL, blank=True, null=True, verbose_name="کاربر")
    amount = models.FloatField("مقدار")
    timestamp = models.DateTimeField("تاریخ و زمان", auto_now_add=True)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = "پرداخت"
        verbose_name_plural = "پرداختها"


class Coupon(models.Model):
    code = models.CharField("کد تخفیف", max_length=15)
    amount = models.FloatField("مقدار")

    def __str__(self):
        return self.code

    class Meta:
        verbose_name = "کد تخفیف"
        verbose_name_plural = "کدهای تخفیف"


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE, verbose_name="کاربر")
    code = models.CharField("کد سفارش", max_length=6, default=shortuuid.random(length=8), editable=False)
    items = models.ManyToManyField(OrderItem, verbose_name="آیتم ها")
    start_date = models.DateTimeField("تاریخ شروغ", auto_now_add=True)
    order_date = models.DateTimeField("تاریخ ثبت سفارش", auto_now=True)
    deliver_method = models.CharField("نوع تحویل", blank=True, max_length=10)
    desc = models.TextField("توضیحات", blank=True)
    payment_method = models.CharField("روش پرداخت", blank=True, max_length=30)
    do_factor = models.BooleanField("فاکتور ارسال شود", default=False)
    ordered = models.BooleanField("سفارش داده شده", default=False)
    shipping_address = models.ForeignKey(
        'Address', related_name='shipping_address', on_delete=models.SET_NULL, blank=True, null=True,
        verbose_name="آدرس")
    payment = models.ForeignKey(
        'Payment', on_delete=models.SET_NULL, blank=True, null=True, verbose_name="پرداخت")
    coupon = models.ForeignKey(
        'Coupon', on_delete=models.SET_NULL, blank=True, null=True, verbose_name="کد تخفیف")
    state = models.CharField("وضعیت", choices=ORDER_STATE, default="در حال بررسی", max_length=17)

    '''
    1. Item added to cart
    2. Adding a billing address
    (Failed checkout)
    3. Payment
    (Preprocessing, processing, packaging etc.)
    4. Being delivered
    5. Received
    6. Refunds
    '''

    def __str__(self):
        return self.user.username

    def get_total(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.item.price
        return total

    def get_total_discounted(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_final_price()
        if self.coupon:
            total -= self.coupon.amount
        return total

    def get_final_payment(self):
        if self.get_total_discounted() < 500000:
            return self.get_total_discounted() + 14000
        else:
            return self.get_total_discounted()

    class Meta:
        verbose_name = "سفارش"
        verbose_name_plural = "سفارش ها"


class Refund(models.Model):
    order_item = models.ForeignKey(OrderItem, on_delete=models.CASCADE, verbose_name="آیتم")
    reason = models.TextField("دلیل")
    accepted = models.BooleanField("پذیرفته شده", default=False)

    def __str__(self):
        return f"{self.pk}"

    class Meta:
        verbose_name = "مرجوعی"
        verbose_name_plural = "مرجوعی ها"
