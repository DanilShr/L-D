
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views import View
from django.views.generic import  ListView

from main.forms import ProfileForm
from main.models import Orders, Profile


class MainView(View):
    def get(self, request):
        user = request.user

        context = {
            'user': user,

        }
        return render(request, 'main/index.html', context=context)



class OrdersView(ListView):
    model = Orders
    context_object_name = 'orders'
    template_name = 'main/orders.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(user=self.request.user)
        return queryset



class ProfileView(View):
    def get(self,request):
        user = request.user
        print(user.id)
        profile = Profile.objects.select_related('user').get(user=user.id)
        context = {
            'profile': profile,
        }
        return render(request, 'main/profile.html', context=context)

    def post(self, request):
        profile = Profile.objects.get(user=request.user)
        if 'delete' in request.POST:
            profile.avatar.delete()
        form = ProfileForm(request.POST, request.FILES, instance=profile)

        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('profile'))


        return render(request, 'main/profile.html', {'form': form})




