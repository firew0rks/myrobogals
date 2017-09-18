import datetime
import json
import logging
import os

import cStringIO
import markdown
import re
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.views.generic import FormView, ListView

from myrobogals.rgwiki.forms import UploadForm, CreateForm, EditForm
from myrobogals.rgwiki.models import Article, Tag

# TODO: Implement logging for production
logger = logging.getLogger('django.request')


def home(request):
    return render(request, 'wiki/home.html')


def article_view(request, slug):
    """
    Renders the markdown article into HTML and displays it
    """
    # TODO: Tags in article view
    try:
        a = Article.objects.get(url=slug)
    except ObjectDoesNotExist:
        messages.error(request, 'The article that was requested does not exist')
        return HttpResponseRedirect(reverse('wiki:home'))

    path = os.path.join(os.path.dirname(__file__), a.location)
    with open(path, 'rU') as f:
        text_string = f.read()
        md = markdown.Markdown(extensions=['markdown.extensions.toc'])
        html = md.convert(text_string)
        s = md.toc

        # Rendering toc to include bootstrap classes
        toc = '<div class="toc">\n<ul>\n'

        while 1:
            idx1 = s.find('<li>')
            idx2 = s.find('<li>', idx1 + 4)

            if idx2 == -1:
                toc += '<li class="list-group-item">' + s[idx1 + 4:]
                break

            toc += '<li class="list-group-item">' + s[idx1 + 4:idx2 - 1] + '\n'
            s = s[idx2:]

        s = toc

        idx1 = s.find('<ul>')
        toc = s[:idx1]

        while 1:
            idx1 = s.find('<ul>')
            idx2 = s.find('<ul>', idx1 + 4)

            if idx2 == -1:
                toc += '<ul class="list-group">' + s[idx1 + 4:]
                break

            toc += '<ul class="list-group">' + s[idx1 + 4:idx2] + '\n'
            s = s[idx2:]

        return render(request, 'wiki/article.html', {'title': a.title, 'text': html, 'toc': toc})


# TODO: MAKE THIS WORK
def generate_pdf(request, slug):
    try:
        a = Article.objects.get(url=slug)
    except ObjectDoesNotExist:
        messages.error(request, 'The article that was requested does not exist')
        return HttpResponseRedirect(reverse('wiki:home'))

    path = os.path.join(os.path.dirname(__file__), a.location)
    output_path = '.'.join([os.path.join(os.path.dirname(__file__), a.location), 'pdf'])

    with open(path, 'rU') as f:
        text_string = f.read()

        # Convert markdown to html
        html = markdown.markdown(text_string)
        pdf = pisa.CreatePDF(cStringIO.StringIO(html), file("test.pdf", "wb"))

        if pdf.err:
            print(pdf.err)

    with open(output_path, 'rb') as f:
        response = HttpResponse(f.read(), content_type="application/pdf")
        response['Content-Disposition'] = 'inline; filename=' + os.path.basename(output_path)
        return response


class SearchView(ListView):
    template_name = 'wiki/search.html'
    paginate_by = 10
    context_object_name = 'article_list'

    def get(self, *args, **kwargs):
        keywords = self.request.GET.get('search')

        self.queryset = Article.objects.filter(
            Q(url__icontains=keywords) |
            Q(title__icontains=keywords) |
            Q(tags__tag__icontains=keywords)
        ).distinct()

        print(self.queryset)
        return super(SearchView, self).get(*args, **kwargs)


class UploadView(FormView):
    template_name = 'wiki/upload.html'
    form_class = UploadForm
    success_url = '/wiki/'
    tags = []

    def post(self, request, *args, **kwargs):
        # Grabbing all the tag values
        self.tags = [value for name, value in request.POST.iteritems() if name.startswith('n_')]
        return super(UploadView, self).post(self, request, *args, **kwargs)

    # Form valid occurs after is_valid is checked in a post request
    def form_valid(self, form):
        """
        Overriding form_valid method to save files to a particular location
        """

        # Filling out information for the article
        a = Article()
        a.author = self.request.user
        a.date_created = datetime.datetime.now()
        a.date_modified = datetime.datetime.now()

        # Filling out information from form
        a.title = form.cleaned_data['title']
        a.url = form.cleaned_data['slug']

        # Obtaining the uploaded file
        file = self.request.FILES['file']

        tmp_path = os.path.join(os.path.dirname(__file__), 'article/%s.md' % a.url)
        with open(tmp_path, 'wb+') as f:
            for chunk in file.chunks():
                f.write(chunk)

        a.location = ('article/%s.md' % a.url)
        a.save()

        generate_preview_text(article_obj=a, path=tmp_path)
        edit_tags(a, self.tags)
        a.save()

        messages.success(self.request, 'Successfully uploaded %s' % a.title)
        return super(UploadView, self).form_valid(form)


def write_article(article_obj, article):
    tmp_path = os.path.join(os.path.dirname(__file__), 'article/%s.md' % article_obj.url)
    with open(tmp_path, 'wb') as f:
        f.write(article)
    article_obj.location = ('article/%s.md' % article_obj.url)
    generate_preview_text(article_obj=article_obj, article=article)


def generate_preview_text(article_obj, article=None, path=None):
    if path:
        print('here')
        # Open file to get article as string
        with open(path, 'rU') as f:
            article = f.read()

    print(article)
    # Generating preview text from text between <p>...</p> elements
    html = markdown.markdown(article)
    text = re.findall('<p>(.+)</p>', html)
    text = ' '.join(text)
    article_obj.preview_text = text[:350] + '...'


def edit_tags(a, tags):
    # Removing previous tag entries
    for dict in a.tags.values():
        for key, value in dict.iteritems():
            if key == 'id':
                curr_tag = Tag.objects.get(id=value)
                a.tags.remove(curr_tag)

    # Associating tags with the article
    for t in tags:
        try:
            tt = Tag.objects.get(tag__iexact=t)
        except ObjectDoesNotExist:
            tt = Tag(tag=t)
            tt.save()

        a.tags.add(tt)


class CreateView(FormView):
    template_name = 'wiki/create.html'
    form_class = CreateForm
    success_url = '/wiki/'

    def post(self, request, *args, **kwargs):
        form = self.get_form()

        # Grabbing all the tag values
        tags = [value for name, value in request.POST.iteritems() if name.startswith('n_')]

        if form.is_valid():
            return self.form_valid2(form, tags)
        else:
            return self.form_invalid(form)

    def form_valid2(self, form, tags):
        a = Article()

        a.author = self.request.user
        a.created = datetime.datetime.now()
        a.modified = datetime.datetime.now()

        a.title = form.cleaned_data['title']

        # Check for slug uniqueness first
        try:
            Article.objects.get(url=form.cleaned_data['slug'])
            messages.error(self.request, 'The chosen url for this article has already been taken, choose another one')
            return self.form_invalid(form)
        except ObjectDoesNotExist:
            a.url = form.cleaned_data['slug']

        # String containing the wiki article
        write_article(a, form.cleaned_data['article'])

        # Saving reference of article to database
        a.save()

        edit_tags(a, tags)
        a.save()

        # Redirects user to success url
        messages.success(self.request, 'New Article Created!')
        return self.form_valid(form)


class EditView(FormView):
    """
    Allows the user to open and edit the document and only update the following fields:
    title, contributor list (auto), article, tags and version
    """

    template_name = 'wiki/create.html'
    form_class = CreateForm
    success_url = '/wiki/'
    failure_url = '/wiki/'

    def get_context_data(self, **kwargs):
        form = kwargs.get('form')
        tags = kwargs.get('tags')
        return {'form': form, 'tags': tags, 'edit': True}

    def get(self, request, *args, **kwargs):
        slug = kwargs['slug']
        try:
            a = Article.objects.get(url=slug)
        except ObjectDoesNotExist:
            messages.error(self.request, 'The article that was requested does not exist')
            return HttpResponseRedirect(self.failure_url)

        path = os.path.join(os.path.dirname(__file__), a.location)
        with open(path, 'rU') as f:
            text_string = f.read()

        data = {'title': a.title, 'slug': a.url, 'article': text_string}
        form = EditForm(initial=data)

        tags = [value.tag for value in a.tags.all()]

        # Render tags as spans
        tag_spans = ''
        for t in tags:
            tag_spans += '<span>' + t + '</span>'

        return render(request, self.template_name, {'form': form, 'tags': tag_spans, 'edit': True})

    def post(self, request, *args, **kwargs):
        form = self.get_form()

        # Grabbing all the tag values
        tags = [value for name, value in request.POST.iteritems() if name.startswith('n_')]

        if form.is_valid():
            return self.form_valid2(form, tags)
        else:
            return self.form_invalid2(form, tags)

    def form_valid2(self, form, tags):
        """
        When editing an article, the items that can only be changed are:
        title, contributor list, article, tags and version
        """

        # Get the existing article from database
        try:
            a = Article.objects.get(url=form.cleaned_data['slug'])
        except ObjectDoesNotExist:
            messages.error(self.request, 'The slug field cannot be changed in edit mode')
            return HttpResponseRedirect(self.failure_url)

        a.title = form.cleaned_data['title']
        a.modified = datetime.datetime.now()

        # TODO: Add contributor list here

        write_article(a, form.cleaned_data['article'])
        edit_tags(a, tags)

        a.save()

        messages.success(self.request, '%s has been successfully edited' % a.title)
        return self.form_valid(form)

    def form_invalid2(self, form, tags):
        return self.render_to_response(self.get_context_data(form=form))


def save_and_continue(request, slug):
    if request.method == "POST":
        try:
            a = Article.objects.get(url=slug)
        except ObjectDoesNotExist:
            print("ObjectDoesNotExist")
            response = HttpResponse(json.dumps({"message": "Cats are in space!"}), content_type="application/json")
            response.status_code = 400
            return response

        title = request.POST.get("title")
        article = request.POST.get("article")
        tags = request.POST.getlist("tags[]")

        a.title = title
        write_article(a, article)
        edit_tags(a, tags)

        a.save()

        response_data = {'is_successful': True}
        return HttpResponse(json.dumps(response_data), content_type="application/json")
