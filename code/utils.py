import json
import csv
import pandas as pd
from tkinter import filedialog, messagebox

def validate_inputs(t, h):
    try:
        t = float(t)
        h = float(h)
        if not (0 <= t <= 40): raise ValueError("Температура має бути від 0 до 40 °C")
        if not (0 <= h <= 100): raise ValueError("Вологість має бути від 0 до 100 %")
        return t, h
    except Exception as e:
        raise ValueError(f"Помилка вхідних даних: {str(e)}")

def save_data(data_dict):
    file_path = filedialog.asksaveasfilename(
        defaultextension=".json",
        filetypes=[("JSON files", "*.json"), ("CSV files", "*.csv"), ("Text files", "*.txt")],
        title="Зберегти результати"
    )
    if not file_path: return

    try:
        if file_path.endswith('.json'):
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data_dict, f, ensure_ascii=False, indent=4)
        elif file_path.endswith('.csv'):
            df = pd.DataFrame([data_dict])
            df.to_csv(file_path, index=False, encoding='utf-8-sig')
        elif file_path.endswith('.txt'):
            with open(file_path, 'w', encoding='utf-8') as f:
                for key, value in data_dict.items():
                    f.write(f"{key}: {value}\n")
        messagebox.showinfo("Успіх", f"Дані успішно збережено у файл:\n{file_path}")
    except Exception as e:
        messagebox.showerror("Помилка", f"Не вдалося зберегти файл:\n{str(e)}")