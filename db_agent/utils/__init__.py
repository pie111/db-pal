def create_conn_url(db_config):
    host, user, password, database, port = db_config.values()
    return f"postgresql://{user}:{password}@{host}:{port}/{database}"


reserved_words = {
    "exit": "Exiting the chat.",
    "help": "Displaying help information...",
    "clear": "Clearing the chat window...",
    "reset": "Resetting the session..."
}

