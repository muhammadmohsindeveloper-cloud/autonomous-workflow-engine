class SendEmailPlugin:

    name = "send_email"

    def execute(self, data):
        print("Sending email:", data)
        return {"status": "email_sent"}