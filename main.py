import queue
import tkinter as tk
from tkinter import ttk

import keyboard


APP_TITLE = "Key Pressed"
MAX_KEYS = 10
KEY_REPEAT_INTERVAL_MS = 50
KEY_OPTIONS = [""] + list("abcdefghijklmnopqrstuvwxyz0123456789") + [
    "space",
    "enter",
    "tab",
    "esc",
    "backspace",
    "shift",
    "ctrl",
    "alt",
    "up",
    "down",
    "left",
    "right",
] + [f"f{number}" for number in range(1, 13)]


class KeyPressedApp:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title(APP_TITLE)
        self.root.resizable(False, False)
        self.root.protocol("WM_DELETE_WINDOW", self.close)

        self.active = False
        self.held_keys: set[str] = set()
        self.events: queue.Queue[str] = queue.Queue()
        self.key_vars = [tk.StringVar() for _ in range(MAX_KEYS)]
        self.status_var = tk.StringVar(value="Deshabilitado")

        self._build_ui()
        self._register_hotkeys()
        self.root.after(KEY_REPEAT_INTERVAL_MS, self._process_events)

    def _build_ui(self) -> None:
        frame = ttk.Frame(self.root, padding=18)
        frame.grid()

        ttk.Label(frame, text="Teclas sostenidas", font=("Segoe UI", 15, "bold")).grid(
            row=0, column=0, columnspan=4, sticky="w"
        )
        ttk.Label(
            frame,
            text="Elige hasta 10 teclas. Se mantendran presionadas mientras este habilitado.",
        ).grid(row=1, column=0, columnspan=4, sticky="w", pady=(4, 14))

        for index, key_var in enumerate(self.key_vars):
            column = (index // 5) * 2
            row = 2 + (index % 5)
            ttk.Label(frame, text=f"{index + 1:02d}").grid(
                row=row, column=column, sticky="e", padx=(0, 8), pady=4
            )
            selector = ttk.Combobox(
                frame,
                textvariable=key_var,
                values=KEY_OPTIONS,
                state="readonly",
                width=15,
            )
            selector.grid(row=row, column=column + 1, sticky="ew", padx=(0, 16), pady=4)
            selector.bind("<<ComboboxSelected>>", self._selection_changed)

        ttk.Separator(frame).grid(row=7, column=0, columnspan=4, sticky="ew", pady=(12, 10))
        ttk.Label(frame, text="Estado:").grid(row=8, column=0, sticky="w")
        ttk.Label(frame, textvariable=self.status_var, font=("Segoe UI", 10, "bold")).grid(
            row=8, column=1, columnspan=3, sticky="w"
        )

        buttons = ttk.Frame(frame)
        buttons.grid(row=9, column=0, columnspan=4, sticky="ew", pady=(12, 0))
        ttk.Button(buttons, text="Habilitar  Ctrl+F12", command=self.enable).pack(
            side="left", padx=(0, 8)
        )
        ttk.Button(buttons, text="Deshabilitar  Ctrl+F10", command=self.disable).pack(
            side="left"
        )

    def _register_hotkeys(self) -> None:
        keyboard.add_hotkey(
            "ctrl+f10", lambda: self.events.put("disable"), suppress=True
        )
        keyboard.add_hotkey(
            "ctrl+f12", lambda: self.events.put("enable"), suppress=True
        )

    def _selected_keys(self) -> set[str]:
        return {value for variable in self.key_vars if (value := variable.get())}

    def _selection_changed(self, _event: tk.Event) -> None:
        if self.active:
            self._sync_held_keys()

    def _sync_held_keys(self) -> None:
        desired_keys = self._selected_keys() if self.active else set()
        for key in self.held_keys - desired_keys:
            keyboard.release(key)
        for key in desired_keys - self.held_keys:
            keyboard.press(key)
        self.held_keys = desired_keys

    def enable(self) -> None:
        self.active = True
        self.status_var.set("Habilitado")
        self._sync_held_keys()

    def disable(self) -> None:
        self.active = False
        self.status_var.set("Deshabilitado")
        self._sync_held_keys()

    def _process_events(self) -> None:
        while True:
            try:
                action = self.events.get_nowait()
            except queue.Empty:
                break
            if action == "enable":
                self.enable()
            else:
                self.disable()
        if self.active:
            for key in self.held_keys:
                keyboard.press(key)
        self.root.after(KEY_REPEAT_INTERVAL_MS, self._process_events)

    def close(self) -> None:
        self.disable()
        keyboard.unhook_all_hotkeys()
        self.root.destroy()


def main() -> None:
    root = tk.Tk()
    KeyPressedApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()