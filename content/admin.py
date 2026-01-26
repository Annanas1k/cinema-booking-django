from django.contrib import admin
from .models import Cinema, News, AdminTask, ShopCategory, ShopProducts


@admin.register(Cinema)
class CinemaAdmin(admin.ModelAdmin):
    list_display  = ('name', 'image', 'description', 'program_phone',
                     'reservations_phone', 'admin_phone',
                     'address', 'email', 'opening_hours',
                     'halls_count', 'google_maps_embed')

    search_fields = ('name', 'address')
    list_filter = ('name', 'address')

    def halls_count(self, obj):
        return obj.halls.count()

@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'image', 'short_description', 'long_description', 'created_at')
    search_fields = ('title',)
    list_filter = ('title','created_at')


@admin.register(AdminTask)
class AdminTaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'created_at', 'deadline', 'status', 'priority')
    list_filter = ('status', 'priority')
    search_fields = ('title', 'description')
    list_editable = ('status', 'priority', 'deadline')


    class Media:
        css = {
            'all': ('css/custom_admin.css',)
        }


class ProductInline(admin.TabularInline):
    model = ShopProducts
    extra = 1
    fields = ('product_name', 'product_volume', 'product_price', 'is_active', 'product_image')

@admin.register(ShopCategory)
class ShopCategoryAdmin(admin.ModelAdmin):
    list_display = ('category_name', 'get_product_count')
    search_fields = ('category_name',)
    inlines = [ProductInline]

    def get_product_count(self, obj):
        return obj.products.count()
    get_product_count.short_description = "Number of Products"

@admin.register(ShopProducts)
class ShopProductsAdmin(admin.ModelAdmin):

    list_display = ('product_name','product_volume', 'category', 'product_price', 'is_active')
    list_filter = ('category', 'is_active')
    search_fields = ('product_name', 'product_description')
    list_editable = ('product_price', 'is_active')