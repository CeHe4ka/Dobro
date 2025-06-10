from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.http import HttpResponse
from openpyxl import Workbook
from .models import CustomUser
from django.utils.html import format_html
from django.urls import reverse

# Действие: экспорт пользователей в Excel
def export_users_to_excel(modeladmin, request, queryset):
    wb = Workbook()
    ws = wb.active
    ws.title = "Users"
    ws.append(['ID', 'Email', 'Дата рождения', 'Имя', 'Фамилия', 'Активен', 'Редактор', 'Заявка на редактора'])
    for user in queryset:
        ws.append([
            user.id,
            user.email,
            user.birth_date,
            user.first_name,
            user.last_name,
            user.is_active,
            "Да" if user.is_editor else "Нет",
            "Да" if user.is_editor_request else "Нет"
        ])
    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    )
    response['Content-Disposition'] = 'attachment; filename=users.xlsx'
    wb.save(response)
    return response

export_users_to_excel.short_description = "Экспортировать выбранных пользователей в Excel"

# Настройка отображения CustomUser в админке
@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    actions = [export_users_to_excel]

    list_display = (
        'email', 'username', 'first_name', 'last_name',
        'is_staff', 'is_active', 'is_editor', 'is_editor_request', 'editor_social_link'
    )
    list_filter = ('is_staff', 'is_active', 'is_editor', 'is_editor_request')

    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': (
            'birth_date', 'avatar', 'is_editor', 'is_editor_request'
        )}),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': (
            'birth_date', 'avatar', 'is_editor', 'is_editor_request'
        )}),
    )

    search_fields = ('email', 'username', 'first_name', 'last_name')
    ordering = ('email',)

    # Убираем действие экспорта, если нет прав
    def get_actions(self, request):
        actions = super().get_actions(request)
        if not request.user.has_perm('accounts.can_export_users') and not request.user.is_superuser:
            actions.pop('export_users_to_excel', None)
        return actions
@admin.register
class VideoAdmin(admin.ModelAdmin):
    list_display = ('title', 'author_link', 'created_at', 'is_approved')
    list_filter = ('is_approved',)
    search_fields = ('title', 'author__email')
    actions = ['approve_selected']

    @admin.display(description='Автор')
    def author_link(self, obj):
        if obj.author:
            url = reverse('admin:accounts_customuser_change', args=[obj.author.id])
            return format_html('<a href="{}">{}</a>', url, obj.author.email)
        return '-'

    @admin.action(description='Одобрить выбранные видео')
    def approve_selected(self, request, queryset):
        updated = queryset.update(is_approved=True)
        self.message_user(request, f"Одобрено {updated} видео.")
