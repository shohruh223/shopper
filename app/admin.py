from django.contrib import admin
from mptt.admin import DraggableMPTTAdmin

from app.models import Product, Category


admin.site.register(Product)

@admin.register(Category)
class CustomMPTTModelAdmin(DraggableMPTTAdmin):
    # specify pixel amount for this ModelAdmin only:
    mptt_level_indent = 20
    exclude = ('slug',)

