from django import template
from django.db.models import query
from django.shortcuts import redirect, render
from django.views.generic import ListView, DetailView
from django.views.generic.base import View

from .forms import ReviewForm
from .models import Actor, Movie, Category


class MoviesView(ListView):

    model = Movie
    queryset = Movie.objects.filter(draft=False)
    template_name="movies/movie_list.html"
    # def get(self, request):
    #     movie_list = Movie.objects.all()
    #     context = {
    #          'movie_list': movie_list
    #     }
    #     return render(request, 'movies/movie_list.html', context)



class MovieDetailView(DetailView):

    # def get(self, request, slug):
    #     movie = Movie.objects.get(url=slug)
    #     context = {
    #         'movie': movie
    #     }
    #     return render(request, 'movies/movie_detail.html', context)

    model = Movie
    slug_field = "url"


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


class ActorView(DetailView):
    model = Actor
    template_name = 'movies/actor.html'
    slug_field = 'name'