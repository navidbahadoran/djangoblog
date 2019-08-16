from django.shortcuts import render, redirect
from users.forms import UserRegisterForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.views.generic import CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from users.forms import UserUpdateForm, ProfileUpdateForm
from users.models import Profile
from django.contrib.auth.models import User


class RegisterFormView(CreateView):
    template_name = 'users/register.html'
    form_class = UserRegisterForm

    def get_success_url(self):
        return reverse_lazy('login')

    def form_valid(self, form):
        messages.success(self.request, message=f'Your account has been created! You are now able to log in')
        return super().form_valid(form)


@login_required
def logout_confirm_view(request):
    return render(request, template_name='users/logout_confirm.html')


def logout_view(request):
    if request.method == "POST":
        logout(request)
        return render(request, template_name='users/logout.html')
    else:
        return redirect('post-list')


@login_required
def profile(request):
    if request.POST:
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, message=f'Your account has been updated!')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
    context = {'u_form': u_form,
               'p_form': p_form}
    return render(request, template_name='users/profile.html', context=context)


