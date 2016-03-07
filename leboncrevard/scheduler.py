import schedule, time, csv, config
from leboncrevard import scrapper, job

class LbcScheduler:
    def __init__(self):
        self.jobs = []
        self.running = False

    def add_job(self, job):
        self.jobs.append(job)
        schedule.every(job.interval).minutes.do(job.run)
        print("Adding job for: " + job.scrapper.url)

    def parse_job(self, row):
        name = row[0]
        url = row[1]
        interval = row[2]
        recipients = row[3].split(',')
        print("Parsed job for (" + name + "): url = " + url + ", interval = " + interval + ", Recipients are: " + str(recipients))
        j = job.LbcJob(name, url, int(interval), recipients)
        return j

    def load_job(self, row):
        j = self.parse_job(row)
        for loaded_job in self.jobs:
            if j == loaded_job:
                print("Job already loaded, ignoring.\n")
                return
        self.jobs.append(j)
        schedule.every(j.interval).minutes.do(j.run)
        print("Adding job for: " + j.scrapper.url + "\n")

    def unload_job(self, row):
        j = self.parse_job(row)
        nb_job = 0
        for loaded_job in self.jobs:
            if j == loaded_job:
                loaded_job.disable()
                print("Job for " + loaded_job.scrapper.url + " unloaded.\n")
                return
        print("No such job, ignoring.\n")

    def load_jobs(self):
        print("Loading new jobs from " + config.job_file + ": \n")
        try:
            cr = csv.reader(open(config.job_file ,"r"))
        except Exception as e:
            print("Could not parse " + config.job_file + ", no jobs loaded.")
            return
        line = 0
        for row in cr:
            line = line + 1
            try:
                self.load_job(row)
            except Exception as e:
                print("Could not parse (and ignoring) line: " + str(line))
                pass

    def unload_jobs(self):
        print("Unloading jobs mentionned in " + config.delete_file + ": \n")
        try:
            cr = csv.reader(open(config.delete_file ,"r"))
        except Exception as e:
            print("Could not parse " + config.delete_file + ", no jobs unloaded.")
            return
        line = 0
        for row in cr:
            line = line + 1
            try:
                self.unload_job(row)
            except Exception as e:
                print("Could not parse (and ignoring) line: " + str(line))
                pass

    def update_jobs(self):
        self.load_jobs()
        self.unload_jobs()

    def run_jobs_now(self):
        for job in self.jobs:
            job.run()

    def start(self):
        schedule.every(1).minutes.do(self.update_jobs)
        self.running = True
        while (self.running):
            schedule.run_pending()
            time.sleep(1)
