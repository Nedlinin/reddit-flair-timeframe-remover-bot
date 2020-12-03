import datetime
import time

from praw import Reddit

from config import Config
from logger import Logger


class Submissions:

    def __init__(self):
        self.config = Config()
        self.logger = Logger()

        self.reddit = Reddit(client_id=self.config.REDDIT.CLIENT_ID, client_secret=self.config.REDDIT.CLIENT_SECRET,
                             password=self.config.REDDIT.PASSWORD, user_agent=self.config.REDDIT.USER_AGENT,
                             username=self.config.REDDIT.USER_NAME)

        self.subreddit = self.reddit.subreddit(self.config.REDDIT.SUBREDDIT)

        self.start_day_int = time.strptime(self.config.REDDIT.DAY_START, '%A').tm_wday
        self.end_day_int = time.strptime(self.config.REDDIT.DAY_END, '%A').tm_wday

    def run(self):
        print("Removing seller postings between " + self.config.REDDIT.DAY_START + " and " + self.config.REDDIT.DAY_END)

        for submission in self.subreddit.stream.submissions():
            # If the submission was already removed we don't need to process it.
            if submission.removed is True:
                continue

            self.logger.info(f"Handling submission: {submission.title} - http://reddit.com{submission.permalink}")

            if submission.author_flair_css_class is not None \
                    and self.config.REDDIT.FLAIR_TO_REMOVE in submission.author_flair_css_class:

                # Found a seller tagged post.  We might want to act on it.
                post_creation_date_time = datetime.datetime.fromtimestamp(submission.created_utc)

                creation_day = post_creation_date_time.weekday()

                # Check we are within the range of days we should be removing posts for...
                if creation_day in range(self.start_day_int, self.end_day_int):
                    self._remove_post(submission)

    def _remove_post(self, submission):
        self.logger.info(f"Removing post by user: {submission.author.name}")

        # reason = self.subreddit.mod.removal_reasons[self.config.REDDIT.REMOVAL_REASON_ID]
        # submission.mod.remove(reason_id=reason.id)

        # comment = submission.reply(reason.message)
        # comment.mod.distinguish("yes", sticky=True)

        self.logger.info("Removed post successfully.")

    def daemon(self):
        try:
            self.run()
        except Exception:
            self.logger.exception("Execution failed.  Restarting execution shortly.")
            time.sleep(5)
            self.daemon()


if __name__ == "__main__":
    Submissions().daemon()