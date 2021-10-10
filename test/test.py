import os
import smtplib
from email.message import EmailMessage
import imghdr

msg = EmailMessage()


EMAIL_ADDRESS = os.getenv("EMAIL_USER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASS")
EMAIL_RECIPENT = "owobuwilfred@gmail.com"

msg["Subject"] = "Sending HTML Message"
msg["From"] = EMAIL_ADDRESS
msg["To"] = EMAIL_RECIPENT
msg.set_content("This is a plain text email")
name = "Wilfred"
html = """\
<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">

    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>

    <style>
        body {
            background-color: green;
        }

        .btn {
            height: 50px;
            border: solid blue 1px;
            font-family: Arial, Helvetica, sans-serif;
            font-size: large;
            margin: auto;
        }
    </style>
</head>

<body>
    <h1 style="color:grey">This is a simple HTML</h1>

    <div class='form-group'>
        <button class='btn'>Download Whitepaper</button>
    </div>
</body>

</html>
    """
msg.add_alternative(html, subtype="html")

# files = ["flask_blog.pdf"]

# for file in files:
#     with open(file, "rb") as f:
#         file_data = f.read()
#         # file_type = imghdr.what(f.name)
#         file_name = f.name
#     msg.add_attachment(
#         file_data, maintype="application", subtype="octet-stream", filename=file_name
#     )


try:
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        smtp.send_message(msg)
        print("Your message has been sent successfully")
except:
    print("Sorry, Unable to send message!")


# from flask_blog.models import User,Post
# from flask_blog import db
# import json
# # users = User.query.all()
# # for user in users:
# #     print(user.username)
# # posts = Post.query.all()
# # for post in posts:
# #     print(post )
# with open('post1.json') as file:
#     data = json.load(file)
#     for post in data:
#         posts =  Post(title = post['title'], content = post['content'],user_id = post['user_id'])
#         db.session.add(posts)
#         db.session.commit()
# data = json.dumps(file)
# print(type(data))
# print(post.user_id)
# posts = Post.query.all()
# index = 1
# for post in posts:
#     print( f' {index}. Post title: {post.title}\n Post Content: {post.content}')
#     index += 1

# import socket
# import requests
# import json

# hostname = socket.gethostname()
# IPAddr = socket.gethostbyname(hostname)
# print(IPAddr)
# print(hostname)

# query = IPAddr
# fields = [
#     "status",
#     "message",
#     "country",
#     "countryCode",
#     "region",
#     "regionName",
#     "city",
#     "zip",
#     "lat",
#     "lon",
#     "timezone",
#     "isp",
#     "org",
#     "as",
#     "query",
# ]

# url = f"http://ip-api.com/json/{query}?={fields}"

# r = requests.get(url)
# data = r.json()
# print(type(data))
# for key, value in enumerate(data):
#     print(f"{key} = {data}")


# response = requests.get(url)
# print(response.status_code)

# import re
# import json
# import urlopen

# url = "http://ipinfo.io/json"
# response = urlopen(url)
# data = json.load(response)

# ip = data["ip"]
# org = data["org"]
# city = data["city"]

# print(ip)
# print(org)
# print(city)
