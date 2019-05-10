from django.urls import path
from . import views
from .views import poll

app_name = 'polls'

urlpatterns = [

    path('', views.poll, name='index'),

    path('<int:question_id>/', views.detail, name='details'),
    path('<int:question_id>/results/', views.results, name='results'),
    path('<int:question_id>/vote', views.vote, name='vote'),
    # path('', views.poll, name='votes'),
]

# path('like/', views.add_like, name='like'),
# path('dislike/', views.add_dislike, name='dislike')