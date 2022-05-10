from django.urls import path

from myapp import views

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path("register", views.register_request, name="register"),
    path('intro', views.index, name='index'),
    path('similarity_match', views.similarity_match, name='similarity_match'),
    path('stored_sql', views.stored_sql, name='stored_sql')
] 