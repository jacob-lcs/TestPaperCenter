from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'login$', views.login),
    url(r'add_paper$', views.add_paper),
    url(r'query_difficulty$', views.query_difficulty),
    url(r'query_types$', views.query_types),
    url(r'query_knowledgepoint$', views.query_knowledgepoint),
    url(r'query_grades$', views.query_grades),
    url(r'query_subjects$', views.query_subjects),
    url(r'save_single_topic_selection$', views.save_single_topic_selection)
]
