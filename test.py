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

import socket
import requests
import json

hostname = socket.gethostname()
IPAddr = socket.gethostbyname(hostname)
print(IPAddr)
print(hostname)

query = IPAddr
fields = [
    "status",
    "message",
    "country",
    "countryCode",
    "region",
    "regionName",
    "city",
    "zip",
    "lat",
    "lon",
    "timezone",
    "isp",
    "org",
    "as",
    "query",
]

url = f"http://ip-api.com/json/{query}?={fields}"

r = requests.get(url)
data = r.json()
print(type(data))
for key, value in enumerate(data):
    print(f"{key} = {data}")


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
