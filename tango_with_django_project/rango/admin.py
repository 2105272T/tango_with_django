from django.contrib import admin
from rango.models import Category, Page, UserProfile


#Chapter 6 Exercise
class PageAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'url', 'views')

# Add in this class to customized the Admin Interface
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('name',)}

# Update the registeration to include this customised interface
admin.site.register(Category, CategoryAdmin)
admin.site.register(Page, PageAdmin)
admin.site.register(UserProfile)