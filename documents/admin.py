from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from documents.models import Document
from main.admin import UsernameSearch


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    fieldsets = (
        (
            None,
            {'fields': ('content_type', 'object_pk')}
        ),
        (
            _('Content'),
            {'fields': ('user_created', 'title', 'file', 'thumbnails', 'tags',)}
        ),
        (
            _('Metadata'),
            {'fields': ('updated', 'created', 'size', 'file_type', 'is_multimedia',)}
        ),
    )

    list_display = ('title', 'file_type', 'object_pk', 'created',)
    list_filter = ('created', 'file_type',)
    date_hierarchy = 'created'
    ordering = ('-created',)
    raw_id_fields = ('user_created',)
    readonly_fields = ["updated", "created", 'size', 'file_type', 'is_multimedia', 'thumbnails']
    search_fields = ('title', UsernameSearch(), 'user_name', 'user_email',)
