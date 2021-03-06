from datetime import tzinfo, timedelta, datetime
from django.shortcuts import render
from django.views.generic import TemplateView
from braces import views
from braces.views import AnonymousRequiredMixin
from braces.views import LoginRequiredMixin
from django.http import HttpResponseForbidden, HttpResponseRedirect, HttpRequest
from django.core.urlresolvers import reverse
from django.contrib.auth import logout
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework.views import APIView
from rest_framework.response import Response
from registration_api import utils
from restless.views import Endpoint
from utils.forms import MemberLoginForm
from utils.forms import MemberForm
from property.forms import SearchForm
from icon.models import ActionIcon
from forms import MessageForm, PropertyForm, ThreadForm, PostForm
from models import Post, Thread


class DashboardViewMixin(object):

    def get_context_data(self,**kwargs):
        context = super(DashboardViewMixin,
                  self).get_context_data(**kwargs)
        member_form = MemberForm()
        thread_form = ThreadForm()
        post_form = PostForm()
        user = HttpRequest.user
        context['user'] = user
        context['member_form'] = member_form
        context['thread_form'] = thread_form
        context['post_form'] = post_form
        context['form'] = MessageForm()
        post_action = ActionIcon.objects.get(action_id=1)
        context['post_action'] = post_action
        context.update(message_form=MessageForm())
        return context


class DashboardLogoutViewMixin(object):
    def get_context_data(self,**kwargs):
        context = super(DashboardLogoutViewMixin,
                  self).get_context_data(**kwargs)
        form = MemberLoginForm()
        context['member_login_form'] = form
        sform =  SearchForm()
        context['property_form'] = sform
        return context

class DashboardView(LoginRequiredMixin,DashboardViewMixin, TemplateView):
    template_name = "dashboard.html"
    
    def get(self, request):
         
        if not request.user.is_authenticated():
            #return render_to_response('signin.html')  
            return render_to_response('signin.html', c, context_instance=RequestContext(request)) 

        message_form = MessageForm()
        property_form = PropertyForm()
        thread_form = ThreadForm() 
        post_form = PostForm()
        return render(request, 'dashboard.html',{'message_form': message_form,
                                                 'property_form': property_form,
                                                  'thread_form': thread_form,
                                                  'post_form': post_form})


class DashboardLogoutView(LoginRequiredMixin, DashboardLogoutViewMixin, TemplateView):
    template_name = "signin.html"
    def get(self, request):
 #       if request.user.is_authenticated(): 
        logout(request)
        form = MemberLoginForm()
        return render(request,'signin.html',{'member_login_form':form})


