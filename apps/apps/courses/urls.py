from django.conf.urls import url, include

from .views import CourseListView, CourseDetailView, CourseInfoView, CommentsView, AddComentsView,  VideoPlayView

urlpatterns = [
    #课程机构列表
    url(r'^list/$', CourseListView.as_view(), name='course_list'),
    url(r'^detail/(?P<course_id>\d+)/$', CourseDetailView.as_view(), name='course_detail'),
    url(r'^info/(?P<course_id>\d+)/$', CourseInfoView.as_view(), name='course_info'),
    url(r'^comment/(?P<course_id>\d+)/$', CommentsView.as_view(), name='course_comment'),
    url(r'^add_comment/$', AddComentsView.as_view(), name='add_comment'),
    url(r'^video/(?P<video_id>\d+)/$', VideoPlayView.as_view(), name='video_play'),


]