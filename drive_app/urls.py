from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('signup/', views.user_signup, name='signup'),
    path('login/', views.user_login, name='login'),
    path('', views.home, {'folder_id': 0}, name='home'),  # Root directory view
    path('<int:folder_id>/', views.home, name='home'),  # Subfolder view
    path('create_folder/<int:folder_id>/', views.create_folder, name='create_folder'),
    path('upload_file/<int:folder_id>/', views.upload_file, name='upload_file'),

    path('update_folder/<int:folder_id>/', views.update_folder, name='update_folder'),
    path('update_file/<int:file_id>/', views.update_file, name='update_file'),

    path('delete_folder/<int:folder_id>/', views.delete_folder, name='delete_folder'),
    path('delete_file/<int:file_id>/', views.delete_file, name='delete_file'),




    # path('delete_folder/<int:folder_id>/', views.delete_folder, name='delete_folder'),
    # path('delete_file/<int:file_id>/', views.delete_file, name='delete_file'),


]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)