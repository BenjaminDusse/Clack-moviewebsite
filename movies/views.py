from django.db.models import query
from django.shortcuts import redirect, render
from django.views.generic import ListView, DetailView
from django.views.generic.base import View

from .forms import ReviewForm
from .models import Movie


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
            form.movie = movie
            form.save()

        print(request.POST)
        return redirect('/')

