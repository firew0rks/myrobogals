from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^article/(?P<slug>[a-zA-Z0-9_-]+)/$', views.article_view, name='view'),
    url(r'^article/(?P<slug>[a-zA-Z0-9_-]+)/pdf/$', views.generate_pdf, name='generate-pdf'),
    url(r'^article/(?P<slug>[a-zA-Z0-9_-]+)/edit/$', views.EditView.as_view(), name='edit'),
    url(r'^article/(?P<slug>[a-zA-Z0-9_-]+)/edit/ajax/$', views.save_and_continue, name='save-continue'),
    url(r'^upload/$', views.UploadView.as_view(), name='upload'),
    url(r'^search/$', views.SearchView.as_view(), name='search'),
    url(r'^create/$', views.CreateView.as_view(), name='create'),
    url(r'^$', views.home, name='home'),
]



