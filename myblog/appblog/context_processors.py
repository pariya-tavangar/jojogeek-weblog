from django.db.models import Count
from .models import Category

def top_categories(request):
    categories = (Category.objects.annotate(post_count=Count('posts')).order_by('-post_count')[:5])
    return {'top_categories': categories}