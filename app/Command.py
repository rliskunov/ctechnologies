from __future__ import annotations
from abc import ABC, abstractmethod


class ICommand(ABC):
    """
    Интерфейс Команды объявляет метод для выполнения команд.
    """

    @abstractmethod
    def execute(self) -> str:
        pass


class ShowMethodName(ICommand):
    """
    Простая команда, способная выполнять простые операции самостоятельно.
    """

    def __init__(self, payload: str):
        self.payload = payload

    def execute(self) -> str:
        return (f"Выполнение метода: "
                f"({self.payload})")


class ExecuteMethod(ICommand):
    """
    Команда, делегирующая операции другим объектам, называемым «получателями».
    """

    # Сложные команды могут принимать один или несколько объектов-получателей вместе с любыми данными о контексте через конструктор.
    def __init__(self, receiver: Receiver, name: str):
        self.receiver = receiver
        self.name = name

    def execute(self) -> str:
        return  self.receiver.executeMethod(self.name)


class Receiver:
    """
    Класс Получатель, содержащий некую важную бизнес-логику. Фактически, любой класс может выступать Получателем.
    """

    def executeMethod(self, a: str) -> str:
        return (f"\nМетод {a} выполнен")


class Invoker:
    """
    Отправитель связан с одной или несколькими командами. Он отправляет запрос команде.
    """

    firstCommand = None
    secondCommand = None
    firstText: str
    secondText: str

    def setFirstCommand(self, command: ICommand):
        self.firstCommand = command

    def setSecondCommand(self, command: ICommand):
        self.secondCommand = command

    def executeCommands(self):
        """
        Отправитель не зависит от классов конкретных команд и получателей.
        Отправитель передаёт запрос получателю косвенно, выполняя команду.
        """

        print("Invoker: Первая имеющаяся команда: ")
        if isinstance(self.firstCommand, ICommand):
            self.firstText = (self.firstCommand.execute())

        print("Invoker: Вторя имющаяся команда")
        if isinstance(self.secondCommand, ICommand):
            self.secondText = self.secondCommand.execute()

        self.firstText += self.secondText
        return self.firstText


if __name__ == "__main__":
    """
    Клиентский код может параметризовать отправителя любыми командами.
    """

    invoker = Invoker()
    invoker.setFirstCommand(ShowMethodName("Say Hi!"))
    receiver = Receiver()
    invoker.setSecondCommand(ExecuteMethod(
        receiver, "Send email", "Save report"))

    invoker.executeCommands()