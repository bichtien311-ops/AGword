import os
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# Настройка шрифтов для кириллицы
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

def draw_magnetization_curve():
    Iv = np.linspace(0, 5, 100)
    Phi = 1.0 * (1 - np.exp(-1.5 * Iv))
    
    plt.figure(figsize=(6, 4))
    plt.plot(Iv, Phi, 'b-', linewidth=2)
    plt.title(r'Кривая намагничивания и х.х. генератора')
    plt.xlabel(r'Ток возбуждения $I_в$, А')
    plt.ylabel(r'ЭДС $E_0$, В / Поток $\Phi$, Вб')
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.plot(0, 0.05, 'ro')
    plt.annotate(r'$E_{ост}$', xy=(0.1, 0.06), xytext=(0.5, 0.1),
                 arrowprops=dict(facecolor='black', arrowstyle='->'))
    save_fig('fig_magnetization_curve.png')

def draw_external_characteristics():
    Ia = np.linspace(0, 1.2, 100)
    U_indep = 1.05 - 0.05 * Ia
    U_shunt = 1.05 - 0.05 * Ia - 0.1 * Ia**2
    U_series = 1.2 * (1 - np.exp(-3*Ia)) - 0.1 * Ia
    U_comp = 1.0 + 0.05 * Ia - 0.05 * Ia**2
    
    plt.figure(figsize=(7, 5))
    plt.plot(Ia, U_indep, 'b-', label=r'Независимое', linewidth=2)
    plt.plot(Ia, U_shunt, 'r--', label=r'Параллельное', linewidth=2)
    plt.plot(Ia, U_comp, 'g-.', label=r'Смешанное', linewidth=2)
    plt.plot(Ia, U_series, 'k:', label=r'Последовательное', linewidth=2)
    
    plt.plot([1, 1], [0, 1], 'k--', alpha=0.5)
    plt.plot([0, 1], [1, 1], 'k--', alpha=0.5)
    
    plt.title(r'Внешние характеристики генераторов $U = f(I_a)$')
    plt.xlabel(r'Ток якоря $I_a$ (о.е.)')
    plt.ylabel(r'Напряжение $U$ (о.е.)')
    plt.xlim(0, 1.3)
    plt.ylim(0, 1.2)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.legend()
    save_fig('fig_external_char.png')

def draw_mech_char_shunt():
    M = np.linspace(0, 1.5, 100)
    n_nat = 1.0 - 0.05 * M
    n_rheo1 = 1.0 - 0.15 * M
    n_rheo2 = 1.0 - 0.3 * M
    n_weak = 1.2 - 0.1 * M
    n_volt = 0.6 - 0.05 * M
    
    plt.figure(figsize=(7, 5))
    plt.plot(M, n_nat, 'b-', label=r'Естественная ($R_{доб}=0, \Phi_{ном}, U_{ном}$)', linewidth=2)
    plt.plot(M, n_rheo1, 'r--', label=r'Искусственная ($R_{доб1} > 0$)', linewidth=1.5)
    plt.plot(M, n_rheo2, 'r:', label=r'Искусственная ($R_{доб2} > R_{доб1}$)', linewidth=1.5)
    plt.plot(M, n_weak, 'g-.', label=r'Ослабление поля ($\Phi < \Phi_{ном}$)', linewidth=1.5)
    plt.plot(M, n_volt, 'k--', label=r'Снижение напряжения ($U < U_{ном}$)', linewidth=1.5)
    
    plt.title(r'Механические характеристики ДПТ параллельного возбуждения')
    plt.xlabel(r'Электромагнитный момент $M$ (о.е.)')
    plt.ylabel(r'Скорость вращения $n$ (о.е.)')
    plt.xlim(0, 1.6)
    plt.ylim(0, 1.4)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.legend()
    save_fig('fig_mech_char_shunt.png')

def draw_mech_char_series():
    M = np.linspace(0.05, 1.5, 100)
    n_nat = 1.0 / np.sqrt(M) - 0.1
    n_rheo = 1.0 / np.sqrt(M) - 0.4
    
    plt.figure(figsize=(6, 5))
    plt.plot(M, n_nat, 'b-', label=r'Естественная', linewidth=2)
    plt.plot(M, n_rheo, 'r--', label=r'Искусственная ($R_{доб}>0$)', linewidth=2)
    
    plt.title(r'Механические характеристики ДПТ послед. возбуждения')
    plt.xlabel(r'Электромагнитный момент $M$ (о.е.)')
    plt.ylabel(r'Скорость вращения $n$ (о.е.)')
    plt.xlim(0, 1.6)
    plt.ylim(0, 3.5)
    plt.axvline(x=0.25, color='gray', linestyle=':', label=r'$M_{min}$ (разнос)')
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.legend()
    save_fig('fig_mech_char_series.png')

def draw_commutation():
    t = np.linspace(-1, 1, 100)
    i_str = -t
    i_del = -np.sin(t * np.pi/2)
    i_acc = -t**3
    
    plt.figure(figsize=(6, 4))
    plt.plot(t, i_str, 'b-', label=r'Прямолинейная', linewidth=2)
    plt.plot(t, i_del, 'r--', label=r'Замедленная (недостаток ДП)', linewidth=2)
    plt.plot(t, i_acc, 'g-.', label=r'Ускоренная (перекомпенсация)', linewidth=2)
    
    plt.title(r'Процесс коммутации секции $i_c = f(t)$')
    plt.xlabel(r'Относительное время коммутации $t/T_k$')
    plt.ylabel(r'Ток коммутируемой секции $i_c/I_a$')
    plt.xlim(-1.1, 1.1)
    plt.ylim(-1.2, 1.2)
    plt.axhline(0, color='black', linewidth=1)
    plt.axvline(-1, color='gray', linestyle=':')
    plt.axvline(1, color='gray', linestyle=':')
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.legend()
    save_fig('fig_commutation.png')

def draw_braking():
    M = np.linspace(-1.5, 1.5, 200)
    n_nat = 1.0 - 0.1 * M
    n_dyn = -0.5 * M
    
    plt.figure(figsize=(7, 7))
    plt.plot(M, n_nat, 'b-', label=r'Двигательный / Рекуперативное', linewidth=2)
    plt.plot(M, n_dyn, 'g--', label=r'Динамическое торможение', linewidth=2)
    plt.plot(M, -1.0 - 0.2*M, 'r-.', label=r'Противовключение', linewidth=2)
    
    plt.title(r'Тормозные режимы ДПТ')
    plt.xlabel(r'Момент $M$')
    plt.ylabel(r'Скорость $n$')
    plt.axhline(0, color='black', linewidth=1.5)
    plt.axvline(0, color='black', linewidth=1.5)
    plt.xlim(-1.5, 1.5)
    plt.ylim(-1.5, 1.5)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.legend()
    save_fig('fig_braking.png')

if __name__ == '__main__':
    draw_magnetization_curve()
    draw_external_characteristics()
    draw_mech_char_shunt()
    draw_mech_char_series()
    draw_commutation()
    draw_braking()
    print("Figures generated successfully in", SAVE_DIR)
