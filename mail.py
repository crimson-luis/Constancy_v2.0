import smtplib
import ssl
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from string import Template
import argparse


def send_mail(user, new_password, receiver):
    port = 465
    sender = 'talkingtoconstancy@gmail.com'
    sl = 'Z73&sj!d&JR*HmwinsZB'

    message = MIMEMultipart('alternative')
    message['Subject'] = 'Recuperação de senha'
    message['From'] = sender
    message['To'] = receiver

    text = "Caro {user}\ncomo solicitado sua senha foi resetada.\nA sua nova senha é: {new_password}.".format(
        user=user, new_password=new_password)

    html = """\
    <html>
      <head>
      <style>

    .outer {
      display: table;
      position: absolute;
      top: 0;
      left: 0;
      height: 100%;
      width: 100%;
    }

    .middle {
      display: table-cell;
      vertical-align: middle;
    }

    .inner {
      margin-left: auto;
      margin-right: auto;
      width: 400px;
      /*whatever width you want*/
    }

      </style>
      </head>
      <body>
        <div class="outer">
          <div class="middle">
            <div class="inner">
              <p><img src="cid:image1"><br>
              <h1>Recuperação de senha.</h1>
              <p>Saudações senhor(a) $user,<br>
              como solicitado sua senha foi resetada.<br>
              A sua nova senha é: $new_password.</p>
            </div>
          </div>
        </div>
      </body>
    </html>
    """
    html = Template(html).safe_substitute(user=user, new_password=new_password)
    text_part = MIMEText(text, 'plain')
    html_part = MIMEText(html, 'html')

    message.attach(text_part)
    message.attach(html_part)

    constancy_image = 'C:/Users/luisg/OneDrive/Documentos/Python_Scripts/' \
                      'Constancy v2... the death of python/images/Constancy_logo.png'

    with open(constancy_image, 'rb') as attachment:
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(attachment.read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', f'attachment; filename= {constancy_image}')
    part.add_header('Content-ID', '<image1>')
    message.attach(part)

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL('smtp.gmail.com', port, context=context) as server:
        server.login(sender, sl)
        server.sendmail(sender, receiver, message.as_string().encode('utf8'))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Create a ArcHydro schema')
    parser.add_argument('--user', metavar='path', required=True,
                        help='the path to workspace')
    parser.add_argument('--new_password', metavar='path', required=True,
                        help='path to schema')
    parser.add_argument('--receiver', metavar='path', required=True,
                        help='path to dem')
    args = parser.parse_args()
    send_mail(user=args.user, new_password=args.new_password, receiver=args.receiver)