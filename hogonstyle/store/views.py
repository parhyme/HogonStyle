import random
import string
from datetime import datetime

import shortuuid
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone

from .models import Item, UserProfile, Order, OrderItem, Set, SetOrderItems, Address, Size, Color


def id_generator(size=6, chars=string.digits):
    return ''.join(random.choice(chars) for _ in range(8))


def get_id(size=6):
    urlhash = id_generator(size)
    while UserProfile.objects.filter(user_code=urlhash).exists():
        urlhash = id_generator(size)
    return urlhash


def get_orders(context, request):
    if not request.user.is_anonymous:
        try:
            order = Order.objects.get(user=request.user, ordered=False)
            order_items = order.items.all()
            context['order'] = order
            context['order_items'] = order_items
        except Order.DoesNotExist:
            pass
    else:
        pass


def register(request):
    if request.method == 'POST':
        # Get form values
        full_name = request.POST['full_name']
        password = request.POST['password']
        password2 = request.POST['password2']
        phone = request.POST['phone']

        # Check if passwords match
        if password == password2:
            if UserProfile.objects.filter(phone=phone).exists():
                messages.error(request, 'That phone is being used')
                return redirect('index')
            else:
                # Looks good
                user = UserProfile.objects.create_user(password=password, first_name=full_name, username=phone)
                # Login after register
                auth.login(request, user)
                # messages.success(request, 'You are now logged in')
                # return redirect('index')
                user.save()
                user_profile = UserProfile(user=user, phone=phone, user_code=get_id())
                user_profile.save()
                messages.success(request, 'You are now registered and can log in')
                return redirect('index')
        else:
            messages.error(request, 'Passwords do not match')
            return redirect('index')


def login(request):
    if request.method == 'POST':
        phone = request.POST['phone']
        password = request.POST['password']

        user = auth.authenticate(username=phone, password=password)

        if user is not None:
            auth.login(request, user)
            messages.success(request, 'You are now logged in')
            return redirect('index')
        else:
            messages.error(request, 'Invalid credentials')
            return redirect('index')
    else:
        return render(request, 'index.html')


def logout(request):
    auth.logout(request)
    messages.success(request, 'You are now logged out')
    return redirect('index')


def index(request):
    if not request.user.is_anonymous:
        try:
            order = Order.objects.get(user=request.user, ordered=False)
            order_items = order.items.all()
            context = {
                'order': order,
                'order_items': order_items
            }
            return render(request, 'index.html', context)
        except Order.DoesNotExist:
            return render(request, 'index.html')

    else:
        return render(request, 'index.html')


def sets(request):
    sets = Set.objects.all()

    paginator = Paginator(sets, 15)
    page = request.GET.get('page')
    paged_sets = paginator.get_page(page)

    context = {
        'sets': paged_sets,
    }

    get_orders(context, request)
    return render(request, 'products/sets.html', context)


def sets_details(request, set_id):
    set = get_object_or_404(Set, pk=set_id)
    try:
        setorderitems = SetOrderItems.objects.get(set=set, user=request.user, is_active=True)
        set_order_items = setorderitems.items.all()
        soi = []
        for oreder_item in set_order_items:
            soi.append(oreder_item.item)
            print(oreder_item.item)

        set_order_total = setorderitems.get_total_discounted()
    except SetOrderItems.DoesNotExist:
        soi = None
        set_order_total = None

    context = {
        'set': set,
        'set_order_items': soi,
        'set_order_total': set_order_total,
    }

    get_orders(context, request)

    return render(request, 'products/set-details.html', context)


@login_required(login_url='index')
def cart(request):
    try:
        order = Order.objects.get(user=request.user, ordered=False)
        order_items = order.items.all()

        context = {
            'order': order,
            'order_items': order_items,
        }
    except Order.DoesNotExist:
        return render(request, 'cart.html')
    return render(request, 'cart.html', context)


@login_required(login_url='index')
def add_address(request):
    if request.method == 'POST':
        # Get form values
        user = request.user
        receiver_name = request.POST['receiver_name']
        phone = request.POST['phone']
        postal_code = request.POST['postal_code']
        distinct = request.POST['distinct']
        city = request.POST['city']
        address_text = request.POST['address']

        # Looks good
        address = Address(user=user, receiver_name=receiver_name, phone=phone, postal_code=postal_code,
                          distinct=distinct, city=city, address=address_text)
        address.save()
        messages.success(request, 'آدرس افزوده شد')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required(login_url='index')
def update_address(request):
    # Get form values
    address = Address.objects.get(id=request.POST.get('address_id'))
    address.receiver_name = request.POST.get('receiver_name')
    address.phone = request.POST.get('phone')
    address.postal_code = request.POST.get('postal_code')
    address.distinct = request.POST.get('distinct')
    address.city = request.POST.get('city')
    address.address = request.POST.get('address_text')

    address.save()
    messages.success(request, 'آدرس ویرایش یافت')
    return redirect('profile-address')


def checkout(request):
    if request.method == 'POST':
        user = request.user
        order = Order.objects.get(user=request.user, ordered=False)
        shipping_address = Address.objects.get(pk=request.POST['address_id'])
        order.shipping_address = shipping_address
        payment_method = request.POST['payment_method']
        order.payment_method = payment_method
        order.desc = request.POST['desc']
        order.order_date = datetime.now()
        order.deliver_method = request.POST['deliver_method']
        if request.POST.get('factor', "False") == 'on':
            order.do_factor = True
        else:
            order.do_factor = False
        order.ordered = True
        order.save()

        return render(request, 'index.html')
    else:
        user = request.user
        order = Order.objects.get(user=request.user, ordered=False)
        order_items = order.items.all()
        addresses = Address.objects.filter(user=user)
        is_teh = False
        for address in addresses:
            if address.distinct == "1":
                is_teh = True

        context = {
            'user': user,
            'order': order,
            'order_items': order_items,
            'addresses': addresses,
            'is_teh': is_teh,
        }

        get_orders(context, request)

        return render(request, 'checkout.html', context)


@login_required(login_url='index')
def add_to_cart(request, id):
    item = get_object_or_404(Item, id=id)
    order_item, created = OrderItem.objects.get_or_create(
        item=item,
        user=request.user,
        size=request.POST["size"],
        color=request.POST["color"],
    )
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__id=item.id, size=request.POST["size"], color=request.POST["color"]).exists():
            order_item.quantity += 1
            order_item.save()
            messages.info(request, "This item quantity was updated.")
            return redirect("index")
        else:
            order.items.add(order_item)
            messages.info(request, "This item was added to your cart.")
            return redirect("index")
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(
            user=request.user, code=get_id(size=8))
        order.items.add(order_item)
        messages.info(request, "This item was added to your cart.")
        return redirect("index")


# @login_required
# def remove_from_cart(request, id, size, color):
#     item = get_object_or_404(Item, id=id, size=size, color=color)
#     order_qs = Order.objects.filter(
#         user=request.user,
#         ordered=False
#     )
#     if order_qs.exists():
#         order = order_qs[0]
#         # check if the order item is in the order
#         if order.items.filter(item__id=item.id).exists():
#             order_item = OrderItem.objects.filter(
#                 item=item,
#                 user=request.user,
#                 ordered=False
#             )[0]
#             order.items.remove(order_item)
#             order_item.delete()
#             messages.info(request, "This item was removed from your cart.")
#             return redirect("index")
#         else:
#             messages.info(request, "This item was not in your cart")
#             return redirect("index")
#     else:
#         messages.info(request, "You do not have an active order")
#         return redirect("index")


@login_required
def remove_single_item_from_cart(request, id):
    order_item = get_object_or_404(OrderItem, id=id, ordered=False)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(id=order_item.id).exists():

            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
            else:
                order.items.remove(order_item)
            messages.info(request, "This item quantity was updated.")
            return redirect("index")
        else:
            messages.info(request, "This item was not in your cart")
            return redirect("index")
    else:
        messages.info(request, "You do not have an active order")
        return redirect("index")


@login_required(login_url='index')
def add_to_set(request, id):
    item = get_object_or_404(Item, id=id)
    order_item, created = OrderItem.objects.get_or_create(
        item=item,
        user=request.user,
        size=request.GET["size"],
        color=request.GET["color"],
    )
    set = Set.objects.get(id=request.GET['set_id'])
    order_qs = SetOrderItems.objects.filter(user=request.user, set=set, is_active=True)
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__id=item.id).exists():
            order.items.filter(item__id=item.id).delete()
            order.items.add(order_item)
            order.save()
            messages.info(request, "This item quantity was updated.")
            return redirect("sets-details", request.GET['set_id'])
        else:
            order_item.save()
            order.items.add(order_item)
            order.save()
            messages.info(request, "This item was added to your cart.")
            return redirect("sets-details", request.GET['set_id'])
    else:
        user_set = SetOrderItems.objects.create(
            user=request.user, set=set)
        user_set.items.add(order_item)
        user_set.save()
        messages.info(request, "This item was added to the set.")
        return redirect("sets-details", request.GET['set_id'])


@login_required(login_url='index')
def remove_from_set(request, id):
    item = get_object_or_404(Item, id=request.GET['item_id'])
    set_qs = SetOrderItems.objects.filter(
        user=request.user,
        set_id=id,
        is_active=True
    )
    if set_qs.exists():
        set_items = set_qs[0]
        set_items_item = set_items.items.all()
        # check if the order item is in the order
        if set_items.items.filter(item__id=item.id).exists():
            set_items.items.filter(item__id=item.id).delete()
            set_items.save()
            messages.info(request, "This item quantity was updated.")
            return redirect("sets-details", id)
        else:
            messages.info(request, "This item was not in your cart")
            return redirect("sets-details", id)
    else:
        messages.info(request, "You do not have an active order")
        return redirect("sets-details", id)


def add_all_to_order(request, id):
    set = Set.objects.get(id=id)
    orderitem_qs = SetOrderItems.objects.filter(user=request.user, set=set, is_active=True)
    order_qs = Order.objects.filter(user=request.user, ordered=False)

    if orderitem_qs.exists():
        orderitems = orderitem_qs[0]

        if order_qs.exists():
            order = order_qs[0]
            # add items to order
            for order_item in orderitems.items.all():
                if order.items.filter(item__id=order_item.item.id, size=order_item.size,
                                      color=order_item.color).exists():
                    order_item.quantity += 1
                    order_item.save()
                else:
                    order.items.add(order_item)
            orderitems.is_active = False
            orderitems.save()
            messages.info(request, "This set was added to your cart.")
            return redirect("sets-details", id)
        else:
            order = Order.objects.create(
                user=request.user, code=get_id(size=8))
            for order_item in orderitems.items.all():
                order.items.add(order_item)
            orderitems.is_active = False
            orderitems.save()
            messages.info(request, "This set was added to your cart.")
            return redirect("sets-details", id)
    else:
        messages.info(request, "No items in list")
        return redirect("sets-details", id)


def products(request, category, subcategory):
    order_by = '-timestamp'
    order_by_text = request.GET.get('sorting')
    if order_by_text == "ارزان ترین":
        order_by = 'price'
    elif order_by_text == "گران ترین":
        order_by = '-price'

    ctg, ctgper, subctg, subctgper = get_categories(category, subcategory)

    size_filters = request.GET.getlist('size-filter')
    color_filters = request.GET.getlist('color-filter')
    if size_filters and color_filters:
        items = Item.objects.order_by(order_by).filter(category=ctg, sub_category=subctg, sizes__name__in=size_filters,
                                                       colors__tag__in=color_filters).distinct()
    elif not color_filters and size_filters:
        items = Item.objects.order_by(order_by).filter(category=ctg, sub_category=subctg,
                                                       sizes__name__in=size_filters).distinct()
    elif not size_filters and color_filters:
        items = Item.objects.order_by(order_by).filter(category=ctg, sub_category=subctg,
                                                       colors__tag__in=color_filters).distinct()
    else:
        items = Item.objects.order_by(order_by).filter(category=ctg, sub_category=subctg).distinct()
    sizes = Size.objects.all()
    colors = Color.objects.all()

    paginator = Paginator(items, 15)
    page = request.GET.get('page')
    paged_items = paginator.get_page(page)

    context = {
        'items': paged_items,
        'ctg': category,
        'sctg': subcategory,
        'category': ctgper,
        'subcategory': subctgper,
        'sizes': sizes,
        'colors': colors,
    }

    get_orders(context, request)

    return render(request, 'products/products.html', context)


def products_street(request):
    ctgper = "استریت استایل"
    items = Item.objects.order_by('-timestamp').filter(category="ST")

    paginator = Paginator(items, 15)
    page = request.GET.get('page')
    paged_items = paginator.get_page(page)

    context = {
        'items': paged_items,
        'category': ctgper,
    }

    get_orders(context, request)

    return render(request, 'products/products-street.html', context)


def product_detail(request, item_id):
    item = get_object_or_404(Item, pk=item_id)

    context = {
        'item': item,
    }

    get_orders(context, request)

    return render(request, 'products/product-details.html', context)


@login_required(login_url='index')
def profile(request):
    user = request.user

    context = {
        'user': user,
    }

    get_orders(context, request)

    return render(request, 'accounts/profile.html', context)


@login_required(login_url='index')
def profile_address(request):
    user = request.user
    addresses = Address.objects.filter(user=user)

    context = {
        'user': user,
        'addresses': addresses,
    }

    get_orders(context, request)

    return render(request, 'accounts/profile-address.html', context)


@login_required(login_url='index')
def profile_orders(request):
    user = request.user
    orders = Order.objects.filter(user=user, ordered=True).order_by('-start_date')

    context = {
        'user': user,
        'orders': orders,
    }

    get_orders(context, request)

    return render(request, 'accounts/profile-order.html', context)


@login_required(login_url='index')
def profile_password(request):
    if request.method == 'POST':
        user = request.user
        old_psw = request.POST.get('old_password')
        if user.check_password(old_psw):
            new_psw = request.POST.get('new_password')
            new_psw_rep = request.POST.get('new_password_rep')
            if new_psw == new_psw_rep:
                user.set_password(new_psw)
                user.save()
                messages.info(request, "رمز تغییر یافت")
                return redirect('profile')
            else:
                messages.error(request, "رمزها با هم یکسان نیستند")
                return redirect('profile-password')
        else:
            messages.error(request, "رمز قبلی درست نیست")
            return redirect('profile-password')
    else:
        user = request.user

        context = {
            'user': user
        }

        get_orders(context, request)

        return render(request, 'accounts/profile-reset-password.html', context)


@login_required(login_url='index')
def update_profile(request):
    user = UserProfile.objects.get(username=request.user.username)
    first_name = request.POST.get("first_name")
    last_name = request.POST.get("last_name")
    email = request.POST.get("email")
    full_name_bank = request.POST.get("full_name_bank")
    sheba = request.POST.get("sheba")
    if first_name:
        user.first_name = first_name
    if last_name:
        user.last_name = last_name
    if email:
        user.email = email
    if full_name_bank:
        print(full_name_bank)
        user.full_name_bank = full_name_bank
    if sheba:
        user.sheba = sheba
    user.save()

    return redirect('profile')


def about(request):
    if not request.user.is_anonymous:
        try:
            order = Order.objects.get(user=request.user, ordered=False)
            order_items = order.items.all()
            context = {
                'order': order,
                'order_items': order_items
            }
            return render(request, 'about/about.html', context)
        except Order.DoesNotExist:
            return render(request, 'about/about.html')

    else:
        return render(request, 'about/about.html')


def contact(request):
    if not request.user.is_anonymous:
        try:
            order = Order.objects.get(user=request.user, ordered=False)
            order_items = order.items.all()
            context = {
                'order': order,
                'order_items': order_items
            }
            return render(request, 'about/contact.html', context)
        except Order.DoesNotExist:
            return render(request, 'about/contact.html')

    else:
        return render(request, 'about/contact.html')


def faq(request):
    if not request.user.is_anonymous:
        try:
            order = Order.objects.get(user=request.user, ordered=False)
            order_items = order.items.all()
            context = {
                'order': order,
                'order_items': order_items
            }
            return render(request, 'about/faq.html', context)
        except Order.DoesNotExist:
            return render(request, 'about/faq.html')

    else:
        return render(request, 'about/faq.html')


def delivery(request):
    if not request.user.is_anonymous:
        try:
            order = Order.objects.get(user=request.user, ordered=False)
            order_items = order.items.all()
            context = {
                'order': order,
                'order_items': order_items
            }
            return render(request, 'about/delivery.html', context)
        except Order.DoesNotExist:
            return render(request, 'about/delivery.html')

    else:
        return render(request, 'about/delivery.html')


def in_person_store(request):
    if not request.user.is_anonymous:
        try:
            order = Order.objects.get(user=request.user, ordered=False)
            order_items = order.items.all()
            context = {
                'order': order,
                'order_items': order_items
            }
            return render(request, 'about/in-person-store.html', context)
        except Order.DoesNotExist:
            return render(request, 'about/in-person-store.html')

    else:
        return render(request, 'about/in-person-store.html')


def payment(request):
    if not request.user.is_anonymous:
        try:
            order = Order.objects.get(user=request.user, ordered=False)
            order_items = order.items.all()
            context = {
                'order': order,
                'order_items': order_items
            }
            return render(request, 'about/payment.html', context)
        except Order.DoesNotExist:
            return render(request, 'about/payment.html')

    else:
        return render(request, 'about/payment.html')


def privacy(request):
    if not request.user.is_anonymous:
        try:
            order = Order.objects.get(user=request.user, ordered=False)
            order_items = order.items.all()
            context = {
                'order': order,
                'order_items': order_items
            }
            return render(request, 'about/privacy.html', context)
        except Order.DoesNotExist:
            return render(request, 'about/privacy.html')

    else:
        return render(request, 'about/privacy.html')


def refunding(request):
    if not request.user.is_anonymous:
        try:
            order = Order.objects.get(user=request.user, ordered=False)
            order_items = order.items.all()
            context = {
                'order': order,
                'order_items': order_items
            }
            return render(request, 'about/refunding.html', context)
        except Order.DoesNotExist:
            return render(request, 'about/refunding.html')

    else:
        return render(request, 'about/refunding.html')


def size_guide(request):
    if not request.user.is_anonymous:
        try:
            order = Order.objects.get(user=request.user, ordered=False)
            order_items = order.items.all()
            context = {
                'order': order,
                'order_items': order_items
            }
            return render(request, 'about/size-guide.html', context)
        except Order.DoesNotExist:
            return render(request, 'about/size-guide.html')

    else:
        return render(request, 'about/size-guide.html')


def get_categories(category, subcategory):
    ctg = 'MA'
    ctgper = ''
    if category == 'men':
        ctg = "MA"
        ctgper = "مردانه"
    elif category == 'women':
        ctg = "WO"
        ctgper = "زنانه"
    elif category == 'street':
        ctg = "ST"
        ctgper = "استریت استایل"
    elif category == 'accessories':
        ctg = "AC"
        ctgper = "اکسسوری"
    subctg = 'TS'
    subctgper = ''
    if subcategory == 't-shirt':
        subctg = 'TS'
        subctgper = 'تی شرت'
    elif subcategory == 'polo':
        subctg = 'PS'
        subctgper = 'پولوشرت'
    elif subcategory == 'shirt':
        subctg = 'SH'
        subctgper = 'پیراهن'
    elif subcategory == 'hoody':
        subctg = 'HO'
        subctgper = 'سویشرت و هودی'
    elif subcategory == 'jacket':
        subctg = 'PA'
        subctgper = 'کاپشن و پالتو'
    elif subcategory == 'knitwear':
        subctg = 'BA'
        subctgper = 'بافت'
    elif subcategory == 'dors':
        subctg = 'DO'
        subctgper = 'دورس'
    elif subcategory == 'jeans':
        subctg = 'JE'
        subctgper = 'شلوار جین'
    elif subcategory == 'trousers':
        subctg = 'SP'
        subctgper = 'شلوار پارچه ای'
    elif subcategory == 'cotton-trousers':
        subctg = 'SK'
        subctgper = 'شلوار کتان'
    elif subcategory == 'shorts':
        subctg = 'SS'
        subctgper = 'شلوارک'
    elif subcategory == 'sneakers':
        subctg = 'KK'
        subctgper = 'کفش کتانی'
    elif subcategory == 'sandals':
        subctg = 'SN'
        subctgper = 'صندل'
    elif subcategory == 'official':
        subctg = 'RS'
        subctgper = 'کفش رسمی'
    elif subcategory == 'wallet':
        subctg = 'MB'
        subctgper = 'کیف پول و جاکارتی'
    elif subcategory == 'bag':
        subctg = 'BS'
        subctgper = 'کیف کمری'
    elif subcategory == 'scarf':
        subctg = 'SC'
        subctgper = 'شال'
    elif subcategory == 'hand-bag':
        subctg = 'HB'
        subctgper = 'کیف دستی و دوشی'
    elif subcategory == 'cap':
        subctg = 'CA'
        subctgper = 'کلاه و کپ'
    elif subcategory == 'belt':
        subctg = 'BE'
        subctgper = 'کمربند'
    elif subcategory == 'socks':
        subctg = 'SO'
        subctgper = 'جوراب'
    elif subcategory == 'landyard':
        subctg = 'LA'
        subctgper = 'لندیارد'
    elif subcategory == 'lighter':
        subctg = 'FA'
        subctgper = 'فندک'
    elif subcategory == 'decorative':
        subctg = 'DE'
        subctgper = 'دکوری'
    elif subcategory == 'manto':
        subctg = 'MA'
        subctgper = 'مانتو'
    elif subcategory == 'blouses':
        subctg = 'BL'
        subctgper = 'بلوز و شومیز'
    elif subcategory == 'backpack':
        subctg = 'BP'
        subctgper = 'کوله پشتی'
    elif subcategory == 'top':
        subctg = 'TP'
        subctgper = 'تاپ'
    return ctg, ctgper, subctg, subctgper
