from django.contrib import admin
from div.models import SendRequest
from div.models import ReceiveRequest
from div.models import ReplyRequest
admin.site.register(SendRequest)
admin.site.register(ReceiveRequest)
admin.site.register(ReplyRequest)