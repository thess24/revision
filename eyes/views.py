# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect, Http404
from eyes.models import Item, Project, User, ItemForm, ProjectForm, ItemFormOnPage, TodoForm, Todo, AnnouncementForm, CommentForm, Announcement, Comment
from django.shortcuts import render, get_object_or_404
from django.views.generic.edit import CreateView
from django.utils import timezone  #for dates on submit
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User,Group

def index(request):
    return render(request, 'eyes/landing.html', )
    
@login_required
def projectpage(request, projectname):
	try:
		project = Project.objects.get(project_name__iexact=projectname)
	except:
		raise Http404

	latest_items_list = Item.objects.filter(sticky=False).filter(project__project_name__iexact=projectname).order_by('-update_date')
	latest_items_list_sticky = Item.objects.filter(sticky=True).filter(project__project_name__iexact=projectname).order_by('-update_date')
	todolist = Todo.objects.filter(project__project_name__iexact=projectname)
	comments = Comment.objects.filter(project__project_name__iexact=projectname).order_by('create_date')
	groups = request.user.groups.values_list('name',flat=True)
	announcements = Announcement.objects.filter(project__project_name__iexact=projectname)[:3]

	if request.method =='POST':
		if 'additem' in request.POST:
			additemform = ItemFormOnPage(request.POST, request.FILES)
			todoform = TodoForm(projectname)
			commentform= CommentForm(projectname)
			if additemform.is_valid():
				instance = additemform.save(commit=False)
				instance.create_user = request.user
				instance.update_user = request.user
				instance.project = project
				if instance.fileitem:
					instance.fileitem = request.FILES['fileitem']
					instance.save()
				else:
					instance.save()
				return HttpResponseRedirect(reverse('eyes.views.projectpage', args=(project,)))	

		elif 'addtodo' in request.POST:
			todoform = TodoForm(projectname, request.POST)
			additemform = ItemFormOnPage()
			commentform= CommentForm(projectname)
			if todoform.is_valid():
				instance = todoform.save(commit=False)
				instance.project = project
				instance.save()
				return HttpResponseRedirect(reverse('eyes.views.projectpage', args=(project,)))

		elif 'deleteitems' in request.POST:
			Item.objects.filter(id__in=request.POST.getlist('deleteitem')).delete()
			return HttpResponseRedirect(reverse('eyes.views.projectpage', args=(project,)))

		elif 'deletetodos' in request.POST:
			Todo.objects.filter(id__in=request.POST.getlist('deletetodo')).delete()
			return HttpResponseRedirect(reverse('eyes.views.projectpage', args=(project,)))

		elif 'subscribe' in request.POST:
			adduser = request.user
			g = Group.objects.get(name=projectname.lower())
			g.user_set.add(adduser)
			return HttpResponseRedirect(reverse('eyes.views.projectpage', args=(project,)))

		elif 'unsubscribe' in request.POST:
			adduser = request.user
			g = Group.objects.get(name=projectname.lower())
			g.user_set.remove(adduser)
			return HttpResponseRedirect(reverse('eyes.views.projectpage', args=(project,)))		

		elif 'commentsubmit' in request.POST:
			todoform = TodoForm(projectname)
			additemform = ItemFormOnPage()
			commentform= CommentForm(projectname, request.POST)
			if commentform.is_valid():
				instance = commentform.save(commit=False)
				instance.project = project
				instance.user= request.user
				instance.save()
				return HttpResponseRedirect(reverse('eyes.views.projectpage', args=(project,)))			


	else:
		additemform = ItemFormOnPage()
		todoform = TodoForm(projectname)
		commentform= CommentForm(projectname)
	context = {'announcements':announcements, 'groups':groups, 'commentform':commentform, 'comments':comments, 'todolist': todolist, 'todoform': todoform, 'additemform': additemform, 'latest_items_list_sticky':latest_items_list_sticky,'latest_items_list':latest_items_list, 'projectname':projectname}
	return render(request, 'eyes/mainviewer.html', context)



@login_required
def additem(request):
	if request.method =='POST':
		form = ItemForm(request.POST, request.FILES)
		if form.is_valid():
			instance = form.save(commit=False)
			instance.create_user = request.user
			instance.update_user = request.user
			project = instance.project	
			if instance.fileitem:
				instance.fileitem = request.FILES['fileitem']
				instance.save()
			else:		
				instance.save()
			return HttpResponseRedirect(reverse('eyes.views.projectpage', args=(project,)))	
	else:
		form = ItemForm()	
	return render(request, 'eyes/submit.html', {'form':form, })	

@login_required
def addproject(request):
	if request.method =='POST':
		form = ProjectForm(request.POST)
		if form.is_valid():
			instance = form.save(commit=False)
			project = instance.project_name
			instance.save()
			Group.objects.create(name=project.lower())
			adduser = request.user
			g = Group.objects.get(name=project.lower())
			g.user_set.add(adduser)
			return HttpResponseRedirect(reverse('eyes.views.projectpage', args=(project,)))		
	else:
		form = ProjectForm()
	return render(request, 'eyes/submit.html', {'form':form, })	

@login_required
def announce(request, projectname):
	try:
		project = Project.objects.get(project_name__iexact=projectname)
	except:
		raise Http404

	announcements = Announcement.objects.filter(project__project_name__iexact=projectname)

	if request.method =='POST':
		form = AnnouncementForm(request.POST)
		if form.is_valid():
			instance = form.save(commit=False)
			instance.project = project
			instance.user = request.user
			instance.save()
	else:
		form = AnnouncementForm()

	context = {'form':form, 'announcements':announcements }
	return render(request, 'eyes/announcements.html', context)


@login_required
def home(request):
	projects = Project.objects.all()
	groups = request.user.groups.values_list('name',flat=True)
	todolist = Todo.objects.filter(owner__username=request.user)
	context = {'groups': groups, 'projects':projects, 'todolist':todolist}
	return render(request, 'eyes/home.html', context)