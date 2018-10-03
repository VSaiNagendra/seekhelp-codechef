from django.db import models

class SendRequest(models.Model):
	rid=models.AutoField(primary_key=True)
	uname=models.CharField(max_length=50)
	problemcode=models.CharField(max_length=50)
	languageused=models.CharField(max_length=10)
	question=models.TextField()
	description=models.TextField()
	codesnapshot=models.TextField()
	status=models.BooleanField(default=False)
	date=models.DateField(auto_now=True)
	time=models.TimeField(auto_now=True)

class ReceiveRequest(models.Model):
	rrid=models.ForeignKey(SendRequest,on_delete=models.CASCADE)
	funame=models.CharField(max_length=50)
	tuname=models.CharField(max_length=50)
	

class ReplyRequest(models.Model):
	rerid=models.ForeignKey(SendRequest,on_delete=models.CASCADE)
	funame=models.CharField(max_length=50)
	tuname=models.CharField(max_length=50)
	suggestion=models.TextField()
	retime=models.DateField(auto_now=True)
	redate=models.TimeField(auto_now=True)


	
	