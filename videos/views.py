from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic
from videos.models import Row, Movies
from .forms import MoviesForm, SearchForm
from django.forms import formset_factory


def home(request):
    return render(request, "videos/home.html")


def dashboard(request):
    return render(request, "videos/dashboard.html")


def add_movie(request, pk):
    form = MoviesForm()
    # video_form_set = formset_factory(MoviesForm, extra=5)
    # form = video_form_set()

    search_form = SearchForm()

    if request.method == "POST":
        filled_form = MoviesForm(request.POST)
        # filled_form = video_form_set(request.POST)
        if filled_form.is_valid():
            #loop for formset and + changes in html
            # for form in filled_form:
            movie = Movies()
            movie.url = filled_form.cleaned_data["url"]
            movie.title = filled_form.cleaned_data["title"]
            movie.youtube_id = filled_form.cleaned_data["youtube_id"]
            movie.row = Row.objects.get(pk=pk)
            movie.save()
            return redirect("home")

    else:
        pass

    return render(request, "videos/add_movie.html", {"form": form, "search_form": search_form})


class SignUp(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy("home")
    template_name = "registration/signup.html"

    # add automatic login after signup
    def form_valid(self, form):
        view = super(SignUp, self).form_valid(form)
        username, password = form.cleaned_data.get("username"), form.cleaned_data.get("password1"),
        user = authenticate(username=username, password=password)
        login(self.request, user)
        return view


class CreateRow(generic.CreateView):
    model = Row
    fields = ["title"]
    template_name = "videos/create_row.html"
    success_url = reverse_lazy("home")

    # adding user data to the form
    def form_valid(self, form):
        form.instance.user = self.request.user
        super(CreateRow, self).form_valid(form)
        return redirect("home")


class DetailRow(generic.DetailView):
    model = Row
    template_name = "videos/detail_row.html"


class UpdateRow(generic.UpdateView):
    model = Row
    template_name = "videos/update_row.html"
    fields = ["title"]
    success_url = reverse_lazy("dashboard")


class DeleteRow(generic.DeleteView):
    model = Row
    template_name = "videos/delete_row.html"
    success_url = reverse_lazy("dashboard")