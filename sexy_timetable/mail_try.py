import uuid

import sendgrid
import os

from PIL import Image
from sendgrid.helpers.mail import *
import base64
from io import BytesIO

sg = sendgrid.SendGridAPIClient(apikey='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')
from_email = Email("test1@example.com")
subject = "Hello World from the SendGrid Python Library!"
to_email = Email("alekseyrozh@gmail.com")
content = Content("text/plain", "Hello, Email!")
mail = Mail(from_email, subject, to_email, content)


buffered = BytesIO()
image = Image.open("static/lang-logo.png")
image.save(buffered, format="PNG")
base64_encoded_result_bytes = base64.b64encode(buffered.getvalue())
base64_encoded_result_str = base64_encoded_result_bytes.decode('ascii')


attachment = Attachment()
attachment.content = base64_encoded_result_str
attachment.type = "image/jpeg"
attachment.filename = "wowow"
attachment.disposition = "attachment"
attachment.content_id = str(uuid.uuid4())

mail.add_attachment(attachment)

response = sg.client.mail.send.post(request_body=mail.get())
print(response.status_code)
print(response.body)
print(response.headers)
