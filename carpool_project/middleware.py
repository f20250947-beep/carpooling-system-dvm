from django.shortcuts import render

class ServiceEnabledMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith('/admin'):
            return self.get_response(request)
        try:
            from network.models import SiteSettings
            settings = SiteSettings.objects.first()
            if settings and not settings.service_enabled:
                return render(request, 'service_disabled.html', status=503)
        except:
            pass
        return self.get_response(request)