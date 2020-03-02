"""boyt URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.urls import path
from videos import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name="home"),
    path('dashboard', views.dashboard, name="dashboard"),

    #Auth
    path('signup', views.SignUp.as_view(), name="signup"),
    path('login', auth_views.LoginView.as_view(), name="login"),
    path('logout', auth_views.LogoutView.as_view(), name="logout"),
    #Rows
    path('row/create', login_required(views.CreateRow.as_view()), name="create_row"),
    path('row/<int:pk>', views.DetailRow.as_view(), name="detail_row"),
    path('row/<int:pk>/delete', views.DeleteRow.as_view(), name="delete_row"),
    path('row/<int:pk>/update', views.UpdateRow.as_view(), name="update_row"),
    #Videos
    path('movie/<int:pk>/delete', views.DeleteMovie.as_view(), name="delete_movie"),
    path('row/<int:pk>/addmovie', views.add_movie, name="add_movie"),
    path('movie/search', views.movie_search, name="movie_search"),

]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)