from typing import Any
from datetime import datetime
from django.shortcuts import render
from django.views.generic import DetailView, ListView
from .models import Tour


class TourDetailView(DetailView):
    model = Tour
    template_name = "main/package_detail.html"
    context_object_name = 'tour'

    def get_context_data(self, **kwargs: Any):
        context = super().get_context_data(**kwargs)

        context['recent_tours'] = (
            Tour.objects.filter(status__in=["available", "discount"])
            .exclude(id=self.object.id)
            .order_by("-created_at")[:3]
        )
        return context


class TourListView(ListView):
    model = Tour
    template_name = "main/package_list.html"
    context_object_name = 'tours'
    paginate_by = 3

    def get_queryset(self):
        return Tour.objects.filter(status="available").order_by("-created_at")


class SpecialTourListView(ListView):
    model = Tour
    template_name = "main/special_package.html"
    context_object_name = 'special_tours'

    def get_queryset(self):
        return Tour.objects.filter(status="discount").order_by("-created_at")


class SearchResultView(ListView):
    model = Tour
    template_name = 'search.html'
    context_object_name = 'search_list'

    def get_queryset(self):
        query = self.request.GET

        country = query.get('country', '').strip()
        start_date = query.get('start_date', '').strip()
        min_price = query.get('min_price')
        max_price = query.get('max_price')

        tours = Tour.objects.all()

        if country:
            tours = tours.filter(country__icontains=country)

        if start_date:
            try:
                parsed_date = datetime.strptime(start_date, '%Y-%m-%d').date()
                tours = tours.filter(start_date__lte=parsed_date, end_date__gte=parsed_date)
            except ValueError:
                pass

        if min_price:
            try:
                min_price = float(min_price)
                tours = tours.filter(prise__gte=min_price)
            except ValueError:
                pass

        if max_price:
            try:
                max_price = float(max_price)
                tours = tours.filter(prise__lte=max_price)
            except ValueError:
                pass

        return tours
