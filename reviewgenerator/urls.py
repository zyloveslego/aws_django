from django.urls import path

from . import views


app_name = 'reviewgenerator'
urlpatterns = [
    # path('', views.frontpage, name='frontpage'),
    # path('/receive_request/', views.vote, name='vote'),
    path('jsview', views.my_js_view, name='jsview'),
    path('jstest', views.my_js_test, name='jstest'),
    path('register', views.register_request, name='register'),
    path('login', views.login_request, name='login'),

    path('uploadpic', views.upload_pic, name='uploadpic'),

]
