from django.contrib import admin

from .models import WeChatInfo, Applicant, PaymentVoucher, Mentor, Match, Task, Image

# Register your models here.
admin.site.register(Applicant)
admin.site.register(WeChatInfo)
admin.site.register(PaymentVoucher)
admin.site.register(Mentor)
admin.site.register(Match)
admin.site.register(Task)
admin.site.register(Image)
