#Importando as bibliotecas necessárias para o funcionamento do programa

import os
import tkinter as tk
from tkinter import ttk, PhotoImage

POMODORO = 25 * 60
SHORT_BREAK = 5 * 60
LONG_BREAK = 15 * 60
FONT = "Arial"

class PomodoroTimer:
    
    def __init__(self):
        
        self.root = tk.Tk()
        self.root.geometry("600x300")
        self.root.title("Timer Pomodoro")

        # Ícone: caminho relativo ao .py; sem o .png, abre sem ícone
        try:
            caminho = os.path.join(os.path.dirname(os.path.abspath(__file__)), "pomodoro.png")
            self.icon = PhotoImage(file=caminho)
            self.root.iconphoto(True, self.icon)
        except tk.TclError:
            pass

        self.s = ttk.Style()
        self.s.configure("TNotebook.Tab", font=(FONT, 16))
        self.s.configure("TButton", font=(FONT, 16))

        self.tabs = ttk.Notebook(self.root)
        self.tabs.pack(fill="both", pady=10, expand=True)

        self.tab1 = ttk.Frame(self.tabs, width=600, height=100)
        self.tab2 = ttk.Frame(self.tabs, width=600, height=100)
        self.tab3 = ttk.Frame(self.tabs, width=600, height=100)

        self.pomodoro_timer_label = ttk.Label(self.tab1, text="25:00", font=(FONT, 48))
        self.pomodoro_timer_label.pack(pady=20)

        self.short_break_timer_label = ttk.Label(self.tab2, text="05:00", font=(FONT, 48))
        self.short_break_timer_label.pack(pady=20)

        self.long_break_timer_label = ttk.Label(self.tab3, text="15:00", font=(FONT, 48))
        self.long_break_timer_label.pack(pady=20)

        self.tabs.add(self.tab1, text="Pomodoro")
        self.tabs.add(self.tab2, text="Pausa Curta")
        self.tabs.add(self.tab3, text="Pausa Longa")

        self.grid_layout = ttk.Frame(self.root)
        self.grid_layout.pack(pady=10)

        self.start_button = ttk.Button(self.grid_layout, text="Start", command=self.start_timer)
        self.start_button.grid(row=0, column=0)

        self.skip_button = ttk.Button(self.grid_layout, text="Skip", command=self.skip_clock)
        self.skip_button.grid(row=0, column=1)

        self.reset_button = ttk.Button(self.grid_layout, text="Reset", command=self.reset_clock)
        self.reset_button.grid(row=0, column=2)

        self.pomodoro_counter_label = ttk.Label(self.grid_layout, text="Pomodoros: 0", font=(FONT, 16))
        self.pomodoro_counter_label.grid(row=1, column=0, columnspan=3, pady=10)

        # Estado do timer
        self.labels = [self.pomodoro_timer_label, self.short_break_timer_label, self.long_break_timer_label]
        self.durations = [POMODORO, SHORT_BREAK, LONG_BREAK]   # segundos
        self.pomodoros = 0
        self.phase = 0                 # 0 pomodoro, 1 pausa curta, 2 pausa longa
        self.remaining = self.durations[0]
        self.running = False
        self.after_id = None

    def run(self):
        self.root.mainloop()
    
    def start_timer(self):
        if self.running:                                  # evita duplo clique
            return
        self.phase = self.tabs.index(self.tabs.select())  # lê a aba atual (0, 1, 2)
        self.remaining = self.durations[self.phase]
        self.running = True
        self.tick()

    def tick(self):
        minutes, seconds = divmod(self.remaining, 60)
        self.labels[self.phase].config(text=f"{minutes:02d}:{seconds:02d}")
        if self.remaining > 0:
            self.remaining -= 1
            self.after_id = self.root.after(1000, self.tick)   # "me chame em 1 s"
        else:
            self.finish_phase()

    def finish_phase(self):
        if self.phase == 0:
            self.pomodoros += 1
            self.pomodoro_counter_label.config(text=f"Pomodoros: {self.pomodoros}")
            self.phase = 2 if self.pomodoros % 4 == 0 else 1   # a cada 4: pausa longa
        else:
            self.phase = 0
        self.tabs.select(self.phase)   # muda a aba
        self.running = False
        self.after_id = None
        self.start_timer()             # começa a próxima fase sozinho

    def reset_clock(self):
        if self.after_id is not None:                 # há tick agendado?
            self.root.after_cancel(self.after_id)     # cancela
            self.after_id = None
        self.running = False
        self.pomodoros = 0                            # era self.pomodros (typo)
        self.phase = 0
        self.remaining = self.durations[0]
        self.pomodoro_timer_label.config(text="25:00")
        self.short_break_timer_label.config(text="05:00")
        self.long_break_timer_label.config(text="15:00")
        self.pomodoro_counter_label.config(text="Pomodoros: 0")
        self.tabs.select(0)                           # volta p/ aba Pomodoro
            
    def skip_clock(self):
        was_running = self.running                    # lembra se estava contando
        if self.after_id is not None:
            self.root.after_cancel(self.after_id)     # cancela o tick pendente
            self.after_id = None
        self.running = False

        # fase atual: se contando, self.phase; se parado, a aba aberta
        current = self.phase if was_running else self.tabs.index(self.tabs.select())

        # restaura o relógio da fase pulada
        minutes, seconds = divmod(self.durations[current], 60)
        self.labels[current].config(text=f"{minutes:02d}:{seconds:02d}")

        # próxima fase: pomodoro -> pausa curta; qualquer pausa -> pomodoro
        self.phase = 1 if current == 0 else 0
        self.tabs.select(self.phase)

        if was_running:                               # só continua sozinho se já contava
            self.start_timer()
        
if __name__ == "__main__":
    PomodoroTimer().run()
