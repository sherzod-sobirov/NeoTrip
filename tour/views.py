from django.shortcuts import render, get_object_or_404
from django.views.generic import DetailView, ListView
from .models import Tour, Category
from django.conf import settings
from django.core.cache import cache
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page

CACHE_TTL = getattr(settings, 'CACHE_TTL', 60 * 15)  # 15 min cache


# Tour Detail View
@method_decorator(cache_page(CACHE_TTL), name='dispatch')
class TourDetailView(DetailView):
    model = Tour
    template_name = "main/package_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        tour_id = self.kwargs['pk']
        tour = self.get_object()

        # Cache recent tours
        context['recent_tours'] = cache.get_or_set(
            f'recent_tours_exclude_{tour_id}',
            lambda: Tour.objects.filter(status__in=["available", "discount"])
                                .exclude(id=tour_id)
                                .order_by("-created_at")[:3],
            CACHE_TTL
        )

        context['category'] = tour.category

        # Cache all categories
        context['categories'] = cache.get_or_set(
            'all_categories',
            lambda: Category.objects.all(),
            CACHE_TTL
        )

        return context


# Tour List View
@method_decorator(cache_page(CACHE_TTL), name='dispatch')
class TourListView(ListView):
    model = Tour
    template_name = "main/package_list.html"
    context_object_name = 'tours'
    paginate_by = 3

    def get_queryset(self):
        return cache.get_or_set(
            'available_tours_list',
            lambda: Tour.objects.filter(status="available").order_by("-created_at"),
            CACHE_TTL
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = cache.get_or_set(
            'all_categories',
            lambda: Category.objects.all(),
            CACHE_TTL
        )
        return context


# Special Tour List View
@method_decorator(cache_page(CACHE_TTL), name='dispatch')
class SpecialTourListView(ListView):
    model = Tour
    template_name = "main/special_package.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['special_tours'] = cache.get_or_set(
            'special_tours_list',
            lambda: Tour.objects.filter(status="discount").order_by("-created_at"),
            CACHE_TTL
        )
        return context


# Category Detail View
@method_decorator(cache_page(CACHE_TTL), name='dispatch')
class CategoryDetailView(ListView):
    model = Tour
    template_name = 'main/category_detail.html'
    context_object_name = 'tours'
    paginate_by = 3

    def get_queryset(self):
        category_id = self.kwargs['id']
        return cache.get_or_set(
            f'category_{category_id}_tours',
            lambda: Tour.objects.filter(category__id=category_id, status="available")
                                .order_by("-created_at"),
            CACHE_TTL
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_id = self.kwargs['id']

        context['category'] = cache.get_or_set(
            f'category_{category_id}_obj',
            lambda: get_object_or_404(Category, id=category_id),
            CACHE_TTL
        )

        context['categories'] = cache.get_or_set(
            'all_categories',
            lambda: Category.objects.all(),
            CACHE_TTL
        )

        return context
