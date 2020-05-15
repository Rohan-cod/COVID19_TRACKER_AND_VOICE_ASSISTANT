from django.urls import path

from .views import (
    TrackView,
    VoiceView,
    TrackDetailView,
    search_view,
    export,
    HomePageView,
)
urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('<int:pk>/',
         TrackDetailView.as_view(), name='track_detail'),
    path('track/', TrackView.as_view(), name='track'),
    path('voice/', VoiceView.as_view(), name='voice'),
    path('search/', search_view, name='search'),
    path('download/', export, name='download'),

]