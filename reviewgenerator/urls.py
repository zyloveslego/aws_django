from django.urls import path

from . import views


app_name = 'reviewgenerator'
urlpatterns = [
    # path('', views.frontpage, name='frontpage'),
    # path('/receive_request/', views.vote, name='vote'),
    path('jsview', views.my_js_view, name='jsview'),
    path('jstest', views.my_js_test, name='jstest'),

]
