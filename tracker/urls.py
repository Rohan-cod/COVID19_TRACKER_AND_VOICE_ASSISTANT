from django.urls import path

from django.conf.urls import url, include

from .views import (
    TrackView,
    VoiceView,
    TrackDetailView,
    search_view,
    export_csv,
    export_json,
    HomePageView,
    GraphView,
    VoiceView
)
urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('<int:pk>/',
         TrackDetailView.as_view(), name='track_detail'),
    path('track/', TrackView.as_view(), name='track'),
    path('voice/', VoiceView.as_view(), name='voice'),
    path('search/', search_view, name='search'),
    path('download_csv/', export_csv, name='download_csv'),
    path('download_json/', export_json, name='download_json'),
    path('graph/', GraphView.as_view(), name='graph'),

]