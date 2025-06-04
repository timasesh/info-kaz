from django.urls import path, include
from . import views

app_name = 'news'

# Choose a secret prefix for the admin panel URLs
ADMIN_URL_PREFIX = 'aadminkaa01news/' # <-- CHANGE THIS TO SOMETHING UNIQUE!

urlpatterns = [
    path('', views.index, name='index'),
    path('category/<slug:category_slug>/', views.category_detail, name='category_detail'),
    path('contact/', views.contact, name='contact'),
    path('contact/success/', views.contact_success, name='contact_success'),
    path('<slug:news_slug>/', views.news_detail, name='news_detail'),

    # Custom Admin URLs
    path(f'{ADMIN_URL_PREFIX}login/', views.admin_login, name='admin_login'),
    path(f'{ADMIN_URL_PREFIX}news/', views.admin_news_list, name='admin_news_list'),
    path(f'{ADMIN_URL_PREFIX}news/create/', views.admin_news_create, name='admin_news_create'),
    path(f'{ADMIN_URL_PREFIX}news/<slug:news_slug>/edit/', views.admin_news_update, name='admin_news_update'),
    path(f'{ADMIN_URL_PREFIX}news/<slug:news_slug>/delete/', views.admin_news_delete, name='admin_news_delete'),
    path(f'{ADMIN_URL_PREFIX}news/trash/', views.admin_news_trash, name='admin_news_trash'),
    path(f'{ADMIN_URL_PREFIX}news/<slug:news_slug>/restore/', views.admin_news_restore, name='admin_news_restore'),

    # Custom Admin URLs for Categories
    path(f'{ADMIN_URL_PREFIX}categories/', views.admin_category_list, name='admin_category_list'),
    path(f'{ADMIN_URL_PREFIX}categories/create/', views.admin_category_create, name='admin_category_create'),
    path(f'{ADMIN_URL_PREFIX}categories/<slug:category_slug>/edit/', views.admin_category_update, name='admin_category_update'),
    path(f'{ADMIN_URL_PREFIX}categories/<slug:category_slug>/delete/', views.admin_category_delete, name='admin_category_delete'),

    # Contact message management
    path(f'{ADMIN_URL_PREFIX}contacts/', views.admin_contact_list, name='admin_contact_list'),
    path(f'{ADMIN_URL_PREFIX}contacts/<int:message_id>/', views.admin_contact_detail, name='admin_contact_detail'),
    path(f'{ADMIN_URL_PREFIX}contacts/<int:message_id>/delete/', views.admin_contact_delete, name='admin_contact_delete'),
    path(f'{ADMIN_URL_PREFIX}contacts/<int:message_id>/mark-read/', views.admin_contact_mark_read, name='admin_contact_mark_read'),
] 