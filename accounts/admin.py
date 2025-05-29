from django.contrib import admin
from django.http import HttpResponse
from openpyxl import Workbook
from .models import CustomUser
from django.contrib.auth.admin import UserAdmin

def export_users_to_excel(modeladmin, request, queryset):
    wb = Workbook()
    ws = wb.active
    ws.title = "Users"
    ws.append(['ID', 'Email', 'Дата рождения', 'Имя', 'Фамилия', 'Активен'])
    for user in queryset:
        ws.append([user.id, user.email, user.birth_date, user.first_name, user.last_name, user.is_active])
    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    )
    response['Content-Disposition'] = 'attachment; filename=users.xlsx'
    wb.save(response)
    return response

export_users_to_excel.short_description = "Экспортировать выбранных пользователей в Excel"

class CustomUserAdmin(UserAdmin):
    actions = [export_users_to_excel]

    def get_actions(self, request):
        actions = super().get_actions(request)
        if not request.user.has_perm('accounts.can_export_users') and not request.user.is_superuser:
            actions.pop('export_users_to_excel', None)
        return actions

admin.site.register(CustomUser, CustomUserAdmin)
