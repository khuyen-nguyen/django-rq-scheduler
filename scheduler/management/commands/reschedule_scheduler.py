from django.core.management.base import BaseCommand, CommandError
from scheduler.models import CronJob, RepeatableJob, ScheduledJob
from django.db.models.functions import Now

class Command(BaseCommand):
  def handle(self, *args, **options):
    print("Doing scanning all scheduled task and reschedule")
    self.reschedule_cron_jobs()
    self.reschedule_repeatable_jobs()
    self.reschedule_scheduled_jobs()

  def reschedule_cron_jobs(self):
    jobs = CronJob.objects.filter(enabled=True)
    self.reschedule_jobs(jobs)

  def reschedule_repeatable_jobs(self):
    jobs = RepeatableJob.objects.filter(enabled=True, scheduled_time__gte=Now())
    self.reschedule_jobs(jobs)

  def reschedule_scheduled_jobs(self):
    jobs = ScheduledJob.objects.filter(enabled=True, scheduled_time__gte=Now())
    self.reschedule_jobs(jobs)

  def reschedule_jobs(self, jobs):
    for job in jobs:
      if job.is_scheduled() is False:
        job.save()
