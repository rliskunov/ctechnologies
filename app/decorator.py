from socket import gethostname

import psutil


class Component:
    """
    Базовый интерфейс Компонента определяет поведение, которое изменяется
    декораторами.
    """

    def show(self) -> str:
        pass


class Hostname(Component):
    """
    Конкретные Компоненты предоставляют реализации поведения по умолчанию. Может
    быть несколько вариаций этих классов.
    """

    def show(self) -> str:
        return f"Hostname: {gethostname()}"


class Decorator(Component):
    """
    Базовый класс Декоратора следует тому же интерфейсу, что и другие
    компоненты. Основная цель этого класса - определить интерфейс обёртки для
    всех конкретных декораторов. Реализация кода обёртки по умолчанию может
    включать в себя поле для хранения завёрнутого компонента и средства его
    инициализации.
    """

    _component: Component = None

    def __init__(self, component: Component) -> None:
        self._component = component

    @property
    def component(self) -> Component:
        """
        Декоратор делегирует всю работу обёрнутому компоненту.
        """

        return self._component

    def show(self) -> str:
        return self._component.show()


class CPU(Decorator):
    """
    Конкретные Декораторы вызывают обёрнутый объект и изменяют его результат
    некоторым образом.
    """

    def show(self) -> str:
        """
        Декораторы могут вызывать родительскую реализацию операции, вместо того,
        чтобы вызвать обёрнутый объект напрямую. Такой подход упрощает
        расширение классов декораторов.
        """
        return f"{self.component.show()}" \
               f"\nCPU:" \
               f"\n\tCount: {psutil.cpu_count()}" \
               f"\n\tUsage: {psutil.cpu_percent(interval=1)}"


class Memory(Decorator):
    """
    Декораторы могут выполнять своё поведение до или после вызова обёрнутого
    объекта.
    """

    def show(self) -> str:
        stats = psutil.virtual_memory()
        total = stats.total
        used = stats.used
        used_percent = stats.percent
        return f"{self.component.show()}" \
               f"\n Memory:" \
               f"\n\tPercent: {used_percent}," \
               f"\n\tTotal: {round(total / 1e+6, 3)}, MB" \
               f"\n\tUsed: {round(used / 1e+6, 3)}, MB"


def client_code(component: Component) -> str:
    """
    Клиентский код работает со всеми объектами, используя интерфейс Компонента.
    Таким образом, он остаётся независимым от конкретных классов компонентов, с
    которыми работает.
    """
    return component.show()


if __name__ == "__main__":
    hostname: Hostname = Hostname()
    cpu: CPU = CPU(hostname)
    memory: Memory = Memory(cpu)
    decorator: str = client_code(memory)
    print(decorator)
