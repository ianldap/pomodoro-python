"""Timer Pomodoro com interface gráfica em Tkinter."""

import math
import os
import time
import tkinter as tk
from tkinter import ttk, PhotoImage

# pygame é opcional: sem ele, o alarme usa o som do sistema.
try:
    import pygame
except ImportError:
    pygame = None

# Durações em segundos.
POMODORO = 25 * 60
SHORT_BREAK = 5 * 60
LONG_BREAK = 15 * 60

FONT = "Arial"
ALARM = os.path.join(os.path.dirname(os.path.abspath(__file__)), "alarme.mp3")
POLL_INTERVAL_MS = 200  # frequência de atualização do relógio na tela


def format_time(seconds):
    """Converte segundos para o formato MM:SS."""
    minutes, seconds = divmod(seconds, 60)
    return f"{minutes:02d}:{seconds:02d}"


def init_mixer():
    """Inicializa o mixer do pygame sob demanda."""
    if pygame is None:
        return False
    try:
        if not pygame.mixer.get_init():
            pygame.mixer.init()
        return True
    except pygame.error:
        return False


class PomodoroTimer:
    """Gerencia a interface e a contagem regressiva do timer."""

    def __init__(self):
        """Monta a interface e inicializa o estado do timer."""

        self.root = tk.Tk()
        self.root.geometry("700x300")
        self.root.title("Timer Pomodoro")

        # O ícone é opcional: se a imagem não existir, a janela abre sem ele.
        try:
            caminho = os.path.join(os.path.dirname(os.path.abspath(__file__)), "pomodoro.png")
            self.icon = PhotoImage(file=caminho)
            self.root.iconphoto(True, self.icon)
        except tk.TclError:
            pass

        style = ttk.Style()
        style.configure("TNotebook.Tab", font=(FONT, 16))
        style.configure("TButton", font=(FONT, 16))

        self.tabs = ttk.Notebook(self.root)
        self.tabs.pack(fill="both", pady=10, expand=True)

        tab1 = ttk.Frame(self.tabs, width=600, height=100)
        tab2 = ttk.Frame(self.tabs, width=600, height=100)
        tab3 = ttk.Frame(self.tabs, width=600, height=100)

        self.pomodoro_timer_label = ttk.Label(tab1, text=format_time(POMODORO), font=(FONT, 48))
        self.pomodoro_timer_label.pack(pady=20)

        self.short_break_timer_label = ttk.Label(tab2, text=format_time(SHORT_BREAK), font=(FONT, 48))
        self.short_break_timer_label.pack(pady=20)

        self.long_break_timer_label = ttk.Label(tab3, text=format_time(LONG_BREAK), font=(FONT, 48))
        self.long_break_timer_label.pack(pady=20)

        self.tabs.add(tab1, text="Pomodoro")
        self.tabs.add(tab2, text="Pausa Curta")
        self.tabs.add(tab3, text="Pausa Longa")

        controls = ttk.Frame(self.root)
        controls.pack(pady=10)

        start_button = ttk.Button(controls, text="Start", command=self.start_timer)
        start_button.grid(row=0, column=0)

        self.pause_button = ttk.Button(controls, text="Pause", command=self.pause_timer)
        self.pause_button.grid(row=0, column=1)

        skip_button = ttk.Button(controls, text="Skip", command=self.skip_clock)
        skip_button.grid(row=0, column=2)

        self.pomodoro_counter_label = ttk.Label(controls, text="Pomodoros: 0", font=(FONT, 16))
        self.pomodoro_counter_label.grid(row=1, column=0, columnspan=3, pady=10)

        # Estado do timer.
        self.labels = [
            self.pomodoro_timer_label,
            self.short_break_timer_label,
            self.long_break_timer_label,
        ]
        self.durations = [POMODORO, SHORT_BREAK, LONG_BREAK]
        self.pomodoros = 0
        self.phase = 0  # 0 = pomodoro, 1 = pausa curta, 2 = pausa longa
        self.remaining = self.durations[0]
        self.deadline = None
        self.running = False
        self.paused = False
        self.after_id = None

    def start_timer(self):
        """Inicia a contagem da aba atual ou retoma uma contagem pausada."""
        if self.running:
            return
        if self.paused:
            self.resume_timer()
            return

        self.phase = self.tabs.index(self.tabs.select())
        self.remaining = self.durations[self.phase]
        self.deadline = time.monotonic() + self.remaining
        self.running = True
        self.tick()

    def tick(self):
        """Atualiza o relógio na tela e agenda a próxima atualização."""
        self.remaining = max(0, math.ceil(self.deadline - time.monotonic()))
        self.labels[self.phase].config(text=format_time(self.remaining))

        if self.remaining > 0:
            self.after_id = self.root.after(POLL_INTERVAL_MS, self.tick)
        else:
            self.finish_phase()

    def finish_phase(self):
        """Notifica o fim da etapa e inicia automaticamente a próxima."""
        self.notify()

        if self.phase == 0:
            self.pomodoros += 1
            self.pomodoro_counter_label.config(text=f"Pomodoros: {self.pomodoros}")
            # A cada quatro pomodoros, a pausa é longa.
            self.phase = 2 if self.pomodoros % 4 == 0 else 1
        else:
            self.phase = 0

        self.tabs.select(self.phase)
        self.running = False
        self.after_id = None
        self.start_timer()

    def pause_timer(self):
        """Pausa a contagem ou retoma se já estiver pausada."""
        if self.running:
            if self.after_id is not None:
                self.root.after_cancel(self.after_id)
                self.after_id = None

            self.remaining = max(0.0, self.deadline - time.monotonic())
            self.running = False
            self.paused = True
            self.pause_button.config(text="Resume")
        elif self.paused:
            self.resume_timer()

    def resume_timer(self):
        """Continua a contagem de onde ela parou."""
        self.paused = False
        self.pause_button.config(text="Pause")
        self.deadline = time.monotonic() + self.remaining
        self.running = True
        self.tick()

    def notify(self):
        """Exibe o aviso de fim de etapa e controla o alarme."""
        self.play_alarm()
        texto = ("Pomodoro concluído! Hora da pausa." if self.phase == 0
                 else "Pausa terminou! Hora de focar.")

        win = tk.Toplevel(self.root)
        win.title("Pomodoro")
        win.geometry("350x140")
        win.transient(self.root)
        ttk.Label(win, text=texto, font=(FONT, 14)).pack(pady=20)
        ttk.Button(win, text="OK", command=win.destroy).pack()
        win.lift()
        win.focus_force()
        win.grab_set()
        self.root.wait_window(win)
        self.stop_alarm()

    def play_alarm(self):
        """Toca o alarme em repetição ou, em caso de falha, o som do sistema."""
        if init_mixer() and os.path.exists(ALARM):
            try:
                pygame.mixer.music.load(ALARM)
                pygame.mixer.music.set_volume(1.0)
                pygame.mixer.music.play(loops=-1)
                return
            except pygame.error:
                pass

        try:
            import winsound
            winsound.MessageBeep()
        except Exception:
            self.root.bell()

    def stop_alarm(self):
        """Interrompe o alarme."""
        if pygame is not None and pygame.mixer.get_init():
            pygame.mixer.music.stop()

    def skip_clock(self):
        """Avança para a próxima etapa sem esperar o fim da contagem."""
        self.paused = False
        self.pause_button.config(text="Pause")
        was_running = self.running

        if self.after_id is not None:
            self.root.after_cancel(self.after_id)
            self.after_id = None
        self.running = False

        current = self.phase if was_running else self.tabs.index(self.tabs.select())

        # Restaura o relógio da etapa que foi pulada.
        self.labels[current].config(text=format_time(self.durations[current]))

        # Pomodoro avança para pausa curta; pausas voltam para o pomodoro.
        self.phase = 1 if current == 0 else 0
        self.tabs.select(self.phase)

        if was_running:
            self.start_timer()
        
    def run(self):
        """Inicia o loop principal da interface."""
        self.root.mainloop()


if __name__ == "__main__":
    PomodoroTimer().run()
