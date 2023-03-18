from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import LogoutView, LoginView
from django.http import HttpResponse, HttpRequest
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse

from .forms import UserProfileUpdateForm, UserRegisterMultiForm, BlogCreateForm, BlogGalleryCreateForm
from .models import Blog, Profile, BlogGallery
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView


class UserListView(ListView):
    # model = User
    template_name = "blog_app/user_list.html"
    context_object_name = "users"
    queryset = User.objects.order_by('username')


class BlogsListView(ListView):
    template_name = "blog_app/index.html"
    # model = Blog
    queryset = Blog.objects.prefetch_related('gallery').order_by('-create_data_time')

    context_object_name = "blogs"


# class BlogCreateView(CreateView):
#     model = Blog
#     template_name = "blog_app/blog_form.html"
#     # fields = "title", "articles", "gallery"
#     success_url = reverse_lazy("blog_app:index")
#     form_class = BlogCreateForm
#
#     def form_valid(self, form):
#         form.instance.user = self.request.user
#         return super().form_valid(form)

def create_blog(request: HttpRequest, *args, **kwargs):
    user = request.user
    if request.method == 'POST':
        form = BlogCreateForm(request.POST)
        file_form = BlogGalleryCreateForm(request.POST, request.FILES)
        gallery = request.FILES.getlist('gallery')  # field name in model
        if form.is_valid() and file_form.is_valid():
            feed_instance = form.save(commit=False)
            feed_instance.user = user
            feed_instance.save()
            for f in gallery:
                file_instance = BlogGallery(gallery=f, blog=feed_instance)
                file_instance.save()
            return redirect('/index/')
    else:
        form = BlogCreateForm()
        file_form = BlogGalleryCreateForm()
        return render(request, 'blog_app/blog_form.html', {'form': form, 'file_form': file_form, })

    # def form_valid(self, form):
    #     form.instance.user = self.request.user
    #     response = super().form_valid(form)
    #     for image in form.files.getlist("gallery"):
    #         Blog.objects.create(
    #             gallery=image)
    #     return response


# class MyLogoutView(LogoutView):
#     next_page = reverse_lazy("blog_app:index")

def logout_view(request: HttpRequest):
    logout(request)
    return redirect(reverse('blog_app:index'))


class AboutMeView(TemplateView):
    template_name = "blog_app/about-me.html"


class UserDetailView(DetailView):
    model = User
    template_name = "blog_app/user_details.html"


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
    success_url = reverse_lazy("blog_app:about-me")

    def form_valid(self, form):
        response = super().form_valid(form)
        username = form['user'].cleaned_data.get("username")
        password = form['user'].cleaned_data.get("password1")
        user = authenticate(
            self.request,
            username=username,
            password=password
        )
        login(request=self.request, user=user)
        return response


class LoginUserView(LoginView):
    form_class = AuthenticationForm
    template_name = 'blog_app/login.html'

    def get_success_url(self):
        return reverse_lazy('blog_app:index')
