# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from django.conf.urls import patterns, url
from . import views

urlpatterns = patterns(
    '',
    url(
        r'^teacher/$',
        views.teacher_view,
        name='teacher',
    ),
    url(
        r'^student/$',
        views.student_view,
        name='student',
    ),
    url(
        r'^teacher/getcourse/$',
        views.getTeachCourse,
        name='getteachcourse',
    ),
    url(
        r'^teacher/getallstudent/$',
        views.getAllStudent,
        name='getallstudent',
    ),
    url(
        r'^teacher/getgroup/$',
        views.getGroup,
        name='getgroup',
    ),
    url(
        r'^teacher/setgroupconfig/$',
        views.setGroupConfig,
        name='setgroupconfig',
    ),
    url(
        r'^teacher/newcourse/$',
        views.newCourse,
        name='newcourse',
    ),
    url(
        r'^teacher/delcourse/$',
        views.delCourse,
        name='delcourse',
    ),
    url(
        r'^teacher/stuxls/$',
        views.stuXls,
        name='stuxls',
    ),
    url(
        r'^student/getcourse/$',
        views.getStuCourse,
        name='getstucourse',
    ),
    url(
        r'^student/getgroup/$',
        views.getStuGroup,
        name='getstugroup',
    ),
)
