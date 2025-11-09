import tkinter as tk
from tkinter import ttk, messagebox
from calculator import calculate


class QueueCalculatorUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Queue System Calculator")

        # === Inputs ===
        row = 0
        ttk.Label(self.root, text="Modelo (ex: M/M/1):").grid(row=row, column=0, sticky="w")
        self.model_entry = ttk.Entry(self.root)
        self.model_entry.insert(0, "M/M/1")
        self.model_entry.grid(row=row, column=1)
        row += 1

        ttk.Label(self.root, text="λ (lambda) - taxa de chegada:").grid(row=row, column=0, sticky="w")
        self.lmbda_entry = ttk.Entry(self.root)
        self.lmbda_entry.grid(row=row, column=1)
        row += 1

        ttk.Label(self.root, text="μ (mu) - taxa de serviço:").grid(row=row, column=0, sticky="w")
        self.mu_entry = ttk.Entry(self.root)
        self.mu_entry.grid(row=row, column=1)
        row += 1

        ttk.Label(self.root, text="n (opcional) - (número de clientes)::").grid(row=row, column=0, sticky="w")
        self.n_entry = ttk.Entry(self.root)
        self.n_entry.grid(row=row, column=1)
        row += 1

        ttk.Label(self.root, text="c (opcional) - (número de servidores):").grid(row=row, column=0, sticky="w")
        self.c_entry = ttk.Entry(self.root)
        self.c_entry.grid(row=row, column=1)
        row += 1

        ttk.Label(self.root, text="K (opcional) - (capacidade do sistema):").grid(row=row, column=0, sticky="w")
        self.k_entry = ttk.Entry(self.root)
        self.k_entry.grid(row=row, column=1)
        row += 1
        
        ttk.Label(self.root, text="t (opcional) - (tempo):").grid(row=row, column=0, sticky="w")
        self.t_entry = ttk.Entry(self.root)
        self.t_entry.grid(row=row, column=1)
        row += 1

        ttk.Button(self.root, text="Calcular", command=self.run_calculation).grid(
            row=row, column=0, columnspan=2, pady=10
        )
        row += 1

        # === Resultados ===
        self.result_text = tk.Text(self.root, height=15, width=50)
        self.result_text.grid(row=row, column=0, columnspan=2, pady=10)

    def run_calculation(self):
        """
        Coleta os valores do usuário, chama calculate() e mostra os resultados.
        """
        model_name = self.model_entry.get().strip()

        try:
            lmbda_raw = self.lmbda_entry.get().strip()
            mu_raw = self.mu_entry.get().strip()

            lmbda = float(lmbda_raw) if lmbda_raw else None
            mu = float(mu_raw) if mu_raw else None
        except ValueError:
            messagebox.showerror("Erro", "λ e μ devem ser números.")
            return

        params = {}
        if lmbda is not None:
            params["lmbda"] = lmbda
        if mu is not None:
            params["mu"] = mu

        # Param opcional: n
        n_raw = self.n_entry.get().strip()
        if n_raw:
            try:
                params["n"] = int(n_raw)
            except ValueError:
                messagebox.showerror("Erro", "n deve ser inteiro.")
                return

        # Param opcional: c
        c_raw = self.c_entry.get().strip()
        if c_raw:
            try:
                params["c"] = int(c_raw)
            except ValueError:
                messagebox.showerror("Erro", "c deve ser inteiro.")
                return

        # Param opcional: K
        k_raw = self.k_entry.get().strip()
        if k_raw:
            try:
                params["K"] = int(k_raw)
            except ValueError:
                messagebox.showerror("Erro", "K deve ser inteiro.")
                return
            
           # Param opcional: t
        t_raw = self.t_entry.get().strip()
        if t_raw:
            try:
                params["t"] = float(t_raw)
            except ValueError:
                messagebox.showerror("Erro", "t deve ser numérico.")
                return

        try:
            result = calculate(model_name, **params)
        except Exception as e:
            messagebox.showerror("Erro", str(e))
            return

        self.show_results(model_name, result)

    def show_results(self, model_name, results: dict):
        self.result_text.delete("1.0", tk.END)

        self.result_text.insert(tk.END, f"=== Resultados ({model_name}) ===\n\n")

        # Mapeamento descritivo
        descriptions = {
            "rho": "Utilização (ρ)",
            "p0": "Probabilidade de 0 clientes (P0)",
            "pn": "Probabilidade de n clientes (Pn)",
            "L": "Número médio no sistema (L)",
            "Lq": "Número médio na fila (Lq)",
            "W": "Tempo médio no sistema (W)",
            "Wq": "Tempo médio na fila (Wq)",
            "P(W>t)": "Prob. de tempo no sistema maior que t (P(W>t))",
            "P(Wq>t)": "Prob. de tempo na fila maior que t (P(Wq>t))",
        }

        for key, value in results.items():
            label = descriptions.get(key, key)

            # Conversão de W e Wq para minutos (se existirem)
            if key in ("W", "Wq"):
                try:
                    value_min = float(value) * 60
                    value_fmt = f"{value:.4f} h  ({value_min:.2f} min)"
                except:
                    value_fmt = value
                    
            # Conversão de probabilidades para porcentagem
            elif key in ("P(W>t)", "P(Wq>t)", "p0", "pn"):
                try:
                    value_pct = float(value) * 100
                    value_fmt = f"{value:.6f}  ({value_pct:.4f} %)"
                except:
                    value_fmt = value
                    
            else:
                value_fmt = value

            self.result_text.insert(tk.END, f"{label}: {value_fmt}\n")


    def start(self):
        self.root.mainloop()
