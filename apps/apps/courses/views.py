from django.shortcuts import render, HttpResponse
from django.views.generic.base import View
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q

from .models import Course, CourseResource, Video
from operation.models import UserFavorite, CourseComments, UserCourse
from utils.mixin_utils import LoginRequiredMixin


class CourseListView(View):
    def get(self, request):
        all_courses = Course.objects.all().order_by('-add_time')
        hot_courses = Course.objects.all().order_by('-click_nums')[:3]
        #课程搜索
        search_keywords = request.GET.get('keywords', "")
        if search_keywords:
            all_courses = all_courses.filter(Q(name__icontains=search_keywords)|Q(desc__icontains=search_keywords)|Q(detail__icontains=search_keywords))

        #课程排序
        sort = request.GET.get('sort', '')
        if sort:
            if sort == 'students':
                all_courses = all_courses.order_by('-students')
            elif sort == 'hot':
                all_courses = all_courses.order_by('-click_nums')

        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_courses, 6, request=request)
        courses = p.page(page)


        return render(request, 'course-list.html', {
            'all_courses':courses,
            'sort':sort,
            'hot_courses':hot_courses,
        })


class CourseDetailView(View):
    def get(self, request, course_id):
        couse = Course.objects.get(id=int(course_id))
        couse.click_nums +=1
        couse.save()
        has_fav_course = False
        has_fav_org = False

        if  request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=couse.id, fav_type=1):
                has_fav_course = True
        if  request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=couse.course_org.id, fav_type=2):
                has_fav_org = True

        tag = couse.tag
        if tag:
            relate_course = Course.objects.filter(tag=tag)[:1]
        else:
            relate_course = []
        return render(request, 'course-detail.html', {
            'couse':couse,
            'relate_course':relate_course,
            'has_fav_org':has_fav_org,
            'has_fav_course':has_fav_course
        })


class CourseInfoView(LoginRequiredMixin, View):
    def get(self, request, course_id):
        couse = Course.objects.get(id=int(course_id))
        couse.students +=1
        couse.save()
        #查询用户
        user_courses = UserCourse.objects.filter(user=request.user, course=couse)
        if not user_courses:
            user_course = UserCourse(user=request.user, course=couse)
            user_course.save()
        user_courses = UserCourse.objects.filter(course=couse)
        user_ids = [user_course.user.id for user_course in user_courses]
        all_user_courses =  UserCourse.objects.filter(user_id__in=user_ids)
        course_ids = [user_course.course.id for user_course in all_user_courses]
        all_resources = CourseResource.objects.filter(course=couse)
        relate_courses = Course.objects.filter(id__in=course_ids).order_by('-click_nums')[:5]
        return render(request, 'course-video.html', {
            'couse': couse,
            'all_resources':all_resources,
            'relate_courses':relate_courses,
        })


class CommentsView(LoginRequiredMixin, View):
    def get(self, request, course_id):
        couse = Course.objects.get(id=int(course_id))
        all_resources = CourseResource.objects.filter(course=couse)
        all_comments = CourseComments.objects.all()
        return render(request, 'course-comment.html', {
            'couse': couse,
            'all_resources':all_resources,
            'all_comments':all_comments,
        })

#r添加课程评论
class AddComentsView(View):
    def post(self, request):
        if not request.user.is_authenticated():
            #判断用户登陆状态
            return HttpResponse('{"status":"fail", "msg":"用户未登录"}', content_type='application/json')
        course_id = request.POST.get('course_id', 0)
        comments = request.POST.get('comments', '')
        if int(course_id) >0 and comments:
            course_comments = CourseComments()
            course = Course.objects.get(id = int(course_id))
            course_comments.course = course
            course_comments.comments = comments
            course_comments.user = request.user
            course_comments.save()
            return HttpResponse('{"status":"success", "msg":"添加成功"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"fail", "msg":"添加失败"}', content_type='application/json')


class VideoPlayView(View):
    """ 视频播放"""
    def get(self, request, video_id):
        video = Video.objects.get(id=int(video_id))
        couse = video.lesson.course
        couse.students +=1
        couse.save()
        # 查询用户
        user_courses = UserCourse.objects.filter(user=request.user, course=couse)
        if not user_courses:
            user_course = UserCourse(user=request.user, course=couse)
            user_course.save()
        user_courses = UserCourse.objects.filter(course=couse)
        user_ids = [user_course.user.id for user_course in user_courses]
        all_user_courses = UserCourse.objects.filter(user_id__in=user_ids)
        course_ids = [user_course.course.id for user_course in all_user_courses]
        all_resources = CourseResource.objects.filter(course=couse)
        relate_courses = Course.objects.filter(id__in=course_ids).order_by('-click_nums')[:5]
        return render(request, 'course-play.html', {
            'couse': couse,
            'all_resources': all_resources,
            'relate_courses': relate_courses,
            'video':video,
        })


