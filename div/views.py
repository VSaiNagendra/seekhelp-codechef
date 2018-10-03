from django.shortcuts import render,render_to_response
from django.http import HttpResponseRedirect,HttpResponse
import urllib,json
from urllib.request import urlopen,Request
from django.views.decorators.csrf import csrf_protect
from div.models import SendRequest,ReceiveRequest,ReplyRequest
def index_view(request):
	return render(request,'div/index.html',{})
def logout(request):
	del request.session['token']
	del request.session['uname']
	return HttpResponseRedirect('http://149.129.138.34/index')
def suggestions_view(request):
	try:
		questions=SendRequest.objects.filter(uname=request.session['uname']).order_by('-rid')
		requests=ReceiveRequest.objects.filter(tuname=request.session['uname']).order_by('-id')
		suggestionsreceived=ReplyRequest.objects.filter(tuname=request.session['uname']).select_related('rerid').order_by('-id')
		suggestionsgiven=ReplyRequest.objects.filter(funame=request.session['uname']).order_by('-id')
		values={
		'uname':request.session['uname'],
		'questions':questions,
		'requests':requests,
		'suggestionsreceived':suggestionsreceived,
		'suggestionsgiven':suggestionsgiven,
		}
	except Exception as err:
		return HttpResponseRedirect("http://149.129.138.34/index")
	return render(request,'div/homesuggestions.html',values)

def request_view(request):
	if request.method=='GET':
		if request.session.has_key('uname'):
			questions=SendRequest.objects.filter(uname=request.session['uname']).order_by('-rid')
			requests=ReceiveRequest.objects.filter(tuname=request.session['uname']).select_related('rrid').order_by('-id')
			suggestionsreceived=ReplyRequest.objects.filter(tuname=request.session['uname']).order_by('-id')
			suggestionsgiven=ReplyRequest.objects.filter(funame=request.session['uname']).order_by('-id')
			values={
			'uname':request.session['uname'],
		    'questions':questions,
		    'requests':requests,
		    'suggestionsreceived':suggestionsreceived,
			'suggestionsgiven':suggestionsgiven
			}
		else:
			return HttpResponseRedirect("http://149.129.138.34/index")
	return render(request,'div/homerequests.html',values)
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
		questions=SendRequest.objects.filter(uname=request.session['uname']).order_by('-rid')
		requests=ReceiveRequest.objects.filter(tuname=request.session['uname']).order_by('-id.')
		suggestionsreceived=ReplyRequest.objects.filter(tuname=request.session['uname']).order_by('-id')
		suggestionsgiven=ReplyRequest.objects.filter(funame=request.session['uname']).order_by('-id')
		values={
		'uname':request.session['uname'],
		'questions':questions,
		'requests':requests,
		'suggestionsreceived':suggestionsreceived,
		'suggestionsgiven':suggestionsgiven
		}

		
	return render(request,'div/homequestions.html',values)
def login_view(request):
	if request.session.has_key('uname'):
		if request.session.has_key('token'):
			return HttpResponseRedirect("http://149.129.138.34/home")
	return HttpResponseRedirect("https://api.codechef.com/oauth/authorize?response_type=code&client_id=a420ca7d74ada05e8b29411205403ca4&redirect_uri=http://149.129.138.34/&state=xyz")
def submit_request(request):
	if request.method=="POST":
		data=request.POST.copy()
		code=data['problemcode']
		try:
			queryset=SendRequest.objects.filter(uname=request.session['uname'],problemcode=code,languageused=data['languageused'])
		except Exception as err:
			values={
			'heading':'Error',
			  'message':'You session has expired .Log in again and ask your question',
			}
			return render(request,'div/questionerror.html',values)

		if queryset.count() >=1:
			values={
			'heading':'Error',
			  'message':'You already requested for this problem in this language.Edit your question or please try other',
			}
			return render(request,'div/questionerror.html',values)
		req = Request('https://api.codechef.com/submissions/?result=AC&language='+data['languageused']+'&problemCode='+code+'&fields='+'username')
		req.add_header('authorization','Bearer '+request.session['token'])
		req.add_header('content-type','application/json')
		resp=''
		try:
			resp =urlopen(req)
		except urllib.error.HTTPError as err:
			values={
			'heading':'Error',
			  'message':'Problem code doesnot exists.Please enter valid problem code'
			}
			return render(request,'div/questionerror.html',values)	

		content = json.loads(resp.read().decode('utf-8'))
		print('content is')
		print(content)
		if content['result']['data']['code']==9001:
			form=SendRequest()
			form.uname=request.session['uname']
			code=data['problemcode']
			form.problemcode=code
			form.languageused=data['languageused']
			form.question=data['question']
			form.description=data['description']
			form.codesnapshot=data['codesnapshot']	
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
			array=content['result']['data']['content']
			i=0
			for i in range(len(array)):
				form=ReceiveRequest()
				for e in queryset:
					form.rrid=e
				form.funame=request.session['uname']
				form.tuname=array[i]['username']
				form.save()
		else:
			values={'heading':'Error',
			'message':'We dont find any submissions for this problem code.This might be due to no submissions for particular language given or problem code does not exist.Try changing language used or recorrecting problem code'
			}
			return render(request,'div/questionerror.html',values)
	else:
		return HttpResponse('Page Not Found 404')
	values={'heading':'Success',
	'message':'Your request is placed Successfully.Wait for responses from your peers in suggestions tab'
	}
	return render(request,'div/questionerror.html',values)
def reply_to_request(request):
	if request.method=="POST":
		form=ReplyRequest()
		data=request.POST.copy()
		queryset=SendRequest.objects.filter(problemcode=data['problemcode'])
		for e in queryset:
			form.rerid=e
		form.tuname=data['tuname']
		form.funame=request.session['uname']
		form.suggestion=data['suggestion']
		form.save()
		return HttpResponseRedirect("http://149.129.138.34/home")
	else:
		return HttpResponse('Page Not Found 404')
def update_question(request):
	if request.method=="POST":
		data=request.POST.copy()
		newdata=SendRequest.objects.get(uname=request.session['uname'],problemcode=data['problemcode'])
		newdata.question=data['question']
		newdata.codesnapshot=data['codesnapshot']
		newdata.description=data['description']
		newdata.save()
		return HttpResponseRedirect("http://149.129.138.34/home")
	else:
		return HttpResponse('Page Not Found 404')
def graph_view(request):
	if request.method=='POST':
		if request.session.has_key('uname'):
			data=request.POST.copy()
			rname=data['username']
			req = Request('https://api.codechef.com/users/'+rname+'?fields=')
			req.add_header('authorization','Bearer '+request.session['token'])
			req.add_header('content-type','application/json')
			resp=''
			try:
				resp=urlopen(req)
			except urllib.error.HTTPError as err:
				values={
				'heading':'Error',
				  'message':'Username doesnot exist'
				}
				return render(request,'div/questionerror.html',values)
			content = json.loads(resp.read().decode('utf-8'))
			req = Request('https://api.codechef.com/users/me?fields=')
			req.add_header('authorization','Bearer '+request.session['token'])
			req.add_header('content-type','application/json')
			resp =urlopen(req)
			content2 = json.loads(resp.read().decode('utf-8'))
			if content['result']['data']['code']==9001:
				questions=SendRequest.objects.filter(uname=request.session['uname'])
				requests=ReceiveRequest.objects.filter(tuname=request.session['uname'])
				suggestionsreceived=ReplyRequest.objects.filter(tuname=request.session['uname'])
				suggestionsgiven=ReplyRequest.objects.filter(funame=request.session['uname'])
				values={
				'uname':request.session['uname'],
     			'u2':rname,
     			'lr1':content2['result']['data']['content']['rankings']['longRanking']['global'],
     			'lr2':content['result']['data']['content']['rankings']['longRanking']['global'],
     			'sr1':content2['result']['data']['content']['rankings']['shortRanking']['global'],
     			'sr2':content['result']['data']['content']['rankings']['shortRanking']['global'],
     			'acr1':content2['result']['data']['content']['rankings']['allContestRanking']['global'],
     			'acr2':content['result']['data']['content']['rankings']['allContestRanking']['global'],
     			'asr1':content2['result']['data']['content']['rankings']['allSchoolRanking']['global'],
     			'asr2':content['result']['data']['content']['rankings']['allSchoolRanking']['global'],
     			'lra1':content2['result']['data']['content']['ratings']['long'],
     			'lra2':content['result']['data']['content']['ratings']['long'],
     			'sra1':content2['result']['data']['content']['ratings']['short'],
     			'sra2':content['result']['data']['content']['ratings']['short'],
     			'acra1':content2['result']['data']['content']['ratings']['allContest'],
     			'acra2':content['result']['data']['content']['ratings']['allContest'],
     			'asra1':content2['result']['data']['content']['ratings']['allSchoolContest'],
     			'asra2':content['result']['data']['content']['ratings']['allSchoolContest'],
     			'questions':questions,
     			'requests':requests,
     			'suggestionsreceived':suggestionsreceived,
     			'suggestionsgiven':suggestionsgiven
				}
				return render(request,'div/graphs.html',values)
			else:
				values={
				'heading':'Error',
				  'message':'Username doesnot exist'
				}
				return render(request,'div/questionerror.html',values)
		else:
			return HttpResponseRedirect("http://149.129.138.34/index")
	else:
		values={
			'heading':'Authentication failed',
			  'message':'You are not allowed'
			}
		return render(request,'div/questionerror.html',values)

			
