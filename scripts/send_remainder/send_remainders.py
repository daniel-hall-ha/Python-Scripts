import sys
import datetime
from email.message import EmailMessage
import smtplib
from dotenv import load_dotenv
import os
import time

# Load env token
load_dotenv()

# Load sender_emaial and sender_app_password
SENDER_EMAIL = os.getenv("SENDER_EMAIL")
SENDER_APP_PASSWORD = os.getenv("SENDER_APP_PASSWORD")
if not SENDER_EMAIL:
    raise ValueError("SENDER_EMAIL not found. Make sure .env file exists and has SENDER_EMAIL defined.")
if not SENDER_APP_PASSWORD:
    raise ValueError("SENDER_EMAIL not found. Make sure .env file exists and has SENDER_APP_PASSWORD defined.")

# Show error message when user doesn't enter full information
def usage():
    print("send_reminders: Send meeting reminders")
    print("")
    print("invocation:")
    print("     send_reminders 'Date|Meeting Title|Emails|Meeting Link'")
    return 1

# Create message object to send via send_message()
def message_template(meeting_date, meeting_title, meeting_link, receiver_email):

    # Convert entered date to the format, October 25, 2025 Wednesday
    date_obj = datetime.datetime.strptime(meeting_date, r"%Y-%m-%d")
    date_professional = date_obj.strftime("%B %d, %Y %A")

    # Create message object, setting the email mandatories Subject, From, To
    message = EmailMessage()
    message["Subject"] = f"Kindly Reminder for Meeting"
    message["From"] = SENDER_EMAIL
    message["To"] = receiver_email

    message.set_content(f"""\
    Dear Team,
                        
    This is a kind reminder about the upcoming daily standup meeting scheduled for {date_professional}.
    Please make sure to join on time, as we will discuss important updates and urgent priorities.
    Join Meeting : {meeting_link}

    Thank you,
    Meeting Coordinator
    """)

    message.add_alternative(f"""
    <!DOCTYPE html>
    <html>
      <body style="font-family: Arial, sans-serif; line-height: 1.6; margin: 0; padding: 0; background-color: #f9f9f9;">
        <table align="center" width="600" cellpadding="0" cellspacing="0" style="background: #ffffff; border-radius: 8px; box-shadow: 0 2px 6px rgba(0,0,0,0.1); padding: 20px;">
          <tr>
            <td>
              <h2 style="color: #333333; text-align: center;">Meeting Reminder</h2>
              <p style="font-size: 16px; color: #555555;">
                Dear team,
              </p>
              <p style="font-size: 16px; color: #555555;">
                This is a kind reminder about the upcoming <b>{meeting_title}</b> scheduled for 
                <span style="color: #0073e6; font-weight: bold;">{date_professional}</span>.
              </p>
              <p style="font-size: 16px; color: #555555;">
                Please make sure to join on time, as we will discuss important updates and urgent priorities.
              </p>
              <p style="font-size: 16px; color: #555555; text-align: center; margin-top: 30px;">
                <a href="{meeting_link}" style="background-color: #0073e6; color: #ffffff; text-decoration: none; padding: 12px 20px; border-radius: 5px; font-weight: bold;">Join Meeting</a>
              </p>
              <p style="font-size: 16px; color: #555555; margin-top: 20px;">
                Thank you,<br>
                <i>Meeting Coordinator</i>
              </p>
            </td>
          </tr>
        </table>
      </body>
    </html>
    """, subtype="html")
    return message

# Send message using smtp
def send_message(message, receiver_email):
    with smtplib.SMTP_SSL('smtp.gmail.com' , 465) as smtp:
        smtp.login(SENDER_EMAIL, SENDER_APP_PASSWORD)
        smtp.send_message(message)
        print("Email successfully sent to ", receiver_email)

def main():
    # If user didn't enter all the mandatories
    if len(sys.argv) < 2:
        return usage()
    try:
        # Extract meeting title, email list (string) and meeting link from user input
        meeting_date, meeting_title, emails, meeting_link = sys.argv[1].split('|')
        # Convert string email list to list to traverse
        emails_list = [email.strip() for email in emails.split(',')]
        # Send email for each email in email list with 3 seconds delay
        for email in emails_list:
            message = message_template(meeting_date, meeting_title, meeting_link, email)
            send_message(message, email)
            time.sleep(3)
    except Exception as e:
        print(f"Failure to send email {e}", file=sys.stderr)

if __name__ == "__main__":
    main()