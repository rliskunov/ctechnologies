from socket import gethostname
from abc import ABC, abstractmethod

import psutil


class IComponent(ABC):
    """
    Базовый интерфейс Компонента определяет поведение, которое изменяется декораторами.
    """

    @abstractmethod
    def operation(self):
        """ операция выводит строку с различной информацией """


class CCHostname(IComponent):
    """
    Конкретные Компоненты предоставляют реализации поведения по умолчанию. Может быть несколько вариаций этих классов.
    """

    def operation(self) -> str:
        return f"Hostname: {gethostname()}"


class IDecorator(IComponent):
    """
    Базовый интерфейс Декоратора следует тому же интерфейсу, что и другие компоненты.
    """

    component: IComponent = None

    def __init__(self, component: IComponent):
        self.component = component

    def operation(self):
        return self.component.operation()

# Конкретные Декораторы вызывают обёрнутый объект и изменяют его результат некоторым образом.
class CDCpu(IDecorator):
    """
    Декоратор добавляет строки информации о процессоре
    """

    # Декораторы могут вызывать родительскую реализацию операции, вместо того, чтобы вызвать обёрнутый объект напрямую.
    def operation(self):

        return f"{self.component.operation()}" \
               f"\nCPU:" \
               f"\n\tCount: {psutil.cpu_count()}" \
               f"\n\tUsage: {psutil.cpu_percent(interval=1)}"


# Декоратор добавляющий тсроку с информацией о памяти
class CDMemory(IDecorator):

    def operation(self):
        stats = psutil.virtual_memory()
        total = stats.total
        used = stats.used
        used_percent = stats.percent
        return f"{self.component.operation()}" \
               f"\n Memory:" \
               f"\n\tPercent: {used_percent}," \
               f"\n\tTotal: {round(total / 1e+6, 3)}, MB" \
               f"\n\tUsed: {round(used / 1e+6, 3)}, MB"


if __name__ == "__main__":
    hostname: CCHostname = CCHostname()
    cpu = CDCpu(hostname)
    memory = CDMemory(cpu)
    print(memory.operation())
