# Activity Recommendation Algorithm

This explains how `tracker.utils.recommend_activity` decides: do we show a **follow-up** to do right now, or do we suggest starting a **new evangelism** (a new person / conversation)?

## Key Ideas (Plain Language)

Terms / constants (all can be tuned in `utils.py`):

| Name | What it means | Default |
| ---- | ------------- | ------- |
| `FOLLOWUP_TARGET` | How many follow-ups we aim to complete for one person before we consider them “sufficiently nurtured”. | 7 |
| `FOLLOWUP_INTERVAL_DAYS` | Maximum comfortable gap. If we have waited at least this many days since the last touch and we still haven't hit the target, it's “overdue”. | 7 |
| `RECENT_TOUCH_WINDOW` | A short freshness window. If we touched someone within this many days, they are still “fresh”. | 2 |
| `MIN_DAYS_BEFORE_SECOND_TOUCH` | Avoid recommending another follow-up the exact same day (minimum spacing for early touches). | 1 |

Simple definition of states:
* Overdue: needs attention because it has waited too long.
* Cadence: not overdue yet, but old enough to keep steady progress.
* Recent / Fresh: touched very recently; normally we would wait — but we now have a gentle “stagger” rule (see below) so daily users still see useful follow-ups.

## Goals

1. Don’t let anyone wait too long (protect against neglect).
2. Spread attention fairly (don’t pile all follow-ups on the same few people).
3. Avoid recommending follow-ups immediately after one was just logged.
4. Still keep growing: allow new evangelism when things look reasonably up to date.
5. Give daily users something actionable even if everything is still “recent”.

## Data Preparation

For the authenticated user, we query all active (not completed) evangelisms and annotate them with:

- `followup_count`: number of follow-ups performed.
- `last_followup_date`: most recent follow-up date (nullable).
- `last_touch_date`: either the last follow-up date or the original evangelism date if there are no follow-ups yet.

This is done in a single queryset using `annotate` + `Coalesce` to avoid N+1 queries.

## Core Decision Flow

Six clear steps, taken in order. The first one that applies wins:

### 1. Overdue (highest priority)
Pick someone whose last touch is at least `FOLLOWUP_INTERVAL_DAYS` ago and still below the target.

Ranking (simplified wording):
1. Longest wait first
2. Higher relevance first
3. Fewer follow-ups so far
4. Older record (tie breaker)

### 2. Cadence
Nothing overdue? Look for those old enough to nudge again (past `RECENT_TOUCH_WINDOW`) but not overdue yet.

Ranking:
1. Fewest follow-ups
2. Higher relevance
3. Older record

### 3. Stagger Recent (new step)
Daily user scenario: All remaining people are still “recent” (inside `RECENT_TOUCH_WINDOW`), but at least `MIN_DAYS_BEFORE_SECOND_TOUCH` days have passed (e.g. touched yesterday). Instead of saying “start something new” every day, we gently advance one of them.

Ranking:
1. Fewest follow-ups
2. Longer (but still recent) wait
3. Higher relevance
4. Older record

### 4. Healthy Progress → New Evangelism
If average progress is already decent (average follow-ups per active person >= half the target) and we didn’t find a follow-up above, suggest a new evangelism.

### 5. All Completed → New Evangelism
Everyone hit the target? Start something new.

### 6. Default
If none of the above yields a follow-up (rare after the stagger step), suggest new evangelism to keep outreach growing.

## Return Value & Template Compatibility
* Follow-up chosen → Return that `Evangelism` instance. We attach two temporary attributes: `recommended_action="followup"` and `recommendation_reason` (e.g. `overdue_followup`, `build_cadence`, `stagger_recent`).
* New evangelism suggested → Return `None`. Existing template code already interprets this as “Go start a new evangelism”.

## Tunability & Future Enhancements
Adjust constants first; that covers 80% of behavior. Further ideas:
* Per-user configurable targets.
* “Early nurturing” rule (ensure first 2–3 touches happen quickly).
* Light randomness among top 2 to avoid monotony.
* Skip repeating the exact same recommendation if ignored for N days.
* Track next scheduled follow-up date and pre-compute it (could enable filtering in DB query instead of Python logic).

## Edge Cases
* No evangelisms yet → Suggest new.
* Not logged in → Suggest new.
* All completed → Suggest new.
* Large backlog, none overdue, average >= half target → Suggest new (healthy distribution).
* Daily login, all still “recent” → Stagger rule now gives a concrete follow-up instead of always new.

## Summary
In order: fix neglect, keep steady rhythm, gently advance recent ones for daily users, then allow growth. This keeps momentum without spamming or stalling.

That’s it: clear, small rules that are easy to tweak.
