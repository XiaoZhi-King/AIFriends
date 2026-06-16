from django.contrib import admin

from web.models.friend import Friend,Message,SystemPrompt
from web.models.user import UserProfile
from web.models.character import Character,Voice

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    raw_id_fields = ('user',) #逗号千万不要删除!!!

@admin.register(Character)
class CharacterAdmin(admin.ModelAdmin):
    raw_id_fields = ('author','voice')

admin.site.register(Voice)


@admin.register(Friend)
class FriendAdmin(admin.ModelAdmin):
    raw_id_fields = ('me', 'character',)

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    raw_id_fields = ('friend',)

admin.site.register(SystemPrompt)
