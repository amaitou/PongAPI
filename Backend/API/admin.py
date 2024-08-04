from django.contrib import admin
from .models import *


admin.site.register(PlayerBasicInfo)
admin.site.register(PlayerDetailInfo)
admin.site.register(PlayerGameStats)
admin.site.register(GameResults)
admin.site.register(FriendRequests)
admin.site.register(FriendshipList)
admin.site.register(BlockList)
admin.site.register(Chat)
admin.site.register(Conversation)
admin.site.register(Notification)