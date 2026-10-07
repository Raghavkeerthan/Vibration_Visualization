import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from scipy.integrate import solve_ivp
import tkinter as tk
from tkinter import ttk

# ============================================================
# MASS-SPRING-DAMPER SIMULATOR (Core Physics)
# ============================================================
class VibrationSimulator:
    def __init__(self, m, k, c):
        self.m = m
        self.k = k
        self.c = c

    def simulate(self, F0=0, omega=0, x0=0, v0=0, t_end=20, n_points=1000):
        t = np.linspace(0, t_end, n_points)

        def ode(t, y):
            x = y[0]
            v = y[1]
            F = F0 * np.sin(omega * t)
            acceleration = (F - self.c * v - self.k * x) / self.m
            return [v, acceleration]

        # ENHANCED ACCURACY: Tightened tolerances and forced a maximum step size
        max_step_size = t_end / (n_points / 2)
        solution = solve_ivp(
            ode, [0, t_end], [x0, v0], 
            t_eval=t, 
            rtol=1e-8, 
            atol=1e-10, 
            max_step=max_step_size
        )
        return solution.t, solution.y[0], solution.y[1]


# ============================================================
# GUI APPLICATION
# ============================================================
class VibrationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Mass-Spring-Damper Simulator (Reactive & Accurate)")
        self.root.geometry("1150x800")
        
        # Simulation State
        self.is_playing = False
        self.t_data = []
        self.x_data = []
        self.current_frame = 0
        self.max_frames = 0
        self.anim_speed_ms = 20
        self.after_id = None
        self.preset_loading = False 
        
        self.setup_vars()
        self.setup_ui()
        self.apply_presets() 
        
    def setup_vars(self):
        """Initialize Tkinter variables to trace inputs."""
        self.case_var = tk.StringVar(value="1. Free vibration - Mass + Spring")
        self.m_var = tk.StringVar()
        self.k_var = tk.StringVar()
        
        self.damp_mode = tk.IntVar(value=1)
        self.damp_val_var = tk.StringVar()
        
        self.F0_var = tk.StringVar()
        self.freq_mode = tk.IntVar(value=1)
        self.freq_val_var = tk.StringVar()
        
        self.x0_var = tk.StringVar()
        self.v0_var = tk.StringVar()
        self.t_end_var = tk.StringVar()
        
        for var in [self.m_var, self.k_var, self.damp_mode, self.damp_val_var, 
                    self.F0_var, self.freq_mode, self.freq_val_var, self.x0_var, self.v0_var, self.t_end_var]:
            var.trace_add("write", self.on_input_change)

    def setup_ui(self):
        # 1. Left Control Panel
        control_frame = ttk.Frame(self.root, padding=10)
        control_frame.pack(side=tk.LEFT, fill=tk.Y)
        
        ttk.Label(control_frame, text="Vibration Settings", font=("Helvetica", 14, "bold")).pack(pady=(0, 10))
        
        ttk.Label(control_frame, text="Select Case:").pack(anchor=tk.W)
        cases = [
            "1. Free vibration - Mass + Spring",
            "2. Free vibration - Critical damping",
            "3. Free vibration - Underdamping",
            "4. Free vibration - Overdamping",
            "5. Forced - Spring+Mass - Below wn",
            "6. Forced - Spring+Mass - Above wn",
            "7. Forced - Damped - Below wn",
            "8. Forced - Damped - Above wn",
            "9. Custom vibration problem (Resonance Demo)"
        ]
        self.case_menu = ttk.Combobox(control_frame, textvariable=self.case_var, values=cases, width=38, state="readonly")
        self.case_menu.pack(pady=5)
        self.case_menu.bind("<<ComboboxSelected>>", self.apply_presets)
        
        # --- System Inputs ---
        sys_frame = ttk.LabelFrame(control_frame, text="System Parameters", padding=5)
        sys_frame.pack(fill=tk.X, pady=5)
        
        self.create_entry(sys_frame, "Mass m (kg):", self.m_var)
        self.create_entry(sys_frame, "Stiffness k (N/m):", self.k_var)
        
        damp_toggle_row = ttk.Frame(sys_frame)
        damp_toggle_row.pack(fill=tk.X, pady=2)
        self.lbl_damp = ttk.Label(damp_toggle_row, text="Damping Mode:", width=20)
        self.lbl_damp.pack(side=tk.LEFT)
        self.rb_zeta = ttk.Radiobutton(damp_toggle_row, text="Ratio(ζ)", variable=self.damp_mode, value=1)
        self.rb_zeta.pack(side=tk.LEFT, padx=(0, 5))
        self.rb_c = ttk.Radiobutton(damp_toggle_row, text="Coeff(c)", variable=self.damp_mode, value=2)
        self.rb_c.pack(side=tk.LEFT)
        
        damp_val_row = ttk.Frame(sys_frame)
        damp_val_row.pack(fill=tk.X, pady=2)
        ttk.Label(damp_val_row, text="Damping Value:", width=20).pack(side=tk.LEFT)
        self.damp_entry = ttk.Entry(damp_val_row, textvariable=self.damp_val_var, width=12)
        self.damp_entry.pack(side=tk.RIGHT)
        
        # --- Forcing Inputs ---
        force_frame = ttk.LabelFrame(control_frame, text="Forcing Parameters", padding=5)
        force_frame.pack(fill=tk.X, pady=5)
        
        self.create_entry(force_frame, "Force Amp F0 (N):", self.F0_var, entry_ref="f0_entry")
        
        freq_toggle_row = ttk.Frame(force_frame)
        freq_toggle_row.pack(fill=tk.X, pady=2)
        self.lbl_freq = ttk.Label(freq_toggle_row, text="Freq Mode:", width=20)
        self.lbl_freq.pack(side=tk.LEFT)
        self.rb_r = ttk.Radiobutton(freq_toggle_row, text="Ratio(r)", variable=self.freq_mode, value=1)
        self.rb_r.pack(side=tk.LEFT, padx=(0, 5))
        self.rb_hz = ttk.Radiobutton(freq_toggle_row, text="Hz(f)", variable=self.freq_mode, value=2)
        self.rb_hz.pack(side=tk.LEFT)
        
        freq_val_row = ttk.Frame(force_frame)
        freq_val_row.pack(fill=tk.X, pady=2)
        ttk.Label(freq_val_row, text="Freq Value:", width=20).pack(side=tk.LEFT)
        self.freq_entry = ttk.Entry(freq_val_row, textvariable=self.freq_val_var, width=12)
        self.freq_entry.pack(side=tk.RIGHT)
        
        # --- Initial Conditions ---
        ic_frame = ttk.LabelFrame(control_frame, text="Initial Conditions", padding=5)
        ic_frame.pack(fill=tk.X, pady=5)
        self.create_entry(ic_frame, "Initial Disp x0 (m):", self.x0_var)
        self.create_entry(ic_frame, "Initial Vel v0 (m/s):", self.v0_var)
        self.create_entry(ic_frame, "Sim Time t_end (s):", self.t_end_var)

        # Buttons
        btn_frame = ttk.Frame(control_frame)
        btn_frame.pack(pady=10, fill=tk.X)
        self.btn_play = ttk.Button(btn_frame, text="Play / Resume", command=self.play_simulation)
        self.btn_play.pack(fill=tk.X, pady=2)
        self.btn_pause = ttk.Button(btn_frame, text="Pause", command=self.pause_simulation, state=tk.DISABLED)
        self.btn_pause.pack(fill=tk.X, pady=2)
        self.btn_reset = ttk.Button(btn_frame, text="Reset to Start", command=self.reset_simulation)
        self.btn_reset.pack(fill=tk.X, pady=2)
        
        # --- System Properties Panel ---
        props_frame = ttk.LabelFrame(control_frame, text="System Properties & Status", padding=10)
        props_frame.pack(fill=tk.X, pady=10)
        self.lbl_sys_info = ttk.Label(props_frame, text="Waiting for valid input...", font=("Consolas", 10), justify=tk.LEFT)
        self.lbl_sys_info.pack(anchor=tk.W)
        self.lbl_live_stats = ttk.Label(props_frame, text="Time: 0.000 s\nDisp: +0.0000 m", font=("Consolas", 10, "bold"), foreground="blue", justify=tk.LEFT)
        self.lbl_live_stats.pack(anchor=tk.W, pady=(10, 0))

        # 2. Right Visualization Panel
        viz_frame = ttk.Frame(self.root)
        viz_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        self.canvas = tk.Canvas(viz_frame, height=180, bg="white", highlightthickness=1, highlightbackground="black")
        self.canvas.pack(fill=tk.X, padx=10, pady=10)
        
        self.fig, self.ax = plt.subplots(figsize=(6, 4), dpi=100)
        self.ax.set_xlabel("Time (s)")
        self.ax.set_ylabel("Displacement x (m)")
        self.ax.grid(True)
        self.line, = self.ax.plot([], [], lw=2, color='blue')
        self.point, = self.ax.plot([], [], 'ro')
        
        self.plot_canvas = FigureCanvasTkAgg(self.fig, master=viz_frame)
        self.plot_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        self.c_active = 0
        self.F0_active = 0
        self.omega_active = 0
        self.draw_environment(0, 0.0)

    def create_entry(self, parent, label, text_var, entry_ref=None):
        frame = ttk.Frame(parent)
        frame.pack(fill=tk.X, pady=2)
        ttk.Label(frame, text=label, width=20).pack(side=tk.LEFT)
        entry = ttk.Entry(frame, textvariable=text_var, width=12)
        entry.pack(side=tk.RIGHT)
        if entry_ref:
            setattr(self, entry_ref, entry)

    def apply_presets(self, event=None):
        """Injects perfect example values based on the chosen case."""
        self.preset_loading = True 
        case_index = int(self.case_var.get()[0])
        
        # Standard Baseline
        self.m_var.set("10.0")
        self.k_var.set("100.0")
        self.damp_val_var.set("0.0")
        self.F0_var.set("0.0")
        self.freq_val_var.set("0.0")
        self.x0_var.set("1.0")
        self.v0_var.set("0.0")
        self.t_end_var.set("10.0")
        
        if case_index == 3: # Underdamped
            self.damp_mode.set(1)
            self.damp_val_var.set("0.1")
        elif case_index == 4: # Overdamped
            self.damp_mode.set(1)
            self.damp_val_var.set("2.0")
        elif case_index == 5: # Forced Below wn
            self.F0_var.set("20.0")
            self.freq_mode.set(1)
            self.freq_val_var.set("0.5")
            self.x0_var.set("0.0")
        elif case_index == 6: # Forced Above wn
            self.F0_var.set("20.0")
            self.freq_mode.set(1)
            self.freq_val_var.set("2.0")
            self.x0_var.set("0.0")
        elif case_index == 7: # Forced Damped Below wn
            self.damp_mode.set(1)
            self.damp_val_var.set("0.15")
            self.F0_var.set("50.0")
            self.freq_mode.set(1)
            self.freq_val_var.set("0.5")
            self.x0_var.set("0.0")
        elif case_index == 8: # Forced Damped Above wn
            self.damp_mode.set(1)
            self.damp_val_var.set("0.15")
            self.F0_var.set("50.0")
            self.freq_mode.set(1)
            self.freq_val_var.set("2.0")
            self.x0_var.set("0.0")
        elif case_index == 9: # Pure Resonance Demo
            self.damp_mode.set(1)
            self.damp_val_var.set("0.0")
            self.F0_var.set("10.0")
            self.freq_mode.set(1)
            self.freq_val_var.set("1.0") 
            self.x0_var.set("0.0")       
            self.t_end_var.set("30.0")   
            
        self.preset_loading = False
        self.update_ui_state()
        self.calculate_simulation()

    def on_input_change(self, *args):
        if self.preset_loading: return
        self.update_ui_state()
        if self.after_id:
            self.root.after_cancel(self.after_id)
        self.after_id = self.root.after(300, self.calculate_simulation)

    def update_ui_state(self):
        case_index = int(self.case_var.get()[0])
        damp_state = tk.NORMAL
        force_state = tk.NORMAL
        
        if case_index in [1, 2]:
            damp_state = tk.DISABLED
            force_state = tk.DISABLED
        elif case_index in [3, 4]:
            force_state = tk.DISABLED
        elif case_index in [5, 6]:
            damp_state = tk.DISABLED
            
        self.rb_zeta.config(state=damp_state)
        self.rb_c.config(state=damp_state)
        self.damp_entry.config(state=damp_state)
        
        if hasattr(self, 'f0_entry'):
            self.f0_entry.config(state=force_state)
        self.rb_r.config(state=force_state)
        self.rb_hz.config(state=force_state)
        self.freq_entry.config(state=force_state)

    def get_val(self, var):
        try:
            return float(var.get())
        except ValueError:
            return 0.0

    def draw_environment(self, x_disp, t_val=0.0):
        self.canvas.delete("all")
        base_x = 350
        mass_x = base_x + (x_disp * getattr(self, 'px_scale', 100))
        
        # Equilibrium line (x=0)
        self.canvas.create_line(base_x, 20, base_x, 160, dash=(4, 4), fill="gray", width=1.5)
        self.canvas.create_text(base_x, 10, text="x = 0", fill="black", font=("Arial", 10))
        
        # Wall
        self.canvas.create_rectangle(10, 20, 30, 160, fill="gray")
        
        # Spring
        self.canvas.create_line(30, 65, mass_x - 30, 65, dash=(4, 4), fill="blue", width=2)
        
        # Damper
        if getattr(self, 'c_active', 0) > 0:
            self.canvas.create_line(30, 115, 120, 115, width=2)
            self.canvas.create_line(120, 100, 120, 130, width=2)
            self.canvas.create_line(120, 100, 220, 100, width=2)
            self.canvas.create_line(120, 130, 220, 130, width=2)
            piston_head_x = mass_x - 180
            self.canvas.create_line(mass_x - 30, 115, piston_head_x, 115, width=2)
            self.canvas.create_line(piston_head_x, 105, piston_head_x, 125, width=4)
            
        # Mass
        self.canvas.create_rectangle(mass_x - 30, 45, mass_x + 30, 135, fill="indianred", outline="black")
        self.canvas.create_text(mass_x, 90, text="m", font=("Arial", 14, "bold"), fill="white")
        
        # Live Force Vector Arrow
        if getattr(self, 'F0_active', 0) > 0:
            current_f = self.F0_active * np.sin(getattr(self, 'omega_active', 0) * t_val)
            if abs(current_f) > 0.05 * self.F0_active: # Prevent tiny jittering arrows when near zero
                max_arrow_len = 75
                arrow_dx = max_arrow_len * (current_f / self.F0_active)
                
                self.canvas.create_line(mass_x, 30, mass_x + arrow_dx, 30, arrow=tk.LAST, fill="darkorange", width=3)
                
                # Dynamic text offset
                text_x = mass_x + arrow_dx + (15 if arrow_dx > 0 else -15)
                self.canvas.create_text(text_x, 30, text="F(t)", fill="darkorange", font=("Arial", 10, "bold"))

    def calculate_simulation(self):
        try:
            case_index = int(self.case_var.get()[0])
            m, k, t_end = self.get_val(self.m_var), self.get_val(self.k_var), self.get_val(self.t_end_var)
            
            if m <= 0 or k <= 0 or t_end <= 0:
                self.lbl_sys_info.config(text="Error: m, k, t_end must be > 0", foreground="red")
                return

            wn = np.sqrt(k / m)
            fn = wn / (2 * np.pi)
            cc = 2 * np.sqrt(k * m)
            damp_val, freq_val = self.get_val(self.damp_val_var), self.get_val(self.freq_val_var)
            c, F0, omega = 0, 0, 0
            
            if case_index in [3, 4, 7, 8, 9]:
                c = damp_val * cc if self.damp_mode.get() == 1 else damp_val
            elif case_index == 2:
                c = cc
                
            if case_index in [5, 6, 7, 8, 9]:
                F0 = self.get_val(self.F0_var)
                omega = freq_val * wn if self.freq_mode.get() == 1 else 2 * np.pi * freq_val

            self.c_active = c
            self.F0_active = F0
            self.omega_active = omega
            
            zeta = c / cc if cc > 0 else 0
            sys_type = "Undamped" if c == 0 else "Underdamped" if zeta < 1 else "Critically Damped" if np.isclose(zeta, 1) else "Overdamped"

            info = f"ωn = {wn:.3f} rad/s\nfn = {fn:.3f} Hz\ncc = {cc:.3f} Ns/m\nζ  = {zeta:.4f} ({sys_type})\n"
            if F0 > 0: info += f"r  = {(omega/wn) if wn > 0 else 0:.4f} (Forced)\n"
            self.lbl_sys_info.config(text=info, foreground="black")

            n_points = int(t_end * 50) 
            sim = VibrationSimulator(m=m, k=k, c=c)
            self.t_data, self.x_data, _ = sim.simulate(F0=F0, omega=omega, 
                                                       x0=self.get_val(self.x0_var), 
                                                       v0=self.get_val(self.v0_var), 
                                                       t_end=t_end, n_points=n_points)
            
            self.max_frames = len(self.t_data)
            max_disp = max(max(abs(self.x_data)), 0.01)
            self.px_scale = 100.0 / max_disp 
            
            self.ax.set_xlim(0, t_end)
            self.ax.set_ylim(-max_disp * 1.2, max_disp * 1.2)
            self.line.set_data([], [])
            self.point.set_data([], [])
            self.plot_canvas.draw()
            
            if not self.is_playing:
                self.current_frame = 0
                self.update_frame(force_update=True)
            
        except Exception:
            self.lbl_sys_info.config(text="Parsing Error. Check Inputs.", foreground="red")

    def update_frame(self, force_update=False):
        if self.current_frame >= self.max_frames:
            self.pause_simulation()
            return
            
        t_val = self.t_data[self.current_frame]
        x_val = self.x_data[self.current_frame]
        
        self.lbl_live_stats.config(text=f"Time: {t_val:.3f} s\nDisp: {x_val:+.4f} m")
        self.draw_environment(x_val, t_val)
        
        self.line.set_data(self.t_data[:self.current_frame], self.x_data[:self.current_frame])
        self.point.set_data([t_val], [x_val])
        self.plot_canvas.draw_idle()
        
        if self.is_playing:
            self.current_frame += 1
            self.root.after(self.anim_speed_ms, self.update_frame)
            
    def play_simulation(self):
        if not self.is_playing:
            self.is_playing = True
            self.btn_play.config(state=tk.DISABLED)
            self.btn_pause.config(state=tk.NORMAL)
            if self.current_frame >= self.max_frames - 1: self.current_frame = 0
            self.update_frame()

    def pause_simulation(self):
        self.is_playing = False
        self.btn_play.config(state=tk.NORMAL)
        self.btn_pause.config(state=tk.DISABLED)

    def reset_simulation(self):
        self.pause_simulation()
        self.current_frame = 0
        self.update_frame(force_update=True)

if __name__ == "__main__":
    root = tk.Tk()
    app = VibrationApp(root)
    root.mainloop()