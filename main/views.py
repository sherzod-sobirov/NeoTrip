from typing import Any
from django.shortcuts import redirect, render
from django.views import View
from post.models import Post
from tour.models import Tour, Destination, Category
from django.views.generic import TemplateView
from .forms import ContactForm, CommentForm
from django.views.generic import DetailView
from datetime import datetime
from django.contrib import messages
from .models import TeamMember, Comment


class HomeView(View):
    def get(self, request):
        last_two_posts = Post.objects.all().order_by("-created_at")[:2]
        last_three_tours_disc = Tour.objects.filter(status="discount").order_by("-created_at")[:2]
        last_four_tours = Tour.objects.filter(status="available").order_by("-created_at")[:4]
        last_three_dests = Destination.objects.all().order_by("-created_at")[:7]
        last_five_testimonials = Comment.objects.all().order_by("-created_at")
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
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Add categories and their associated tour counts to the context
        context['categories'] = Category.objects.all()  # Retrieve all categories
        return context


class AboutUsView(View):
    def get(self, request):
        team_members = TeamMember.objects.all().order_by('display_order')
        form = CommentForm()  # Initialize an empty form
        return render(request, 'main/about.html', {
            'team_members': team_members,
            'form': form,  # Include the form in the context for GET requests
        })

    def post(self, request):
        form = CommentForm(request.POST)
        if form.is_valid():
            form.save()  # Save the comment to the database
            messages.success(request, 'Your comment has been submitted successfully!')
            return redirect('main_about')  # Redirect to the About Us page after submitting
        else:
            messages.error(request, 'There was an error submitting your comment. Please try again.')
            team_members = TeamMember.objects.all().order_by('display_order')  # Fetch team members again
            return render(request, 'main/about.html', {
                'form': form,
                'team_members': team_members,  # Include team members when the form is invalid
            })


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
    """
    Set the language for the current session based on the user's choice.

    Args:
        request: Django HttpRequest object.

    Returns:
        HttpResponseRedirect to the referring page or root ('/').
    """
    # Get the language from the GET parameters (e.g., lang=fr or lang=ru)
    language = request.GET.get('lang', 'fr')  # Default to French if no language is selected

    # Check if the selected language is supported
    if language in dict(settings.LANGUAGES):
        # Activate the selected language
        translation.activate(language)
        # Redirect to the previous page or homepage, setting the language cookie
        response = redirect(request.META.get('HTTP_REFERER', '/'))
        response.set_cookie(settings.LANGUAGE_COOKIE_NAME, language)
    else:
        # If the language is invalid, fall back to French
        translation.activate('fr')
        response = redirect('/')
        response.set_cookie(settings.LANGUAGE_COOKIE_NAME, 'fr')

    return response


