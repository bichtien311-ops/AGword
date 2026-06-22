import os
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

plt.rcParams.update({
    "font.family": "serif",
    "font.serif": ["Times New Roman", "DejaVu Serif"],
    "font.size": 12,
    "axes.titlesize": 14,
    "axes.labelsize": 12,
})

SAVE_DIR = os.path.dirname(os.path.abspath(__file__))

def save_fig(filename):
    plt.tight_layout()
    plt.savefig(os.path.join(SAVE_DIR, filename), dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()

def draw_kloss_curve():
    s = np.linspace(0.001, 1.0, 500)
    # Формула Клосса M = 2 * M_kr / (s/s_kr + s_kr/s)
    M_kr = 2.5
    s_kr = 0.15
    M = 2 * M_kr / (s/s_kr + s_kr/s)
    
    # Генераторный и тормозной режимы
    s_gen = np.linspace(-1.0, -0.001, 500)
    M_gen = 2 * M_kr / (s_gen/s_kr + s_kr/s_gen)
    
    s_brk = np.linspace(1.0, 2.0, 500)
    M_brk = 2 * M_kr / (s_brk/s_kr + s_kr/s_brk)

    plt.figure(figsize=(8, 6))
    plt.plot(s, M, 'b-', linewidth=2, label=r'Двигательный ($0 < s < 1$)')
    plt.plot(s_gen, M_gen, 'g--', linewidth=2, label=r'Генераторный ($s < 0$)')
    plt.plot(s_brk, M_brk, 'r-.', linewidth=2, label=r'Тормоз противовкл. ($s > 1$)')
    
    plt.title(r'Зависимость момента от скольжения $M = f(s)$ (Клосс)')
    plt.xlabel(r'Скольжение $s$')
    plt.ylabel(r'Электромагнитный момент $M$ (о.е.)')
    plt.axhline(0, color='black', linewidth=1)
    plt.axvline(0, color='black', linewidth=1)
    plt.axvline(1, color='gray', linestyle=':')
    plt.xlim(-1.0, 2.0)
    plt.ylim(-3.0, 3.0)
    
    # Отметки критического момента
    plt.plot(s_kr, M_kr, 'ro')
    plt.annotate(r'$M_{кр}$', xy=(s_kr, M_kr), xytext=(s_kr+0.2, M_kr+0.2), arrowprops=dict(arrowstyle='->'))
    
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.legend()
    save_fig('fig_kloss_curve.png')

def draw_mech_char_rheostat():
    # Строим n = f(M)
    M_kr = 2.5
    n1 = 1.0
    
    M_axis = np.linspace(0, 2.5, 300)
    
    # Решаем формулу Клосса для s: s^2 - s*(2*M_kr/M)*s_kr + s_kr^2 = 0
    def get_n(M, s_kr):
        # устойчивая часть корня
        s = s_kr * (M_kr/M - np.sqrt((M_kr/M)**2 - 1 + 1e-9))
        return n1 * (1 - s)

    n_nat = get_n(M_axis, 0.15)
    n_r1 = get_n(M_axis, 0.4)
    n_r2 = get_n(M_axis, 1.0) # s_kr = 1 => пуск с M_kr
    
    plt.figure(figsize=(7, 5))
    plt.plot(M_axis, n_nat, 'b-', linewidth=2, label=r'Естественная ($R_{доб}=0$)')
    plt.plot(M_axis, n_r1, 'g--', linewidth=2, label=r'Искусственная 1')
    plt.plot(M_axis, n_r2, 'r-.', linewidth=2, label=r'Искусственная 2 (макс. пуск. момент)')
    
    plt.title(r'Реостатные механические характеристики $n = f(M)$')
    plt.xlabel(r'Момент $M$ (о.е.)')
    plt.ylabel(r'Скорость $n$ (о.е.)')
    plt.xlim(0, 3.0)
    plt.ylim(0, 1.1)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.legend()
    save_fig('fig_mech_char_rheostat.png')

def draw_mech_char_vfd():
    M_axis = np.linspace(0, 2.5, 300)
    
    def get_n_vfd(M, f_rel):
        # M_kr = const if U/f = const
        M_kr = 2.5
        # s_kr is inversely proportional to f (approx)
        s_kr = 0.15 / f_rel
        s = s_kr * (M_kr/M - np.sqrt((M_kr/M)**2 - 1 + 1e-9))
        n1 = 1.0 * f_rel
        return n1 * (1 - s)

    n_50 = get_n_vfd(M_axis, 1.0)
    n_40 = get_n_vfd(M_axis, 0.8)
    n_25 = get_n_vfd(M_axis, 0.5)
    n_10 = get_n_vfd(M_axis, 0.2)
    
    plt.figure(figsize=(7, 6))
    plt.plot(M_axis, n_50, 'b-', linewidth=2, label=r'$f = 50$ Гц (Ном)')
    plt.plot(M_axis, n_40, 'g--', linewidth=2, label=r'$f = 40$ Гц')
    plt.plot(M_axis, n_25, 'r-.', linewidth=2, label=r'$f = 25$ Гц')
    plt.plot(M_axis, n_10, 'k:', linewidth=2, label=r'$f = 10$ Гц')
    
    plt.title(r'Частотное регулирование скорости (закон $U/f = const$)')
    plt.xlabel(r'Момент $M$ (о.е.)')
    plt.ylabel(r'Скорость $n$ (о.е.)')
    plt.xlim(0, 3.0)
    plt.ylim(0, 1.1)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.legend()
    save_fig('fig_mech_char_vfd.png')

def draw_equivalent_circuit_text():
    # Вместо схемы рисуем красивую энергетическую диаграмму потерь
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.axis('off')
    
    boxes = [
        {"x": 0.1, "y": 0.5, "w": 0.2, "h": 0.3, "text": r"$P_1$ (от сети)"},
        {"x": 0.4, "y": 0.5, "w": 0.2, "h": 0.3, "text": r"$P_{эм}$ (зазор)"},
        {"x": 0.7, "y": 0.5, "w": 0.2, "h": 0.3, "text": r"$P_{мех}$ (вал)"}
    ]
    
    for b in boxes:
        rect = plt.Rectangle((b["x"], b["y"]), b["w"], b["h"], fill=True, facecolor='lightblue', edgecolor='black')
        ax.add_patch(rect)
        ax.text(b["x"]+0.1, b["y"]+0.15, b["text"], ha='center', va='center', fontsize=12)
        
    # Arrows
    ax.arrow(0.3, 0.65, 0.05, 0, head_width=0.03, head_length=0.02, fc='k', ec='k')
    ax.arrow(0.6, 0.65, 0.05, 0, head_width=0.03, head_length=0.02, fc='k', ec='k')
    
    # Losses
    ax.arrow(0.2, 0.5, 0, -0.15, head_width=0.02, head_length=0.03, fc='r', ec='r')
    ax.text(0.2, 0.3, r"$\Delta P_{м1} + \Delta P_{ст1}$", ha='center', va='top', color='r')
    
    ax.arrow(0.5, 0.5, 0, -0.15, head_width=0.02, head_length=0.03, fc='r', ec='r')
    ax.text(0.5, 0.3, r"$\Delta P_{м2}$", ha='center', va='top', color='r')

    ax.arrow(0.8, 0.5, 0, -0.15, head_width=0.02, head_length=0.03, fc='r', ec='r')
    ax.text(0.8, 0.3, r"$\Delta P_{мех} + \Delta P_{доб}$", ha='center', va='top', color='r')
    
    plt.title("Энергетическая диаграмма асинхронного двигателя", pad=20)
    save_fig('fig_equivalent_circuit.png')

if __name__ == '__main__':
    draw_kloss_curve()
    draw_mech_char_rheostat()
    draw_mech_char_vfd()
    draw_equivalent_circuit_text()
    print("AM Figures generated successfully in", SAVE_DIR)
