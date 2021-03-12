from socket import gethostname
from abc import ABC, abstractmethod

import psutil


class IComponent(ABC):
    """
    Базовый интерфейс Компонента определяет поведение, которое изменяется декораторами.
    """

    @abstractmethod
    def ShowStats(self):
        """ операция выводит строку с различной информацией """


class CCHostname(IComponent):
    """
    Конкретные Компоненты предоставляют реализации поведения по умолчанию. Может быть несколько вариаций этих классов.
    """

    def ShowStats(self):
        return f"Hostname: {gethostname()}"


class IDecorator(IComponent):
    """
    Базовый интерфейс Декоратора следует тому же интерфейсу, что и другие компоненты.
    """

    component: IComponent = None

    def __init__(self, component: IComponent):
        self.component = component

    def ShowStats(self):
        return self.component.ShowStats()

# Конкретные Декораторы вызывают обёрнутый объект и изменяют его результат некоторым образом.
class CDCpu(IDecorator):
    """
    Декоратор добавляет строки информации о процессоре
    """

    cpuCount = psutil.cpu_count()
    cpuPercent = psutil.cpu_percent(interval=1)

    def ShowCPU(self):
        return f"\nCPU:" \
               f"\n\tCount: {self.cpuCount}" \
               f"\n\tUsage: {self.cpuPercent}"

    # Декораторы могут вызывать родительскую реализацию операции, вместо того, чтобы вызвать обёрнутый объект напрямую.
    def ShowStats(self):
        return f"{self.component.ShowStats()}" \
               f"{self.ShowCPU()}"



# Декоратор добавляющий тсроку с информацией о памяти
class CDMemory(IDecorator):

    stats = psutil.virtual_memory()
    total = stats.total
    used = stats.used
    used_percent = stats.percent

    def ShowMemory(self):
        return f"\n Memory:" \
               f"\n\tPercent: {self.used_percent}," \
               f"\n\tTotal: {round(self.total / 1e+6, 3)}, MB" \
               f"\n\tUsed: {round(self.used / 1e+6, 3)}, MB"

    def ShowStats(self):
        return f"{self.component.ShowStats()}" \
               f"{self.ShowMemory()}"



if __name__ == "__main__":
    hostname: CCHostname = CCHostname()
    cpu = CDCpu(hostname)
    memory = CDMemory(cpu)
    print(memory.operation())
