from django.contrib import admin
from unfold.admin import ModelAdmin

from .models import WeChatInfo, Applicant, PaymentRecord, Mentor, Match, Task, Image, Mission
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.utils.html import format_html

class ApplicantHasPaidFilter(admin.SimpleListFilter):
    title = "已缴付押金"
    parameter_name = "has_paid"

    def lookups(self, request, model_admin):
        return [
            ('True', "已缴付"),
            ('False', "未缴付"),
        ]

    def queryset(self, request, queryset):
        if self.value() == 'True':
            return queryset.filter(payment__isnull=False)
        if self.value() == 'False':
            return queryset.filter(payment__isnull=True)
        return queryset

@admin.register(Applicant)
class ApplicantAdmin(ModelAdmin):
    search_fields = ['name', 'wxid', 'wechat_info__nickname']

    common_readonly_fields = [
        'id', 'name', 'sex', 'grade', 'school', 
        'email', 'wxid', 'wechat_info',
        'preferred_wxid', 'continue_match', 'comment', 'payment', 'updated_at', 'created_at', 'confirmed', 'payment_expired'
    ]
    
    superuser_readonly_fields = common_readonly_fields + [
        'mbti_ei', 'mbti_sn', 'mbti_tf', 'mbti_jp', 
        'hobby1', 'hobby2', 'hobby3',
        'preferred_sex', 'preferred_grades', 'preferred_schools',
        'preferred_mbti_ei', 'preferred_mbti_sn', 'preferred_mbti_tf', 'preferred_mbti_jp',
        'travel_destination', 'superpower', 'use_of_money', 'family', 'lifestyle',
    ]

    list_display = ['name', 'school', 'grade', 'sex', 'get_nickname', 'has_paid', 'comment', 'quitted', 'exclude', 'created_at']
    list_editable = ['exclude']
    list_filter = ['quitted', 'exclude', ApplicantHasPaidFilter, 'school', 'grade', 'sex']
    list_display_links = ['name', 'school', 'grade', 'sex', 'get_nickname', 'created_at']
    
    @admin.display(description='微信昵称', ordering='wechat_info__nickname')
    def get_nickname(self, obj):
        return obj.wechat_info.nickname
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('wechat_info')
    
    def get_readonly_fields(self, request, obj=None):
        return self.superuser_readonly_fields if request.user.is_superuser else self.common_readonly_fields + ['quitted']

    def get_exclude(self, request, obj):
        return [] if request.user.is_superuser else [
            'mbti_ei', 'mbti_sn', 'mbti_tf', 'mbti_jp', 
            'hobby1', 'hobby2', 'hobby3',
            'preferred_sex', 'preferred_grades', 'preferred_schools',
            'preferred_mbti_ei', 'preferred_mbti_sn', 'preferred_mbti_tf', 'preferred_mbti_jp',
            'travel_destination', 'superpower', 'use_of_money', 'family', 'lifestyle'
        ]
    
class WechatInfoHasAppliedFilter(admin.SimpleListFilter):
    title = "是否提交申请"
    parameter_name = "has_applied"

    def lookups(self, request, model_admin):
        return [
            ('True', "已提交"),
            ('False', "未提交"),
        ]

    def queryset(self, request, queryset):
        if self.value() == 'True':
            return queryset.filter(applicant__isnull=False)
        if self.value() == 'False':
            return queryset.filter(applicant__isnull=True)
        return queryset


@admin.register(WeChatInfo)
class WeChatInfoAdmin(ModelAdmin):
    list_display = ['nickname', 'head_image_tag', 'get_applicant_name', 'created_at']
    fieldsets = (
        (None, {
            'fields': ('nickname', 'head_image_large', 'get_applicant_link', 'created_at')
        }),
    )
    ordering = ['-created_at']
    list_filter = [WechatInfoHasAppliedFilter]
    def get_list_display_links(self, request, list_display):
        return list_display
    def get_readonly_fields(self, request, obj):
        readonly_fields = ['head_image_large', 'created_at']
        readonly_fields.append('get_applicant_link')
        if request.user.is_superuser:
            readonly_fields.append('openid')
            readonly_fields.append('unionid')
        return readonly_fields
    def get_exclude(self, request, obj):
        return [] if request.user.is_superuser else [
            'openid', 'unionid'
        ]
    def get_fieldsets(self, request, obj):
        fieldsets = super().get_fieldsets(request, obj)
        if request.user.is_superuser:
            fieldsets += (('Additional Info', {'fields': ('openid', 'unionid')}),)
        return fieldsets
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('applicant')

    @admin.display(description='申请人姓名', ordering='applicant__name')
    def get_applicant_name(self, obj):
        if hasattr(obj, 'applicant'):
            return obj.applicant.name
        return "-"
    @admin.display(description='申请人', ordering='applicant__name')
    def get_applicant_link(self, obj):
        if hasattr(obj, 'applicant'):
            return format_html('<a class="text-primary-600 dark:text-primary-500" href="/admin/main/applicant/{}/change/">{}</a>'.format(obj.applicant.id, obj.applicant.name))
        return "-"
    @admin.display(description='头像')
    def head_image_tag(self, obj):
        if obj.head_image_url:
            return format_html('<img src="{}" width="50" height="50" />'.format(obj.head_image_url))
        return "无头像"
    @admin.display(description='头像')
    def head_image_large(self, obj):
        if obj.head_image_url:
            return format_html('<img src="{}" width="150" height="150" />'.format(obj.head_image_url))
        return "无头像"


@admin.register(PaymentRecord)
class PaymentRecordAdmin(ModelAdmin):
    pass

class MentorCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Mentor
        fields = ('username', 'email', 'name', 'wechat', 'wechat_qrcode')

class MentorChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = Mentor
        fields = ('username', 'email', 'name', 'wechat', 'wechat_qrcode')

@admin.register(Mentor)
class MentorAdmin(UserAdmin):
    add_form = MentorCreationForm
    form = MentorChangeForm
    model = Mentor
    list_display = ['username', 'is_staff', 'is_active']
    list_filter = ['is_staff', 'is_active']
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('name', 'wechat', 'wechat_qrcode')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'groups', 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'is_staff', 'is_active', 'groups', 'user_permissions')}
        ),
    )
    search_fields = ('username',)
    ordering = ('username',)

    def save_model(self, request, obj, form, change):
        if not change:
            obj.is_staff = True
        super().save_model(request, obj, form, change)

@admin.register(Match)
class MatchAdmin(ModelAdmin):
    list_display = ['id', 'name', 'get_applicant1_name', 'get_applicant2_name', 'discarded', 'get_mentor_name']
    ordering = ['discarded', 'id']
    list_display_links = list_display
    
    def get_list_filter(self, request):
        return ['discarded', 'mentor__name'] if request.user.is_superuser else ['discarded']
    
    def get_search_fields(self, request):
        return ['id', 'name', 'applicant1__name', 'applicant2__name', 'applicant1__wxid', 'applicant2__wxid'] if request.user.is_superuser else ['name', 'applicant1__name', 'applicant2__name', 'applicant1__wxid', 'applicant2__wxid']
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if not request.user.is_superuser:
            qs = qs.filter(mentor=request.user)
        qs.select_related('applicant1', 'applicant2', 'mentor')
        return qs
    
    @admin.display(description='嘉宾1 (F)', ordering='applicant1__name')
    def get_applicant1_name(self, obj):
        return obj.applicant1.name
    
    @admin.display(description='嘉宾2 (M)', ordering='applicant2__name')
    def get_applicant2_name(self, obj):
        return obj.applicant2.name
    
    @admin.display(description='Mentor', ordering='mentor__name')
    def get_mentor_name(self, obj):
        return obj.mentor.name


@admin.register(Task)
class TaskAdmin(ModelAdmin):
    date_hierarchy = 'created_at'


@admin.register(Image)
class ImageAdmin(ModelAdmin):
    pass

@admin.register(Mission)
class MissionAdmin(ModelAdmin):
    pass
