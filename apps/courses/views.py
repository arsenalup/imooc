from django.shortcuts import render
from django.views.generic.base import View
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger

from .models import Course
from operation.models import UserFavorite


class CourseListView(View):
    def get(self, request):
        all_courses = Course.objects.all().order_by('-add_time')
        hot_courses = Course.objects.all().order_by('-click_nums')[:3]

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
            'has_fav_course':has_fav_course,
        })