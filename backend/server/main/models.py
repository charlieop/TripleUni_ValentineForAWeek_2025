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
    HOBBY = {
        "workout": "健身",
        "read": "阅读",
        "film": "看剧、电影",
        "music": "音乐",
        "travel": "旅游",
        "photography": "摄影",
        "acg": "二次元",
        "vediogame": "游戏",
        "sport": "运动",
        "cook": "做饭",
        "paint": "绘画",
        "create": "创作",
    }
    TRAVEL_DESTINATION = {
        "sea": "海边",
        "town": "安静宜人的小镇",
        "city": "现代化大都市",
        "none": "我不喜欢旅游"
    }
    SUPERPOWER = {
        "animal": "能和所有动物交流",
        "fly": "可以飞",
        "mindreading": "读心术",
        "prophecy": "可以预知1小时后的未来",
        "resurrection": "可以复活一次"
    }
    USE_OF_MONEY = {
        "invest": "投资理财",
        "one_off": "旅行或购买心仪已久的东西",
        "save": "储蓄起来，以备不时之需",
        "daily": "摊开用来增加日常开销",
        "charity": "捐赠给需要帮助的人"
    }
    FAMILY = {
        2: "很重要，而且很难改变",
        1: "重要，但是我们可以重塑自己",
        0: "不重要，主要取决于自身"
    }
    LIFESTYLE = {
        "potter": "哈利波特",
        "1984": "1984",
        "prince": "小王子",
        "matrix": "黑客帝国",
        "jurassic": "侏罗纪公园",
        "gatsby": "了不起的盖茨比",
    }
    MBTI_EI = {
        "e": "外向e",
        "i": "内向i",
        "x": "无"
    }
    MBTI_SN = {
        "s": "感觉s",
        "n": "直觉n",
        "x": "无"
    }
    MBTI_TF = {
        "t": "思维t",
        "f": "情感f",
        "x": "无"
    }
    MBTI_JP = {
        "j": "判断j",
        "p": "感知p",
        "x": "无"
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
    wxid = models.CharField(max_length=50, verbose_name="微信号")
    wechat_info = models.OneToOneField(
        "WeChatInfo",
        on_delete=models.PROTECT,
        related_name="applicant",
        db_index=True,
        verbose_name="微信信息"
    )
    
    mbti_ei = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)], verbose_name="MBTI-EI")
    mbti_sn = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)], verbose_name="MBTI-SN")
    mbti_tf = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)], verbose_name="MBTI-TF")
    mbti_jp = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)], verbose_name="MBTI-JP")
    hobby1 = models.CharField(
        max_length=20,
        choices=HOBBY,
        verbose_name="兴趣1"
    )
    hobby2 = models.CharField(
        max_length=20,
        choices=HOBBY,
        null=True,
        blank=True,
        verbose_name="兴趣2"
    )
    hobby3 = models.CharField(
        max_length=20,
        choices=HOBBY,
        null=True,
        blank=True,
        verbose_name="兴趣3"
    )
    travel_destination = models.CharField(
        max_length=10,
        choices=TRAVEL_DESTINATION,
        verbose_name="你更期待前往哪里旅游？"
    )
    superpower = models.CharField(
        max_length=20,
        choices=SUPERPOWER,
        verbose_name="你最希望拥有哪种超能力？"
    )
    use_of_money = models.CharField(
        max_length=10,
        choices=USE_OF_MONEY,
        verbose_name="面对一笔意外的财富，你会："
    )
    family = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(2)],
        choices=FAMILY,
        verbose_name="你觉得原生家庭对一个人的影响"
    )
    lifestyle = models.CharField(
        max_length=20,
        choices=LIFESTYLE,
        verbose_name="你更愿意在哪个书或电影中生活一段时间"
    )
    
    preferred_sex = models.CharField(
        max_length=1,
        choices=SEX,
        verbose_name="性别偏好"
    )
    preferred_grades = models.CharField(
        max_length=30,
        verbose_name="年级偏好"
    )
    preferred_schools = models.CharField(
        max_length=20,
        verbose_name="学校偏好"
    )
    preferred_mbti_ei = models.CharField(
        max_length=1,
        choices=MBTI_EI,
        verbose_name="MBTI-EI偏好"
    )
    preferred_mbti_sn = models.CharField(
        max_length=1,
        choices=MBTI_SN,
        verbose_name="MBTI-SN偏好"
    )
    preferred_mbti_tf = models.CharField(
        max_length=1,
        choices=MBTI_TF,
        verbose_name="MBTI-TF偏好"
    )
    preferred_mbti_jp = models.CharField(
        max_length=1,
        choices=MBTI_JP,
        verbose_name="MBTI-JP偏好"
    )
    preferred_wxid = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        verbose_name="匹配对象偏好"
    )
    continue_match = models.BooleanField(default=True, verbose_name="愿意继续匹配")
    comment = models.CharField(
        max_length=30,
        null=True,
        blank=True,
        verbose_name="留言"
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
    exclude = models.BooleanField(default=False, verbose_name="人工排除")
    
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


class Mission(models.Model):
    DAY = {
        0: "秘密任务",
        1: "第一天任务",
        2: "第二天任务",
        3: "第三天任务",
        4: "第四天任务",
        5: "第五天任务",
        6: "第六天任务",
        7: "第七天任务"
    }
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    day = models.IntegerField(choices=DAY, verbose_name="任务类型")
    
    title = models.CharField(max_length=50, verbose_name="标题")
    content = models.TextField(blank=True, null=True, verbose_name="内容")
    link = models.URLField(blank=True, null=True, verbose_name="链接")
    
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{Mission.DAY[self.day]}: {self.title}"
    
    class Meta:
        verbose_name = "发布任务"
        verbose_name_plural = "发布任务"
        db_table = "mission"
        ordering = ["day"]