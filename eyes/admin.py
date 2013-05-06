from django.contrib import admin
from eyes.models import Item, Project, Todo, Comment, Announcement





class ItemAdmin(admin.ModelAdmin):
	list_display = ('title','project', 'create_user', 'create_date', 'sticky')
	list_filter = ('project', 'create_user')
	search_fields = ['title']


admin.site.register(Item, ItemAdmin)
admin.site.register(Project)
admin.site.register(Todo)
admin.site.register(Comment)
admin.site.register(Announcement)