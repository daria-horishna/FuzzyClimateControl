import customtkinter as ctk
from tkinter import messagebox
from fuzzy_system import ClimateFuzzySystem
from utils import validate_inputs, save_data
from visualization import embed_plot, plot_membership, plot_result

ctk.set_appearance_mode("Light")
ctk.set_default_color_theme("blue")


class ClimateApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Нечітка система керування (Mamdani) | © Автор: Горішна Дар'я Євгенівна")
        self.geometry("900x650")
        self.minsize(800, 600)

        self.system = ClimateFuzzySystem()
        self.last_results = None
        self._build_ui()

    def _build_ui(self):
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # === ЛІВА ПАНЕЛЬ ===
        self.left_frame = ctk.CTkFrame(self, width=250, corner_radius=0)
        self.left_frame.grid(row=0, column=0, sticky="nsew")

        ctk.CTkLabel(self.left_frame, text="Параметри середовища", font=ctk.CTkFont(size=18, weight="bold")).pack(
            pady=(20, 10))

        # Температура
        ctk.CTkLabel(self.left_frame, text="Температура (0-40 °C):").pack(anchor="w", padx=20)
        self.entry_temp = ctk.CTkEntry(self.left_frame, placeholder_text="Напр. 22.5")
        self.entry_temp.pack(fill="x", padx=20, pady=(0, 10))

        # Вологість
        ctk.CTkLabel(self.left_frame, text="Вологість (0-100 %):").pack(anchor="w", padx=20)
        self.entry_hum = ctk.CTkEntry(self.left_frame, placeholder_text="Напр. 45")
        self.entry_hum.pack(fill="x", padx=20, pady=(0, 30))

        # Кнопки
        self.btn_calc = ctk.CTkButton(self.left_frame, text="▶ Обчислити", command=self.calculate)
        self.btn_calc.pack(fill="x", padx=20, pady=5)

        self.btn_clear = ctk.CTkButton(self.left_frame, text="✖ Очистити", fg_color="gray", command=self.clear_inputs)
        self.btn_clear.pack(fill="x", padx=20, pady=5)

        self.btn_save = ctk.CTkButton(self.left_frame, text="💾 Зберегти результати", fg_color="#28a745",
                                      hover_color="#218838", command=self.save_results)
        self.btn_save.pack(fill="x", padx=20, pady=5)

        self.btn_about = ctk.CTkButton(self.left_frame, text="ℹ Про програму", fg_color="transparent", border_width=1,
                                       text_color=("black", "white"), command=self.show_about)
        self.btn_about.pack(side="bottom", fill="x", padx=20, pady=20)

        # === ПРАВА ПАНЕЛЬ ===
        self.right_frame = ctk.CTkFrame(self)
        self.right_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        self.right_frame.grid_columnconfigure(0, weight=1)

        # Текстовий вивід
        self.lbl_result_title = ctk.CTkLabel(self.right_frame, text="Результати обчислень:",
                                             font=ctk.CTkFont(size=16, weight="bold"))
        self.lbl_result_title.grid(row=0, column=0, sticky="w", padx=10, pady=(10, 0))

        self.txt_result = ctk.CTkTextbox(self.right_frame, height=80)
        self.txt_result.grid(row=1, column=0, sticky="new", padx=10, pady=5)
        self.txt_result.insert("1.0", "Введіть дані та натисніть «Обчислити»...")
        self.txt_result.configure(state="disabled")

        # Блок графіків
        self.lbl_graphs = ctk.CTkLabel(self.right_frame, text="Графіки функцій належності:",
                                       font=ctk.CTkFont(size=14, weight="bold"))
        self.lbl_graphs.grid(row=2, column=0, sticky="w", padx=10, pady=(10, 0))

        self.mf_btns_frame = ctk.CTkFrame(self.right_frame, fg_color="transparent")
        self.mf_btns_frame.grid(row=3, column=0, sticky="ew", padx=10, pady=5)

        # Оновлені кнопки (тепер вони передають значення!)
        btn_temp = ctk.CTkButton(self.mf_btns_frame, text="ТЕМПЕРАТУРА", width=120,
                                 command=lambda: self.show_membership_graph('temp'))
        btn_temp.pack(side="left", padx=5)

        btn_hum = ctk.CTkButton(self.mf_btns_frame, text="ВОЛОГІСТЬ", width=120,
                                command=lambda: self.show_membership_graph('hum'))
        btn_hum.pack(side="left", padx=5)

        btn_power = ctk.CTkButton(self.mf_btns_frame, text="ПОТУЖНІСТЬ", width=120,
                                  command=self.show_power_graph)
        btn_power.pack(side="left", padx=5)

        self.plot_frame = ctk.CTkFrame(self.right_frame, fg_color="transparent")
        self.plot_frame.grid(row=4, column=0, sticky="nsew", padx=10, pady=5)
        self.right_frame.grid_rowconfigure(4, weight=1)

        self._show_placeholder("Графік з'явиться тут після виконання розрахунків\nабо вибору функції належності.")

    def _show_placeholder(self, text):
        for widget in self.plot_frame.winfo_children():
            widget.destroy()
        lbl = ctk.CTkLabel(self.plot_frame, text=text, text_color="gray", font=ctk.CTkFont(size=14))
        lbl.pack(expand=True)

    def show_membership_graph(self, var_name):
        """Виводить графік функцій належності, і якщо є розрахунки - малює лінію вводу"""
        current_val = None
        # Якщо ми вже обчислювали, дістаємо значення з пам'яті
        if self.last_results:
            if var_name == 'temp':
                current_val = self.last_results.get("Temperature")
            elif var_name == 'hum':
                current_val = self.last_results.get("Humidity")

        embed_plot(plot_membership(self.system, var_name, current_val), self.plot_frame)

    def show_power_graph(self):
        if self.last_results:
            embed_plot(plot_result(self.system, 'power'), self.plot_frame)
        else:
            embed_plot(plot_membership(self.system, 'power'), self.plot_frame)

    def calculate(self):
        try:
            t, h = validate_inputs(self.entry_temp.get(), self.entry_hum.get())
            power_val = self.system.compute(t, h)

            output_text = (
                f"Вхідні дані: Температура: {t}°C, Вологість: {h}%\n"
                f"----------------------------------------------------\n"
                f"Необхідна потужність кліматичної системи: {power_val:.2f} %"
            )

            self.txt_result.configure(state="normal")
            self.txt_result.delete("1.0", "end")
            self.txt_result.insert("1.0", output_text)
            self.txt_result.configure(state="disabled")

            self.last_results = {
                "Temperature": t, "Humidity": h,
                "Power": round(power_val, 2)
            }

            self.show_power_graph()

        except ValueError as ve:
            messagebox.showerror("Помилка вводу", str(ve))
        except Exception as e:
            messagebox.showerror("Критична помилка", f"Сталася помилка при обчисленні:\n{str(e)}")

    def clear_inputs(self):
        self.entry_temp.delete(0, 'end')
        self.entry_hum.delete(0, 'end')
        self.txt_result.configure(state="normal")
        self.txt_result.delete("1.0", "end")
        self.txt_result.insert("1.0", "Дані очищено. Введіть нові значення...")
        self.txt_result.configure(state="disabled")
        self.last_results = None
        self._show_placeholder("Дані очищено. Очікування нових розрахунків...")

    def save_results(self):
        if not self.last_results:
            messagebox.showwarning("Увага", "Немає результатів для збереження.")
            return
        save_data(self.last_results)

    def show_about(self):
        messagebox.showinfo("Про програму",
                            "Нечітка система керування кліматом.\nМетод дефазифікації: Centroid (Центр мас)\n\n© Автор: Горішна Дар'я Євгенівна")