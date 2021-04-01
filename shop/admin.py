from django.contrib import admin
from shop.models import Category, Product, Genre, Season

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
	list_display = ["name", "slug"]
	prepopulated_fields = {"slug": ("name",)}

@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
	list_display = ["name"]
	prepopulated_fields = {"slug": ("name",)}

@admin.register(Season)
class SeasonAdmin(admin.ModelAdmin):
	list_display = ["name"]
	prepopulated_fields = {"slug": ("name",)}

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
	list_display = ["name",
                    "available",
                    "price",
					"get_genres",
                    "category",
                    "get_seasons",
                    "main_color",
                    "styles",
                    "materials",
                    "brand",
                    "thickness",
                    "slug",
                    "image",
                    "description",
                    "create_date",
                    "update_date"]
	list_filter = ["available", "create_date", "update_date"]
	list_editable = ["price", "available"]
	filter_horizontal = ("seasons", "genres",)
	prepopulated_fields = {"slug": ("name",)}
