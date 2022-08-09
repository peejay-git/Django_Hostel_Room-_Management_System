from multiprocessing import context
from re import U
from secrets import choice
from urllib import request
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views import generic
from bootstrap_modal_forms.mixins import PassRequestMixin
from .models import Hostel, User, Complain
from django.contrib import messages
from django.db.models import Sum
from django.views.generic import CreateView, DetailView, UpdateView, ListView
from django.views.generic.edit import DeleteView, CreateView
from .forms import ComplaintForm, SAComplaintForm
from . import models
import operator
import itertools
import datetime
from django.utils import timezone
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth import authenticate, logout
from django.contrib import auth, messages
from django.contrib.auth.hashers import make_password
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django.db.models import Q
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.forms import PasswordChangeForm

def login_form(request):
    return render(request, 'roomapp/login.html')


def logoutView(request):
    logout(request)
    return redirect('home')

def loginView(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_active:
            auth.login(request, user)
            if user.is_admin or user.is_superuser:
                return redirect('/admin')
            elif user.is_supervisor:
                return redirect('supervisor')
            else:
                
                return redirect('student')
        else:
            messages.info(request, "Invalid Username or password")
            return redirect('home')


class PasswordChangeView(PasswordChangeView):
    form_class = PasswordChangeForm
    success_url = reverse_lazy('home')


# student view
def student(request):
    return render(request, 'student/home.html')
# this is where I am, I wanted to make only the user complaint appear on the home oage

class ComplaintListView(LoginRequiredMixin, ListView):
    model = Complain
    template_name = 'student/home.html'
    context_object_name = 'complains'
    paginate_by = 4

    def get_queryset(self):
        return Complain.objects.order_by('-date_reported')

def my_complaint(request):
    return render(request, 'student/my_complaint.html')

class MyComplaintListView(ListView):
    model = Complain
    template_name = 'student/my_complaint.html'
    context_object_name = 'complains'
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Complain.objects.filter(user=user).order_by('-date_reported')

    
class ComplaintView(LoginRequiredMixin, CreateView):
    form_class = ComplaintForm
    model = Complain
    template_name = 'student/complaint_form.html'
    success_url = reverse_lazy('student')
    

    def __init__(self, *args, **kwargs):
        super(ComplaintView, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-exampleForm'
        self.helper.form_class = 'blueForms'
        self.helper.form_method = 'post'
        self.helper.form_action = 'url_action_call'
    
    def get_context_data(self, **kwargs):
        context = super(ComplaintView, self).get_context_data(**kwargs)
        context['helper'] = self.helper
        return context
    
    def form_valid(self, form):
        self.object = form.save(commit = False)
        self.object.user = self.request.user
        self.object.save()
        return super().form_valid(form)




# supervisor view
def supervisor(request):
    complain = Complain.objects.all().count()
    attended_complain = Complain.objects.filter(is_attended = 'YES').count()
    on_process_complain = Complain.objects.filter(is_attended = 'ON PROCESS').count()
    student = User.objects.filter(is_student= True).count()
    context = {'complain':complain, 'on_process_complain':on_process_complain, 'attended_complain': attended_complain, 'student':student}
    return render(request, 'supervisor/home.html', context)

class SManageComplain(LoginRequiredMixin, ListView):
    model = Complain
    template_name = 'supervisor/manage_complaint.html'
    context_object_name = 'complains'
    paginate_by = 4

    def get_queryset(self):
        return Complain.objects.order_by('-date_reported')


class SEditComplaintView(LoginRequiredMixin,UpdateView):
	model = Complain
	form_class = SAComplaintForm
	template_name = 'supervisor/edit_complaint.html'
	success_url = reverse_lazy('smcomplain')
	success_message = 'Complaint was updated successfully'

class SViewComplain(LoginRequiredMixin,DetailView):
	model = Complain
	template_name = 'supervisor/complaint_detail.html'


@login_required
def asearch(request):
    query = request.GET['query']
    print(type(query))
    
    
    data = query
    print(len(data))
    if(len(data) == 0):
        return redirect('dashboard')
    else:
        a = data
        # search by id
        qs1 = models.Complain.objects.filter(id__iexact=a).distinct()
        qs2 = models.Complain.objects.all().filter(id__contains = a)
        qs3 = models.Complain.objects.select_related().filter(id__contains=a).distinct()
        qs4 = models.Complain.objects.filter(id__startswith=a).distinct()
        qs5 = models.Complain.objects.filter(id__endswith=a).distinct()
        qs6 = models.Complain.objects.filter(id__istartswith=a).distinct()
        qs7 = models.Complain.objects.all().filter(id__icontains=a)
        qs8 = models.Complain.objects.filter(id__iendswith=a).distinct()
        
        # search by category
        qs9 = models.Complain.objects.filter(category__iexact=a).distinct()
        qs10 = models.Complain.objects.all().filter(category__contains = a)
        qs11 = models.Complain.objects.select_related().filter(category__contains=a).distinct()
        qs12 = models.Complain.objects.filter(category__startswith=a).distinct()
        qs13 = models.Complain.objects.filter(category__endswith=a).distinct()
        qs14 = models.Complain.objects.filter(category__istartswith=a).distinct()
        qs15 = models.Complain.objects.all().filter(category__icontains=a)
        qs16 = models.Complain.objects.filter(category__iendswith=a).distinct()
        
        # search by hostel
        qs17 = models.Complain.objects.filter(hostel__name__iexact=a).distinct()
        qs18 = models.Complain.objects.all().filter(hostel__name__contains = a)
        qs19 = models.Complain.objects.select_related().filter(hostel__name__contains=a).distinct()
        qs20 = models.Complain.objects.filter(hostel__name__startswith=a).distinct()
        qs21 = models.Complain.objects.filter(hostel__name__endswith=a).distinct()
        qs22 = models.Complain.objects.filter(hostel__name__istartswith=a).distinct()
        qs23 = models.Complain.objects.all().filter(hostel__name__icontains=a)
        # qs24 = models.Complain.objects.filter(hostel__name__iendswith=a).distinct()
        
        complaints = itertools.chain(qs1, qs2, qs3, qs4, qs5, qs6, qs7, qs8, qs9,qs10, qs11, qs12, qs13, qs14, qs15, qs16, qs17, qs18, qs19, qs20, qs21,qs22, qs23)
        res = []
        for i in complaints:
            if i not in res:
                res.append(i)
        
        word = "Searched Result :"        
        print(res)
        complaints = res
        
        page = request.GET.get('page', 1)
        paginator = Paginator(complaints, 10)
        try:
            complaints = paginator.page(page)
        except PageNotAnInteger:
            complaints = paginator.page(1)
        except EmptyPage:
            complaints = paginator.page(paginator.num_pages)
        
        if complaints:
            return render(request, 'supervisor/search_result.html',{'complaints':complaints, 'word':word})
        return render(request, 'supervisor/search_result.html', {'complaints':complaints, 'word':word})
