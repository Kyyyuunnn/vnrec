import asyncio
import os
from azaka import Client

info_file = "info.txt"

async def login_and_greet(token: str):
    try:
        async with Client(token=token) as client:
            auth_info = await client.get_auth_info()
            username = auth_info.username
            
            # saves token
            with open(info_file, "w") as f:
                f.write(f"token={token}\nusername={username}")

            print(f"Login successful! Welcome {username}!")

    except Exception as e:
        print("Login failed: ", e)

def login(token: str):
    asyncio.run(login_and_greet(token))


def auto_login():
    if os.path.exists(info_file):
        with open(token_file, "r") as f:
            saved_token = f.read().strip()
        login(saved_token)
        return True
    else: 
        return False

def logout():
    if os.path.exists(info_file):
        os.remove(token_file)
        print("Logged out successfully.")
    else:
        print("You are not logged in.")