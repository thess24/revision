# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect, Http404
from eyes.models import Item, Project, User, ItemForm, ProjectForm, ItemFormOnPage, TodoForm, Todo
from django.shortcuts import render, get_object_or_404
from django.views.generic.edit import CreateView
from django.utils import timezone  #for dates on submit
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse


def index(request):
    return HttpResponse("/accounts/register <br> /addproject <br> /accounts/logout <br> /accounts/login")

def projectpage(request, projectname):
	try:
		project = Project.objects.get(project_name__iexact=projectname)
	except:
		raise Http404

	latest_items_list = Item.objects.filter(sticky=False).filter(project__project_name__iexact=projectname).order_by('-update_date')
	latest_items_list_sticky = Item.objects.filter(sticky=True).filter(project__project_name__iexact=projectname).order_by('-update_date')
	todolist = Todo.objects.filter(project__project_name__iexact=projectname)

	if request.method =='POST':
		if 'additem' in request.POST:
			additemform = ItemFormOnPage(request.POST, request.FILES)
			todoform = TodoForm()
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
			todoform = TodoForm(request.POST)
			additemform = ItemFormOnPage()
			if todoform.is_valid():
				instance = todoform.save(commit=False)
				instance.project = project
				instance.save()
				return HttpResponseRedirect(reverse('eyes.views.projectpage', args=(project,)))
	else:
		additemform = ItemFormOnPage()
		todoform = TodoForm()
	context = {'todolist': todolist, 'todoform': todoform, 'additemform': additemform, 'latest_items_list_sticky':latest_items_list_sticky,'latest_items_list':latest_items_list, 'projectname':projectname}
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
			return HttpResponseRedirect(reverse('eyes.views.projectpage', args=(project,)))		
	else:
		form = ProjectForm()
	return render(request, 'eyes/submit.html', {'form':form, })	