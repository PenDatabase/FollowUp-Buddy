import os
import django
import random
import datetime
from faker import Faker

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'followup_buddy.settings')
django.setup()

from django.contrib.auth.models import User
from tracker.models import Evangelism, FollowUp

fake = Faker()

# Optional: Clear old data
Evangelism.objects.all().delete()
FollowUp.objects.all().delete()

# Create or get a default superuser evangelist
evangelist, created = User.objects.get_or_create(
    username='evangelist',
    defaults={
        'email': 'evangelist@example.com',
        'is_staff': True,
        'is_superuser': True,
    }
)
if created:
    evangelist.set_password('password123')
    evangelist.save()
    print("✅ Created default superuser: evangelist / password123")

FAITH_OPTIONS = ['strong_faith', 'less_faith', 'unbeliever', 'unknown']
LOCATIONS = ['Hostel A', 'Cafeteria', 'Lecture Hall 2', 'University Chapel', 'Main Library']
COURSES = [
    'Computer Science', 'Industrial Mathematics', 'Industrial Physics',
    'State Management', 'Civil Engineering', 'Mechanical Engineering',
    'Mass Communication', 'Business Administration', 'Architecture',
    'Political Science'
]

# Seed Evangelism records
for _ in range(10):
    faith = random.choice(FAITH_OPTIONS)
    date = fake.date_between(start_date='-14d', end_date='today')
    evangelism = Evangelism.objects.create(
        evangelist=evangelist,
        person_name=fake.name(),
        course=random.choice(COURSES),
        location=random.choice(LOCATIONS),
        date=date,
        description=fake.paragraph(nb_sentences=2),
        faith=faith,
        completed=random.choice([True, False])
    )

    # Add 1–3 follow-ups per evangelism
    for i in range(random.randint(1, 3)):
        FollowUp.objects.create(
            evangelism=evangelism,
            description=fake.sentence(),
            date=date + datetime.timedelta(days=i + 1)
        )

print("✅ Database successfully seeded with evangelism and follow-up data.")
