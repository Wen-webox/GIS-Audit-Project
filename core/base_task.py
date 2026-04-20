# -*- coding: utf-8 -*-
from abc import ABC, abstractmethod

class BaseTask(ABC):
    def __init__(self, task_name: str):
        self.task_name = task_name

    @abstractmethod
    def execute(self, *args, **kwargs):
        pass
