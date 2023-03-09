from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth.views import LogoutView, LoginView
from django.http import HttpResponse, HttpRequest
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse

from .forms import UserForm, RegisterUserForm
from .models import Blog, Profile
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView


class BlogsListView(ListView):
    template_name = "blog_app/index.html"
    model = Blog
    context_object_name = "title"
    queryset = [
        Blog.objects.filter(archived=False),
        Blog.objects.filter(),
    ]


class BlogCreateView(CreateView):
    model = Blog
    fields = "title", "articles", "gallery"
    success_url = reverse_lazy("blog_app:index")


# class MyLogoutView(LogoutView):
#     next_page = reverse_lazy("blog_app:index")

def logout_view(request: HttpRequest):
    logout(request)
    return redirect(reverse('blog_app:index'))


class AboutMeView(TemplateView):
    template_name = "blog_app/about-me.html"


# def update_user(request: HttpRequest) -> HttpResponse:
#     if request.method == "POST":
#         form = UserForm(request.POST)
#         if form.is_valid():
#             form.save()
#             url = reverse("blog_app:index")
#             return redirect(url)
#     else:
#         form = UserForm()
#     context = {
#         "form": form,
#     }
#     return render(request, "blog_app/profile_update_form.html", context=context)


class UserUpdateView(UpdateView):
    template_name = "blog_app/profile_update_form.html"
    queryset = Profile.objects.select_related("user")
    fields = "bio", "avatar"
    success_url = reverse_lazy("blog_app:index")

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = "blog_app/register.html"
    success_url = reverse_lazy("blog_app:about-me")

    # def form_valid(self, form):
    #     response = super().form_valid(form)
    #     Profile.objects.create(user=self.object)
    #     username = form.cleaned_data.get("username")
    #     password = form.cleaned_data.get("password1")
    #     user = authenticate(
    #         self.request,
    #         username=username,
    #         password=password,
    #     )
    #     login(request=self.request, user=user)
    #     return response


class LoginUserView(LoginView):
    form_class = AuthenticationForm
    template_name = 'blog_app/login.html'

    def get_success_url(self):
        return reverse_lazy('blog_app:index')
