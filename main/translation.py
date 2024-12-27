from tour.models import Tour, Country, Destination
from post.models import Post
from modeltranslation.translator import register, TranslationOptions
from .models import TeamMember
from tour.models import Category

@register(Category)
class CategoryTranslationOptions(TranslationOptions):
    fields = ('name',)


@register(TeamMember)
class TeamMemberTranslationOptions(TranslationOptions):
    fields = ('designation',)  # Bu erda kerakli maydonlarni ro'yxatga oling

    
@register(Post)
class PostTranslationOptions(TranslationOptions):
    fields = ['title', 'body']


@register(Tour)
class TourTranslationOptions(TranslationOptions):
    fields = ['title', 'duration', 'overview', "price"]



@register(Country)
class CountryTranslationOptions(TranslationOptions):
    fields = ['name']


@register(Destination)
class DestinationTranslationOptions(TranslationOptions):
    fields = ['city', 'about']