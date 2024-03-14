from django.db.models import F
from django.shortcuts import render, redirect
from carts.models import Cart
from goods.models import Item
from django.shortcuts import get_object_or_404


def view_cart(request):
    """
    Представление для отображения товаров в корзине.
    """
    cart_positions = Cart.cart_objects.all().filter(
        customer=request.user.id,
    ).order_by("item_id").annotate(
        total=F("item__cost") * F("count"),
    )

    total_sum = sum(cart_position.total for cart_position in cart_positions)

    context = {
        'title': 'Корзина',
        'content': 'Корзина',
        'cart_positions': cart_positions,
        'total_sum': total_sum,
    }
    return render(request, 'carts/view_cart.html', context)


def add_cart(request, item_id):

    if not request.user.is_authenticated:
        return redirect('login')

    item_id = get_object_or_404(Item, pk=item_id)

    cart_position, created = Cart.cart_objects.all().filter(
        customer=request.user.id,
    ).get_or_create(
        customer=request.user,
        item=item_id,
    )

    if not created and cart_position.count < cart_position.item.count_in_stock:
        cart_position.count += 1
        cart_position.save()

    return redirect(request.META['HTTP_REFERER'])


def remove_cart(request, item_id):

    item_id = get_object_or_404(Item, pk=item_id)

    cart_position, created = Cart.cart_objects.all().get_or_create(
        customer=request.user,
        item=item_id,
    )

    if not created and cart_position.count > 0:
        cart_position.count -= 1
        cart_position.save()
    if not created and cart_position.count == 0:
        cart_position.delete()

    return redirect(request.META['HTTP_REFERER'])


def remove_cart_position(request, item_id):

    item_id = get_object_or_404(Item, pk=item_id)

    cart_position, created = Cart.cart_objects.all().get_or_create(
        customer=request.user,
        item=item_id,
    )

    cart_position.delete()

    return redirect(request.META['HTTP_REFERER'])


def create_order(request):

    order_positions = Cart.cart_objects.all().filter(
        customer=request.user.id,
    ).order_by("item_id").annotate(
        total=F("item__cost") * F("count"),
    ).update(status='PENDING')

    return redirect(request.META['HTTP_REFERER'])
