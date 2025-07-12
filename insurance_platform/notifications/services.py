def send_notification(recipient, message):
    """
    Sends a notification to a recipient.

    For now, this just prints to the console. In a real application,
    this would integrate with an SMS gateway like Twilio, an email service,
    or a push notification service.
    """
    print(f"--- NOTIFICATION ---")
    print(f"Recipient: {recipient}")
    print(f"Message: {message}")
    print(f"--------------------")

    # Example of how you might extend this for different channels:
    # if is_sms_recipient(recipient):
    #     send_sms(recipient, message)
    # elif is_email_recipient(recipient):
    #     send_email(recipient, "You have a new notification", message)

    return True # Assume success for now
