# -*- coding: utf-8 -*-
from django.contrib.auth import get_user_model

from rest_framework import serializers
from rest_framework.relations import reverse

from .models import (
    Student, Class, Course, Takes,
    Instructor, Teaches, Group, GroupMembership,
    has_four_level_perm,
    get_role_of,
)


# -----------------------------------------------------------------------------
# Custom Fields Class
# -----------------------------------------------------------------------------
class ChildHyperlinkedIdentityField(serializers.HyperlinkedIdentityField):

    def __init__(self, *args, **kwargs):
        self.parent_field_name = kwargs.pop('parent_field_name', None)
        self.parent_query_lookup = kwargs.pop('parent_query_lookup', None)
        super(ChildHyperlinkedIdentityField, self).__init__(*args, **kwargs)

    def get_parent_field_name(self):
        assert self.parent_field_name is not None, (
            "'%s' should either include a `parent_field_name` attribute, "
            "or override the `get_parent_field_name()` method."
            % self.__class__.__name__
        )
        return self.parent_field_name

    def get_parent_query_lookup(self):
        if not self.parent_query_lookup:
            return 'parent_lookup_{0}'.format(self.get_parent_field_name())
        return self.parent_query_lookup

    def get_url(self, obj, view_name, request, format):
        url_kwargs = {
            self.get_parent_query_lookup(): getattr(obj, self.get_parent_field_name()).pk,
            'pk': obj.pk,
        }
        return reverse(view_name, kwargs=url_kwargs, request=request, format=format)


class ChildHyperlinkedRelatedField(serializers.HyperlinkedRelatedField):

    def __init__(self, *args, **kwargs):
        self.parent_field_name = kwargs.pop('parent_field_name', None)
        self.parent_query_lookup = kwargs.pop('parent_query_lookup', None)
        super(ChildHyperlinkedRelatedField, self).__init__(*args, **kwargs)

    def get_parent_field_name(self):
        assert self.parent_field_name is not None, (
            "'%s' should either include a `parent_field_name` attribute, "
            "or override the `get_parent_field_name()` method."
            % self.__class__.__name__
        )
        return self.parent_field_name

    def get_parent_query_lookup(self):
        if not self.parent_query_lookup:
            return 'parent_lookup_{0}'.format(self.get_parent_field_name())
        return self.parent_query_lookup

    def get_url(self, obj, view_name, request, format):
        url_kwargs = {
            self.get_parent_query_lookup(): getattr(obj, self.get_parent_field_name()).pk,
            'pk': obj.pk,
        }
        return reverse(view_name, kwargs=url_kwargs, request=request, format=format)

    def get_object(self, view_name, view_args, view_kwargs):
        parent_query_lookup = self.get_parent_query_lookup()
        lookup_kwargs = {
           self.get_parent_field_name(): view_kwargs[parent_query_lookup],
           'pk': view_kwargs['pk']
        }
        return self.get_queryset().get(**lookup_kwargs)


# -----------------------------------------------------------------------------
# Relationship Mixins
# -----------------------------------------------------------------------------
class CreateTakesMixin(object):
    def to_internal_value(self, data):
        validated_data = super(CreateTakesMixin, self).to_internal_value(data)
        if getattr(self, 'context'):
            request = self.context['request']
            user = request.user
            user_role = get_role_of(user)
            if (isinstance(user_role, Instructor) and
                        request.method == 'POST' and
                        'course' in validated_data):
                # When instructor tries to add a 'takes' with this student,
                # it can only add the student to its course
                request_instructor = user_role
                course = validated_data['course']
                if not request_instructor.is_giving(course):
                    raise serializers.ValidationError({
                        'course': 'Cannot add student to a course not given by you.'
                    })
        return validated_data


class ReadTakesMixin(object):
    def to_representation(self, instance):
        ret = super(ReadTakesMixin, self).to_representation(instance)
        user = self.context['request'].user
        if not has_four_level_perm('core.view_takes', user, instance):
            del ret['grade']

        return ret


class CreateTeachesMixin(object):

    def to_internal_value(self, data):
        validated_data = super(CreateTeachesMixin, self).to_internal_value(data)
        if getattr(self, 'context'):
            request = self.context['request']
            user = request.user
            user_role = get_role_of(user)

            if (isinstance(user_role, Instructor) and
                        request.method == 'POST' and
                        'course' in validated_data and
                        'instructor' in validated_data):
                # When instructor tries to add 'teaches' with a course not given by itself,
                # it can only add itself to this course
                requeset_inst = user_role
                instructor = validated_data['instructor']
                course = validated_data['course']
                if not instructor.pk == requeset_inst.pk and not course.is_given_by(requeset_inst):
                    raise serializers.ValidationError({
                        'course': 'Cannot add an instructor to a course not given by you.'
                    })
        return validated_data


# -----------------------------------------------------------------------------
# Student Serializers
# -----------------------------------------------------------------------------
class CreateStudentSerializer(serializers.HyperlinkedModelSerializer):
    courses = serializers.HyperlinkedIdentityField(
        source='takes',
        view_name='api:student-course-list',
        lookup_url_kwarg='parent_lookup_student',
    )

    class Meta:
        model = Student
        fields = ('url', 'id', 'user', 'name', 'sex', 's_id', 's_class', 'courses', )
        extra_kwargs = {
            'url': {'view_name': 'api:student-detail', },
            'user': {
                'view_name': 'api:user-detail',
            },
            's_class': {
                'view_name': 'api:class-detail',
            }
        }


class ReadStudentSerializer(serializers.HyperlinkedModelSerializer):
    courses = serializers.HyperlinkedIdentityField(
        source='takes',
        view_name='api:student-course-list',
        lookup_url_kwarg='parent_lookup_student',
    )

    class Meta:
        model = Student
        fields = ('url', 'id', 'user', 'name', 'sex', 's_id', 's_class', 'courses', )
        read_only_fields = ('user', 'name', 'sex', 's_id', 's_class', 'courses', )
        extra_kwargs = {
            'url': {'view_name': 'api:student-detail', },
            'user': {
                'view_name': 'api:user-detail',
            },
            's_class': {
                'view_name': 'api:class-detail',
            }
        }

    def to_representation(self, instance):
        ret = super(ReadStudentSerializer, self).to_representation(instance)
        user = self.context['request'].user
        if not has_four_level_perm('core.view_student', user, instance):
            del ret['user']

            if not has_four_level_perm('core.view_student_advanced', user, instance):
                del ret['courses']

                if not has_four_level_perm('core.view_student_normal', user, instance):
                    del ret['s_id']
                    del ret['s_class']

        return ret


# -----------------------------------------------------------------------------
# Instructor Serializers
# -----------------------------------------------------------------------------
class CreateInstructorSerializer(serializers.HyperlinkedModelSerializer):
    courses = serializers.HyperlinkedIdentityField(
        source='teaches',
        view_name='api:instructor-course-list',
        lookup_url_kwarg='parent_lookup_instructor',
    )

    class Meta:
        model = Instructor
        fields = ('url', 'id', 'user', 'name', 'sex', 'inst_id', 'courses')
        extra_kwargs = {
            'url': {'view_name': 'api:instructor-detail', },
            'user': {'view_name': 'api:user-detail', },
        }


class ReadInstructorSerializer(serializers.HyperlinkedModelSerializer):

    courses = serializers.HyperlinkedIdentityField(
        source='teaches',
        view_name='api:instructor-course-list',
        lookup_url_kwarg='parent_lookup_instructor',
    )

    class Meta:
        model = Instructor
        fields = ('url', 'id', 'user', 'name', 'sex', 'inst_id', 'courses')
        read_only_fields = ('user', 'name', 'sex', 'inst_id', 'courses', )
        extra_kwargs = {
            'url': {'view_name': 'api:instructor-detail', },
            'user': {'view_name': 'api:user-detail', },
        }

    def to_representation(self, instance):
        ret = super(ReadInstructorSerializer, self).to_representation(instance)
        user = self.context['request'].user
        if not has_four_level_perm('core.view_instructor', user, instance):
            del ret['user']

            if not has_four_level_perm('core.view_instructor_normal', user, instance):
                del ret['inst_id']

        return ret


# -----------------------------------------------------------------------------
# StudentCourses Serializers (students/{pk}/courses/)
# -----------------------------------------------------------------------------
class CreateStudentCoursesSerializer(CreateTakesMixin,
                                     serializers.HyperlinkedModelSerializer):

    url = ChildHyperlinkedIdentityField(
        view_name='api:student-course-detail',
        parent_field_name='student',
    )

    class Meta:
        model = Takes
        fields = ('url', 'id', 'student', 'course', 'grade')
        extra_kwargs = {
            'student': {'view_name': 'api:student-detail'},
            'course': {'view_name': 'api:course-detail'},
        }


class ReadStudentCoursesSerializer(ReadTakesMixin,
                                   serializers.HyperlinkedModelSerializer):

    url = ChildHyperlinkedIdentityField(
        view_name='api:student-course-detail',
        parent_field_name='student',
    )

    class Meta:
        model = Takes
        fields = ('url', 'id', 'student', 'course', 'grade')
        read_only_fields = ('student', 'course', 'grade', )
        extra_kwargs = {
            'student': {'view_name': 'api:student-detail'},
            'course': {'view_name': 'api:course-detail'},
        }


class BaseWriteStudentCoursesSerializer(CreateStudentCoursesSerializer):

    class Meta(CreateStudentCoursesSerializer.Meta):
        fields = ('url', 'id', 'grade')


# -----------------------------------------------------------------------------
# InstructorCourses Serializers (instructors/{pk}/courses/)
# -----------------------------------------------------------------------------
class CreateInstructorCoursesSerializer(CreateTeachesMixin,
                                        serializers.HyperlinkedModelSerializer):

    url = ChildHyperlinkedIdentityField(
        view_name='api:instructor-course-detail',
        parent_field_name='instructor',
    )

    class Meta:
        model = Teaches
        fields = ('url', 'id', 'instructor', 'course')
        extra_kwargs = {
            'instructor': {'view_name': 'api:instructor-detail'},
            'course': {'view_name': 'api:course-detail'},
        }


class ReadInstructorCoursesSerializer(serializers.HyperlinkedModelSerializer):

    url = ChildHyperlinkedIdentityField(
        view_name='api:instructor-course-detail',
        parent_field_name='instructor',
    )

    class Meta:
        model = Teaches
        fields = ('url', 'id', 'instructor', 'course')
        read_only_fields = ('instructor', 'course', )
        extra_kwargs = {
            'instructor': {'view_name': 'api:instructor-detail'},
            'course': {'view_name': 'api:course-detail'},
        }


# -----------------------------------------------------------------------------
# Course Serializers (courses/{pk}/)
# -----------------------------------------------------------------------------
class ReadCourseSerializer(serializers.HyperlinkedModelSerializer):

    instructors = ChildHyperlinkedRelatedField(
        source='teaches',
        many=True,
        read_only=True,
        view_name='api:course-instructor-detail',
        parent_field_name='course',
    )

    groups = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='api:group-detail',
    )

    class Meta:
        model = Course
        fields = ('url', 'id', 'title', 'year', 'semester', 'description',
                  'min_group_size', 'max_group_size', 'instructors', 'groups')
        read_only_fields = (
            'title', 'year', 'semester', 'description',
            'min_group_size', 'max_group_size', 'instructors'
        )
        extra_kwargs = {
            'url': {'view_name': 'api:course-detail'},
        }

    def to_representation(self, instance):
        ret = super(ReadCourseSerializer, self).to_representation(instance)
        user = self.context['request'].user
        if not has_four_level_perm('core.view_course', user, instance):
            del ret['min_group_size']
            del ret['max_group_size']
            del ret['groups']

            if not has_four_level_perm('core.view_course_advanced', user, instance):
                del ret['instructors']

        return ret


class CreateCourseSerializer(serializers.HyperlinkedModelSerializer):

    instructors = serializers.HyperlinkedRelatedField(
        many=True,
        required=False,
        queryset=Instructor.objects.all(),
        view_name='api:instructor-detail',
    )

    groups = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='api:group-detail',
    )

    class Meta:
        model = Course
        fields = ('url', 'id', 'title', 'year', 'semester', 'description',
                  'min_group_size', 'max_group_size', 'instructors', 'groups')
        extra_kwargs = {
            'url': {'view_name': 'api:course-detail'},
        }

    def create(self, validated_data):
        instructors_data = validated_data.pop('instructors', None)
        course = Course.objects.create(**validated_data)
        if instructors_data:
            for instructor in instructors_data:
                Teaches.objects.create(instructor=instructor, course=course)
        else:
            # if no instructors set, add user to course instructors
            if hasattr(self, 'context'):
                user = self.context['request'].user
                user_role = get_role_of(user)
                if isinstance(user_role, Instructor):
                    user_inst = user_role
                    if not course.is_given_by(user_inst):
                        Teaches.objects.create(instructor=user_inst, course=course)

        return course


class BaseWriteCourseSerializer(CreateCourseSerializer):
    class Meta(CreateCourseSerializer.Meta):
        fields = ('url', 'id', 'min_group_size', 'max_group_size', 'description')


# -----------------------------------------------------------------------------
# CourseInstructors Serializers (courses/{pk}/instructors/)
# -----------------------------------------------------------------------------
class CourseInstructorsSerializer(CreateTeachesMixin,
                                  serializers.HyperlinkedModelSerializer):

    url = ChildHyperlinkedIdentityField(
        view_name='api:course-instructor-detail',
        parent_field_name='course',
    )

    class Meta:
        model = Teaches
        fields = ('url', 'id', 'instructor', 'course')
        extra_kwargs = {
            'instructor': {'view_name': 'api:instructor-detail'},
            'course': {'view_name': 'api:course-detail'},
        }


class ReadCourseInstructorsSerializer(serializers.HyperlinkedModelSerializer):

    url = ChildHyperlinkedIdentityField(
        view_name='api:course-instructor-detail',
        parent_field_name='course',
    )

    class Meta:
        model = Teaches
        fields = ('url', 'id', 'instructor', 'course')
        read_only_fields = ('instructor', 'course')
        extra_kwargs = {
            'instructor': {'view_name': 'api:instructor-detail'},
            'course': {'view_name': 'api:course-detail'},
        }


# -----------------------------------------------------------------------------
# CourseStudents Serializers (courses/{pk}/students/)
# -----------------------------------------------------------------------------
class CreateCourseStudentsSerializer(CreateTakesMixin,
                                     serializers.HyperlinkedModelSerializer):

    url = ChildHyperlinkedIdentityField(
        view_name='api:course-student-detail',
        parent_field_name='course',
    )

    class Meta:
        model = Takes
        fields = ('url', 'id', 'student', 'course', 'grade')
        extra_kwargs = {
            'student': {'view_name': 'api:student-detail'},
            'course': {'view_name': 'api:course-detail'},
        }


class ReadCourseStudentsSerializer(ReadTakesMixin,
                                   serializers.HyperlinkedModelSerializer):

    url = ChildHyperlinkedIdentityField(
        view_name='api:course-student-detail',
        parent_field_name='course',
    )

    class Meta:
        model = Takes
        fields = ('url', 'id', 'student', 'course', 'grade')
        read_only_fields = ('student', 'course', 'grade', )
        extra_kwargs = {
            'student': {'view_name': 'api:student-detail'},
            'course': {'view_name': 'api:course-detail'},
        }


class BaseWriteCourseStudentsSerializer(CreateCourseStudentsSerializer):

    class Meta(CreateCourseStudentsSerializer.Meta):
        fields = ('url', 'id', 'grade')


# -----------------------------------------------------------------------------
# Group Serializers (groups/, courses/{pk}/groups/)
# -----------------------------------------------------------------------------
class CreateGroupSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer for create a group.
    """
    members = serializers.HyperlinkedRelatedField(
        many=True,
        required=False,
        queryset=Student.objects.all(),
        view_name='api:student-detail',
    )

    class Meta:
        model = Group
        fields = ('url', 'id', 'number', 'name', 'course', 'leader', 'members', )
        read_only_fields = ('number', )
        extra_kwargs = {
            'url': {'view_name': 'api:group-detail'},
            'course': {'view_name': 'api:course-detail'},
            'leader': {'view_name': 'api:student-detail'},
        }

    def create(self, validated_data):
        """
        Accept student urls as parameters to `members` and `leader`.
        """
        members_data = validated_data.pop('members', None)
        group = Group.objects.create(**validated_data)
        if members_data:
            for member in members_data:
                GroupMembership.objects.create(student=member, group=group)
        return group


class ReadGroupSerializer(serializers.HyperlinkedModelSerializer):

    members = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='api:group-detail',
    )

    class Meta:
        model = Group
        fields = ('url', 'id', 'number', 'name', 'course', 'leader', 'members', )
        read_only_fields = ('number', 'name', 'course', 'leader', 'members', )
        extra_kwargs = {
            'url': {'view_name': 'api:group-detail'},
            'course': {'view_name': 'api:course-detail'},
            'leader': {'view_name': 'api:student-detail'},
        }


class WriteGroupSerializer(serializers.HyperlinkedModelSerializer):

    members = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='api:group-detail',
    )

    class Meta:
        model = Group
        fields = ('url', 'id', 'number', 'name', 'course', 'leader', 'members', )
        read_only_fields = ('number', 'course', 'members', )
        extra_kwargs = {
            'url': {'view_name': 'api:group-detail'},
            'course': {'view_name': 'api:course-detail'},
            'leader': {'view_name': 'api:student-detail'},
        }

    def update(self, instance, validated_data):
        """
        Add custom actions.

        1. Change leader: after successful changing, pre-leader becomes member, pre-member
        becomes leader.
        """
        leader = validated_data.pop('leader', None)
        group = super(WriteGroupSerializer, self).update(instance, validated_data)
        if leader:
            old_leader = group.leader
            if old_leader.pk == leader.pk:
                return group

            group.leader = leader
            group.save()
            group.group_memberships.get(student=leader).delete()
            GroupMembership.objects.create(student=old_leader, group=group)
        return group


class ClassSerializer(serializers.HyperlinkedModelSerializer):

    url = serializers.HyperlinkedIdentityField(view_name='api:class-detail')
    students = serializers.HyperlinkedRelatedField(
        many=True,
        queryset=Class.objects.all(),
        view_name='api:student-detail',
    )

    class Meta:
        model = Class
        fields = ('url', 'class_id', 'students', )
        read_only_fields = ('url', 'class_id', )


