from notion.client import NotionClient
from account import Account
from datetime import datetime

# NOTE: This script only works for a Notion Weekly Agenda that
# is structured like mine

days = (
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday",
    "Sunday"
)

# Enter the token_v2 for your notion (Found by inspecting cookies)
token = ("Enter your token_v2")

# Enter link to your notion
notion_link = "Link to your Notion Weekly Agenda"

todo_list = {}

# Enter you gmail details below
sender = Account("Email@gmail.com", "password")

# Enter the email to send to below
receiver = Account("receiver@123.ca")

# Extract time and create datetime object for notion task
def extract_time(task):
    colon = task.find(":")
    hour = int(task[:colon])
    minute = int(task[colon + 1:colon + 3])

    period = task[colon + 3 : colon + 5]
    if period == "pm":
        hour += 12

    curr_year = datetime.now().year
    curr_month = datetime.now().month
    curr_day = datetime.now().day

    return datetime(curr_year, curr_month, curr_day, hour, minute)


def main():
    client = NotionClient(token_v2=token)

    page = client.get_block(notion_link)

    week = list(page.children[-1].children)

# Make list of daily tasks for the entire week
    for index, day in enumerate(week):
        items = [item.title for item in list(day.children)[2:] if item.title]
        todo_list[days[index]] = items

    curr_day = datetime.now().strftime("%A")

# Find upcoming tasks for today
    upcoming_tasks = [task[task.find("m") + 2:] for task in todo_list[curr_day] if extract_time(task) >= datetime.now()]
    email_tasks = ", ".join(upcoming_tasks)

    sender.send_email(receiver, email_tasks, datetime.now().time())
    print("Reminder Email Sent")


if __name__ == "__main__":
    main()
