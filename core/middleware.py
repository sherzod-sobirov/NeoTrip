import logging
from django.utils import translation

logger = logging.getLogger(__name__)

class ForceFrenchLanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        logger.info("ForceFrenchLanguageMiddleware activated")
        translation.activate('fr')
        response = self.get_response(request)
        response.set_cookie('django_language', 'fr', max_age=3600)
        return response
