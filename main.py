import os

# --- ЦЕЙ БЛОК ВИРІШУЄ КОНФЛІКТ ВЕРСІЙ PYTHON ---
# Видаляємо змінні середовища, які можуть тягнути налаштування від Python 3.13
if 'TCL_LIBRARY' in os.environ:
    del os.environ['TCL_LIBRARY']
if 'TK_LIBRARY' in os.environ:
    del os.environ['TK_LIBRARY']
# -----------------------------------------------

from ui import ClimateApp

if __name__ == "__main__":
    app = ClimateApp()
    app.mainloop()