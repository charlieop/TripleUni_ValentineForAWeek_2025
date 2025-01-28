from datetime import timedelta
from rest_framework.exceptions import APIException, NotFound, PermissionDenied, ParseError
import uuid
import pickle
from django.core.cache import cache

from .models import Applicant, Match
from .AppConfig import AppConfig


class Gone(APIException):
    status_code = 410
    default_detail = "The requested resource is no longer available."
    default_code = "gone"


class Conflict(APIException):
    status_code = 409
    default_detail = "A conflict occurred."
    default_code = "conflict"


class PaymentRequired(APIException):
    status_code = 402
    default_detail = "Payment is required to proceed."
    default_code = "payment_required"


class UtilMixin:
    def _get_applicant_key(self, pk):
        return f"applicants:{pk}"
    def _get_match_key(self, pk):
        return f"matches:{pk}"
    def _get_task_key(self, match, day):
        return f"tasks:{match.id}:day{day}"
    
    
    def get_openid(self, request):
        openid = request.headers.get('Authorization')
        if openid is None:
            raise ParseError("Authorization header with user \"openid\" is required")
        return openid


    def get_applicant(self, pk, openid):
        try:
            uuid.UUID(pk)
        except ValueError:
            raise ParseError("The code is not a valid UUID")
        
        KEY = self._get_applicant_key(pk)
        cached_applicant = cache.get(KEY)
        
        if cached_applicant:
            print(f"cache hit for applicant: {pk}")
            applicant = pickle.loads(cached_applicant)
        else:
            print(f"cache miss for applicant: {pk}")
            applicant = Applicant.objects.filter(id=pk).first()
            if not applicant:
                raise PermissionDenied("Unauthorized to access this applicant")
            pickled = pickle.dumps(applicant)
            cache.set(KEY, pickled)
            
        if applicant.quitted:
            raise Gone("Applicant has quitted")
        if applicant.wechat_info.openid != openid:
            raise PermissionDenied("Unauthorized to access this applicant")
        
        return applicant
    
    def refresh_applicant_cache(self, applicant):
        print(f"refreshing cache for applicant: {applicant.id}")
        KEY = self._get_applicant_key(applicant.id)
        cache.delete(KEY)


    def get_match(self, pk, openid):
        KEY = self._get_match_key(pk)
        cached_match = cache.get(KEY)
        if cached_match:
            print(f"cache hit for match: {pk}")
            match = pickle.loads(cached_match)
        else:
            print(f"cache miss for match: {pk}")
            match = Match.objects.filter(id=pk).first()
            if not match:
                raise PermissionDenied("Unauthorized to access this match")
            pickled = pickle.dumps(match)
            cache.set(KEY, pickled)
        
        if match.applicant1.wechat_info.openid != openid and match.applicant2.wechat_info.openid != openid:
            raise PermissionDenied("Unauthorized to access this match")
        return match
    
    def refresh_match_cache(self, match):
        print(f"refreshing cache for match: {match.id}")
        KEY = self._get_match_key(match.id)
        cache.delete(KEY)
    
    
    def get_match_participants(self, match, openid):
        my_index = 1 if match.applicant1.wechat_info.openid == openid else 2
        me = match.applicant1 if my_index == 1 else match.applicant2
        partner = match.applicant2 if my_index == 1 else match.applicant1
        return my_index, me, partner
    

    def assert_match_auth(self, match, me):
        if me.payment is None:
            raise PaymentRequired("Deposit payment is required to proceed")
        if match.discarded:
            raise PermissionDenied(f"Match has already been discarded due to: {match.discard_reason or 'Unknown'}")


    def get_task(self, match, day):
        KEY = self._get_task_key(match, day)
        cached_task = cache.get(KEY)
        
        if cached_task:
            print(f"cache hit for task: {match.id} day{day}")
            task = pickle.loads(cached_task)
        else:
            print(f"cache miss for task: {match.id} day{day}")
            task = match.tasks.filter(day=day).first()
            if task:
                cache.set(KEY, pickle.dumps(task))

        return task
    
    def refresh_task_cache(self, task):
        print(f"refreshing cache for task: {task.match.id} day{task.day}")
        KEY = self._get_task_key(task.match, task.day)
        cache.delete(KEY)


    def assert_application_deadline(self):
        if AppConfig.passed(AppConfig.APPLICATION_DEADLINE):
            raise PermissionDenied("The application deadline has passed")

    def assert_match_results_released(self, match):
        if match.round == 1 and not AppConfig.passed(AppConfig.FIRST_ROUND_MATCH_RESULTS_RELEASE):
            raise PermissionDenied("Match results for first round are not yet available")
        elif not AppConfig.passed(AppConfig.SECOND_ROUND_MATCH_RESULTS_RELEASE):
            raise PermissionDenied("Match results for second round are not yet available")
        
    def assert_match_confirm_deadline(self, match):
        if match.round == 1 and AppConfig.passed(AppConfig.FIRST_ROUND_MATCH_RESULTS_CONFIRMATION_DEADLINE):
            raise PermissionDenied("The deadline to confirm match results for first round has passed")
        elif AppConfig.passed(AppConfig.SECOND_ROUND_MATCH_RESULTS_CONFIRMATION_DEADLINE):
            raise PermissionDenied("The deadline to confirm match results for second round has passed")

    def assert_event_started(self):
        if not AppConfig.passed(AppConfig.EVENT_START):
            raise PermissionDenied("The event has not started yet")
        
    def assert_event_not_ended(self):
        if AppConfig.passed(AppConfig.EVENT_END):
            raise PermissionDenied("The event has ended")
        
    def assert_task_open(self, day):
        offset_day = day - 1
        task_start_time = AppConfig.FIRST_TASK_START + timedelta(days=offset_day)
        task_end_time = AppConfig.FIRST_TASK_DEADLINE + timedelta(days=offset_day)
        
        if not AppConfig.passed(task_start_time):
            raise PermissionDenied(f"The task for day {day} has not started yet")
        if AppConfig.passed(task_end_time):
            raise PermissionDenied(f"The task for day {day} has ended")
