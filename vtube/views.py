from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from .models import Channels, Videos, userHistory
from django.http import JsonResponse
from django.core import serializers


# Create your views here.
def home(request):
	print(request.user.is_anonymous)
	if request.user.is_anonymous:
		params = {'user':request.user, 'isChannel':False}
	else:
		channel = Channels.objects.filter(user=request.user)
		if len(channel) != 0:
			basic = {'channelId':channel[0].id}
			params = {'user':request.user, 'isChannel':True,'basic':basic }
		else:
			params = {'user':request.user, 'isChannel':False}

	# print(Channels.objects.filter())
	# params = {'user':request.user, 'isChannel':True}
	return render(request, "index.html", params)


def getTrending(request):
	videos = list(Videos.objects.all())
	print(type(videos))
	maxview = 0
	trendingv = []
	for video in videos:
		if maxview < video.views:
			trendingv.append(video)
			videos.pop()

	params = {'video':trendingv}
	print(params)
	return render(request, "singleRowCard.html", params)

def handleSignUp(request):
	if request.method == "POST":
		username1 = request.POST.get('username')
		first_name = request.POST.get('fname')
		last_name = request.POST.get('lname')
		phone1 = request.POST.get('phone')
		email1 = request.POST.get('email')
		pass1 = request.POST.get('pass1')
		pass2 = request.POST.get('pass2')

		# Checking crediantial	
		if pass1 != pass2:
			messages.error(request, 'Please Enter <b>Correct Password!!!</b>')
			return redirect('/')
		if authenticate(username=username1, password=pass1) != None:
			messages.error(request, 'That username is already taken. <b>Try another</b>')
			return redirect('/')
		if not username1.isalnum():
			messages.error(request, 'Enter Proper <b>Username!!!</b>')
			return redirect('/')

		myuser = User.objects.create_user(username1, email1, pass1,)
		print(myuser)
		myuser.first_name = first_name
		myuser.last_name = last_name
		myuser.save()
		messages.success(request, "Signed Up <b>Successfully</b>")
		return redirect('/')
	else:
		return HttpResponse("404 - Not Found")

def handleLogin(request):
	if request.method == "POST":
		loginUsername = request.POST.get('usernameLogin')
		loginPass = request.POST.get('passLogin')
		user = authenticate(username=loginUsername, password=loginPass)

		if user is not None:
			login(request, user)
			messages.success(request, "Successfully <b>Logged in</b>")
			return redirect('/')
		else:
			messages.error(request,"Please Check your <b>Username and Password</b>")
			return redirect('/')
	else:
		return HttpResponse("<h1>404 - Not Found</h1>")


def handleLogout(request):
	print(type(request.user.username))
	logout(request)
	return redirect('/')

def handleChannel(request, id):
	# print(len(Channels.objects.filter(user=request.user)))

	if len(Channels.objects.filter(id=id)) > 0:
		channel = Channels.objects.get(id=id)
		basic = {'channelId':channel.id,'title':channel.channelTitle, 'about':channel.about}
		# print(basic)
		if request.user.is_anonymous:
			user_videos = Videos.objects.filter(channel=channel)
			params = {'auth':False, 'basic':basic, 'isChannel':False, 'videos':user_videos}
			return render(request, 'channel.html', params)
		elif request.user == channel.user:
			user_videos = Videos.objects.filter(user=request.user)
			params = {'auth':True, 'basic':basic, 'isChannel':isUserChannel(request.user), 'videos':user_videos}
			return render(request, 'channel.html', params)
		else:
			user_videos = Videos.objects.filter(channel=channel)
			params = {'auth':False, 'basic':basic, 'isChannel':isUserChannel(request.user), 'videos':user_videos}
			return render(request, 'channel.html', params)
	else:
		return HttpResponse("<h1>404 - Not Found</h1>")
	

def CreateChannel(request):
	if request.method == "POST":
		name = request.POST.get('title')
		cAbout = request.POST.get('about')

		# cheack channel name not match to other
		print(request.user)
		channel = Channels(user=request.user, channelTitle=name, about=cAbout)
		channel.save()
		messages.success(request, f"Your Channel <b>{name}</b> is Created!!!")
		return redirect('/')

	else:
		return HttpResponse("404 - Not Found")

def isUserChannel(user):
	if len(Channels.objects.filter(user=user)):
		return True
	else:
		return False


def UploadVideo(request):
	channel = Channels.objects.filter(user=request.user).first()
	params = {'user':request.user, 'channel':channel}

	return render(request, 'upload-video.html', params)

@csrf_exempt
def UploadVideoSave(request):
	if request.method == "POST":
		channel = Channels.objects.filter(user=request.user).first()
		# print(request.FILES['thumbnail'])
		video = Videos(user=request.user, channel=channel, videoTitle=request.POST['title'], desc=request.POST['desc'],thumbnail=request.FILES['thumbnail'], videoFile=request.FILES['video'])
		video.save()
		messages.success(request, "Your Video Successfully Uploaded...")
		return HttpResponse("Uploaded Video Successfully")

	else:
		return HttpResponse("Some Error Occured While Uploading Video<br>Please Try Again")

@csrf_exempt
def editVideo(request, id):
	if request.method == 'POST':
		video = Videos.objects.get(id=id)
		print('Upper Layer')
		if request.user == video.user:
			# print('Safe User')
			# print(request.POST['title'])
			video.videoTitle = request.POST['title']
			video.desc = request.POST['desc']
			video.thumbnail = request.FILES['thumbnail']
			video.save()
			# print('Completed')
			return HttpResponse('Successfully Uploaded ')

	else:
		video = Videos.objects.get(id=id)
		params = {'video':video}
		return render(request, 'Edit-Panel.html', params)

def ChannelAbout(request,id):
	if len(Channels.objects.filter(id=id)) > 0:
		channel = Channels.objects.get(id=id)
		basic = {'channelId':channel.id,'title':channel.channelTitle, 'about':channel.about}
		print(basic)
		if request.user == channel.user:
			params = {'auth':True, 'basic':basic, 'isChannel':isUserChannel(request.user)}
			print(type(params))
			return JsonResponse(params)
		else:
			params = {'auth':False, 'basic':basic, 'isChannel':isUserChannel(request.user)}
			return JsonResponse(params)
	else:
		return HttpResponse("<h1>404 - Not Found</h1>")


def getVideos(request):
	videos = serializers.serialize("json", Videos.objects.all())
	params = {'videos':videos}
	# print(params)
	return HttpResponse(videos)

def watchVideo(request,id):
	video = Videos.objects.get(id=id)
	# print(type(video.views))
	video.views += 1
	video.save()

	print(type(id))
	history = userHistory(user=request.user, vid_id=id)
	history.save()
	return render(request, 'watchVideo.html',{'video':Videos.objects.get(id=id)})


def yourVideo(request):
	if request.user.is_anonymous:
		params = {'user':request.user, 'isChannel':False, 'videos':[]}
	else:
		videos = list(Videos.objects.filter(user=request.user))
		print(videos)
		params = {'videos':videos}

	return render(request, 'your_Videos.html', params)

def userHistoryFunc(request):
	if request.user.is_anonymous:
		params = {'user':request.user, 'isChannel':False, 'videos':[]}
	else:
		uhistory = list(userHistory.objects.filter(user=request.user))
		# print(uhistory[0].vid_id)
		# params = {'videos':videos}
		if (len(uhistory)>0):
			history_list = []
			uhistory.reverse()
			for vid in uhistory:
				print(vid.vid_id)
				history_list.append(Videos.objects.get(id=vid.vid_id))

			print(history_list)
			params = {'video':history_list}
			return render(request, "userHistory.html", params)

		else:
			return render(request, "userHistory.html", params = {'video':[]})



# videos = list(Videos.objects.all())
# 	print(type(videos))
# 	maxview = 0
# 	trendingv = []
# 	for video in videos:
# 		if maxview < video.views:
# 			trendingv.append(video)
# 			videos.pop()

# 	params = {'video':trendingv}
# 	print(params)
# 	return render(request, "singleRowCard.html", params)



