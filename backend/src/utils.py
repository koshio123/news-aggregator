import boto3

class SESClient:
    def __init__(self, sender: str):
        self.client = boto3.client("ses")
        self.sender = sender

    def send_email(self, to, subject: str, body: str) -> dict:
        response = self.client.send_email(
            Source=self.sender,
            Destination={
                'ToAddresses': [to]
            },
            Message={
                'Subject': {
                    'Data': subject
                },
                'Body': {
                    'Text': {
                        'Data': body
                    }
                }
            }
        )
        return response