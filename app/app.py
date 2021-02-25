import platform

from flask import Flask, render_template

from bridge import (
    OperationSystem,
    CurrentDirectory,
    HomeDirectory,
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
        home: Mac = Mac(CurrentDirectory())
        current: Mac = Mac(HomeDirectory())
        bridge: str = f"{home.operation()}\n{current.operation()}"
    else:
        home: OperationSystem = OperationSystem(CurrentDirectory())
        current: OperationSystem = OperationSystem(HomeDirectory())
        bridge: str = f"{home.operation()}\n{current.operation()}"

    return render_template(
        'index.html',
        decorator=html(metrics),
        bridge=html(bridge),
    )
