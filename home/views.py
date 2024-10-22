from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.paginator import Paginator
from django.http import HttpResponse
from .models import Author, Item, AuthorItem
from django.db.models import Q, Count
from .forms import ItemForm, AuthorItemFormSet
from pdf2image import convert_from_path
import os
from django.conf import settings

# Create your views here.
def index(request):
    content_types = Item.objects.values('content_type_id', 'content_type__name').annotate(num_items=Count('id'))
    areas = Item.objects.values('area_id', 'area__name').annotate(num_items=Count('id'))
    repositories = Item.objects.values('repository_id', 'repository__name').annotate(num_items=Count('id'))
    year_production = Item.objects.values('year').annotate(recursos=Count('year'))
    last_added = Item.objects.all().order_by('-id').values()[:50]
    authors = Author.objects.all()
    
    context = {
        'content_types': content_types,
        'areas': areas,
        'repositories': repositories,
        'year_production': year_production,
        'last_added': last_added,
        'authors' : authors
    }

    return render(request, 'index.html', context)

def autores(request):
    letter = request.GET.get('letter', '')
    authors = Author.objects.filter(first_name__istartswith=letter)
    authors = authors.distinct().annotate(item_count=Count('authoritem__item')).order_by('first_name', 'last_name')

    context = {
        'authors': authors,
        'letter': letter,
    }

    return render(request, 'autores.html', context)

def generate_pdf_thumbnail(pdf_path, thumbnail_path):
    pages = convert_from_path(pdf_path, 60, poppler_path=r'C:\Program Files\poppler-24.07.0\Library\bin')
    page = pages[0]
    page.save(thumbnail_path, 'JPEG')

def contenido (request):
    search = request.GET.get('search', '')
    year = request.GET.get('year', '')
    content_type = request.GET.get('content_type', '')
    area = request.GET.get('area', '')
    repository = request.GET.get('repository', '')
    page_number = request.GET.get('page', 1)
    author_id = request.GET.get('author_id', '')

    items = Item.objects.all().prefetch_related('authors')

    if search:
        search_terms = search.split()
        if len(search_terms) == 2:
            first_name, last_name = search_terms
            items = items.filter(
                Q(title__icontains=search) |
                Q(authors__first_name__icontains=first_name) &
                Q(authors__last_name__icontains=last_name)
            ).distinct()
        else:
            items = items.filter(
                Q(title__icontains=search) |
                Q(authors__first_name__icontains=search) |
                Q(authors__last_name__icontains=search)
            ).distinct()

    if year:
        items = items.filter(year=year)

    if content_type:
        items = items.filter(content_type=content_type)

    if area:
        items = items.filter(area=area)
    
    if repository:
        items = items.filter(repository=repository)

    if author_id:
        items = items.filter(authors__id=author_id).distinct()

    paginator = Paginator(items, 12)
    page_obj = paginator.get_page(page_number)


    content_types = Item.objects.values('content_type_id', 'content_type__name').annotate(num_items=Count('id'))
    areas = Item.objects.values('area_id', 'area__name').annotate(num_items=Count('id'))
    repositories = Item.objects.values('repository_id', 'repository__name').annotate(num_items=Count('id'))
    year_production = Item.objects.values('year').annotate(recursos=Count('year'))
    last_added = Item.objects.all().order_by('-id').values()[:50]
    authors = Author.objects.all()
    
    context = {
        'items': page_obj,
        'content_types': content_types,
        'areas': areas,
        'repositories': repositories,
        'year_production': year_production,
        'last_added': last_added,
        'author_id': author_id,
        'search': search,
        'year': year,
        'content_type': content_type,
        'area': area,
        'repository': repository,
        'paginator': paginator,
        'page_obj': page_obj,
        'authors': authors
    }

    return render(request, 'contenido.html', context)

def visualizar(request, id):
    item = Item.objects.get(pk=id)
    authors = item.authors.all()
    return render(request, 'visualizar.html', {'item': item, 'authors': authors})

def agregar(request):
    if not request.session.get('has_access'):
        return redirect('validacion')

    if request.method == 'POST':
        form = ItemForm(request.POST, request.FILES)
        formset = AuthorItemFormSet(request.POST)

        if form.is_valid() and formset.is_valid():
            try:
                item = form.save()
                pdf = request.FILES['pdf']
                pdf_path = os.path.join(settings.MEDIA_ROOT, item.pdf.name)
                
                for author_form in formset:
                    if author_form.cleaned_data:
                        first_name = author_form.cleaned_data.get('first_name')
                        last_name = author_form.cleaned_data.get('last_name')
                        if first_name and last_name:
                            author, created = Author.objects.get_or_create(
                                first_name=first_name,
                                last_name=last_name
                            )
                            AuthorItem.objects.create(author=author, item=item)
                
                thumbnail_path = os.path.join(settings.MEDIA_ROOT, f'thumbnails/{item.id}.jpg')
                generate_pdf_thumbnail(pdf_path, thumbnail_path)

                messages.success(request, 'La obra fue subida exitosamente!')
                form = ItemForm()
                formset = AuthorItemFormSet()
            except Exception as e:
                messages.error(request, f'Error: {str(e)}')
    else:
        form = ItemForm()
        formset = AuthorItemFormSet()

    return render(request, 'agregar.html', {'form': form, 'formset': formset})

def validacion(request):
    if request.method == 'POST':
        key = request.POST.get('key')
        if key == '1234':  # Remplaza '1234' con una clave segura
            request.session['has_access'] = True
            return redirect('agregar')
        else:
            return HttpResponse('Clave invalida', status=403)

    return render(request, 'validacion.html')

def clear_session(request):
    request.session['has_access'] = False
    return redirect('enter_key')