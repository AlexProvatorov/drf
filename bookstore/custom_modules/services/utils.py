from uuid import uuid4
from pytils.translit import slugify


def generate_unique_slugify(instance, slug):
    """
    Генерация уникального slug для модели, если такой slug существует.
    """
    model = instance.__class__
    unique_slug = slugify(slug)
    while model.objects.filter(slug=unique_slug).exists():
        unique_slug = f'{unique_slug}-{uuid4().hex[:8]}'
    return unique_slug
