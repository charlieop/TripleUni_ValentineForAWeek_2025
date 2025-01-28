import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError

class WeChatInfo(models.Model):
    def generateUploadPath(self, filename):
        ext = filename.split('.')[-1]
        modified_filename = '{}.{}'.format(self.openid, ext)
        return f"uploads/wechat-headimg/{modified_filename}"

    # XXX: openid is primary key, so it should be unique
    # openid = models.CharField(max_length=50, primary_key=True, editable=False, verbose_name="OpenID")
    openid = models.CharField(max_length=50, primary_key=True, verbose_name="OpenID")

    nickname = models.CharField(max_length=50, verbose_name="昵称")
    head_image = models.ImageField(upload_to=generateUploadPath, verbose_name="头像")
    head_image_url = models.URLField(verbose_name="头像URL")
    
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    
    def __str__(self):
        return f"{self.nickname}"
    
    class Meta:
        verbose_name = "微信信息"
        verbose_name_plural = "微信信息"
        db_table = "wechat_info"
        ordering = ["nickname"]


# Create your models here.
class Applicant(models.Model):
    SCHOOL_LABELS = {
        "UST": "UST",
        "HKU": "HKU",
        "CUHK": "CU"
    }
    GRADE = {
        "UG1": "大一",
        "UG2": "大二",
        "UG3": "大三",
        "UG4": "大四",
        "UG5": "大五",
        "PG": "硕/博士生",
        "PROF": "教授"
    }
    SEX = {
        "M": "男",
        "F": "女"
    }
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    name = models.CharField(max_length=10, verbose_name="姓名")
    sex = models.CharField(
        max_length=1,
        choices=SEX,
        verbose_name="性别"
    )
    grade = models.CharField(
        max_length=4,
        choices=GRADE,
        verbose_name="年级"
    )
    school = models.CharField(
        max_length=4,
        choices=SCHOOL_LABELS,
        verbose_name="学校"
    )
    email = models.EmailField(verbose_name="邮箱")
    wechat_account = models.CharField(max_length=50, verbose_name="微信号")
    
    wechat_info = models.OneToOneField(
        "WeChatInfo",
        on_delete=models.PROTECT,
        related_name="applicant",
        db_index=True,
        verbose_name="微信信息"
    )
    
    payment = models.OneToOneField(
        "PaymentVoucher",
        on_delete=models.PROTECT,
        related_name="applicant",
        null=True,
        blank=True,
        verbose_name="付款凭证"
    )
    
    quitted = models.BooleanField(default=False, verbose_name="已退出")
    
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)
    
    def hasPaid(self):
        return self.payment is not None

    def __str__(self):
        return f"{self.name}-{Applicant.SEX[self.sex]}-{self.school}-{Applicant.GRADE[self.grade]}"
    
    class Meta:
        verbose_name = "申请人"
        verbose_name_plural = "申请人"
        db_table = "applicant"
        ordering = ["school", "grade", "name", "created_at"]
    
    
class PaymentVoucher(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    assigned_to = models.ForeignKey(
        "Mentor",
        on_delete=models.PROTECT,
        related_name="vouchers",
        verbose_name="发放者",
    )
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    def __str__(self):
        return f"发放人:{self.assigned_to.name} | 兑换人:{self.applicant.name if hasattr(self, 'applicant') else '未指定'}"
    class Meta:
        verbose_name = "付款凭证"
        verbose_name_plural = "付款凭证"
        db_table = "payment_voucher"
        ordering = ["assigned_to", "applicant", "created_at"]


class Mentor(AbstractUser):
    def generateUploadPath(self, filename):
        ext = filename.split('.')[-1]
        modified_filename = '{}.{}'.format(self.id, ext)
        return f"uploads/mentor-qr-code/{modified_filename}"
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=10, verbose_name="姓名")
    wechat = models.CharField(max_length=30, verbose_name="微信号")
    wechat_qrcode = models.ImageField(upload_to=generateUploadPath, null=True, blank=True, verbose_name="微信二维码")
    
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.name}"
    
    class Meta:
        verbose_name = "Mentor"
        verbose_name_plural = "Mentors"
        db_table = "mentor"
        ordering = ["name", "created_at"]
        

class Match(models.Model):
    ROUNDS = {
        1: "第一轮",
        2: "第二轮"
    }
    STATUS = {
        "A": "已接受",
        "R": "已拒绝",
        "P": "待确认"
    }
    
    id = models.AutoField(primary_key=True, editable=False, verbose_name="组号")
    name = models.CharField(max_length=30, default="取一个组名吧!", verbose_name="组名")
    
    round = models.IntegerField(choices=ROUNDS, verbose_name="轮次")
    
    mentor = models.ForeignKey(
        "Mentor",
        on_delete=models.PROTECT,
        related_name="matches",
        verbose_name="负责Mentor"
    )
    applicant1 = models.ForeignKey(
        "Applicant",
        on_delete=models.PROTECT,
        related_name="+",
        verbose_name="嘉宾1号"
    )
    applicant1_status = models.CharField(
        max_length=1,
        choices=STATUS,
        default="P",
        verbose_name="嘉宾1号状态"
    )
    applicant2 = models.ForeignKey(
        "Applicant",
        on_delete=models.PROTECT,
        related_name="+",
        verbose_name="嘉宾2号"
    )
    applicant2_status = models.CharField(
        max_length=1,
        choices=STATUS,
        default="P",
        verbose_name="嘉宾2号状态"
    )
    
    discarded = models.BooleanField(default=False, verbose_name="已废弃")
    discard_reason = models.TextField(blank=True, null=True, verbose_name="废弃原因")
            
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"#{self.id}-{self.name}  | Mentor: {self.mentor.name}"
    
    class Meta:
        verbose_name = "CP组"
        verbose_name_plural = "CP组"
        db_table = "match"
        ordering = ["id"]


class Task(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    match = models.ForeignKey(
        "Match",
        on_delete=models.PROTECT,
        related_name="tasks",
        verbose_name="对应CP组"
    )
    day = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(7)], verbose_name="第X天")
    
    submit_text = models.TextField(blank=True, null=True, verbose_name="提交内容")
    submit_by = models.ForeignKey(
        "Applicant",
        on_delete=models.PROTECT,
        related_name="created_tasks",
        verbose_name="创建者"
    )
    
    basic_completed = models.BooleanField(default=False, verbose_name="基础任务完成")
    basic_score = models.IntegerField(default=0, verbose_name="基础任务分数")
    bonus_score = models.IntegerField(default=0, verbose_name="支线&Bonus任务分数")
    daily_score = models.IntegerField(default=0, verbose_name="日常任务分数")
    
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"第{self.day}天: #{self.match.id}-{self.match.name}"
    
    class Meta:
        verbose_name = "任务"
        verbose_name_plural = "任务"
        db_table = "task"
        ordering = ["match", "day"]


class Image(models.Model):
    def generateUploadPath(self, filename):
        ext = filename.split('.')[-1]
        modified_filename = '{}.{}'.format(self.id, ext)
        return f"uploads/tasks/{self.task.match.id}/day-{self.task.day}/{modified_filename}"
    
    def check_image(value):
        SIZE_LIMIT = 5 * 1024 * 1024
        if value.size > SIZE_LIMIT:
            raise ValidationError('File too large. Size should not exceed 5 MiB.')
        valid_mime_types = ['image/jpeg', 'image/png', 'image/jpg', 'image/heic']
        file_mime_type = value.file.content_type
        if file_mime_type not in valid_mime_types:
            raise ValidationError('Unsupported file type. Only JPEG, PNG, JPG and HEIC are allowed.')
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    task = models.ForeignKey(
        "Task",
        on_delete=models.CASCADE,
        related_name="imgs",
        verbose_name="对应任务"
    )
    image = models.ImageField(upload_to=generateUploadPath, validators=[check_image], verbose_name="图片")
    
    deleted = models.BooleanField(default=False, verbose_name="已删除")
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    
    def __str__(self):
        return f"#{self.task.match.id}-{self.task.match.name}  第{self.task.day}天 - {self.image.url}"
    
    class Meta:
        verbose_name = "任务图片"
        verbose_name_plural = "任务图片"
        db_table = "image"
        ordering = ["task", "created_at"]