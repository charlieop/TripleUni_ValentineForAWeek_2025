from datetime import datetime

from django.conf import settings
import json

class AppConfig():
    CONFIG_SAVE_PATH = settings.MEDIA_ROOT / "config.json"
    
    DATETIME_FORMAT = "%Y/%m/%d %H:%M:%S"

    APPLICATION_DEADLINE = datetime(year=2025, month=2, day=4, hour=14, minute=00, second=00)
    FIRST_ROUND_MATCH_RESULTS_RELEASE = datetime(year=2025, month=2, day=4, hour=19, minute=00, second=00)
    FIRST_ROUND_MATCH_RESULTS_CONFIRMATION_DEADLINE = datetime(year=2025, month=2, day=5, hour=23, minute=59, second=59)
    SECOND_ROUND_MATCH_RESULTS_RELEASE = datetime(year=2025, month=2, day=6, hour=8, minute=00, second=00)
    SECOND_ROUND_MATCH_RESULTS_CONFIRMATION_DEADLINE = datetime(year=2025, month=2, day=7, hour=14, minute=00, second=00)
    EVENT_START = datetime(year=2025, month=2, day=7, hour=22, minute=00, second=00)
    FIRST_TASK_START = datetime(year=2025, month=2, day=8, hour=0, minute=00, second=00)
    FIRST_TASK_DEADLINE = datetime(year=2025, month=2, day=9, hour=5, minute=00, second=00)
    EVENT_END = datetime(year=2025, month=2, day=15, hour=6, minute=00, second=00)
    
    
    # APPLICATION_DEADLINE = datetime(year=2024, month=2, day=4, hour=12, minute=00, second=00)
    # FIRST_ROUND_MATCH_RESULTS_RELEASE = datetime(year=2024, month=2, day=4, hour=19, minute=00, second=00)
    # FIRST_ROUND_MATCH_RESULTS_CONFIRMATION_DEADLINE = datetime(year=2024, month=2, day=5, hour=23, minute=59, second=59)
    # SECOND_ROUND_MATCH_RESULTS_RELEASE = datetime(year=2024, month=2, day=6, hour=8, minute=00, second=00)
    # SECOND_ROUND_MATCH_RESULTS_CONFIRMATION_DEADLINE = datetime(year=2024, month=2, day=7, hour=14, minute=00, second=00)
    # EVENT_START = datetime(year=2024, month=2, day=7, hour=22, minute=00, second=00)
    # FIRST_TASK_START = datetime(year=2024, month=2, day=8, hour=0, minute=00, second=00)
    # FIRST_TASK_DEADLINE = datetime(year=2024, month=2, day=9, hour=5, minute=00, second=00)
    # EVENT_END = datetime(year=2024, month=2, day=15, hour=6, minute=00, second=00)

    @staticmethod
    def passed(event_time):
        return datetime.now() > event_time
    
    @staticmethod
    def save():
        data = {
            "APPLICATION_DEADLINE": AppConfig.APPLICATION_DEADLINE.strftime(AppConfig.DATETIME_FORMAT),
            "FIRST_ROUND_MATCH_RESULTS_RELEASE": AppConfig.FIRST_ROUND_MATCH_RESULTS_RELEASE.strftime(AppConfig.DATETIME_FORMAT),
            "FIRST_ROUND_MATCH_RESULTS_CONFIRMATION_DEADLINE": AppConfig.FIRST_ROUND_MATCH_RESULTS_CONFIRMATION_DEADLINE.strftime(AppConfig.DATETIME_FORMAT),
            "SECOND_ROUND_MATCH_RESULTS_RELEASE": AppConfig.SECOND_ROUND_MATCH_RESULTS_RELEASE.strftime(AppConfig.DATETIME_FORMAT),
            "SECOND_ROUND_MATCH_RESULTS_CONFIRMATION_DEADLINE": AppConfig.SECOND_ROUND_MATCH_RESULTS_CONFIRMATION_DEADLINE.strftime(AppConfig.DATETIME_FORMAT),
            "EVENT_START": AppConfig.EVENT_START.strftime(AppConfig.DATETIME_FORMAT),
            "FIRST_TASK_START": AppConfig.FIRST_TASK_START.strftime(AppConfig.DATETIME_FORMAT),
            "FIRST_TASK_DEADLINE": AppConfig.FIRST_TASK_DEADLINE.strftime(AppConfig.DATETIME_FORMAT),
            "EVENT_END": AppConfig.EVENT_END.strftime(AppConfig.DATETIME_FORMAT),
        }
        with open(AppConfig.CONFIG_SAVE_PATH, "w") as f:
            json.dump(data, f)
            
print("===\nSaving AppConfig ...")
AppConfig.save()
print("AppConfig saved\n===\n")