import platform

from flask import Flask, render_template

from Command import (
    Invoker,
    Receiver,
    SimpleCommand,
    ComplexCommand
)
from decorator import (
    CCHostname,
    CDCpu,
    CDMemory
)

app = Flask(__name__)


def html(text: str) -> str:
    return text.replace("\n", "<br/>").replace("\t", "&nbsp;&nbsp;&nbsp;&nbsp;")


@app.route('/')
def index():
    hostname: CCHostname = CCHostname()
    cpu: CDCpu = CDCpu(hostname)
    memory: CDMemory = CDMemory(cpu)
    metrics: str = memory.operation()

    invoker = Invoker()
    invoker.setFirstCommand(SimpleCommand("Проверка"))
    receiver = Receiver()
    invoker.setSecondCommand(ComplexCommand(
        receiver, "Тестовый текст"))

    command = invoker.executeCommands()
    print(command)

    return render_template(
        'index.html',
        decorator=html(metrics),
        command=html(command),
    )
