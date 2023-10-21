from abc import ABC, abstractmethod


class MyApp_Base(ABC):
    @abstractmethod
    def start_button_clicked(self):
        pass

    @abstractmethod
    def stop_button_clicked(self):
        pass

    @abstractmethod
    def run_program(self):
        pass

    @abstractmethod
    def run(self):
        pass
