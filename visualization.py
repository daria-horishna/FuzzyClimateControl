import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


def embed_plot(fig, parent_frame):
    for widget in parent_frame.winfo_children():
        widget.destroy()
    canvas = FigureCanvasTkAgg(fig, master=parent_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill="both", expand=True)


def plot_membership(system, variable_name, current_val=None):
    """Будує графік функцій належності та позначає введений користувачем рівень"""
    plt.close('all')

    fig, ax = plt.subplots(figsize=(6, 4), dpi=100)
    var = getattr(system, variable_name)

    # Малюємо самі функції належності
    for label, mf in var.terms.items():
        ax.plot(var.universe, mf.mf, label=label, linewidth=2)

    # ДОДАЄМО: Якщо є значення користувача - малюємо вертикальну лінію!
    if current_val is not None:
        ax.axvline(x=current_val, color='red', linestyle='--', linewidth=2, label=f'Ваш ввід: {current_val}')

    ax.set_title(f'Функції належності: {variable_name.upper()}')
    ax.legend(loc='best', fontsize='small')
    ax.grid(True, alpha=0.3)
    fig.tight_layout()

    return fig


def plot_result(system, variable_name):
    """Власна надійна побудова графіка результату"""
    plt.close('all')

    fig, ax = plt.subplots(figsize=(6, 4), dpi=100)
    var = getattr(system, variable_name)

    for label, mf in var.terms.items():
        ax.plot(var.universe, mf.mf, label=label, linestyle='--', alpha=0.7)

    val = system.simulation.output.get(variable_name, None)

    if val is not None:
        ax.axvline(x=val, color='red', linewidth=3, label=f'Результат: {val:.2f} %')
        ax.fill_between(var.universe, 0, 1, where=(var.universe <= val), color='red', alpha=0.1)

    ax.set_title(f'Результат логічного виведення: {variable_name.upper()}')
    ax.legend(loc='best', fontsize='small')
    ax.grid(True, alpha=0.3)
    fig.tight_layout()

    return fig