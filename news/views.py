from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from datetime import datetime
from django.utils import timezone
from django.contrib.admin.views.decorators import staff_member_required
from django.urls import reverse
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as auth_login
from django.conf import settings
from django import forms
from django.contrib import messages
from .models import Category, News, Contact
from .forms import ContactForm, NewsAdminForm, CategoryAdminForm

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def get_categories():
    return Category.objects.all()

def index(request):
    search_query = request.GET.get('search', '')
    news_list = News.objects.filter(is_published=True)
    
    if search_query:
        news_list = news_list.filter(
            Q(title__icontains=search_query) |
            Q(content__icontains=search_query)
        )
    
    categories = Category.objects.all()
    context = {
        'news_list': news_list,
        'categories': categories,
        'search_query': search_query,
    }
    return render(request, 'news/index.html', context)

def category_detail(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug)
    news_list = News.objects.filter(category=category, is_published=True)
    
    search_query = request.GET.get('search', '')
    date_filter = request.GET.get('date_filter', '')
    
    if search_query:
        news_list = news_list.filter(
            Q(title__icontains=search_query) |
            Q(content__icontains=search_query)
        )
    
    if date_filter:
        news_list = news_list.filter(created_at__date=date_filter)
    
    available_dates = News.objects.filter(
        category=category,
        is_published=True
    ).dates('created_at', 'day', order='DESC')
    
    categories = Category.objects.all()
    context = {
        'category': category,
        'news_list': news_list,
        'search_query': search_query,
        'date_filter': date_filter,
        'available_dates': available_dates,
        'categories': categories,
    }
    return render(request, 'news/category_detail.html', context)

def news_detail(request, news_slug):
    news = get_object_or_404(News, slug=news_slug, is_published=True)
    
    # Логика комментариев удалена
    
    categories = Category.objects.all()
    context = {
        'news': news,
        'categories': categories,
    }
    return render(request, 'news/news_detail.html', context)

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('news:contact_success')
    else:
        form = ContactForm()
    
    categories = Category.objects.all()
    context = {
        'form': form,
        'categories': categories,
    }
    return render(request, 'news/contact.html', context)

def contact_success(request):
    categories = Category.objects.all()
    context = {
        'categories': categories,
    }
    return render(request, 'news/contact_success.html', context)

@staff_member_required
def admin_news_list(request):
    news_list = News.objects.all().order_by('-created_at')
    context = {
        'news_list': news_list,
        'categories': Category.objects.all(), # Для навигации
    }
    return render(request, 'news/admin/news_list.html', context)

@staff_member_required
def admin_news_create(request):
    if request.method == 'POST':
        form = NewsAdminForm(request.POST, request.FILES)
        if form.is_valid():
            news_item = form.save()
            return redirect(reverse('news:admin_news_list'))
    else:
        form = NewsAdminForm()
    
    context = {
        'form': form,
        'categories': Category.objects.all(), # Для навигации
    }
    return render(request, 'news/admin/news_form.html', context)

@staff_member_required
def admin_news_update(request, news_slug):
    news_item = get_object_or_404(News, slug=news_slug)
    if request.method == 'POST':
        form = NewsAdminForm(request.POST, request.FILES, instance=news_item)
        if form.is_valid():
            form.save()
            return redirect(reverse('news:admin_news_list'))
    else:
        form = NewsAdminForm(instance=news_item)
    
    context = {
        'form': form,
        'categories': Category.objects.all(), # Для навигации
    }
    return render(request, 'news/admin/news_form.html', context)

@staff_member_required
def admin_news_delete(request, news_slug):
    news_item = get_object_or_404(News, slug=news_slug)
    if request.method == 'POST':
        news_item.delete()
        return redirect(reverse('news:admin_news_list'))
    
    context = {
        'news_item': news_item,
        'categories': Category.objects.all(), # Для навигации
    }
    return render(request, 'news/admin/news_confirm_delete.html', context)

# Custom Admin Views for Categories
@staff_member_required
def admin_category_list(request):
    categories_list = Category.objects.all().order_by('name')
    context = {
        'categories_list': categories_list,
        'categories': Category.objects.all(), # Для навигации
    }
    return render(request, 'news/admin/category_list.html', context)

@staff_member_required
def admin_category_create(request):
    if request.method == 'POST':
        form = CategoryAdminForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('news:admin_category_list'))
    else:
        form = CategoryAdminForm()
    
    context = {
        'form': form,
        'categories': Category.objects.all(), # Для навигации
    }
    return render(request, 'news/admin/category_form.html', context)

@staff_member_required
def admin_category_update(request, category_slug):
    category_item = get_object_or_404(Category, slug=category_slug)
    if request.method == 'POST':
        form = CategoryAdminForm(request.POST, instance=category_item)
        if form.is_valid():
            form.save()
            return redirect(reverse('news:admin_category_list'))
    else:
        form = CategoryAdminForm(instance=category_item)
    
    context = {
        'form': form,
        'categories': Category.objects.all(), # Для навигации
    }
    return render(request, 'news/admin/category_form.html', context)

@staff_member_required
def admin_category_delete(request, category_slug):
    category_item = get_object_or_404(Category, slug=category_slug)
    if request.method == 'POST':
        category_item.delete()
        return redirect(reverse('news:admin_category_list'))
    
    context = {
        'category_item': category_item,
        'categories': Category.objects.all(), # Для навигации
    }
    return render(request, 'news/admin/category_confirm_delete.html', context)

def admin_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if user.is_staff:
                auth_login(request, user)
                # Перенаправление на страницу списка новостей в админке
                return redirect(reverse('news:admin_news_list'))
            else:
                # Возможно, добавить сообщение об ошибке для не-персонала
                pass # Пока просто оставим без перенаправления
    else:
        form = AuthenticationForm()
    
    context = {
        'form': form,
        'categories': Category.objects.all(), # Для навигации
    }
    return render(request, 'news/admin/login.html', context)

@staff_member_required
def admin_contact_list(request):
    status = request.GET.get('status')
    if status == 'unread':
        messages = Contact.objects.filter(status='new').order_by('-created_at')
    elif status == 'read':
        messages = Contact.objects.filter(status='read').order_by('-created_at')
    else:
        messages = Contact.objects.all().order_by('-created_at')
    
    unread_count = Contact.objects.filter(status='new').count()
    
    context = {
        'messages': messages,
        'unread_messages_count': unread_count,
    }
    return render(request, 'news/admin/contact_list.html', context)

@staff_member_required
def admin_contact_detail(request, message_id):
    message = get_object_or_404(Contact, id=message_id)
    context = {
        'message': message,
        'unread_messages_count': Contact.objects.filter(status='new').count(),
    }
    return render(request, 'news/admin/contact_detail.html', context)

@staff_member_required
def admin_contact_delete(request, message_id):
    message = get_object_or_404(Contact, id=message_id)
    if request.method == 'POST':
        message.delete()
        messages.success(request, 'Сообщение успешно удалено')
        return redirect('news:admin_contact_list')
    return render(request, 'news/admin/contact_confirm_delete.html', {'message': message})

@staff_member_required
def admin_contact_mark_read(request, message_id):
    message = get_object_or_404(Contact, id=message_id)
    if request.method == 'POST':
        message.status = 'read'
        message.save()
        messages.success(request, 'Сообщение отмечено как прочитанное')
    return redirect('news:admin_contact_detail', message_id=message.id) 