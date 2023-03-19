from threading import Lock
from typing import Any, Callable


class Progress:
    __slots__ = (
        "__step",
        "__total_step",
        "__progress",
        "__total_progress",
        "__description",
        "__description_template",
        "__lock",
        "__progress_hooks",
        "__complete_hooks",
    )

    def __init__(
        self,
        *,
        total_step: int = 1,
        total_progress: int = 0,
    ):
        self.__step = 1
        self.__progress = 0
        self.__total_step = total_step
        self.__total_progress = total_progress
        self.__description = ""
        self.__description_template = ""

        self.__progress_hooks = []
        self.__complete_hooks = []
        self.__lock = Lock()

    def __add__(self, value: int):
        self.progress += value
        return self

    def __sub__(self, value: int):
        self.progress -= value
        return self

    def clear_step(self):
        self.__step = 0
        self.__total_step = 1
        self._invoke_progress_hooks()

    def clear_progress(self):
        self.__progress = 0
        self.__total_progress = 0
        self._invoke_progress_hooks()

    def clear(self):
        self.clear_step()
        self.clear_progress()

    def add_progress_hook(self, hook: Callable[["Progress"], Any]):
        if hook not in self.__progress_hooks:
            with self.__lock:
                self.__progress_hooks.append(hook)

    def in_progress_hook(self, hook: Any):
        return hook in self.__progress_hooks

    def _invoke_progress_hooks(self):
        for hook in self.__progress_hooks:
            with self.__lock:
                hook(self)

    def add_complete_hook(self, hook: Callable[["Progress"], Any]):
        if hook not in self.__complete_hooks:
            with self.__lock:
                self.__complete_hooks.append(hook)

    def in_complete_hook(self, hook: Any):
        return hook in self.__complete_hooks

    def invoke_complete_hooks(self):
        for hook in self.__complete_hooks:
            with self.__lock:
                hook(self)

    @property
    def step(self):
        return max(1, self.__step)

    @property
    def total_step(self):
        return max(1, self.__total_step)

    @property
    def progress(self):
        return max(0, self.__progress)

    @property
    def total_progress(self):
        return max(0, self.__total_progress)

    @property
    def description(self):
        if self.__description_template:
            return self.__description_template.format(
                s=self.step,
                ts=self.total_step,
                p=self.progress,
                tp=self.total_progress,
            )
        return self.__description

    @property
    def description_template(self):
        return self.__description_template

    @step.setter
    def step(self, value: int):
        with self.__lock:
            self.__step = max(1, value)
            self.__progress = 0
            self.__total_progress = -1
        self._invoke_progress_hooks()

    @total_step.setter
    def total_step(self, value: int):
        with self.__lock:
            self.__total_step = max(1, value)
            self.__progress = 0
            self.__total_progress = -1
        self._invoke_progress_hooks()

    @progress.setter
    def progress(self, value: int):
        with self.__lock:
            self.__progress = value
        self._invoke_progress_hooks()

    @total_progress.setter
    def total_progress(self, value: int):
        with self.__lock:
            self.__total_progress = value
        self._invoke_progress_hooks()

    @description.setter
    def description(self, value: str):
        with self.__lock:
            self.__description = value
        self._invoke_progress_hooks()

    @description_template.setter
    def description_template(self, value: str):
        with self.__lock:
            self.__description_template = value
        self._invoke_progress_hooks()
