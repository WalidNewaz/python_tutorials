# Imagine you’re building a system that needs to **send notifications**.
# Your app expects a `Notifier` interface, but you have multiple third-party
# services with very different APIs (e.g., Slack, Email, SMS).
#
# Instead of rewriting your app for each provider, you write **adapters**
# to normalize them to a common interface.


class Notifier:
    def send(self, message: str):
        raise NotImplementedError

# Pretend this is a library you can't change
class SlackAPI:
    def post_message(self, channel: str, text: str):
        print(f"[Slack] #{channel}: {text}")

class EmailAPI:
    def send_email(self, to: str, subject: str, body: str):
        print(f"[Email] To:{to} | {subject}: {body}")

# --- Adapters for 3rd Party libraries ------
class SlackAdapter(Notifier):
    def __init__(self, slack_api: SlackAPI, channel: str):
        self.slack_api = slack_api
        self.channel = channel

    def send(self, message: str):
        self.slack_api.post_message(self.channel, message)


class EmailAdapter(Notifier):
    def __init__(self, email_api: EmailAPI, recipient: str):
        self.email_api = email_api
        self.recipient = recipient

    def send(self, message: str):
        subject = "Notification"
        self.email_api.send_email(self.recipient, subject, message)

def notify_all(notifiers: list[Notifier], message: str):
    for notifier in notifiers:
        notifier.send(message)

# Usage
slack = SlackAdapter(SlackAPI(), channel="dev-team")
email = EmailAdapter(EmailAPI(), recipient="admin@example.com")

my_notifiers = [slack, email]
notify_all(my_notifiers, "Adapter Pattern makes integrations easy!")
