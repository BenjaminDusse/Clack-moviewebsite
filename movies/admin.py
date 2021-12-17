from django import forms
from django.contrib import admin
from django.utils.safestring import mark_safe
from ckeditor_uploader.widgets import CKEditorUploadingWidget

from .models import Category, Genre, Movie, MovieShots, Actor, Rating, RatingStar, Reviews


class MovieAdminForm(forms.ModelForm):
    description = forms.CharField(
        label="Описание", widget=CKEditorUploadingWidget())

    class Meta:
        model = Movie
        fields = "__all__"


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'url']
    list_display_links = ['name', ]


class ReviewInline(admin.StackedInline):
    model = Reviews
    extra = 1
    # readonly_fields = ['name', 'email', ]


class MovieShotsInline(admin.StackedInline):
    model = MovieShots
    extra = 1
    readonly_fields = ("get_image", )

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width="50" height="60"')

    get_image.short_description = "Изображение"


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'url', 'draft', ]
    list_filter = ['category', 'year', ]
    search_fields = ['title', 'category__name', ]
    save_on_top = True
    save_as = True
    actions = ['publish', 'unpublish']
    list_editable = ['draft', ]
    form = MovieAdminForm
    inlines = [MovieShotsInline, ReviewInline]
    readonly_fields = ("get_image", )

    fieldsets = (
        (None, {
            "fields": (("title", "tagline"),)
        }),
        (None, {
            "fields": ("description", "poster", 'get_image')
        }),
        (None, {
            "fields": (("year", "world_premiere", "country"),)
        }),
        ('Actors', {
            "classes": ('collapse',),
            "fields": (("actors", "directors", "genres", "category"),)
        }),
        (None, {
            "fields": (("budget", "fees_in_usa", "fess_in_world"),)
        }),
        ("Options", {
            "fields": (("url", "draft"),)
        }),
    )

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.poster.url} width="50" height="60"')

    get_image.short_description = "Постер"

    def unpublish(self, request, queryset):
        row_update = queryset.update(draft=False)
        if row_update == "1":
            message_bit = f"{row_update} записей были обновлен"
        else:
            message_bit = f"{row_update} записей были обновлен"
        self.message_user(request, f"{message_bit}")

    def publish(self, request, queryset):
        row_update = queryset.update(draft=False)
        if row_update == "1":
            message_bit = f"{row_update} записей были обновлен"
        else:
            message_bit = f"{row_update} записей были обновлен"
        self.message_user(request, f"{message_bit}")

    publish.short_description = "Опублыковать"
    publish.allowrd_permissions = ['change']


    unpublish.short_description = "Снять с публикации"
    unpublish.allowrd_permissions = ['change']


@admin.register(Reviews)
class ReviewAdmin(admin.ModelAdmin):
    """Отзывы к фильму"""
    list_display = ("name", "email", "parent", "movie", "id")
    readonly_fields = ("name", "email")


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    """Жанры"""
    list_display = ("name", "url")


@admin.register(Actor)
class ActorAdmin(admin.ModelAdmin):
    """Актеры"""
    list_display = ("name", "age", 'get_image')
    readonly_fields = ("get_image", )

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width="50" height="60"')

    get_image.short_description = "Изображение"


@admin.register(MovieShots)
class MovieShotsAdmin(admin.ModelAdmin):
    """Кадры из фильма"""
    list_display = ("title", "movie", "get_image", )
    readonly_fields = ("get_image", )

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width="50" height="60"')

    get_image.short_description = "Изображение"


admin.site.register(RatingStar)


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    """Рейтинг"""
    list_display = ("star", 'movie',  "ip")


admin.site.site_title = "Django Movies"
admin.site.site_header = "Django Movies"
