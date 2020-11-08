from django.contrib import admin

from .models import *


class ProductHasImageInline(admin.TabularInline):
    model = ProductHasImage


class ProductAdmin(admin.ModelAdmin):
    inlines = [
        ProductHasImageInline,
    ]


admin.site.register(Category)
admin.site.register(Product, ProductAdmin)
# admin.site.register(ProductHasImage)
# admin.site.register(ProductHasReview)

# Register your models here.
