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
        qs5 = models.Complain.objects.filter(id__iexact=a).distinct()
        qs7 = models.Complain.objects.all().filter(id__contains = a)
        qs8 = models.Complain.objects.select_related().filter(id__contains=a).distinct()
        qs9 = models.Complain.objects.filter(id__startswith=a).distinct()
        qs10 = models.Complain.objects.filter(id__endswith=a).distinct()
        qs11 = models.Complain.objects.filter(id__istartswith=a).distinct()
        qs12 = models.Complain.objects.all().filter(id__icontains=a)
        qs13 = models.Complain.objects.filter(id__iendswith=a).distinct()
        
        files = itertools.chain(qs5,qs7, qs8, qs9, qs10, qs11, qs12, qs13)
        res = []
        for i in files:
            if i not in res:
                res.append(i)
        
        word = "Searched Result :"
        print("Result")
        
        print(res)
        files = res
        
        page = request.GET.get('page', 1)
        paginator = Paginator(files, 10)
        try:
            files = paginator.page(page)
        except PageNotAnInteger:
            files = paginator.page(1)
        except EmptyPage:
            files = paginator.page(paginator.num_pages)
        
        if files:
            return render(request, 'dashboard/search_result.html',{'files':files, 'word':word})
        return render(request, 'dashboard/search_result.html', {'files':files, 'word':word})
