import tkinter as tk
import random

BG      = "#070e1a"
CARD    = "#0c1729"
SURFACE = "#111f35"
ACCENT  = "#00d4e8"
DIM     = "#1a2d4a"
TEXT    = "#e8f4f8"
TEXT2   = "#5a8a9f"
TEXT3   = "#1e3a52"
GREEN   = "#00e5a0"
RED     = "#ff4d6d"
ORANGE  = "#ff8c42"
YELLOW  = "#ffd166"

DIFF = {"Easy":(1,50,10),"Medium":(1,100,7),"Hard":(1,200,5)}

class GuessingGame(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Number Guessing Game")
        self.geometry("440x640")
        self.configure(bg=BG)
        self.resizable(False,False)
        self.diff     = "Medium"
        self.secret   = 0
        self.attempts = 0
        self.max_att  = 7
        self.lo = self.hi = 0
        self.over     = False
        self.best     = None
        self._ui()
        self._new_game()

    def _ui(self):
        # header
        h = tk.Frame(self, bg=BG)
        h.pack(fill="x", padx=28, pady=(24,0))
        tk.Label(h, text="Number", bg=BG, fg=TEXT2,
                 font=("SF Pro Display","12")).pack(side="left")
        tk.Label(h, text=" Guessing Game", bg=BG, fg=TEXT,
                 font=("SF Pro Display","12","bold")).pack(side="left")

        # big target display
        self.display_frame = tk.Frame(self, bg=CARD, height=130)
        self.display_frame.pack(fill="x", padx=28, pady=(20,0))
        self.display_frame.pack_propagate(False)
        self.big_icon = tk.Label(self.display_frame, text="?", bg=CARD, fg=ACCENT,
                                  font=("SF Pro Display","64","bold"))
        self.big_icon.place(relx=.5, rely=.38, anchor="center")
        self.sub_msg = tk.Label(self.display_frame, text="A secret number awaits...", bg=CARD,
                                 fg=TEXT2, font=("SF Pro Display","11"))
        self.sub_msg.place(relx=.5, rely=.78, anchor="center")

        # difficulty
        dr = tk.Frame(self, bg=BG)
        dr.pack(pady=(16,0))
        tk.Label(dr, text="DIFFICULTY", bg=BG, fg=TEXT3,
                 font=("SF Pro Display","8")).pack(side="left", padx=(0,12))
        self.d_btns = {}
        for name in DIFF:
            b = tk.Button(dr, text=name, bg=DIM, fg=TEXT2,
                          font=("SF Pro Display","9"), bd=0,
                          padx=12, pady=5, cursor="hand2", relief="flat",
                          command=lambda n=name: self._set_diff(n))
            b.pack(side="left", padx=3)
            self.d_btns[name] = b

        # stat row
        st = tk.Frame(self, bg=BG)
        st.pack(fill="x", padx=28, pady=(14,0))
        st.columnconfigure((0,1,2), weight=1)
        self.stat_lbls = {}
        for i,(title,key,col) in enumerate([("RANGE","range",ACCENT),
                                             ("ATTEMPTS LEFT","left",YELLOW),
                                             ("BEST","best",GREEN)]):
            f = tk.Frame(st, bg=CARD, padx=12, pady=8)
            f.grid(row=0,column=i,sticky="nsew",padx=(0 if i==0 else 8,0))
            tk.Label(f,text=title,bg=CARD,fg=TEXT3,font=("SF Pro Display","8")).pack()
            l = tk.Label(f,text="—",bg=CARD,fg=col,font=("SF Pro Display","15","bold"))
            l.pack()
            self.stat_lbls[key] = l

        # progress bar
        self.prog_c = tk.Canvas(self, height=4, bg=BG, highlightthickness=0)
        self.prog_c.pack(fill="x", padx=28, pady=(12,0))

        # input
        inp = tk.Frame(self, bg=CARD, padx=20, pady=14)
        inp.pack(fill="x", padx=28, pady=(14,0))
        tk.Label(inp,text="YOUR GUESS",bg=CARD,fg=TEXT3,font=("SF Pro Display","8")).pack(anchor="w")
        row = tk.Frame(inp, bg=CARD)
        row.pack(fill="x", pady=(6,0))
        self.guess_var = tk.StringVar()
        e = tk.Entry(row, textvariable=self.guess_var, bg=CARD, fg=TEXT,
                     insertbackground=ACCENT, font=("SF Pro Display","26","bold"),
                     bd=0, highlightthickness=0, width=10)
        e.pack(side="left")
        e.bind("<Return>", lambda _: self._submit())
        tk.Button(row, text="→", bg=ACCENT, fg=BG,
                  font=("SF Pro Display","16","bold"), bd=0, padx=14, pady=4,
                  cursor="hand2", relief="flat", command=self._submit).pack(side="right")

        # new game
        tk.Button(self, text="New Game", bg=DIM, fg=TEXT2,
                  font=("SF Pro Display","10"), bd=0, padx=16, pady=6,
                  cursor="hand2", relief="flat", command=self._new_game).pack(pady=(12,0))

        # history
        tk.Label(self, text="HISTORY", bg=BG, fg=TEXT3,
                 font=("SF Pro Display","8")).pack(anchor="w", padx=28, pady=(14,4))
        self.hist_frame = tk.Frame(self, bg=BG)
        self.hist_frame.pack(fill="x", padx=28)

        tk.Label(self, text="Task 02  ·  Software Engineering Intern",
                 bg=BG, fg=TEXT3, font=("SF Pro Display","8")).pack(side="bottom", pady=10)

    def _set_diff(self, name):
        self.diff = name
        self._new_game()

    def _hl_diff(self):
        for n,b in self.d_btns.items():
            b.config(bg=ACCENT if n==self.diff else DIM,
                     fg=BG    if n==self.diff else TEXT2)

    def _new_game(self):
        self.lo, self.hi, self.max_att = DIFF[self.diff]
        self.secret   = random.randint(self.lo, self.hi)
        self.attempts = 0
        self.over     = False
        self.history  = []
        self._hl_diff()
        self.guess_var.set("")
        self.big_icon.config(text="?", fg=ACCENT)
        self.sub_msg.config(text=f"Guess a number between {self.lo} and {self.hi}", fg=TEXT2)
        self.display_frame.config(bg=CARD)
        self.big_icon.config(bg=CARD)
        self.sub_msg.config(bg=CARD)
        self.stat_lbls["range"].config(text=f"{self.lo}–{self.hi}")
        self.stat_lbls["left"].config(text=str(self.max_att))
        self.stat_lbls["best"].config(text=str(self.best) if self.best else "—")
        self._draw_prog()
        self._refresh_hist()

    def _submit(self):
        if self.over: return
        raw = self.guess_var.get().strip()
        if not raw.lstrip("-").isdigit():
            self.sub_msg.config(text="Enter a valid number", fg=ORANGE)
            return
        g = int(raw)
        if not (self.lo <= g <= self.hi):
            self.sub_msg.config(text=f"Must be between {self.lo}–{self.hi}", fg=ORANGE)
            return
        self.attempts += 1
        rem = self.max_att - self.attempts
        diff = abs(g - self.secret)

        if g == self.secret:
            self.history.append((g,"✓"))
            self.big_icon.config(text=str(g), fg=GREEN)
            self.sub_msg.config(text=f"Correct! Solved in {self.attempts} attempt{'s' if self.attempts>1 else ''}  🎉", fg=GREEN)
            self.over = True
            if self.best is None or self.attempts < self.best:
                self.best = self.attempts
                self.stat_lbls["best"].config(text=str(self.best))
        elif rem == 0:
            self.history.append((g,"✗"))
            self.big_icon.config(text=str(self.secret), fg=RED)
            self.sub_msg.config(text=f"Game over — the number was {self.secret}", fg=RED)
            self.over = True
        else:
            arrow = "↑ Too low" if g < self.secret else "↓ Too high"
            if diff<=5:      warm="Very hot 🔥"
            elif diff<=15:   warm="Warm ♨️"
            elif diff<=30:   warm="Cold 🌊"
            else:            warm="Freezing 🧊"
            self.history.append((g,"↑" if g<self.secret else "↓"))
            self.big_icon.config(text=str(g), fg=YELLOW)
            self.sub_msg.config(text=f"{arrow}  ·  {warm}  ·  {rem} left", fg=TEXT2)

        self.stat_lbls["left"].config(text=str(max(0, self.max_att-self.attempts)))
        self.guess_var.set("")
        self._draw_prog()
        self._refresh_hist()

    def _draw_prog(self):
        self.prog_c.update_idletasks()
        w = self.prog_c.winfo_width() or 380
        self.prog_c.delete("all")
        self.prog_c.create_rectangle(0,0,w,4,fill=DIM,outline="")
        if self.max_att:
            p = self.attempts/self.max_att
            col = GREEN if p<.5 else ORANGE if p<.8 else RED
            self.prog_c.create_rectangle(0,0,int(w*p),4,fill=col,outline="")

    def _refresh_hist(self):
        for w in self.hist_frame.winfo_children(): w.destroy()
        for g,icon in reversed(self.history[-5:]):
            r = tk.Frame(self.hist_frame, bg=SURFACE, padx=12, pady=5)
            r.pack(fill="x", pady=2)
            col = GREEN if icon=="✓" else RED if icon=="✗" else YELLOW
            tk.Label(r, text=str(g), bg=SURFACE, fg=TEXT,
                     font=("SF Pro Display","11")).pack(side="left")
            tk.Label(r, text=icon, bg=SURFACE, fg=col,
                     font=("SF Pro Display","11","bold")).pack(side="right")

if __name__=="__main__":
    GuessingGame().mainloop()
