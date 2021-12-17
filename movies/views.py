from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.views.generic import ListView, DetailView
from django.views.generic.base import View
from django.db.models import Q
from .forms import ReviewForm, RatingForm
from .models import Actor, Genre, Movie, Category, Rating


class GenreYear:
    def get_genres(self):
        return Genre.objects.all()

    def get_years(self):
        # or values_list
        return Movie.objects.filter(draft=False).values("year")


class MoviesView(GenreYear, ListView):

    model = Movie
    queryset = Movie.objects.filter(draft=False)
    template_name = "movies/movie_list.html"
    # def get(self, request):
    #     movie_list = Movie.objects.all()
    #     context = {
    #          'movie_list': movie_list
    #     }
    #     return render(request, 'movies/movie_list.html', context)


class MovieDetailView(GenreYear, DetailView):

    # def get(self, request, slug):
    #     movie = Movie.objects.get(url=slug)
    #     context = {
    #         'movie': movie
    #     }
    #     return render(request, 'movies/movie_detail.html', context)

    model = Movie
    slug_field = "url"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['star_form'] = RatingForm()
        return context


class AddReview(View):

    def post(self, request, pk):
        form = ReviewForm(request.POST)
        movie = Movie.objects.get(id=pk)
        if form.is_valid():
            form = form.save(commit=False)
            if request.POST.get('parent', None):
                form.parent_id = int(request.POST.get("parent"))
            form.movie = movie
            form.save()

        return redirect(movie.get_absolute_url())


class ActorView(GenreYear, DetailView):
    model = Actor
    template_name = 'movies/actor.html'
    slug_field = 'name'


class FilterMoviesView(GenreYear, ListView):
    """Фильтр фильмов"""
    paginate_by = 5

    def get_queryset(self):
        queryset = Movie.objects.filter(
            Q(year__in=self.request.GET.getlist("year")) |
            Q(genres__in=self.request.GET.getlist("genre"))
        ).distinct()
        return queryset


class JsonFilterMoviesView(ListView):
    def get_queryset(self):
        queryset = Movie.objects.filter(
            Q(year__in=self.request.GET.getlist("year")) |
            Q(genres__in=self.request.GET.getlist("genre"))
        ).distinct().values('title', 'tagline', 'url', 'poster')
        return queryset

    def get(self, request, *args, **kwargs):
        queryset = list(self.get_queryset())
        return JsonResponse({'movies:': queryset}, safe=False)


class AddStarRating(View):
    """Добавление рейтинга фильму"""

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

    def post(self, request):
        form = RatingForm(request.POST)
        if form.is_valid():
            Rating.objects.update_or_create(
                ip=self.get_client_ip(request),
                movie_id=int(request.POST.get("movie")),
                defaults={'star_id': int(request.POST.get("star"))}
            )
            return HttpResponse(status=201)
        else:
            return HttpResponse(status=400)
