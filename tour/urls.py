from django.urls import path
from .views import *

urlpatterns = [
    path("tour/<int:pk>/", TourDetailView.as_view(), name="tour_tour_detail"),
    path('tours/', TourListView.as_view(), name="tours"),
    path("all-special-tour", SpecialTourListView.as_view(), name="tour_special_tours"),
    path("search/", SearchResultView.as_view(), name="search_page")
]