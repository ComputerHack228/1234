from pywebio import start_server
from pywebio.input import *
from pywebio.output import *
from pywebio.session import *
from pywebio.pin import *
from pywebio.platform.flask import webio_view
from flask import Flask
import threading

# Global variables to store messages and users
messages = []
users = set()

app = Flask(__name__)

def chat():
    global messages, users

    # Get the user's name
    user = input("Enter your name to join the chat", required=True)
    users.add(user)
    put_markdown(f"### Welcome to the chat, {user}!")

    # Display the chat history
    for msg in messages:
        put_text(msg)

    # Input field for new messages
    while True:
        msg = input("Type your message", required=True)
        messages.append(f"{user}: {msg}")
        
        # Update the chat for all users
        for u in users:
            if u != user:
                run_js(f'addMessage("{user}: {msg}")', session_id=u)

        # Display the message in the current session
        put_text(f"{user}: {msg}")

def add_message_js():
    return """
    <script>
    function addMessage(msg) {
        var p = document.createElement("p");
        p.textContent = msg;
        document.body.appendChild(p);
    }
    </script>
    """

def main():
    put_html(add_message_js())
    chat()

app.add_url_rule('/', 'webio_view', webio_view(main), methods=['GET', 'POST'])

if __name__ == '__main__':
    start_server(main, port=8080, debug=True)
