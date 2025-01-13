from datetime import datetime, timedelta
from calendar import monthrange
import os, django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "followup_buddy.settings")
django.setup()

from tracker.models import Evangelism, FollowUp
from tracker.utils import create_evangelism

create_evangelism(
    user
)
