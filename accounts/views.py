from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import TemplateView, View
from accounts.forms import EditProfileForm
from accounts.models import Profile
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import UserPassesTestMixin,LoginRequiredMixin
from social.forms import SocialPostForm
from social.models import Image, SocialPost, SocialComment
from django.contrib import messages
from django.template import loader
from django.http import HttpResponse



User=get_user_model()

class UserProfileView(View):
    def get(self, request, *args,username, **kwargs):
        user=get_object_or_404(User,username=username)
        profile=Profile.objects.get(user=user)
        logged_in_user = request.user
        posts=SocialPost.objects.all()
        
        followers = profile.followers.all()
        
        form=SocialPostForm()
        
        if len(followers)==0:
            is_following=False
        for follower in followers:
            if follower==request.user:
                is_following=True
                break
            else:
                is_following=False
        number_of_followers=len(followers)
        template=loader.get_template('users/detail.html')
        
        context={
            'profile':profile,
            'posts':posts,
            'form':form,
            'number_of_followers':number_of_followers,
            'is_following':is_following,
        }
        return HttpResponse(template.render(context, request))
    
    def post(self, request, *args, **kwargs):
        logged_in_user = request.user
        posts=SocialPost.objects.all()
        
        form=SocialPostForm(request.POST,request.FILES)
        files=request.FILES.getlist('image')
        
        if form.is_valid():
            new_post=form.save(commit=False) 
            new_post.author=logged_in_user
            new_post.save() 
            
            for f in files:
                img=Image(image=f) 
                img.save()  
                new_post.image.add(img)
            
        context={
            'form':form  ,
            'posts':posts         
        }
        return render(request, 'users/detail.html', context)






@login_required
def EditProfile(request):
    user =request.user.id 
    profile=Profile.objects.get(user__id=user)
    user_basic_info=User.objects.get(id=user)
    if request.method == 'POST':
        form=EditProfileForm(request.POST,request.FILES,instance=profile)
        if form.is_valid():
            user_basic_info.first_name=form.cleaned_data.get('first_name')
            user_basic_info.last_name=form.cleaned_data.get('last_name')
            
            profile.pinture=form.cleaned_data.get('pinture')
            profile.banner=form.cleaned_data.get('banner')
            profile.location=form.cleaned_data.get('location')
            profile.url=form.cleaned_data.get('url')
            profile.bio=form.cleaned_data.get('bio')
            profile.birthday=form.cleaned_data.get('birthday')
            
            profile.save()
            user_basic_info.save()
            return redirect('users:profile', username=request.user.username)
    else:
        form=EditProfileForm(instance=profile)
    context={
        'form':form,
    }
    return render(request, 'users/edit.html', context)
    

class AddFollower(LoginRequiredMixin, View):
	def post(self, request, pk, *args, **kwargs):
		profile = Profile.objects.get(pk=pk)
		profile.followers.add(request.user)
		messages.add_message(
            self.request,
            messages.SUCCESS,
            'User Followed'
        )
		return redirect('users:profile', username=profile.user.username)


class RemoveFollower(LoginRequiredMixin, View):
	def post(self, request, pk, *args, **kwargs):
		profile = Profile.objects.get(pk=pk)
		profile.followers.remove(request.user)
		messages.add_message(
            self.request,
            messages.SUCCESS,
            'User Unfollowed'
        )
		return redirect('users:profile', username=profile.user.username)

class ListFollowers(View):
    def get(self,request,pk,*args, **kwargs):
        profile=Profile.objects.get(pk=pk)
        followers=Profile.objects.all()
        context={"profile":profile,"followers":followers}
        return render(request,'pages/social/followers_list.html',context)