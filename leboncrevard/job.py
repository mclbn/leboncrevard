import smtplib
import time
from email.mime.text import MIMEText

from leboncrevard import scrapper, config


class LbcJob:
    def __init__(self, name, url, interval, recipients):
        self.name = name
        self.url = url
        self.scrapper = scrapper.LbcScrapper(url)
        self.interval = interval
        self.recipients = recipients
        self.outfile = name + ".csv"
        self.shouldrun = True

    def __eq__(self, other):
        if self.name != other.name:
            return False
        if self.url != other.url:
            return False
        # Ignoring interval and recipients for now
        # if self.interval != other.interval:
        #     return False
        # if self.recipients != other.recipients:
        #     return False
        return True

    def disable(self):
        self.shouldrun = False

    def enable(self):
        self.shouldrun = False

    def run(self):
        if not self.shouldrun:
            return
        if (self.scrapper.test_connectivity() == False):
            print("No connectivity, aborting for now...")
            return False
        else:
            print("Starting scraping job: " + self.name)
            ads = self.scrapper.scrap()
            if ads == None:
                print("Nothing to scrap for " + self.name + ", aborting job.")
                return False
            text = ""
            hashes = ""
            f = open(self.outfile, "a+")
            f.seek(0)
            lines = f.read()
            for ad in ads:
                ad_hash = ad.get_hash()
                line = "\"" + ad.get_link() + "\"," + ad_hash
                if lines.find(line) != -1:
                    print("Known ad, skipping.")
                    continue
                if lines.find(ad_hash) != -1:
                    text += "Repost: "
                print("Unknown ad, sending...")
                text += ad.get_text()
                hashes += time.strftime("%d-%m-%y") + "," + line + "\n"
            if len(text) > 0:
                for recipient in self.recipients:
                    print(recipient)
                    try:
                        print("Sending mail...")
                        msg = MIMEText(text)
                        msg['Subject'] = "Nouvelles annonces (" + self.name + ")"
                        msg['From'] = config.SMTP_USER
                        msg['To'] = recipient
                        s = smtplib.SMTP(config.SMTP_SERVER)
                        s.ehlo()
                        s.starttls()
                        s.login(config.SMTP_USER, config.SMTP_PASS)
                        s.send_message(msg)
                        s.quit()
                        f.write(hashes)
                    except Exception as e:
                        print(str(e))
                        pass
            f.close()
