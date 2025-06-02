from django.contrib import admin
from . import models


@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['pk', 'name', 'slug', 'created_at']
    prepopulated_fields = {'slug': ('name',)}
    list_display_links = ['pk', 'name']
    list_filter = ['created_at']
    search_fields = ['name']


@admin.register(models.Slider)
class SliderAdmin(admin.ModelAdmin):
    list_display = ['pk', 'title', 'description', 'image']
    list_display_links = ['pk', 'title']


@admin.register(models.FAQ)
class FaqAdmin(admin.ModelAdmin):
    list_display = ['pk', 'question', 'answer']
    list_display_links = ['pk', 'question']


class ProductImageInline(admin.TabularInline):
    model = models.ProductImage
    extra = 1


class CommentInline(admin.TabularInline):
    model = models.Comment
    extra = 1


@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['pk', 'title', 'category', 'author', 'views', 'created_at']
    list_display_links = ['pk', 'title']
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ['views']
    inlines = [ProductImageInline, CommentInline]
    list_filter = ['category', 'created_at']
    search_fields = ['title', 'description', 'full_description']


@admin.register(models.Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['pk', 'product', 'author', 'created_at']
    list_display_links = ['pk', 'product']
    search_fields = ['text']
    list_filter = ['created_at']


@admin.register(models.ProductCountView)
class ProductCountViewAdmin(admin.ModelAdmin):
    list_display = ['pk', 'product', 'user']
    list_display_links = ['pk', 'product']
    list_filter = ['product', 'user']


@admin.register(models.Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ['pk', 'product']
    filter_horizontal = ['user']


@admin.register(models.Dislike)
class DislikeAdmin(admin.ModelAdmin):
    list_display = ['pk', 'product']
    filter_horizontal = ['user']


@admin.register(models.Favourite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ['pk', 'user', 'product', 'added_at']
    list_display_links = ['pk', 'user']
    list_filter = ['added_at', 'user']
    search_fields = ['user__username', 'product__title']

@admin.register(models.Basket)
class BasketAdmin(admin.ModelAdmin):
    list_display = ['pk', 'user', 'product', 'quantity', 'added_at']
    list_display_links = ['pk', 'user']
    list_filter = ['added_at']
    search_fields = ['user__username', 'product__title']
