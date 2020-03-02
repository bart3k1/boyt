from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.http import Http404, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic
from videos.models import Row, Movies
from .forms import MoviesForm, SearchForm
from django.forms import formset_factory
import urllib
import requests
from django.forms.utils import ErrorList

YOUTUBE_API_KEY = ""


def home(request):
    recent_rows = Row.objects.all().order_by("-id")[:3]
    popular_rows = [Row.objects.get(pk=5), Row.objects.get(pk=4), Row.objects.get(pk=2)]
    return render(request, "videos/home.html", {"recent_rows": recent_rows, "popular_rows": popular_rows})


@login_required()
def dashboard(request):
    rows = Row.objects.filter(user=request.user)
    return render(request, "videos/dashboard.html", {"rows": rows})


class DeleteMovie(LoginRequiredMixin, generic.DeleteView):
    model = Movies
    template_name = "videos/delete_movie.html"
    success_url = reverse_lazy("dashboard")

    def get_object(self):
        movie = super(DeleteMovie, self).get_object()
        if not movie.row.user == self.request.user:
            raise Http404
        return movie


@login_required()
def movie_search(request):
    search_form = SearchForm(request.GET)
    if search_form.is_valid():
        encoded_search_term = urllib.parse.quote(search_form.cleaned_data["search_term"])
        response = requests.get(
            f"https://www.googleapis.com/youtube/v3/search?part=snippet&maxResults=6&q={encoded_search_term}&key={YOUTUBE_API_KEY}")
        return JsonResponse(response.json())
    return JsonResponse({"error": "Form not validated"})


def add_movie(request, pk):
    form = MoviesForm()
    # video_form_set = formset_factory(MoviesForm, extra=5)
    # form = video_form_set()

    search_form = SearchForm()
    row = Row.objects.get(pk=pk)
    if not row.user == request.user:
        raise Http404

    if request.method == "POST":
        form = MoviesForm(request.POST)
        # filled_form = video_form_set(request.POST)
        if form.is_valid():
            # loop for formset and + changes in html
            # for form in filled_form:
            movie = Movies()
            movie.row = row
            movie.url = form.cleaned_data["url"]
            # movie.title = filled_form.cleaned_data["title"]
            # movie.youtube_id = filled_form.cleaned_data["youtube_id"]
            parsed_url = urllib.parse.urlparse(movie.url)
            movie_id = urllib.parse.parse_qs(parsed_url.query).get("v")
            if movie_id:
                movie.youtube_id = movie_id[0]
                response = requests.get(
                    f"https://www.googleapis.com/youtube/v3/videos?part=snippet&id={movie_id[0]}&key={YOUTUBE_API_KEY}")
                json = response.json()
                title = json["items"][0]["snippet"]["title"]
                movie.title = title
                movie.save()
                return redirect("detail_row", pk)
            else:
                errors = form._errors.setdefault("url", ErrorList())
                errors.append("Needs to be youtube url")
    else:
        pass

    return render(request, "videos/add_movie.html", {"form": form, "search_form": search_form, "row": row})


class CreateRow(LoginRequiredMixin, generic.CreateView):
    model = Row
    fields = ["title"]
    template_name = "videos/create_row.html"
    success_url = reverse_lazy("dashboard")

    # adding user data to the form
    def form_valid(self, form):
        form.instance.user = self.request.user
        super(CreateRow, self).form_valid(form)
        return redirect("dashboard")


class DetailRow(generic.DetailView):
    model = Row
    template_name = "videos/detail_row.html"


class UpdateRow(LoginRequiredMixin, generic.UpdateView):
    model = Row
    template_name = "videos/update_row.html"
    fields = ["title"]
    success_url = reverse_lazy("dashboard")

    def get_object(self):
        row = super(UpdateRow, self).get_object()
        if not row.user == self.request.user:
            raise Http404
        return row


class DeleteRow(LoginRequiredMixin, generic.DeleteView):
    model = Row
    template_name = "videos/delete_row.html"
    success_url = reverse_lazy("dashboard")

    def get_object(self):
        row = super(DeleteRow, self).get_object()
        if not row.user == self.request.user:
            raise Http404
        return row


class SignUp(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy("dashboard")
    template_name = "registration/signup.html"

    # add automatic login after signup
    def form_valid(self, form):
        view = super(SignUp, self).form_valid(form)
        username, password = form.cleaned_data.get("username"), form.cleaned_data.get("password1"),
        user = authenticate(username=username, password=password)
        login(self.request, user)
        return view


