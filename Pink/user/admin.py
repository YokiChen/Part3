from django.contrib import admin
# 导入模型
from . import models
# Register your models here.

#
@admin.register(models.student)
class UserAdmin(admin.ModelAdmin):
    list_display = ['name','password','header','teaid']
    list_filter = ['name','teaid_id']
    fields = ['name','password','header','teaid']

    # 改变操作（执行）框的位置
    actions_on_top = False
    actions_on_bottom = True


admin.site.register(models.Article)
# admin.site.register(models.student,UserAdmin)
# @admin.register(models.student)  二者作用完全相同
admin.site.register(models.Teacher)