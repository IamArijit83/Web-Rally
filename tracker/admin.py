from django.contrib import admin
from .models import UserActivity

admin.site.register(UserActivity)
from django.contrib import admin
from .models import Feedback

from django.contrib import admin
from .models import Feedback

@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('user', 'rating', 'short_comment', 'submitted_at')
    list_filter = ('rating', 'submitted_at')
    search_fields = ('user__username', 'comment')
    readonly_fields = ('user', 'submitted_at')

    # Optional: clean comment preview in the list
    def short_comment(self, obj):
        return (obj.comment[:50] + '...') if len(obj.comment) > 50 else obj.comment
    short_comment.short_description = 'Comment'
