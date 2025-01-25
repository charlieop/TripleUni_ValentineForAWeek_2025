from django.contrib import admin

from .models import Applicant, PaymentVoucher, Mentor, MatchedPair, Task, Image

# Register your models here.
admin.site.register(Applicant)
admin.site.register(PaymentVoucher)
admin.site.register(Mentor)
admin.site.register(MatchedPair)
admin.site.register(Task)
admin.site.register(Image)
