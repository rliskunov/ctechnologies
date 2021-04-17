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
    return render_template(
        'index.html'
    )


@app.route('/bridge')
def bridge():
    if platform.system() == "Darwin":
        home: Mac = Mac(CurrentDirectory())
        current: Mac = Mac(HomeDirectory())
        result: str = f"{home.operation()}\n{current.operation()}"
    else:
        home: OperationSystem = OperationSystem(CurrentDirectory())
        current: OperationSystem = OperationSystem(HomeDirectory())
        result: str = f"{home.operation()}\n{current.operation()}"
    return render_template(
        'bridge.html',
        bridge=html(result)
    )


@app.route('/decorator')
def decorator():
    hostname: Hostname = Hostname()
    cpu: CPU = CPU(hostname)
    memory: Memory = Memory(cpu)

    return render_template(
        'decorator.html',
        decorator=html(memory.show())
    )
