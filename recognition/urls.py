from django.urls import path
# from .views import upload_image
from .views import upload_video

urlpatterns = [
# path('upload/', upload_image, name='upload'),
path('upload/', upload_video, name='upload_video'),

]
