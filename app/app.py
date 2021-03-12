import platform

from flask import Flask, render_template

from Command import (
    Invoker,
    Receiver,
    ShowMethodName,
    ExecuteMethod
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
    metrics: str = memory.ShowStats()

    invoker = Invoker()
    invoker.setFirstCommand(ShowMethodName("Запрос операций"))
    receiver = Receiver()
    invoker.setSecondCommand(ExecuteMethod(
        receiver, "Запрос операций"))

    command = invoker.executeCommands()
    print(command)

    return render_template(
        'index.html',
        decorator=html(metrics),
        command=html(command),
    )
