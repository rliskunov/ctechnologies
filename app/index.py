from flask import Flask, render_template

from bridge import (
    Abstraction,
    ConcreteImplementationA,
    ConcreteImplementationB,
    ExtendedAbstraction
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

    implementation: ConcreteImplementationA = ConcreteImplementationA()
    abstraction: Abstraction = Abstraction(implementation)
    bridgeA: str = abstraction.operation()

    implementation: ConcreteImplementationB = ConcreteImplementationB()
    abstraction: Abstraction = ExtendedAbstraction(implementation)
    bridgeB: str = abstraction.operation()

    return render_template(
        'index.html',
        decorator=html(metrics),
        bridgeA=html(bridgeA),
        bridgeB=html(bridgeB),
    )
