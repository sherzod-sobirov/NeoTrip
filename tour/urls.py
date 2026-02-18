from django.urls import path
from .views import TourDetailView, TourListView, SpecialTourListView, CategoryDetailView

urlpatterns = [
    path("tour/<int:pk>/", TourDetailView.as_view(), name="tour_tour_detail"),
    path('tours/', TourListView.as_view(), name="tours"),
    path("all-special-tour", SpecialTourListView.as_view(), name="tour_special_tours"),
    path('category/<int:id>/', CategoryDetailView.as_view(), name='category_tours'),

]
