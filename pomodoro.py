#Importando as bibliotecas necessárias para o funcionamento do programa

import os
import tkinter as tk
from tkinter import ttk, PhotoImage

POMODORO = 25 * 60
SHORT_BREAK = 5 * 60
LONG_BREAK = 15 * 60
FONT = "FONT"

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
        self.s.configure("TNotebook.Tab", font=("FONT", 16))
        self.s.configure("TButton", font=("FONT", 16))

        self.tabs = ttk.Notebook(self.root)
        self.tabs.pack(fill="both", pady=10, expand=True)

        self.tab1 = ttk.Frame(self.tabs, width=600, height=100)
        self.tab2 = ttk.Frame(self.tabs, width=600, height=100)
        self.tab3 = ttk.Frame(self.tabs, width=600, height=100)

        self.pomodoro_timer_label = ttk.Label(self.tab1, text="25:00", font=("FONT", 48))
        self.pomodoro_timer_label.pack(pady=20)

        self.short_break_timer_label = ttk.Label(self.tab2, text="05:00", font=("FONT", 48))
        self.short_break_timer_label.pack(pady=20)

        self.long_break_timer_label = ttk.Label(self.tab3, text="15:00", font=("FONT", 48))
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

        self.pomodoro_counter_label = ttk.Label(self.grid_layout, text="Pomodoros: 0", font=("FONT", 16))
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
    
    def start_timer_thread(self):
        pass
    
    def start_timer(self):
        pass
    
    def reset_clock(self):
        pass
    
    def skip_clock(self):
        pass
    

if __name__ == "__main__":
    PomodoroTimer().run()

        