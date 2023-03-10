from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import LogoutView, LoginView
from django.http import HttpResponse, HttpRequest
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse

from .forms import UserProfileUpdateForm, UserRegisterMultiForm
from .models import Blog, Profile
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView


class BlogsListView(ListView):
    template_name = "blog_app/index.html"
    model = Blog


class BlogCreateView(CreateView):
    model = Blog
    template_name = "blog_app/blog_form.html"
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
    model = User
    form_class = UserProfileUpdateForm
    success_url = reverse_lazy("blog_app:about-me")

    def get_form_kwargs(self):
        kwargs = super(UserUpdateView, self).get_form_kwargs()
        kwargs.update(instance={
            'user': self.object,
            'profile': self.object.profile,
        })
        return kwargs

    # def get_context_data(self, **kwargs):
    #     context = super(UserUpdateView, self).get_context_data(**kwargs)
    #     user = self.request.user
    #     bio = Profile.objects.order_by('bio').filter(user=user.pk).first()
    #     avatar = Profile.objects.order_by('avatar').filter(user=user.pk).first()
    #     context['bio'] = bio
    #     context['avatar'] = avatar
    #     return context


class RegisterUserView(CreateView):
    form_class = UserRegisterMultiForm
    template_name = "blog_app/register.html"
    success_url = reverse_lazy("blog_app:index")

    def form_valid(self, form):
        user = form['user'].save()
        profile = form['profile'].save(commit=False)
        profile.user = user
        profile.save()
        return redirect(self.get_success_url())


class LoginUserView(LoginView):
    form_class = AuthenticationForm
    template_name = 'blog_app/login.html'

    def get_success_url(self):
        return reverse_lazy('blog_app:index')
