from django import template

register = template.Library()

@register.simple_tag
def query_params_helper(request, request_page):
    params = request.GET.copy()
    params['page'] = request_page
    return params.urlencode()