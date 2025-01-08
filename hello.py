from datetime import datetime
from calendar import monthrange


year = 2025
month = 1

 # First day of the week (0 = Monday, 6 = Sunday)
first_day_of_week = datetime(year, month, 2).weekday()

# Placeholder for empty slots in the calendar
placeholders = list(range(first_day_of_week))

print(first_day_of_week)
print(placeholders)