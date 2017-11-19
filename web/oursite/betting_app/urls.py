from django.conf.urls import url, include

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^start', views.start_league, name='start_league'),
    url(r'^bidding', views.bidding, name='bidding'),
    url(r'^confirm_players', views.confirm_players, name='confirm_players'),
]