import jwt
import os

token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6IjE1NDNhNmE1ZDU5NTRiNGJiOTNkZjY3NTc5Nzk0OTExIn0.CzzUXZ660lftL08EiwKgqjNrnI8kYljqlIFkRmvkrcA'
data = jwt.decode(token, os.environ['SECRET'], algorithms=["HS256"])
