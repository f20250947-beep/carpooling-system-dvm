from django.contrib import admin
from .models import Node, Edge, SiteSettings

admin.site.register(Node)
admin.site.register(Edge)
admin.site.register(SiteSettings)


