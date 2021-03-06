# vim: ai ts=4 sts=4 et sw=4

import sys,string

from django.template import Library
from django.utils.safestring import *

from rapidsms.webui.utils import render_to_response, paginated
from apps.displaymanager.models import *
from apps.displaymanager.utils import *
register = Library()


@register.filter
def titles(value):
    try :
        klass =[v.klass for v in value][0]
        return klass+";"+'|'.join([v.title for v in value])+";"+'|'.join([v.func for v in value])
    except:
        return []

@register.filter
def listify(value):
    try:
        return list(value)
    except:
        return []

@register.filter
def linkify(value,crumbs,link=None):
    crumbs = crumbs.replace("->","/")
     
    strparams = {value.func:value.title}
    if "?" in value.title or "&" in value.title :strparams["title"] = "" #bogus error checking for scripts - dont need it
    
    if value.title == "":
        link = "<a href='/%s%%(%s)s/%s'>%%(%s)s</a>" % (crumbs,value.func,value.link,value.func)
        try:
            link_data_list = dataEval(value,value.func) #,stringHash(value.params))
            return  mark_safe(' '.join([link % l for l in link_data_list]))
            #div-ify formatting here or link to display manager display
            #return mark_safe(' '.join(lambda(x: link % x: ,link_data_list)))
        except Exception,e:
            return e  
    else:
        link = "<a href='/%s%s'>%%(%s)s</a>" % (crumbs,value.link,value.func)
        return mark_safe(link % strparams)

linkify.needs_autoescape = False

@register.inclusion_tag("displaymanager/partials/reportview.html")
def flowify(value,data,breadcrumbs,view,filter=""):
    if filter == "":
        return {"value":value}
    else:
        b = breadcrumbs.split("->")
        b = b[1:len(b)]
        breadcrumbs = '/'.join(b)+"/%s/%s" % (value,view)
        return {"data":breadcrumbs,"value":value,"filter":filter}


flowify.needs_autoescape = False
@register.tag
def test(parser,token):
    return mark_safe("test")

@register.filter
def keys(value):
    try: 
        return value.keys()
    except:
        return []

@register.filter
def gettype(value,key):
   try:
       return type(value[key])
   except Exception, e:
        return e 

@register.filter
def get(value,key):
   try:
       return value[key]
   except Exception, e:
        return ""

@register.filter
def get_object_list(value,key):
   try:
       return value[key].object_list
   except:
        None


@register.filter
def formatter(value,report):
    try:
        return [evalFunc(value,l) for l in  list(report)]
    except Exception, e:
        return "error"
    
