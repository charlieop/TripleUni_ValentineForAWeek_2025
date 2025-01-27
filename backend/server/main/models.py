import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator


class WeChatInfo(models.Model):
    def generateUploadPath(self, filename):
        ext = filename.split('.')[-1]
        modified_filename = '{}.{}'.format(self.openid, ext)
        return f"uploads/wechat-headimg/{modified_filename}"

    openid = models.CharField(max_length=50, primary_key=True, editable=False, verbose_name="OpenID")
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
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=10, verbose_name="姓名")
    wechat = models.CharField(max_length=30, verbose_name="微信号")
    wechat_img = models.ImageField(upload_to="uploads/mentor-qr-code/", null=True, blank=True, verbose_name="微信二维码")
    
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.name}"
    
    class Meta:
        verbose_name = "Mentor"
        verbose_name_plural = "Mentors"
        db_table = "mentor"
        ordering = ["name", "created_at"]
        

class MatchedPair(models.Model):
    id = models.AutoField(primary_key=True, editable=False, verbose_name="组号")
    name = models.CharField(max_length=30, default="取一个组名吧!", verbose_name="组名")
    
    mentor = models.ForeignKey(
        "Mentor",
        on_delete=models.PROTECT,
        related_name="matched_pairs",
        verbose_name="负责Mentor"
    )
    applicant1 = models.ForeignKey(
        "Applicant",
        on_delete=models.PROTECT,
        related_name="matched_pairs_pos1",
        verbose_name="嘉宾1号"
    )
    applicant2 = models.ForeignKey(
        "Applicant",
        on_delete=models.PROTECT,
        related_name="matched_pairs_pos2",
        verbose_name="嘉宾2号"
    )
    
    discarded = models.BooleanField(default=False, verbose_name="已废弃")
    discard_reason = models.TextField(blank=True, null=True, verbose_name="废弃原因")
            
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"#{self.id}-{self.name}  | Mentor: {self.mentor.name}"
    
    class Meta:
        verbose_name = "嘉宾组"
        verbose_name_plural = "嘉宾组"
        db_table = "matched_pair"
        ordering = ["id"]


class Task(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    pair = models.ForeignKey(
        "MatchedPair",
        on_delete=models.PROTECT,
        related_name="tasks",
        verbose_name="对应嘉宾组"
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
        return f"第{self.day}天: #{self.pair.id}-{self.pair.name}"
    
    class Meta:
        verbose_name = "任务"
        verbose_name_plural = "任务"
        db_table = "task"
        ordering = ["pair", "day"]


class Image(models.Model):
    def generateUploadPath(self, filename):
        ext = filename.split('.')[-1]
        modified_filename = '{}.{}'.format(uuid.uuid4().hex[:10], ext)
        return f"uploads/tasks/{self.task.pair.id}/day-{self.task.day}/{modified_filename}"
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    task = models.ForeignKey(
        "Task",
        on_delete=models.CASCADE,
        related_name="imgs",
        verbose_name="对应任务"
    )
    image = models.ImageField(upload_to=generateUploadPath, verbose_name="图片")
    
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    
    def __str__(self):
        return f"#{self.task.pair.id}-{self.task.pair.name}  第{self.task.day}天 - {self.image.url}"
    
    class Meta:
        verbose_name = "任务图片"
        verbose_name_plural = "任务图片"
        db_table = "image"
        ordering = ["task", "created_at"]