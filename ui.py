import tkinter as tk
from tkinter import ttk, messagebox
from calculator import calculate, normalize_model_name


class QueueCalculatorUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Queue System Calculator")

        # === Inputs ===
        row = 0
        ttk.Label(self.root, text="Modelo (ex: M/M/1, M/M/s, M/M/1/K, M/M/s/K, M/M/1/N):").grid(row=row, column=0, sticky="w")
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

        ttk.Label(self.root, text="n (opcional) - (número de clientes):").grid(row=row, column=0, sticky="w")
        self.n_entry = ttk.Entry(self.root)
        self.n_entry.grid(row=row, column=1)
        row += 1

        ttk.Label(self.root, text="s (opcional) - (número de servidores):").grid(row=row, column=0, sticky="w")
        self.s_entry = ttk.Entry(self.root)
        self.s_entry.grid(row=row, column=1)
        row += 1

        ttk.Label(self.root, text="K (opcional) - (capacidade do sistema):").grid(row=row, column=0, sticky="w")
        self.k_entry = ttk.Entry(self.root)
        self.k_entry.grid(row=row, column=1)
        row += 1

        ttk.Label(self.root, text="N (opcional) - (tamanho da população finita):").grid(row=row, column=0, sticky="w")
        self.N_entry = ttk.Entry(self.root)
        self.N_entry.grid(row=row, column=1)
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

        # Param opcional: s (número de servidores)
        s_raw = self.s_entry.get().strip()
        if s_raw:
            try:
                params["s"] = int(s_raw)
            except ValueError:
                messagebox.showerror("Erro", "s deve ser inteiro.")
                return

        # Param opcional: K
        k_raw = self.k_entry.get().strip()
        if k_raw:
            try:
                params["K"] = int(k_raw)
            except ValueError:
                messagebox.showerror("Erro", "K deve ser inteiro.")
                return

        # Param opcional: N (população finita)
        N_raw = self.N_entry.get().strip()
        if N_raw:
            try:
                params["N"] = int(N_raw)
            except ValueError:
                messagebox.showerror("Erro", "N deve ser inteiro.")
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

        model_key = normalize_model_name(model_name)

        self.result_text.insert(tk.END, f"=== Resultados ({model_name}) ===\n\n")

        # Labels for all possible keys returned by the models
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
            "lambda_eff": "Taxa efetiva de chegada (λ̄)",
            "pK": "Probabilidade de sistema cheio (P_K)",
            "L_operational": "Número médio de itens operacionais (N − L)",
            "P(any_idle_server)": "Prob. de pelo menos 1 servidor ocioso",
        }

        # --- print base results ---
        for key, value in results.items():
            label = descriptions.get(key, key)

            # W and Wq in hours + minutes
            if key in ("W", "Wq"):
                try:
                    value_min = float(value) * 60
                    value_fmt = f"{value:.4f} h  ({value_min:.2f} min)"
                except Exception:
                    value_fmt = value

            # probabilities as %
            elif key in ("P(W>t)", "P(Wq>t)", "p0", "pn", "pK", "P(any_idle_server)"):
                try:
                    value_pct = float(value) * 100
                    value_fmt = f"{value:.6f}  ({value_pct:.4f} %)"
                except Exception:
                    value_fmt = value

            else:
                value_fmt = value

            self.result_text.insert(tk.END, f"{label}: {value_fmt}\n")

        # --- extra, model-specific outputs ---

        # 1) Finite capacity models: M/M/1/K and M/M/s/K → clientes perdidos por unidade de tempo
        if model_key in ("M/M/1/K", "M/M/S/K"):
            lam_eff = results.get("lambda_eff")
            pK = results.get("pK")
            if lam_eff is not None and pK is not None and pK < 1:
                # λ̄ = λ(1−P_K) → λ = λ̄ / (1−P_K)
                lam = lam_eff / (1.0 - pK)
                lost_rate = lam * pK          # chegadas perdidas por unidade de tempo
                self.result_text.insert(
                    tk.END,
                    f"\nChegadas perdidas por unidade de tempo (λ · P_K): {lost_rate:.4f}\n",
                )

        # 2) Finite population models: M/M/1/N and M/M/s/N → tempo parado, % ocioso etc.
        if model_key in ("M/M/1/N", "M/M/S/N"):
            L_oper = results.get("L_operational")
            W = results.get("W")
            idle_prob = results.get("P(any_idle_server)")
            if L_oper is not None:
                self.result_text.insert(
                    tk.END,
                    f"\nNúmero médio de unidades operacionais: {L_oper:.4f}\n",
                )
            if W is not None:
                try:
                    W_min = float(W) * 60
                    self.result_text.insert(
                        tk.END,
                        f"Tempo médio parado (W – tempo quebrado): {W:.4f} h ({W_min:.2f} min)\n",
                    )
                except Exception:
                    pass
            if idle_prob is not None:
                self.result_text.insert(
                    tk.END,
                    f"Tempo com pelo menos 1 servidor ocioso: {idle_prob:.6f} ({idle_prob*100:.4f} %)\n",
                )

    def start(self):
        self.root.mainloop()
