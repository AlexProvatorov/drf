from django.shortcuts import render
from goods.models import Tag, Item, Author


def item(request, catalog_slug):
    order_by = request.GET.get('order_by', None)
    filter_by_tags = request.GET.get('filter_by_tags', None)

    if catalog_slug == "all":
        items = Item.item_objects.all()
    else:
        items = Item.item_objects.filter(catalog__slug=catalog_slug)
    if order_by:
        items = items.order_by(order_by)
    if filter_by_tags:
        items = items.filter(tags__name=filter_by_tags)

    tags = Tag.objects.all()

    context = {
        'title': 'Book Store - Каталог',
        'tags': tags,
        'items': items,
        'catalog_slug': catalog_slug,
    }

    return render(request, 'goods/catalog.html', context)


def item_in_detail(request, product_slug):

    good = Item.item_objects.get(slug=product_slug)
    authors = Author.objects.filter(book__exact=good)
    tags = Tag.objects.filter(item__exact=good)

    context = {
        'title': 'Book Store - Товары',
        'good': good,
        'authors': ', '.join(author.full_name for author in authors),
        'tags': ', '.join(tage.name for tage in tags),
    }

    return render(request, 'goods/product.html', context)
