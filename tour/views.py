from django.shortcuts import render
from django.views.generic import DetailView, ListView
from .models import Tour, Category, Country, Destination
from datetime import datetime
from django.shortcuts import get_object_or_404


# Tour Detail View
class TourDetailView(DetailView):
    model = Tour
    template_name = "main/package_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Fetching recent tours
        context['recent_tours'] = Tour.objects.filter(status__in=["available", "discount"]).exclude(
            id=self.kwargs['pk']).order_by("-created_at")[:3]
        
        # Adding category to the context
        tour = self.get_object()  # This gets the current tour object
        context['category'] = tour.category  # Assuming 'category' is a field in your Tour model
        
        # Adding categories to the context
        context['categories'] = Category.objects.all()  # Assuming 'Category' is the model for categories
        
        return context


# Tour List View
class TourListView(ListView):
    model = Tour
    template_name = "main/package_list.html"
    context_object_name = 'tours'
    paginate_by = 3  # 3 tours per page

    def get_queryset(self):
        return Tour.objects.filter(status="available").order_by("-created_at")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Add categories and their associated tour counts to the context
        context['categories'] = Category.objects.all()  # Retrieve all categories
        return context

# Special Tour List View
class SpecialTourListView(ListView):
    model = Tour
    template_name = "main/special_package.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['special_tours'] = Tour.objects.filter(status="discount").order_by("-created_at")
        return context


class CategoryDetailView(ListView):
    model = Tour
    template_name = 'main/category_detail.html'
    context_object_name = 'tours'
    paginate_by = 3  # Adjust the number of items per page as needed

    def get_queryset(self):
        category_id = self.kwargs['id']  # Get the category ID from the URL
        return Tour.objects.filter(category__id=category_id, status="available").order_by("-created_at")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_id = self.kwargs['id']
        category = get_object_or_404(Category, id=category_id)  # Fetch the category
        context['category'] = category  # Add category to the context
        context['categories'] = Category.objects.all()  # Add all categories to the context
        return context

