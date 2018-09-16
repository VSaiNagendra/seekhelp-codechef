from django.shortcuts import render,render_to_response
from django.http import HttpResponseRedirect
import urllib,json
from urllib.request import urlopen,Request
from django.views.decorators.csrf import csrf_protect
from div.models import SendRequest,ReceiveRequest
def index_view(request):
	return render(request,'div/index.html',{})
def logout(request):
	del request.session['token']
	del request.session['uname']
	return HttpResponseRedirect('http://149.129.138.34/login')
def home_view(request):
	token=''
	uname=''
	if request.method=='GET':
		if not request.session.has_key('uname'):
			name=request.GET.get('code')
			post_data = [("grant_type","authorization_code"),("code",name),("client_id","a420ca7d74ada05e8b29411205403ca4"),("client_secret","ab9b1e3c02b7bb2f98080f26372b16f6"),("redirect_uri","http://149.129.138.34/")]     # a sequence of two element tuples
			result=''
			try:
				result = urlopen('https://api.codechef.com/oauth/token', urllib.parse.urlencode(post_data).encode("utf-8"))
			except urllib.error.HTTPError as err:
				print(result)
				return HttpResponseRedirect("http://149.129.138.34/index")
			content = json.loads(result.read().decode('utf-8'))
			token=content['result']['data']['access_token']
			req = Request('https://api.codechef.com/users/me')
			req.add_header('authorization','Bearer '+token)
			req.add_header('content-type','application/json')
			resp =urlopen(req)
			content = json.loads(resp.read().decode('utf-8'))
			uname=content['result']['data']['content']['username']
			request.session['uname']=uname
			request.session['token']=token
			print('token is ')
			print(request.session['token'])
			request.session.set_expiry(3600)
		else:
			print('user already logged in')
			print(request.session['token'])
	return render(request,'div/home.html',{})
def login_view(request):
	if request.session.has_key('uname'):
		if request.session.has_key('token'):
			return HttpResponseRedirect("http://149.129.138.34/home")
	return HttpResponseRedirect("https://api.codechef.com/oauth/authorize?response_type=code&client_id=a420ca7d74ada05e8b29411205403ca4&redirect_uri=http://149.129.138.34/&state=xyz")
def receive_request(request):
	queryset=ReceiveRequest.objects.filter(uname=request.session['uname'])


def submit_request(request):
	if request.method=="POST":
		form=SendRequest()
		form.uname=request.session['uname']
		data=request.POST.copy()
		code=data['problemcode']
		print('code is ')
		print(data)
		print(data['description'])
		form.problemcode=code
		form.languageused=data['languageused']
		form.question=data['question']
		form.description=data['description']
		form.snapshot=data['snapshot']	
		form.save()
		queryset=SendRequest.objects.filter(uname=request.session['uname'])
		if queryset.count()>1:
			queryset=queryset.filter(problemcode=code)
			if queryset.count()>1:
				queryset=queryset.filter(languageused=data['languageused'])
				if queryset.count()>1:
					queryset=queryset.filter(question=data['question'])
		for e in queryset:
			id=e.rid	
		req = Request('https://api.codechef.com/submissions/?result=AC&language='+data['languageused']+'&problemCode='+code+'&fields='+'username')
		req.add_header('authorization','Bearer '+request.session['token'])
		print('url is ')
		print('https://api.codechef.com/submissions/?result=AC&language='+data['languageused']+'&problemCode='+code+'&fields='+'username')
		req.add_header('content-type','application/json')
		resp =urlopen(req)
		content = json.loads(resp.read().decode('utf-8'))
		print('content is ')
		print(content)
		array=content['result']['data']['content']
		i=0
		for i in range(len(array)):
			form=ReceiveRequest()
			form.rrid=id
			form.fname=request.session['uname']
			form.tuname=array[i]['username']
			form.save()
	return render(request,'div/home.html')
