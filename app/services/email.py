from jinja2 import Environment, FileSystemLoader, select_autoescape
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class EmailBuilder:
    def __init__(self, template_dir="templates",filename:str='email_registration.html'):
        self.env = Environment(
            loader=FileSystemLoader(template_dir),
            autoescape=select_autoescape(['html', 'xml'])
        )
        self.filename = filename

    def render(self, name: str, code: str) -> str:
        template = self.env.get_template(self.filename)
        return template.render(name=name, code=code)


class EmailSender:
    def __init__(self, smtp_server: str, smtp_port: int, username: str, password: str):
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.username = username
        self.password = password

    def send_email(self, to_email: str, subject: str, html_content: str):
        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject
        msg["From"] = self.username
        msg["To"] = to_email

        part = MIMEText(html_content, "html")
        msg.attach(part)

        with smtplib.SMTP_SSL(self.smtp_server, self.smtp_port) as server:
            server.login(self.username, self.password)
            server.sendmail(self.username, to_email, msg.as_string())
