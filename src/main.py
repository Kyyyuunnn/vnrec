import os
import asyncio
from login import login, auto_login, logout, read_saved_user_info
from manual_search import manual_search, vn_search
from fetch_user_list import import_user_list
from fetch_tags import main_fetch_tags
from recommend import recommend, pipeline

def main():
    info_file = "data/info.txt"

    token = None
    username = None

    if os.path.exists(info_file):
        with open(info_file, "r") as f:
            lines = f.readlines()
            for line in lines:
                if line.startswith("token="):
                    token = line.strip().split("=", 1)[1]
                elif line.startswith("username="):
                    username = line.strip().split("=", 1)[1]
                elif line.startswith("user_id="):
                    user_id = line.strip().split("=", 1)[1]

    if username:
        print(f"Welcome Back {username}! ")
    else:
        print(f"Welcome to VNReccommender! ")
    
    print(f"Please choose an option below. ")

    print("1: Login (please go through this option at least once before beginning to use the application.) ")
    print("2: Manually input novels")
    print("3: Import your VNDB read list")
    print("4: Load recommendations") # will combine this later on with the rec system
    print("5: Logout")

    choice = input("Enter your choice (1-5): ").strip()

    # placeholder functions
    if choice == "1":
        token = input("Please enter your VNDB API token: ").strip()
        login(token)
        username, token = read_saved_user_info()
    elif choice == "2": 
        if token:
            asyncio.run(manual_search(token))
        else:
            print("You must login first.")
    elif choice == "3":
        asyncio.run(import_user_list(token, user_id))
    elif choice == "4":
        if not token:
            print("You must login first.")
        else:
            input_file = "data/read_list.txt"
            if not os.path.exists(input_file):
                print("Read list not found.")
            else:
                with open(input_file, "r", encoding="utf-8") as f:
                    vn_titles = [line.strip() for line in f.readlines() if line.strip()]
                asyncio.run(pipeline(token, vn_titles))
    elif choice == "5":
        logout()
    else:
        print("Invalid option ")

# for main to exe
if __name__ == "__main__":
    main()
