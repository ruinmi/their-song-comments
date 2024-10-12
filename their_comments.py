# ta 的网易音乐主页url
user_home_url = 'https://music.163.com/#/user/home?id=123456'

# 找寻 ta 在这些歌里的评论
song_urls = [
    'https://music.163.com/song?id=2619125556', # 才二十三 - 方大同
    '',
]

import json
import random
import requests
import re

class Comment:
    def __init__(self, id, user_id, nickname, content, time=None, time_str=None, location=None, device=None, reply=None):
        self.id = id
        self.user_id = user_id
        self.nickname = nickname
        self.content = content
        self.time = time
        self.time_str = time_str if time_str is not None else ""
        self.location = location if location is not None else "Unknown"
        self.device = device if device is not None else "Unknown"
        self.reply = reply

    def __str__(self):
            indent_str = '    '
            result = []
            if isinstance(self.reply, Comment):
                result.append(f"{self.reply.nickname}（{self.reply.device} {self.reply.location}）: {self.reply.content}")
                result.append(f"{indent_str}{self.nickname}（{self.time_str} {self.device} {self.location}）: {self.content}")
            else:
                result.append(f"{self.nickname}（{self.time_str} {self.device} {self.location}）: {self.content}")
            return '\n'.join(result)

class RequestComposer:
    def __init__(self):
        pass

    def __a(self, a):
        b = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
        c = ""
        for d in range(a):
            e = random.random() * len(b)
            e = int(e)
            c += b[e]
        return c

    def __b(self, a, b):
        import base64
        from cryptography.hazmat.primitives import padding
        from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
        from cryptography.hazmat.backends import default_backend

        # Convert inputs to bytes
        c = b.encode('utf-8')  # Key
        d = "0102030405060708".encode('utf-8')  # IV
        e = a.encode('utf-8')  # Plaintext

        # Ensure key is 16, 24, or 32 bytes long
        if len(c) not in [16, 24, 32]:
            c = (c * ((16 // len(c)) + 1))[:16]

        # Pad plaintext using PKCS7
        padder = padding.PKCS7(128).padder()
        padded_e = padder.update(e) + padder.finalize()

        # Create AES cipher in CBC mode
        cipher = Cipher(algorithms.AES(c), modes.CBC(d), backend=default_backend())
        encryptor = cipher.encryptor()

        # Encrypt the plaintext
        f = encryptor.update(padded_e) + encryptor.finalize()

        # Return Base64 encoded ciphertext
        return base64.b64encode(f).decode('utf-8')

    def __c(self, a, b, c):
        # a: string to encrypt
        # b: exponent as a hexadecimal string
        # c: modulus as a hexadecimal string

        # Convert exponent and modulus from hexadecimal strings to integers
        e = int(b, 16)
        n = int(c, 16)

        # Call the encryptedString function with the key and the plaintext
        return self.__encryptedString((e, n), a)

    def __encryptedString(self, key, s):
        # key: tuple (e, n) where e is the exponent and n is the modulus
        # s: plaintext string to encrypt

        e, n = key

        # Convert the plaintext string into an array of character codes
        c = [ord(ch) for ch in s]

        # Calculate chunk size based on key size
        key_size_in_bits = n.bit_length()
        max_chunk_size = ((key_size_in_bits + 7) // 8) - 11  # PKCS#1 padding

        # Pad the array with zeros until its length is a multiple of the chunk size
        while len(c) % max_chunk_size != 0:
            c.append(0)

        encrypted = ''

        # Process the array in chunks
        for chunk_start in range(0, len(c), max_chunk_size):
            m = 0  # Initialize the integer representation of the chunk
            i = chunk_start
            h = 0
            # Combine bytes into a big integer, mimicking the JavaScript logic
            while i < chunk_start + max_chunk_size:
                val = c[i]
                i += 1
                if i < chunk_start + max_chunk_size:
                    val += c[i] << 8
                    i += 1
                else:
                    val += 0 << 8
                m += val * (2 ** (16 * h))
                h += 1

            # Perform RSA encryption: c = m^e mod n
            k = pow(m, e, n)

            # Convert the encrypted integer to a hexadecimal string
            l = format(k, 'x')

            # Append the encrypted chunk to the result string
            encrypted += l + ' '

        # Return the final encrypted string without the trailing space
        return encrypted.strip()

    def __d(self, d, e, f, g):
        h = {}
        i = self.__a(16)
        h['encText'] = self.__b(d, g)
        h['encText'] = self.__b(h['encText'], i)
        h['encSecKey'] = self.__c(i, e, f)
        return h

    def send(self, url, params):
        res = self.__d(params, '010001', '00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7', '0CoJUm6Qyw8W8jud')
        data = {
            'params': res['encText'],
            'encSecKey': res['encSecKey']
        }
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        response = requests.post(url, data=data, headers=headers)
        if (response.text is not None and response.text != ''):
            return json.loads(response.text)
        return None

composer = RequestComposer()

def get_user_follows(user_id):
    url = f'https://music.163.com/weapi/user/getfollows/{user_id}'
    params = '{"uid":"118051408","offset":"0","total":"false","limit":"1000","csrf_token":""}'

    data = composer.send(url, params)
    followss = {}
    for user in data['follow']:
        followss[user['followeds']] = user["userId"]
    for i in sorted (followss) : 
        print((i, followss[i]))

def get_song_comments(song_id, pageNo, pageSize, cursor):
    url = 'https://music.163.com/weapi/comment/resource/comments/get'
    params = {
        "rid": f"R_SO_4_{song_id}",
        "threadId": f"R_SO_4_{song_id}",
        "pageNo": pageNo,
        "pageSize": pageSize,
        "cursor": cursor,
        "offset": "0",
        "orderType": "1",
        "csrf_token": ""
    }

    data = composer.send(url, json.dumps(params))
    comments = []
    if (data is None):
        return comments
    if ('data' not in data):
        raise Exception(data)
    for comment in data['data']['comments']:
        user = comment['user']
        user_id = user['userId']
        nickname = user['nickname']
        content = comment['content']
        time_str = comment['timeStr']
        location = comment['ipLocation']['location']
        time = comment['time']
        id = comment['commentId']
        comment_obj = Comment(id, user_id, nickname, content, time, time_str, location)
        if ('endpoint' in comment['extInfo']):
            if ('USER_AGENT' in comment['extInfo']['endpoint']):
                comment_obj.device = comment['extInfo']['endpoint']['USER_AGENT']
            else:
                comment_obj.device = comment['extInfo']['endpoint']['CLIENT_TYPE']
        if (comment['beReplied'] is not None and len(comment['beReplied']) > 0):
            repr = comment['beReplied'][0]
            comment_obj.reply = Comment(id=repr['commentId'], user_id=repr['user']['userId'], nickname=repr['user']['nickname'], content=repr['content'], location=repr['ipLocation']['location'])
        comments.append(comment_obj)
    return comments

def print_user_comments_in_song(song_id: int, user_id: int):
    cursor = -1
    pageNo = 1
    retry = 0
    while (True):
        if (retry == 0):
            print(f'page: {pageNo}')

        comments = get_song_comments(song_id, pageNo, 1000, cursor)
        for comment in comments:
            if (comment.user_id == user_id or (comment.reply is not None and comment.reply.user_id == user_id)):
                print('')
                print(comment)
                print('')

        if (0 < len(comments) < 1000):
            break
        elif (len(comments) == 0):
            if (retry >= 3):
                break
            else:
                retry += 1
                continue
        
        pageNo += 1
        cursor = comments[-1].time
        retry = 0

user_id = int(re.search(r'id=(\d+)', user_home_url).group(1))
for song_url in song_urls:
    if song_url == '':
        break
    song_id = re.search(r'(?<!user)id=(\d+)', song_url).group(1)
    print(f'song: {song_id}')
    print_user_comments_in_song(song_id=song_id, user_id=user_id)