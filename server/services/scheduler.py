from apscheduler.schedulers.background import BackgroundScheduler
from services.webhook_processor import process_pending

def start_scheduler(app):
    scheduler = BackgroundScheduler(daemon=True)

    def job():
        with app.app_context():
            process_pending()

    scheduler.add_job(
        job,
        trigger="interval",
        seconds=60,
        id="process_pending_job",
        replace_existing=True
    )

    scheduler.start()
