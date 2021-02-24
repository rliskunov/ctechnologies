import platform

from flask import Flask, render_template

from bridge import (
    OperationSystem,
    HomeDirectory,
    CurrentDirectory,
    Mac
)
from decorator import (
    Hostname,
    CPU,
    Memory
)

app = Flask(__name__)


def html(text: str) -> str:
    return text.replace("\n", "<br/>").replace("\t", "&nbsp;&nbsp;&nbsp;&nbsp;")


@app.route('/')
def index():
    hostname: Hostname = Hostname()
    cpu: CPU = CPU(hostname)
    memory: Memory = Memory(cpu)
    metrics: str = memory.operation()

    if platform.system() == "Darwin":
        home: Mac = Mac(HomeDirectory())
        current: Mac = Mac(CurrentDirectory())
        bridge: str = f"Home: {home.operation()}\nCurrent: {current.operation()}"
    else:
        home: OperationSystem = OperationSystem(HomeDirectory())
        current: OperationSystem = OperationSystem(CurrentDirectory())
        bridge: str = f"Home: {home.operation()}\nCurrent: {current.operation()}"

    return render_template(
        'index.html',
        decorator=html(metrics),
        bridge=html(bridge),
    )
