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
    url(r'save_single_topic_selection$', views.save_single_topic_selection),
    url(r'query_knowledge_point_list$', views.query_knowledge_point_list),
    url(r'add_knowledge_points$', views.add_knowledge_points),
    url(r'query_data_count$', views.query_data_count),
    url(r'query_question_data$', views.query_question_data),
    url(r'delete_question$', views.delete_question)
]
