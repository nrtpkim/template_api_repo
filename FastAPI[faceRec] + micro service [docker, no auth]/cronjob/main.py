import schedule
import time
from datetime import datetime
from src.utils.logs_setting import log_setting
from src.service.delete_indice_service import DeleteIndeiceService

logger = log_setting(file_name="cronjob_service", logs_tag = "cronjob")
logger.info("start cronjob_service")

#### All Cronjob
dis = DeleteIndeiceService()


def main():
    logger_day = datetime.now().day


    # schedule.every(5).seconds.do(dis.delete_indice)
    schedule.every().day.at("03:00:00").do(dis.delete_indice)


    while True:
        # print(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        schedule.run_pending()
        time.sleep(1)


if __name__ == "__main__":
    main()
