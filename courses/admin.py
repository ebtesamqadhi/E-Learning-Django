from django.contrib import admin
from .models import Subject, Courses, Module

@admin.register(Subject) 
class SubjectAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug']
    prepopulated_fields = {'slug':('title',)} 


class ModuleInline(admin.StackedInline):
    model = Module


@admin.register(Courses)
class Courses(admin.ModelAdmin):
    list_display = ['title', 'subject', 'created', 'status'] 
    list_filter = ['created', 'subject']
    search_fields = ['title', 'overview']
    inlines = [ModuleInline]
    prepopulated_fields = {"slug": ("title",)}

# @admin.register(Module)
admin.site.register(Module)