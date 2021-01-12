from zoom_app.views import channel,code_callback,contacts, chat
from django.urls import path, include

urlpatterns = [
    path('Channel/', channel),
    path('callback/', code_callback),
    path('contacts/', contacts),
    path('chat/', chat),
]