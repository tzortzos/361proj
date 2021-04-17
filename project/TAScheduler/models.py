from django.db import models
from enum import Enum


class User(models.Model):
    """
    Represents all three types of user of our application
    """
    class UserType(models.TextChoices):
        ADMIN = "A", ("Administrator")
        PROF = "P", ("Professor")
        TA = "T", ("TA")

    user_id = models.AutoField('User ID (Autogenerated)', primary_key=True)
    type = models.CharField('User Type', max_length=1, choices=UserType.choices, blank=False)

    """The first part of the university email"""
    univ_id = models.CharField('University ID', max_length=20, blank=False)

    l_name = models.CharField('Last Name', max_length=20, blank=True)
    f_name = models.CharField('First Name', max_length=20, blank=True)

    phone = models.CharField(max_length=10, blank=True)

    """
    Output of a Password Hasher
    see: https://docs.djangoproject.com/en/3.2/topics/auth/passwords/
    """
    password = models.CharField(max_length=64, blank=False)
    tmp_password = models.BooleanField(default=True, blank=False)



    def __str__(self):
        return f'{self.f_name} {self.l_name} ({self.univ_id}@umw.edu) [{self.get_type_display()}]'


class Course(models.Model):
    """
    Represents an Abstract Course (Software Engineering 361) which may have multiple
    Course Sections(online,12-2 MW,etc.)
    """

    course_id = models.AutoField('Course Id (Autogenerated)', primary_key=True)
    course_code = models.CharField('Course Code', max_length=4, blank=False)
    course_name = models.TextField('Course Name', max_length=40, blank=False)
    admin_id = models.ForeignKey('User', on_delete=models.SET_NULL, blank=True, null=True)


class CourseSection(models.Model):
    """
    Represents an Abstract Course Section (section 201 of CS361) which may have multiple Lab Sections
    associated to it.
    """

    course_section_id = models.AutoField ('Course Section ID', primary_key=True)
    course_section_code = models.CharField('Course Section Code', blank=False, max_length=3)
    lecture_days = models.CharField('Lecture Day(s)', blank=True, max_length=6)
    lecture_time = models.TextField('Lecture Time', blank=True, max_length=12)
    course_id = models.ForeignKey('Course', on_delete=models.CASCADE, blank=False, help_text="Course ID" )
    instructor_id = models.ForeignKey('User', on_delete=models.SET_NULL, blank=True, null=True,
                                      help_text="Instructor ID")

    class Meta:
        # Adds a unique constraint combination on the two fields
        unique_together = ['course_section_code', 'course_id']



class LabSection(models.Model):
    """
    Represent an Abstract Lab Section (lab section 901, 902, etc.. for Course section 201, Course CS361)
    """

    lab_section_id = models.AutoField('Lab Section ID', primary_key=True)
    lab_section_code = models.CharField('Lab Section Code', blank=False, max_length=3)
    lab_days = models.CharField('Lab Day(s)', blank=True, max_length=6)
    lab_time = models.TextField('Lab Time', blank=True, max_length=12)
    course_section_id = models.ForeignKey('CourseSection', on_delete=models.CASCADE, blank=False,
                                          help_text="Course Section ID")
    ta_id = models.ForeignKey('User', on_delete=models.SET_NULL, blank=True, null=True,
                              help_text="TA ID")

    class Meta:
        # Adds a unique constraint combination on the two fields
        unique_together = ['lab_section_code', 'course_section_id']

class TACourseSectionAssign(models.Model):
    """
    Represents a bridge Entity for the Many to Many relationship between Course Section and TA
    """

    course_section_id = models.ForeignKey('CourseSection', primary_key=True, on_delete=models.CASCADE, blank=False,
                                          help_text="Course Section ID")
    ta_id = models.ForeignKey('User', on_delete=models.CASCADE, blank=False,
                              help_text="TA ID")

    class Meta:
        # Adds a unique constraint combination on the two fields
        unique_together = ['course_section_id', 'ta_id']









