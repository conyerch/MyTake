from django.contrib import admin
from django.urls import path
from .views import Index, SignUpView, Dashboard, ImageView, chat_gpt, DesignPageView, image_gallery, load_image_for_customization, upload_design_to_printful, upload_to_photodeck
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path("", Index.as_view(), name = 'index'),
    path("dashboard/", Dashboard.as_view(), name = 'dashboard'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name = 'take/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name = 'take/logout.html'), name='logout'),
    path('gallery/', ImageView.as_view(), name = 'img_gallery'),
    path('chat/', chat_gpt, name = 'chat_gpt'),
    path('custom/', DesignPageView.as_view(), name = 'custom'),
    path('design/', image_gallery, name = 'design'),
    path('load-image/<str:image_name>/', load_image_for_customization, name='load_image'),
    path('upload/', upload_to_photodeck, name='upload_to_photodeck')
] + static(settings.STATIC_URL)

