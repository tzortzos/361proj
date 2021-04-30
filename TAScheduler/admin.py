from django.contrib import admin
from TAScheduler.models import *

class RecipientInline(admin.TabularInline):
    model = Recipient
    exclude = ('read',)
    extra = 0

class MessageAdmin(admin.ModelAdmin):
    inlines = (RecipientInline,)

class AssignmentInline(admin.TabularInline):
    model = Assignment
    extra = 0

class SectionAdmin(admin.ModelAdmin):
    inlines = (AssignmentInline,)

# Register your models here.
admin.site.register(User)
admin.site.register(Course)
admin.site.register(Section, SectionAdmin)
admin.site.register(Lab)
admin.site.register(Message, MessageAdmin)
admin.site.register(Skill)
admin.site.register(Recipient)
