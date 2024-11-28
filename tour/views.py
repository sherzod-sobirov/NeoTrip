from typing import Any
from django.shortcuts import render
from django.views.generic import DetailView, ListView
from .models import *
from datetime import datetime

class TourDetailView(DetailView):
    model = Tour
    template_name = "main/package_detail.html"

    def get_context_data(self, **kwargs: Any):
        context = super().get_context_data(**kwargs)

        context['recent_tours'] = Tour.objects.filter(status__in=["available", "discount"]).exclude(
            id=self.kwargs['pk']).order_by("-created_at")[:3]
        return context

from django.views.generic import ListView
from .models import Tour

class TourListView(ListView):
    model = Tour
    template_name = "main/package_list.html"
    context_object_name = 'tours'
    paginate_by = 3  # 3 tours per page

    def get_queryset(self):
        return Tour.objects.filter(status="available").order_by("-created_at")



class SpecialTourListView(ListView):
    model = Tour
    template_name = "main/special_package.html"

    def get_context_data(self, **kwargs: Any):
        context = super().get_context_data(**kwargs)
        context['special_tours'] = Tour.objects.filter(status__in=["discount"]).order_by("-created_at")
        return context
    
    
class SearchResultView(ListView):
    model = Tour
    template_name = 'search.html'
    context_object_name = 'search_list'

    def get_queryset(self):
        query_params = self.request.GET
        
        country = query_params.get('country', '')
        start_date = query_params.get('start_date', '')
        min_price = query_params.get('min_price', 0)
        max_price = query_params.get('max_price', 10000000)
        
        queryset = Tour.objects.all()
        
        if country:
            queryset = queryset.filter(country__icontains=country)
        
        if start_date:
            try:
                start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
                queryset = queryset.filter(start_date__lte=start_date, end_date__gte=start_date)
            except ValueError:
                pass 
        
        if min_price and max_price:
            queryset = queryset.filter(prise__gte=min_price, prise__lte=max_price)
        
        return queryset
