# Generated by Django 3.2.5 on 2021-10-10 14:17

import colorful.fields
from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import store.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('user_code', models.CharField(default='Ft38EBD8', editable=False, max_length=8, verbose_name='کد مشتری')),
                ('phone', models.CharField(blank=True, max_length=12, verbose_name='شماره موبایل')),
                ('full_name_bank', models.CharField(blank=True, max_length=100, verbose_name='نام صاحب حساب')),
                ('bank_name', models.CharField(blank=True, max_length=50, verbose_name='نام بانک')),
                ('sheba', models.CharField(blank=True, max_length=26, verbose_name='شماره شبا')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'کاربر',
                'verbose_name_plural': 'کاربرها',
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('receiver_name', models.CharField(max_length=200, verbose_name='نام و نام خانوادگی تحویل گیرنده')),
                ('phone', models.CharField(max_length=13, verbose_name='شماره موبایل')),
                ('postal_code', models.CharField(max_length=20, verbose_name='کد پستی')),
                ('distinct', models.CharField(max_length=50, verbose_name='استان')),
                ('city', models.CharField(max_length=50, verbose_name='شهر')),
                ('address', models.TextField(verbose_name='آدرس')),
                ('default', models.BooleanField(default=False)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'آدرس',
                'verbose_name_plural': 'آدرسها',
            },
        ),
        migrations.CreateModel(
            name='Color',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tag', models.CharField(max_length=200)),
                ('color', colorful.fields.RGBColorField(colors=['#FF0000', '#00FF00', '#0000FF'])),
            ],
            options={
                'verbose_name': 'رنگ',
                'verbose_name_plural': 'رنگها',
            },
        ),
        migrations.CreateModel(
            name='Coupon',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=15, verbose_name='کد تخفیف')),
                ('amount', models.FloatField(verbose_name='مقدار')),
            ],
            options={
                'verbose_name': 'کد تخفیف',
                'verbose_name_plural': 'کدهای تخفیف',
            },
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='عنوان')),
                ('price', models.IntegerField(verbose_name='قیمت اصلی')),
                ('discount_price', models.IntegerField(blank=True, null=True, verbose_name='قیمت با تخفیف')),
                ('category', models.CharField(choices=[('MA', 'مردانه'), ('WO', 'زنانه'), ('AC', 'اکسسوری'), ('ST', 'استریت')], max_length=2, verbose_name='دسته بندی')),
                ('sub_category', models.CharField(choices=[('TS', 'تی شرت'), ('PS', 'پولوشرت'), ('SH', 'پیراهن'), ('HO', 'سویشرت و هودی'), ('PA', 'کاپشن و پالتو'), ('BA', 'بافت'), ('DO', 'دورس'), ('JE', 'شلوار جین'), ('SP', 'شلوار پارچه ای'), ('SK', 'شلوار کتان'), ('SS', 'شلوارک'), ('KK', 'کفش کتانی'), ('SN', 'صندل'), ('RS', 'کفش رسمی'), ('MB', 'کیف پول و جاکارتی'), ('BS', 'کیف کمری'), ('SC', 'شال'), ('CA', 'کلاه و کپ'), ('BE', 'کمربند'), ('SO', 'جوراب'), ('LA', 'لندیارد'), ('FA', 'فندک'), ('DE', 'دکوری'), ('MA', 'مانتو'), ('TP', 'تاپ'), ('BL', 'بلوز و شومیز'), ('BB', 'کیف دستی و دوشی'), ('BP', 'کوله پشتی')], max_length=2, verbose_name='زیر دسته')),
                ('description', models.TextField(verbose_name='توضیحات')),
                ('is_active', models.BooleanField(default=True, verbose_name='موجود است؟')),
                ('timestamp', models.DateTimeField(auto_now_add=True, verbose_name='تاریخ و زمان ایجاد')),
                ('image_1', models.ImageField(upload_to=store.models.get_upload_path, verbose_name='عکس 1')),
                ('image_2', models.ImageField(upload_to=store.models.get_upload_path, verbose_name='عکس 2')),
                ('image_3', models.ImageField(upload_to=store.models.get_upload_path, verbose_name='عکس 3')),
                ('image_4', models.ImageField(upload_to=store.models.get_upload_path, verbose_name='عکس 4')),
                ('colors', models.ManyToManyField(to='store.Color', verbose_name='رنگ ها')),
            ],
            options={
                'verbose_name': 'آیتم',
                'verbose_name_plural': 'آیتمها',
            },
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ordered', models.BooleanField(default=False, verbose_name='سفارش داده شده')),
                ('size', models.CharField(max_length=3, verbose_name='سایز')),
                ('color', models.CharField(max_length=50, verbose_name='رنگ')),
                ('quantity', models.IntegerField(default=1, verbose_name='تعداد')),
                ('is_refunded', models.BooleanField(default=False, verbose_name='برگشت داده شده')),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.item', verbose_name='آیتم')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='کاربر')),
            ],
            options={
                'verbose_name': 'آیتم سفارش',
                'verbose_name_plural': 'آیتم سفارشها',
            },
        ),
        migrations.CreateModel(
            name='Set',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='عنوان')),
                ('is_active', models.BooleanField(default=True, verbose_name='موجود است؟')),
                ('timestamp', models.DateTimeField(auto_now_add=True, verbose_name='تاریخ و زمان ایجاد')),
                ('image', models.ImageField(upload_to=store.models.get_upload_path, verbose_name='عکس 1')),
                ('items', models.ManyToManyField(to='store.Item', verbose_name='آیتم ها')),
            ],
            options={
                'verbose_name': 'ست',
                'verbose_name_plural': 'ستها',
            },
        ),
        migrations.CreateModel(
            name='SiteSettings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slide_image_1', models.ImageField(help_text='Size: 1903x630', upload_to='', verbose_name='عکس اسلاید 1')),
                ('slide_image_2', models.ImageField(help_text='Size: 1903x630', upload_to='', verbose_name='عکس اسلاید 2')),
                ('slide_image_3', models.ImageField(help_text='Size: 1903x630', upload_to='', verbose_name='عکس اسلاید 3')),
                ('slide_image_4', models.ImageField(help_text='Size: 1903x630', upload_to='', verbose_name='عکس اسلاید 4')),
                ('intro_image_4', models.ImageField(help_text='Size: 1903x630', upload_to='', verbose_name='عکس پاپ آپ')),
            ],
            options={
                'verbose_name': 'تنظیم سایت',
                'verbose_name_plural': 'تنظیمات سایت',
            },
        ),
        migrations.CreateModel(
            name='Size',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=10, verbose_name='نام')),
            ],
            options={
                'verbose_name': 'سایز',
                'verbose_name_plural': 'سایزها',
            },
        ),
        migrations.CreateModel(
            name='SetOrderItems',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=True)),
                ('items', models.ManyToManyField(to='store.OrderItem', verbose_name='آیتم ها')),
                ('set', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.set', verbose_name='ست')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='کاربر')),
            ],
            options={
                'verbose_name': 'ست آیتم',
                'verbose_name_plural': 'ست آیتم ها',
            },
        ),
        migrations.CreateModel(
            name='Refund',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reason', models.TextField(verbose_name='دلیل')),
                ('accepted', models.BooleanField(default=False, verbose_name='پذیرفته شده')),
                ('order_item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.orderitem', verbose_name='آیتم')),
            ],
            options={
                'verbose_name': 'مرجوعی',
                'verbose_name_plural': 'مرجوعی ها',
            },
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stripe_charge_id', models.CharField(max_length=50)),
                ('amount', models.FloatField(verbose_name='مقدار')),
                ('timestamp', models.DateTimeField(auto_now_add=True, verbose_name='تاریخ و زمان')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='کاربر')),
            ],
            options={
                'verbose_name': 'پرداخت',
                'verbose_name_plural': 'پرداختها',
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(default='qhkJAAW7', editable=False, max_length=6, verbose_name='کد سفارش')),
                ('start_date', models.DateTimeField(auto_now_add=True, verbose_name='تاریخ شروغ')),
                ('order_date', models.DateTimeField(auto_now=True, verbose_name='تاریخ ثبت سفارش')),
                ('deliver_method', models.CharField(blank=True, max_length=10, verbose_name='نوع تحویل')),
                ('desc', models.TextField(blank=True, verbose_name='توضیحات')),
                ('payment_method', models.CharField(blank=True, max_length=30, verbose_name='روش پرداخت')),
                ('do_factor', models.BooleanField(default=False, verbose_name='فاکتور ارسال شود')),
                ('ordered', models.BooleanField(default=False, verbose_name='سفارش داده شده')),
                ('state', models.CharField(choices=[('در حال بررسی', 'در حال بررسی'), ('در حال آماده سازی', 'در حال آماده سازی'), ('ارسال شده', 'ارسال شده'), ('تحویل گرفته شده', 'تحویل گرفته شده')], default='در حال بررسی', max_length=17, verbose_name='وضعیت')),
                ('coupon', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='store.coupon', verbose_name='کد تخفیف')),
                ('items', models.ManyToManyField(to='store.OrderItem', verbose_name='آیتم ها')),
                ('payment', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='store.payment', verbose_name='پرداخت')),
                ('shipping_address', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='shipping_address', to='store.address', verbose_name='آدرس')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='کاربر')),
            ],
            options={
                'verbose_name': 'سفارش',
                'verbose_name_plural': 'سفارش ها',
            },
        ),
        migrations.AddField(
            model_name='item',
            name='sizes',
            field=models.ManyToManyField(to='store.Size', verbose_name='سایزها'),
        ),
    ]
