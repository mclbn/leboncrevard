#!/usr/bin/env python3
from leboncrevard import scheduler, job

S = scheduler.LbcScheduler()
S.update_jobs()
S.start()
