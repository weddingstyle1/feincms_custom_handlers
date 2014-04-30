from feincms.views.base import Handler
from django.shortcuts import get_object_or_404, redirect
from django.http import Http404
from feincms.module.page.models import Page
from feincms_handlers import NotMyJob

class PageIdFallbackHandler(Handler):
    """ This Handler is used if you have static links within your content.
        You can append a get parameter 'p' with the page id. The CMS will
        find the page even if it has been moved.
    """

    def __call__(self, request, path=None):
        if not request.GET.get('p', None):
            raise NotMyJob(self)
        try:
            page = get_object_or_404(Page, pk=request.GET.get('p', None))
        except ValueError:
            raise Http404
        
        url = page.get_absolute_url()
        get_vars = request.GET.copy()
        del(get_vars['p'])
        return redirect(self.url_with_querystring(url, get_vars))
    
    def url_with_querystring(self, url, get_vars):
        if len(get_vars) > 0:
            return '%s?%s' % (url, get_vars.urlencode())
        else:
            return url

handler = PageIdFallbackHandler()
