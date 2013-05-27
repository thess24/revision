from django.db import models
from django.forms import ModelForm, Textarea
from django.contrib.auth.models import User, Group
from django import forms




class Project(models.Model):
	project_name = models.CharField(max_length=200)
	due_date = models.DateTimeField('Due Date')

	def __unicode__(self):
		return self.project_name

class Item(models.Model):
	project = models.ForeignKey(Project)
	create_user = models.CharField(max_length=40)
	update_user = models.CharField(max_length=200)
	title = models.CharField(max_length=200)
	comments = models.CharField(max_length=500, blank=True)	
	create_date = models.DateTimeField(auto_now_add=True)
	update_date = models.DateTimeField(auto_now=True)
	sticky = models.BooleanField()
	url = models.URLField(blank=True)
	fileitem = models.FileField(upload_to='files/', blank=True)

	def __unicode__(self):
		return self.title	

class Todo(models.Model):
	project = models.ForeignKey(Project)
	title = models.CharField(max_length=60)
	description = models.CharField(max_length=200, blank=True)
	done = models.BooleanField(default=False)
	due_date = models.DateTimeField('Due Date')
	owner = models.ForeignKey(User)

	def __unicode__(self):
		return self.title	

class Comment(models.Model):
	project = models.ForeignKey(Project)
	item = models.ForeignKey(Item)
	title = models.CharField(max_length=60, default=False)
	comment = models.CharField(max_length=4000, blank=True)
	user = models.ForeignKey(User)
	create_date = models.DateTimeField(auto_now_add=True)

	def __unicode__(self):
		return self.title	

class Announcement(models.Model):
	project = models.ForeignKey(Project)
	title = models.CharField(max_length=60)
	description = models.CharField(max_length=200, blank=True)
	user = models.ForeignKey(User)
	create_date = models.DateTimeField(auto_now_add=True)

	def __unicode__(self):
		return self.title	

## ON FUTURE DB ##

# delete comment title
# make todo duedate optional
# add todo category
# add project description
# add general comments for project
# project owner
# item textarea



###  Forms to create items and projects  ###
class ItemForm(ModelForm):
	class Meta:
		model = Item
		exclude = ('create_date', 'update_date','create_user', 'update_user' )

class ProjectForm(ModelForm):
	class Meta:
		model = Project

class ItemFormOnPage(ModelForm):
	class Meta:
		model = Item
		exclude = ('create_date', 'update_date','create_user', 'update_user', 'project' )

class TodoForm(ModelForm):
	class Meta:
		model = Todo
		exclude = ('project', 'done')

	def __init__(self,project,*args,**kwargs):
		super(TodoForm, self).__init__(*args,**kwargs)
		g=Group.objects.get(name=project.lower())
		self.fields['owner'].queryset = g.user_set.all()


class CommentForm(ModelForm):
	class Meta:
		model = Comment
		exclude = ('create_date', 'user', 'project', 'title')
		widgets = {'comment': Textarea(attrs={'cols': 40, 'rows': 5}),'item': Textarea(attrs={'cols': 15, 'rows': 1}) }

	def __init__(self,project,*args,**kwargs):
		super(CommentForm, self).__init__(*args,**kwargs)
		self.fields['item'].queryset = Item.objects.filter(project__project_name__iexact=project)


class AnnouncementForm(ModelForm):
	class Meta:
		model = Announcement
		exclude = ('create_date', 'user', 'project')
		widgets = {'description': Textarea(attrs={'cols': 40, 'rows': 5}),}

