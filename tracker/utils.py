"""Utility helpers for recommendation logic."""

from dataclasses import dataclass
from typing import Optional, Iterable

from django.db.models import Count, Max
from django.db.models.functions import Coalesce
from django.utils import timezone

from .models import Evangelism


# Tunable constants (can later be moved to settings.py)
FOLLOWUP_TARGET = 7                # How many followups we aim to complete for each evangelism
FOLLOWUP_INTERVAL_DAYS = 7         # Ideal maximum gap between touches while still < target
RECENT_TOUCH_WINDOW = 2            # If last touch within this many days we consider it "fresh"
MIN_DAYS_BEFORE_SECOND_TOUCH = 1   # Avoid recommending followup same day unless necessary


@dataclass
class Recommendation:
    """Represents a recommended action.

    Attributes:
        action: 'followup' or 'evangelize'
        evangelism: the Evangelism object to follow up (if action == 'followup')
        reason: short machine-readable reason string
        details: human friendly explanation (optional usage)
    """
    action: str
    evangelism: Optional[Evangelism] = None
    reason: str = ""
    details: str = ""

    def to_context_object(self):
        """Return an object compatible with current template expectations.

        The existing home template checks for a truthy object ("followup") and then
        expects attributes person_name, location, faith. To preserve backward
        compatibility we return the evangelism itself when recommending a follow up.
        """
        if self.action == "followup" and self.evangelism:
            # Monkey patch attributes for potential UI enhancements
            setattr(self.evangelism, "recommended_action", "followup")
            setattr(self.evangelism, "recommendation_reason", self.reason)
            return self.evangelism
        return None  # Causes template to show evangelism (new) encouragement


def _annotated_evangelisms(evangelist) -> Iterable[Evangelism]:
    """Return evangelisms with aggregated followup info to avoid N+1 queries."""
    return (
        Evangelism.objects.filter(evangelist=evangelist, completed=False)
        .annotate(
            followup_count=Count("followups"),
            last_followup_date=Max("followups__date"),
        )
        .annotate(
            # 'last_touch_date' = last followup date or original evangelism date
            last_touch_date=Coalesce("last_followup_date", "date"),
        )
        .order_by("date")
    )


def recommend_activity(evangelist=None):
    """Recommend next activity (followup vs new evangelism) for an evangelist.

     Strategy overview:
     1. Identify *overdue* evangelisms (fewer than FOLLOWUP_TARGET followups AND
         days since last touch >= FOLLOWUP_INTERVAL_DAYS). If any exist, pick the
         highest priority one (most overdue, highest relevance, fewest followups).
     2. If no overdue, look for evangelisms still needing followups (count < target)
         where days since last touch >= MIN_DAYS_BEFORE_SECOND_TOUCH and beyond the
         RECENT_TOUCH_WINDOW – we nudge steady cadence without over‑touching.
     3. (New) If everything is still within the RECENT_TOUCH_WINDOW (e.g. user logs
         in daily) we still gently advance the lowest‑progress evangelism that was
         last touched at least MIN_DAYS_BEFORE_SECOND_TOUCH days ago (staggering
         progress) instead of always suggesting only new evangelism.
     4. If all active evangelisms have reached the followup target OR (after the
         stagger step) we judge distribution healthy (average followups >= half target)
         we encourage a new evangelism (returning None keeps existing template
         behavior).
    """
    if evangelist is None:
        # Without an authenticated user we cannot tailor; encourage evangelism.
        return None

    today = timezone.now().date()
    evangelisms = list(_annotated_evangelisms(evangelist))

    if not evangelisms:
        return None  # Start evangelizing

    # Build priority lists
    overdue_candidates = []
    cadence_candidates = []
    fresh_recent_candidates = []  # NEW: within RECENT_TOUCH_WINDOW but eligible to gently stagger

    total_followups = 0
    for e in evangelisms:
        followup_count = getattr(e, "followup_count", 0) or 0
        total_followups += followup_count
        last_touch = getattr(e, "last_touch_date", e.date)
        days_since_last_touch = (today - last_touch).days

        # Skip recommending followups for evangelisms already at or above target
        if followup_count >= FOLLOWUP_TARGET:
            continue

        # Determine categories
        if days_since_last_touch >= FOLLOWUP_INTERVAL_DAYS:
            overdue_candidates.append((e, days_since_last_touch, followup_count))
        elif (
            days_since_last_touch >= MIN_DAYS_BEFORE_SECOND_TOUCH
            and days_since_last_touch > RECENT_TOUCH_WINDOW
        ):
            cadence_candidates.append((e, days_since_last_touch, followup_count))
        elif days_since_last_touch >= MIN_DAYS_BEFORE_SECOND_TOUCH:
            # Inside RECENT_TOUCH_WINDOW: keep as possible stagger candidate (not touched today)
            fresh_recent_candidates.append((e, days_since_last_touch, followup_count))

    # 1. Overdue priority: sort by (days overdue desc, relevance desc, followup_count asc, oldest evangelism first)
    if overdue_candidates:
        overdue_candidates.sort(
            key=lambda t: (
                t[1],                    # days since last touch (larger first after reverse)
                t[0].relevance,          # higher relevance first
                -t[2],                   # fewer followups first => invert sign later or adjust ordering
                t[0].date.toordinal(),
            ),
            reverse=True,
        )
        chosen = overdue_candidates[0][0]
        return Recommendation(
            action="followup",
            evangelism=chosen,
            reason="overdue_followup",
            details="This person has waited more than the target interval and has not yet reached the followup goal.",
        ).to_context_object()

    # 2. Cadence maintenance: choose the one with fewest followups, then highest relevance, then oldest
    if cadence_candidates:
        cadence_candidates.sort(
            key=lambda t: (
                t[2],             # followup_count (want smallest)
                -t[0].relevance,  # relevance high first -> negate
                t[0].date.toordinal(),
            )
        )
        chosen = cadence_candidates[0][0]
        return Recommendation(
            action="followup",
            evangelism=chosen,
            reason="build_cadence",
            details="Continue steady followup cadence toward the target count.",
        ).to_context_object()

    # 3. Stagger within recent window: if no other candidates, pick lowest progress
    #    even though last touch is still "recent" (>=1 day but <= RECENT_TOUCH_WINDOW)
    if fresh_recent_candidates:
        # Sort: fewest followups, then older (larger days_since_last_touch), then higher relevance, then oldest creation
        fresh_recent_candidates.sort(
            key=lambda t: (
                t[2],              # fewest followups first
                -t[1],             # larger days_since_last_touch next
                -t[0].relevance,   # higher relevance
                t[0].date.toordinal(),
            )
        )
        chosen = fresh_recent_candidates[0][0]
        return Recommendation(
            action="followup",
            evangelism=chosen,
            reason="stagger_recent",
            details="Advancing a recent contact to maintain momentum without waiting full interval.",
        ).to_context_object()

    # 4. Encourage new evangelism if distribution already healthy (avg >= half target)
    #    or nothing else to recommend.
    avg_followups = total_followups / len(evangelisms) if evangelisms else 0
    if avg_followups >= FOLLOWUP_TARGET / 2:
        return None

    return None


