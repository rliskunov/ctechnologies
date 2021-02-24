from flask import Flask, render_template

from bridge import (
    ConcreteImplementationA,
    ConcreteImplementationB,
    Abstraction,
    client_code,
    ExtendedAbstraction
)
from decorator import (
    ConcreteComponent,
    client_code,
    ConcreteDecoratorA,
    ConcreteDecoratorB
)

app = Flask(__name__)


@app.route('/')
def index():
    simple: ConcreteComponent = ConcreteComponent()
    decorator1: ConcreteDecoratorA = ConcreteDecoratorA(simple)
    decorator2: ConcreteDecoratorB = ConcreteDecoratorB(decorator1)
    decorator: str = client_code(decorator2)

    implementation: ConcreteImplementationA = ConcreteImplementationA()
    abstraction: Abstraction = Abstraction(implementation)
    bridgeA: str = client_code(abstraction)

    implementation: ConcreteImplementationB = ConcreteImplementationB()
    abstraction: Abstraction = ExtendedAbstraction(implementation)
    bridgeB: str = client_code(abstraction)

    return render_template(
        'index.html',
        decorator=decorator,
        bridgeA=bridgeA,
        bridgeB=bridgeB,
    )
