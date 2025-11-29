from django.db.models import Count
from .models import Category, Tag

def top_categories(request):
    categories = (Category.objects.annotate(post_count=Count('posts')).order_by('-post_count')[:5])
    return {'top_categories': categories}


def top_tags(request):
    tags = (Tag.objects.annotate(post_count=Count("posts")).order_by("-post_count")[:5])
    return {"top_tags": tags}