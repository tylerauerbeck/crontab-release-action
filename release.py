import datetime, croniter, json, os, git
from crontab import CronTab

# Github event path
EVENT = os.getenv('GITHUB_EVENT_PATH')
WORKSPACE = os.getenv('GITHUB_WORKSPACE')
RELEASE_CMD = os.getenv('RELEASE_CMD')
CHANGELOG = os.getenv('CHANGELOG')

# Read in the event so we can parse the schedule
with open(EVENT) as ev:
  data = json.load(ev)
  cron_sched = data['schedule']

# Create an empty crontab
cron = CronTab()

# Create a dummy job -- we just need to be able to evaluate a cron schedule
job = cron.new(command='/usr/bin/echo')
job.setall(cron_sched)

# Create a schedule so that we can look at the previous run
schedule = job.schedule(date_from=datetime.datetime.now())
last_run = schedule.get_prev()
last_run = schedule.get_prev()

repo = git.Repo('/workspace/dash')
logs = repo.git.log('--oneline', '--pretty=format:" %h %s by %an"', '--no-merges', '--since=' + str(last_run)).split('\n')

if len(logs) >= 1:
    print("There have been changes since the last run. Creating a new release...")
    try:
        print("Running build command: " + RUN_CMD)
    except NameError:
        print("No build command provided. Using Release API")
else:
    print("There have been no changes since the last run. Exiting...")
