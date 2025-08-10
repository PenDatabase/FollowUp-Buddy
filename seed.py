"""Seed script to create/update a default evangelist user.

Run with:
	python seed.py

Idempotent: running multiple times won't duplicate the user. If the user
already exists, the password is reset to the provided value so you can
recover access easily in development.
"""

import os
import sys
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

	print("[seed] Done.")


if __name__ == "__main__":
	main()

