"""Database seed script.

Features:
 1. Ensures a default evangelist user exists (or updates password).
 2. Seeds tracker app data (Evangelism + FollowUp) using Faker.

Usage:
	python seed.py

Environment variables (optional):
	EVANGELIST_USERNAME=evangelist
	EVANGELIST_EMAIL=evangelist@example.com
	EVANGELIST_PASSWORD=password123
	EVANGELIST_IS_STAFF=true|false
	EVANGELIST_IS_SUPERUSER=false|true

	SEED_EVANGELISMS=25              # How many evangelism records to ensure/create
	SEED_FOLLOWUPS_MIN=0             # Min followups per evangelism
	SEED_FOLLOWUPS_MAX=5             # Max followups per evangelism
	SEED_PAST_DAYS=90                # Randomize evangelism date within this many past days
	SEED_CLEAR=false                 # If 'true', will delete existing Evangelism & FollowUp first

Idempotency:
	Without SEED_CLEAR the script only adds new evangelisms until the count
	of existing (for the evangelist) >= SEED_EVANGELISMS. Names are generated
	uniquely per run to avoid constraint collisions.
"""

import os
import sys
import random
import datetime
import django
from django.core.exceptions import ImproperlyConfigured


def setup_django() -> None:
	os.environ.setdefault("DJANGO_SETTINGS_MODULE", "followup_buddy.settings")
	try:
		django.setup()
	except ImproperlyConfigured as e:
		print(f"[seed] Django ImproperlyConfigured: {e}")
		sys.exit(1)


def create_evangelist_user(
	username: str = "evangelist",
	email: str = "evangelist@example.com",
	password: str = "password123",
	make_staff: bool = True,
	make_superuser: bool = False,
):
	from django.contrib.auth import get_user_model

	User = get_user_model()

	user, created = User.objects.get_or_create(
		username=username,
		defaults={
			"email": email,
			"is_staff": make_staff,
			"is_superuser": make_superuser,
		},
	)

	if created:
		user.set_password(password)
		user.save()
		action = "created"
	else:
		# Always reset password to ensure known credentials in dev seeding.
		changed = False
		if make_staff and not user.is_staff:
			user.is_staff = True
			changed = True
		if make_superuser and not user.is_superuser:
			user.is_superuser = True
			changed = True
		user.set_password(password)
		changed = True
		if changed:
			user.save()
		action = "updated"

	print(
		f"[seed] Evangelist user {action}: username='{user.username}', password='{password}', "
		f"staff={user.is_staff}, superuser={user.is_superuser}"
	)
	return user


def seed_tracker_data(
	evangelist,
	target_evangelisms: int = 25,
	followups_min: int = 0,
	followups_max: int = 5,
	past_days: int = 90,
	clear: bool = False,
):
	"""Seed Evangelism and FollowUp models with synthetic data.

	Args:
		evangelist: User instance (assigned to evangelisms)
		target_evangelisms: desired count of evangelisms for this evangelist
		followups_min/max: range of followups to create per evangelism
		past_days: pick evangelism dates within this many days in the past
		clear: if True, wipe existing Evangelism & FollowUp for all users first
	"""
	from tracker.models import Evangelism, FollowUp
	from faker import Faker
	from django.db import transaction

	fake = Faker()

	if clear:
		print("[seed] Clearing existing Evangelism & FollowUp data ...")
		Evangelism.objects.all().delete()  # cascades to FollowUp

	existing_count = Evangelism.objects.filter(evangelist=evangelist).count()
	if existing_count >= target_evangelisms:
		print(f"[seed] Evangelism count ({existing_count}) already >= target ({target_evangelisms}); skipping creation.")
		return

	remaining = target_evangelisms - existing_count
	print(f"[seed] Creating {remaining} evangelism records (target {target_evangelisms}) ...")

	# Faith choices (keys) from model constant (can't import constant directly easily w/out instance; replicate keys)
	faith_keys = ["strong_faith", "less_faith", "unbeliever", "unknown"]

	created_e_ids = []
	with transaction.atomic():
		for i in range(remaining):
			# Ensure uniqueness of person_name per evangelist.
			# Compose name + suffix if accidental duplication.
			base_name = fake.name()
			person_name = base_name
			attempt = 1
			while Evangelism.objects.filter(evangelist=evangelist, person_name=person_name).exists():
				attempt += 1
				person_name = f"{base_name} #{attempt}"  # guaranteed eventually

			days_back = random.randint(0, past_days)
			ev_date = datetime.date.today() - datetime.timedelta(days=days_back)
			faith = random.choice(faith_keys)
			description = fake.paragraph(nb_sentences=3)
			course = fake.word().title() if random.random() < 0.6 else None
			location = fake.city()
			# Relevance auto-set in save() based on faith.
			e = Evangelism(
				evangelist=evangelist,
				person_name=person_name,
				course=course,
				location=location,
				date=ev_date,
				description=description,
				faith=faith,
				relevance=0,  # placeholder; model save() recalculates
				completed=False,
			)
			e.save()
			created_e_ids.append(e.id)

	# Create followups per evangelism
	FOLLOWUP_TARGET = 7  # Mirror constant in utils (avoid import side-effects)
	evangelisms = list(Evangelism.objects.filter(id__in=created_e_ids))
	total_followups = 0
	for e in evangelisms:
		n_followups = random.randint(followups_min, followups_max)
		# Ensure chronological order after evangelism date
		followup_dates = sorted(
			{
				e.date + datetime.timedelta(days=random.randint(1, max(1, past_days - (datetime.date.today() - e.date).days + 1)))
				for _ in range(n_followups)
			}
		)
		made = 0
		for d in followup_dates:
			if d > datetime.date.today():
				# Skip future-dated followups
				continue
			FollowUp.objects.create(
				evangelism=e,
				description=fake.sentence(),
				date=d,
			)
			made += 1
		total_followups += made
		# Mark completed if reached target threshold
		if made >= FOLLOWUP_TARGET:
			e.completed = True
			e.save(update_fields=["completed"])

	print(
		f"[seed] Created {len(created_e_ids)} evangelisms and {total_followups} followups (range {followups_min}-{followups_max})."
	)


def main():
	print("[seed] Starting seeding process...")
	setup_django()

	# Allow overriding via environment variables if needed.
	username = os.getenv("EVANGELIST_USERNAME", "evangelist")
	email = os.getenv("EVANGELIST_EMAIL", "evangelist@example.com")
	password = os.getenv("EVANGELIST_PASSWORD", "password123")
	make_staff = os.getenv("EVANGELIST_IS_STAFF", "true").lower() in {"1", "true", "yes"}
	make_superuser = (
		os.getenv("EVANGELIST_IS_SUPERUSER", "false").lower() in {"1", "true", "yes"}
	)

	try:
		create_evangelist_user(
			username=username,
			email=email,
			password=password,
			make_staff=make_staff,
			make_superuser=make_superuser,
		)
	except Exception as e:  # pragma: no cover - simple seed helper
		print(f"[seed] Error while creating evangelist user: {e}")
		sys.exit(1)

	# Import user now to pass to seeding
	from django.contrib.auth import get_user_model
	User = get_user_model()
	evangelist = User.objects.get(username=username)

	# Tracker seeding params
	target_evangelisms = int(os.getenv("SEED_EVANGELISMS", "25"))
	followups_min = int(os.getenv("SEED_FOLLOWUPS_MIN", "0"))
	followups_max = int(os.getenv("SEED_FOLLOWUPS_MAX", "5"))
	past_days = int(os.getenv("SEED_PAST_DAYS", "90"))
	clear = os.getenv("SEED_CLEAR", "false").lower() in {"1", "true", "yes"}

	# Sanity adjustments
	if followups_min > followups_max:
		followups_min, followups_max = followups_max, followups_min

	try:
		seed_tracker_data(
			evangelist=evangelist,
			target_evangelisms=target_evangelisms,
			followups_min=followups_min,
			followups_max=followups_max,
			past_days=past_days,
			clear=clear,
		)
	except Exception as e:
		print(f"[seed] Error while seeding tracker data: {e}")
		sys.exit(1)

	print("[seed] Done.")


if __name__ == "__main__":
	main()

