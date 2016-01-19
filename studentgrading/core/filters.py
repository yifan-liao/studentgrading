# -*- coding: utf-8 -*-
from . import models

import django_filters


class StudentFilter(django_filters.FilterSet):

    course = django_filters.NumberFilter(name='courses__pk')
    grouped = django_filters.MethodFilter()

    class Meta:
        model = models.Student
        fields = ['course', 'grouped']

    def filter_grouped(self, queryset, value):
        """
        Filter against if student has any group.
        """
        if value == 'True':
            queryset = queryset.in_any_group(True)
        elif value == 'False':
            queryset = queryset.in_any_group(False)

        return queryset


class GroupFilter(django_filters.FilterSet):

    course = django_filters.NumberFilter(name='course__id')
    leader = django_filters.NumberFilter(name='leader__id')
    has_member = django_filters.NumberFilter(name='members__id')
    has_student = django_filters.MethodFilter()

    class Meta:
        model = models.Group
        fields = ['course', 'leader', 'has_member', 'has_student']

    def filter_has_student(self, queryset, value):
        return queryset.has_student(value)
