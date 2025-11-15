if __name__ == "__main__":
    with open("auth.txt") as f:
        api_key = f.read()[10:]
        if api_key == "" or api_key == "?":
            print("ERROR: Please input API_KEY in auth.txt")
            print("EXITING...")
            exit(0)
