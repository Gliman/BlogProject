from django.conf.urls imort urls
from basic_app import views



app_name = 'basic_app'
urlpatterns = [
    url(r'^register/$', views.register, name = 'register' )
]
