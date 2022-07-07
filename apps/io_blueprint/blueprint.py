from flask_socketio import emit
from . import IOBlueprint

ws_blueprint = IOBlueprint("/ws")


@ws_blueprint.on("say")
def say():
    emit("flash", "Server says...", namespace="/")


@ws_blueprint.on("echo")
def echo(msg):
    emit("flash", msg.get("data"), namespace="/")


@ws_blueprint.on("my event")
def handle_my_custom_event(json):
    emit("connect response", "hello client", namespace="/ws")
    print("received json: " + str(json))


@ws_blueprint.on("hello")
def hello_event(json):
    print("received hello json: " + str(json))