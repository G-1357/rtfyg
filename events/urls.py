from django.contrib.auth import views as auth_views
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.start, name='start'),
    path('enter/', views.enter, name='enter'),
    path('registration/', views.registration, name='registration'),
    path('profile/', views.profile, name='profile'),
    path('logout/', auth_views.LoginView.as_view(), name='logout'),
    path('create_event/', views.create_event, name='create_event'),
    path('event_detail/<int:event_id>/', views.event_detail, name='event_detail'),
    path('edit_event/<int:event_id>/', views.edit_event, name='edit_event'),
    path('delete_event/<int:event_id>/', views.delete_event, name='delete_event'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)