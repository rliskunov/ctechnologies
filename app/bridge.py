from __future__ import annotations
from abc import ABC, abstractmethod
from pathlib import Path
import platform


class OperationSystem:
    """
    Абстракция устанавливает интерфейс для «управляющей» части двух иерархий
    классов. Она содержит ссылку на объект из иерархии Реализации и делегирует
    ему всю настоящую работу.
    """

    def __init__(self, implementation: Implementation) -> None:
        self.implementation = implementation

    def operation(self) -> str:
        return f"Platform: {platform.system()}" \
               f"\n\t{self.implementation.operation_implementation()}"


class Mac(OperationSystem):
    """
    Можно расширить Абстракцию без изменения классов Реализации.
    """

    def operation(self) -> str:
        return f"Platform: {platform.system()}" \
               f"\n\t{self.implementation.operation_implementation()}"


class Windows(OperationSystem):
    """
    Можно расширить Абстракцию без изменения классов Реализации.
    """

    def operation(self) -> str:
        return f"Platform: Windows\n\t{self.implementation.operation_implementation()}"


class Implementation(ABC):
    """
    Реализация устанавливает интерфейс для всех классов реализации. Он не должен
    соответствовать интерфейсу Абстракции. На практике оба интерфейса могут быть
    совершенно разными. Как правило, интерфейс Реализации предоставляет только
    примитивные операции, в то время как Абстракция определяет операции более
    высокого уровня, основанные на этих примитивах.
    """

    @abstractmethod
    def operation_implementation(self) -> str:
        pass


"""
Каждая Конкретная Реализация соответствует определённой платформе и реализует
интерфейс Реализации с использованием API этой платформы.
"""


class CurrentDirectory(Implementation):
    def operation_implementation(self) -> str:
        return f"Current: {Path.cwd()}"


class HomeDirectory(Implementation):
    def operation_implementation(self) -> str:
        return f"Home: {Path.home()}"


def client_code(abstraction: OperationSystem) -> str:
    """
    За исключением этапа инициализации, когда объект Абстракции связывается с
    определённым объектом Реализации, клиентский код должен зависеть только от
    класса Абстракции. Таким образом, клиентский код может поддерживать любую
    комбинацию абстракции и реализации.
    """
    return abstraction.operation()


if __name__ == "__main__":
    """
    Клиентский код должен работать с любой предварительно сконфигурированной
    комбинацией абстракции и реализации.
    """

    implementation: CurrentDirectory = CurrentDirectory()
    abstraction: OperationSystem = OperationSystem(implementation)
    print(client_code(abstraction))

    implementation: HomeDirectory = HomeDirectory()
    abstraction: Windows = Windows(implementation)
    print(client_code(abstraction))
