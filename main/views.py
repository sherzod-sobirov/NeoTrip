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


from django.core.cache import cache
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.conf import settings

CACHE_TTL = getattr(settings, 'CACHE_TTL', 60 * 15)  # 15 min default


@method_decorator(cache_page(CACHE_TTL), name='dispatch')
class HomeView(View):
    def get(self, request):
        last_two_posts = cache.get_or_set(
            'last_two_posts',
            lambda: Post.objects.all().order_by("-created_at")[:2],
            CACHE_TTL
        )
        last_three_tours_disc = cache.get_or_set(
            'last_three_tours_disc',
            lambda: Tour.objects.filter(status="discount").order_by("-created_at")[:2],
            CACHE_TTL
        )
        last_four_tours = cache.get_or_set(
            'last_four_tours',
            lambda: Tour.objects.filter(status="available").order_by("-created_at")[:4],
            CACHE_TTL
        )
        last_three_dests = cache.get_or_set(
            'last_three_dests',
            lambda: Destination.objects.all().order_by("-created_at")[:7],
            CACHE_TTL
        )
        last_five_testimonials = cache.get_or_set(
            'last_five_testimonials',
            lambda: Comment.objects.all().order_by("-created_at"),
            CACHE_TTL
        )

        context = {
            "last_two_posts": last_two_posts,
            "last_four_tours": last_four_tours,
            "last_three_dests": last_three_dests,
            "last_three_tours_disc": last_three_tours_disc,
            "last_five_testimonials": last_five_testimonials
        }
        return render(request, "index.html", context)


@method_decorator(cache_page(CACHE_TTL), name='dispatch')
class DestinationView(TemplateView):
    template_name = "main/destinations.html"

    def get_context_data(self, **kwargs: Any):
        context = super().get_context_data(**kwargs)
        context['dests'] = cache.get_or_set(
            'all_destinations',
            lambda: Destination.objects.all(),
            CACHE_TTL
        )
        return context


@method_decorator(cache_page(CACHE_TTL), name='dispatch')
class DestinationDetailView(DetailView):
    model = Destination
    template_name = "main/destination_detail.html"
    context_object_name = "destination"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = cache.get_or_set(
            'all_categories',
            lambda: Category.objects.all(),
            CACHE_TTL
        )
        return context


@method_decorator(cache_page(CACHE_TTL), name='dispatch')
class AboutUsView(View):
    def get(self, request):
        team_members = cache.get_or_set(
            'team_members',
            lambda: TeamMember.objects.all().order_by('display_order'),
            CACHE_TTL
        )
        form = CommentForm()
        return render(request, 'main/about.html', {
            'team_members': team_members,
            'form': form,
        })

    def post(self, request):
        form = CommentForm(request.POST)
        if form.is_valid():
            form.save()
            cache.delete('team_members')  # Clear cache after new comment
            messages.success(request, 'Your comment has been submitted successfully!')
            return redirect('main_about')
        else:
            messages.error(request, 'There was an error submitting your comment. Please try again.')
            team_members = TeamMember.objects.all().order_by('display_order')
            return render(request, 'main/about.html', {
                'form': form,
                'team_members': team_members,
            })


@method_decorator(cache_page(CACHE_TTL), name='dispatch')
class ContactView(View):
    def get(self, request):
        return render(request, 'main/contact.html')

    def post(self, request):
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your message has been sent successfully!')
            return redirect('main_contact')
        else:
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


from django.shortcuts import redirect
from django.utils import translation
from django.conf import settings

def set_language(request):
    language = request.GET.get('lang', 'fr')  # Default language as 'fr'
    if language in dict(settings.LANGUAGES):
        translation.activate(language)
        response = redirect(request.META.get('HTTP_REFERER', '/'))
        response.set_cookie(settings.LANGUAGE_COOKIE_NAME, language)
    else:
        translation.activate('fr')
        response = redirect('/')
        response.set_cookie(settings.LANGUAGE_COOKIE_NAME, 'fr')
    return response
