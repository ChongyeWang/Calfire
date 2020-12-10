from django.urls import path

from .views import (
    home,
    create_database,
    get_map,
    result,
    stat,
    marker,
    chart,
    kMeans,
    about
)

app_name = 'data'

urlpatterns = [
    path('home/', home, name='home'),
    path('create/', create_database, name='create'),
    path('map/', get_map, name='get_map'),
    path('result/', result, name='result'),
    path('stat/', stat, name='stat'),
    path('marker/', marker, name='marker'),
    path('chart/', chart, name='chart'),
    path('kMeans/', kMeans, name='kMeans'),
    path('about/', about, name='about'),
]
