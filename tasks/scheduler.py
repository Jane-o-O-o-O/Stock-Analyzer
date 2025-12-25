"""Daily scheduler to trigger analysis after market close."""
from __future__ import annotations
import logging
from apscheduler.schedulers.blocking import BlockingScheduler

from api.app import run_sector_analysis
from modules.utils import setup_logging

setup_logging()
logger = logging.getLogger(__name__)


def job():
    logger.info("Starting scheduled sector analysis...")
    run_sector_analysis()
    logger.info("Scheduled sector analysis completed")


def main():
    scheduler = BlockingScheduler(timezone="Asia/Shanghai")
    # Run every day at 15:10 local time
    scheduler.add_job(job, "cron", hour=15, minute=10)
    logger.info("Scheduler started, waiting for trigger...")
    scheduler.start()


if __name__ == "__main__":
    main()
