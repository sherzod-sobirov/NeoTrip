from typing import Any
from django.views.generic import ListView
from django.shortcuts import redirect, render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from post.models import Post
from tour.models import Tour, Destination
from user.models import Testimonial
from user.forms import TestimonialForm
from django.views.generic import TemplateView
from .forms import ContactForm
from django.shortcuts import HttpResponse
from django.views.generic import DetailView
from datetime import datetime
from django.contrib import messages
from .models import TeamMember


def team_view(request):
    team_members = TeamMember.objects.all().order_by('display_order')
    return render(request, 'main/about.html', {'team_members': team_members})


class HomeView(View):
    def get(self, request):
        last_two_posts = Post.objects.all().order_by("-created_at")[:2]
        last_three_tours_disc = Tour.objects.filter(status="discount").order_by("-created_at")[:2]
        last_four_tours = Tour.objects.filter(status="available").order_by("-created_at")[:4]
        last_three_dests = Destination.objects.all().order_by("-created_at")[:7]
        last_five_testimonials = Testimonial.objects.all().order_by("-created_at")[:5]
        context = {
            "last_two_posts": last_two_posts,
            "last_four_tours": last_four_tours,
            "last_three_dests": last_three_dests,
            "last_three_tours_disc": last_three_tours_disc,
            "last_five_testimonials": last_five_testimonials
        }
        return render(request, "index.html", context)


class DestinationView(TemplateView):
    template_name = "main/destinations.html"

    def get_context_data(self, **kwargs: Any):
        context = super().get_context_data(**kwargs)
        context['dests'] = Destination.objects.all()
        return context

class DestinationDetailView(DetailView):
    model = Destination
    template_name = "main/destination_detail.html"
    context_object_name = "destination"
    
    
class AboutUsView(View):
    def get(self, request):
        testimonials = Testimonial.objects.all()
        team_members = TeamMember.objects.all().order_by('display_order')
        return render(request, 'main/about.html', {
            'testimonials': testimonials,
            'team_members': team_members
        })

    def post(self, request):
        form = TestimonialForm(request.POST)
        if form.is_valid():
            f = form.save(commit=False)
            f.user = request.user
            f.save()
            return redirect('main_about')
        return HttpResponse('ERROR!')
    
    
class ContactView(View):
    def get(self, request):
        return render(request, 'main/contact.html')

    def post(self, request):
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            # Display a success message
            messages.success(request, 'Your message has been sent successfully!')
            return redirect('main_contact')  # Adjust the redirect to the correct URL name
        else:
            # Display an error message if the form is not valid
            messages.error(request, 'There was an error submitting your form. Please try again.')
            return redirect('main_contact')

# class FilterTourView(View):
#     def get(self, request):
#         country = request.GET.get('country')
#         date = request.GET.get('date')
#         min_price = request.GET.get('min', 0)
#         max_price = request.GET.get('max', 10000)
        
#         filtered_tours = Tour.objects.all()
        
#         if country:
#             filtered_tours = filtered_tours.filter(country__name__icontains=country)
        
#         if min_price and max_price:
#             filtered_tours = filtered_tours.filter(price__gte=min_price, price__lte=max_price)
        
#         context = {
#             "filtered_tours": filtered_tours,
#         }
        
#         return render(request, "search.html", context)


# views.py
# main/views.py
# main/views.py
from django.shortcuts import redirect
from django.utils import translation
from django.conf import settings

def set_language(request):
    # Get the language from the GET parameters (e.g., lang=ru or lang=fr)
    language = request.GET.get('lang', 'en')  # Default to English if no language is selected

    # Check if the language is in the list of supported languages
    if language in dict(settings.LANGUAGES):
        # Activate the language
        translation.activate(language)
        # Set the language cookie to remember the user's choice
        response = redirect(request.META.get('HTTP_REFERER', '/'))
        response.set_cookie(settings.LANGUAGE_COOKIE_NAME, language)
        return response
    else:
        # If the language is invalid, fall back to the default language ('en')
        translation.activate('en')
        response = redirect('/')
        response.set_cookie(settings.LANGUAGE_COOKIE_NAME, 'en')
        return response


