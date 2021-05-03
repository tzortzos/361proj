from __future__ import annotations
from django.db import models
from typing import Optional



class UserType(models.TextChoices):
    ADMIN = "A", "Administrator"
    PROF = "P", "Professor"
    TA = "T", "TA"

    @classmethod
    def from_str(cls, maybe_type: str, user_types: dict = None) -> UserType:
        if user_types is None:
            user_types = dict([('A', UserType.ADMIN), ('P', UserType.PROF), ('T', UserType.TA)])
        for key in user_types:
            if maybe_type == key:
                return user_types[key]
        raise TypeError(f'user_type {maybe_type} is not in the set of {user_types}')


    @classmethod
    def try_from_str(cls, maybe_type: str) -> Optional[UserType]:
        try:
            return cls.from_str(maybe_type)
        except TypeError:
            return None


class User(models.Model):
    """
    Represents all three types of user of our application
    """
    id = models.AutoField('User ID (Autogenerated)', primary_key=True)
    type = models.CharField('User Type', max_length=1, choices=UserType.choices, blank=False)

    """The first part of the university email"""
    username = models.CharField('University ID', max_length=20, blank=False)

    l_name = models.CharField('Last Name', max_length=20, blank=True)
    f_name = models.CharField('First Name', max_length=20, blank=True)

    phone = models.CharField(max_length=10, blank=True)

    skills = models.ManyToManyField(to='Skill', blank=True, help_text='What skills does this user possess?')
    description = models.TextField('Extra skills and information', max_length=500, blank=True, default='')

    """
    Output of a Password Hasher
    see: https://docs.djangoproject.com/en/3.2/topics/auth/passwords/
    """
    password = models.CharField(max_length=64, blank=False)
    password_tmp = models.BooleanField(default=True, blank=False)

    def __str__(self):
        return f'{self.f_name} {self.l_name} ({self.username}@umw.edu) [{self.get_type_display()}]'

    def email(self) -> str:
        return f'{self.username}@uwm.edu'


class Course(models.Model):
    """
    Represents an Abstract Course (Software Engineering 361) which may have multiple
    Course Sections(online,12-2 MW,etc.)
    """

    id = models.AutoField('Course Id (Autogenerated)', primary_key=True)
    code = models.CharField('Course Code', max_length=4, blank=False)
    name = models.CharField('Course Name', max_length=40, blank=False)

    preferred_skills = models.ManyToManyField(
        to='TAScheduler.Skill',
        help_text='Preferred Skills',
    )

    def __str__(self):
        return f'({self.code}) {self.name}'


class Section(models.Model):
    """
    Represents an Abstract Course Section (section 201 of CS361) which may have multiple Lab Sections
    associated to it.
    """

    id = models.AutoField('Course Section ID', primary_key=True)
    code = models.CharField('Course Section Code', blank=False, max_length=3)
    days = models.CharField('Lecture Day(s)', blank=True, max_length=6)
    time = models.CharField('Lecture Time', blank=True, max_length=12)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, blank=False, help_text="Course ID")
    prof = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True,
                             help_text="Instructor ID")

    tas = models.ManyToManyField(User, through='Assignment', related_name='section_assign', blank=True,
                                 help_text='Ta\'s Assigned to this Course Section')

    class Meta:
        # Adds a unique constraint combination on the two fields
        unique_together = ['code', 'course']

    def __str__(self):
        if self.prof is not None:
            return f'{self.course} - {self.code} [{self.prof.email()}]'
        else:
            return f'{self.course} - {self.code}'


class Assignment(models.Model):
    ta = models.ForeignKey(User, on_delete=models.CASCADE)
    section = models.ForeignKey(Section, on_delete=models.CASCADE)
    max_labs = models.IntegerField(verbose_name='Maximum number of labs that this TA can be assigned', blank=False)


class Lab(models.Model):
    """
    Represent an Abstract Lab Section (lab section 901, 902, etc.. for Course section 201, Course CS361)
    """

    id = models.AutoField('Lab Section ID', primary_key=True)
    code = models.CharField('Lab Section Code', blank=False, max_length=3)
    day = models.CharField('Lab Day(s)', blank=True, max_length=1)
    time = models.CharField('Lab Time', blank=True, max_length=12)
    section = models.ForeignKey('TAScheduler.Section', on_delete=models.CASCADE, blank=False,
                                help_text="Course Section ID")
    ta = models.ForeignKey('User', on_delete=models.SET_NULL, blank=True, null=True,
                           help_text="TA ID")

    class Meta:
        # Adds a unique constraint combination on the two fields
        unique_together = ['code', 'section']

    def __str__(self):
        if self.ta is not None:
            return f'{self.section} lab {self.code} [{self.ta.email()}]'
        else:
            return f'{self.section} lab {self.code}'


class Message(models.Model):
    """
    Represents a message sent from one user to a set of users.
    """

    sender = models.ForeignKey(
        to='TAScheduler.User', on_delete=models.CASCADE,
        blank=False,
        help_text='From',
    )

    recipients = models.ManyToManyField(
        to='TAScheduler.User', through='TAScheduler.Recipient',
        related_name='messages_received',
        blank=False,
        help_text='To',
    )

    """Setting this in the future is not legal and does not 'schedule' a message"""
    sent = models.DateTimeField(
        null=True, blank=True,
        help_text='Sent date',
    )

    parent = models.ForeignKey(
        # May possibly want to be cascade to make threads easier to delete
        to='TAScheduler.Message', on_delete=models.SET_NULL,
        null=True, blank=True,
        help_text='In response to',
    )

    title = models.CharField(
        max_length=60,
        blank=True,
        help_text='Title',
    )

    body = models.TextField(
        max_length=500,
        blank=False,
        help_text='Body',
    )

    def __str__(self) -> str:
        return f'[{self.sent}] ({self.sender.email()}) {self.title}'


class Recipient(models.Model):
    """
    Represents a single recipient for a message
    """

    recipient = models.ForeignKey(
        to='TAScheduler.User', on_delete=models.CASCADE,
        help_text='To',
    )

    message = models.ForeignKey(
        to='TAScheduler.Message', on_delete=models.CASCADE,
    )

    read = models.DateTimeField(
        null=True, blank=True,
        help_text='Read date',
    )

    def __str__(self) -> str:
        return f'{self.message} -> {self.recipient.email()}'


class Skill(models.Model):
    """
    Represents a singular skill that a TA could possess
    """
    name = models.CharField('Skill', blank=False, unique=True, max_length=30)

    def __str__(self) -> str:
        return self.name
