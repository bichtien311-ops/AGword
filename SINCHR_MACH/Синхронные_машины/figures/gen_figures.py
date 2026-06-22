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

def draw_u_curves():
    Iv = np.linspace(0.2, 2.5, 300)
    
    # Упрощенная математическая модель U-образных характеристик
    # Ia = sqrt( I_a_act^2 + I_a_react^2 )
    # I_a_react ~ (E - U)/Xd ~ (k*Iv - U)/Xd
    
    U = 1.0
    Xd = 1.0
    k = 1.0
    
    def get_Ia(P_active):
        Ia_act = P_active / U
        # Ток возбуждения для cos(phi)=1 при данной активной нагрузке:
        Iv_min = np.sqrt(U**2 + (Ia_act*Xd)**2) / k
        # Реактивная составляющая тока (упрощенно)
        Ia_react = (U - k*Iv) / Xd
        Ia = np.sqrt(Ia_act**2 + Ia_react**2)
        return Ia

    Ia_0 = get_Ia(0.0)
    Ia_05 = get_Ia(0.5)
    Ia_10 = get_Ia(1.0)
    
    plt.figure(figsize=(7, 5))
    plt.plot(Iv, Ia_0, 'b-', linewidth=2, label=r'$P = 0$ (Холостой ход)')
    plt.plot(Iv, Ia_05, 'g--', linewidth=2, label=r'$P = 0.5 P_{ном}$')
    plt.plot(Iv, Ia_10, 'r-.', linewidth=2, label=r'$P = P_{ном}$')
    
    # Линия cos(phi)=1
    min_Ia = [np.min(Ia_0), np.min(Ia_05), np.min(Ia_10)]
    min_Iv = [Iv[np.argmin(Ia_0)], Iv[np.argmin(Ia_05)], Iv[np.argmin(Ia_10)]]
    plt.plot(min_Iv, min_Ia, 'k:', linewidth=2, label=r'$\cos \varphi = 1$')

    # Зоны недовозбуждения и перевозбуждения
    plt.axvline(1.0, color='gray', linestyle='-', alpha=0.3)
    plt.text(0.5, 2.0, 'Недовозбуждение\n(потребляет $Q$)', ha='center', fontsize=10, color='gray')
    plt.text(2.0, 2.0, 'Перевозбуждение\n(выдает $Q$)', ha='center', fontsize=10, color='gray')

    plt.title(r'U-образные характеристики СД $I_a = f(I_в)$')
    plt.xlabel(r'Ток возбуждения $I_в$ (о.е.)')
    plt.ylabel(r'Ток статора $I_a$ (о.е.)')
    plt.xlim(0.2, 2.5)
    plt.ylim(0, 2.5)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.legend()
    save_fig('fig_u_curves.png')

def draw_angular_characteristics():
    theta = np.linspace(0, 180, 500)
    theta_rad = np.radians(theta)
    
    # Неявнополюсная машина: P = (m*U*E / Xd) * sin(theta)
    P_cyl = 1.5 * np.sin(theta_rad)
    
    # Явнополюсная машина: P = P_em + P_rel
    # P_em = (m*U*E / Xd) * sin(theta)
    # P_rel = m*U^2/2 * (1/Xq - 1/Xd) * sin(2*theta)
    P_em = 1.5 * np.sin(theta_rad)
    P_rel = 0.4 * np.sin(2 * theta_rad)
    P_salient = P_em + P_rel
    
    plt.figure(figsize=(8, 5))
    plt.plot(theta, P_cyl, 'b--', linewidth=2, label=r'Неявнополюсная СМ')
    plt.plot(theta, P_salient, 'r-', linewidth=2, label=r'Явнополюсная СМ ($P_{\Sigma}$)')
    plt.plot(theta, P_rel, 'g:', linewidth=2, label=r'Реактивная мощность $P_{р}$')
    
    plt.title(r'Угловые характеристики $P = f(\theta)$')
    plt.xlabel(r'Угол $\theta$ (электрические градусы)')
    plt.ylabel(r'Активная мощность $P$ (о.е.)')
    
    plt.xlim(0, 180)
    plt.ylim(0, 2.0)
    plt.axhline(0, color='black', linewidth=1)
    
    # Пик явнополюсной (меньше 90 град)
    max_idx = np.argmax(P_salient)
    plt.plot(theta[max_idx], P_salient[max_idx], 'ro')
    plt.annotate(r'$P_{max}$', xy=(theta[max_idx], P_salient[max_idx]), 
                 xytext=(theta[max_idx]+10, P_salient[max_idx]+0.1), arrowprops=dict(arrowstyle='->'))

    plt.grid(True, linestyle='--', alpha=0.7)
    plt.legend()
    save_fig('fig_angular_char.png')

def draw_external_characteristics():
    Ia = np.linspace(0, 1.5, 300)
    
    # Упрощенная модель внешней характеристики U = f(Ia)
    # При индуктивной нагрузке (cos phi = 0.8 lag)
    U_ind = 1.0 - 0.2 * Ia - 0.1 * Ia**2
    # При активной нагрузке (cos phi = 1)
    U_act = 1.0 - 0.05 * Ia - 0.05 * Ia**2
    # При емкостной нагрузке (cos phi = 0.8 lead)
    U_cap = 1.0 + 0.15 * Ia - 0.02 * Ia**2
    
    plt.figure(figsize=(7, 5))
    plt.plot(Ia, U_ind, 'b-', linewidth=2, label=r'Индуктивная ($\cos \varphi=0.8$)')
    plt.plot(Ia, U_act, 'k--', linewidth=2, label=r'Активная ($\cos \varphi=1$)')
    plt.plot(Ia, U_cap, 'r-.', linewidth=2, label=r'Емкостная ($\cos \varphi=0.8_{оп}$)')
    
    plt.plot([1, 1], [0, 1.3], 'gray', linestyle=':', label=r'$I_{ном}$')
    
    plt.title(r'Внешние характеристики генератора $U = f(I_a)$')
    plt.xlabel(r'Ток статора $I_a$ (о.е.)')
    plt.ylabel(r'Напряжение $U$ (о.е.)')
    
    plt.xlim(0, 1.5)
    plt.ylim(0.6, 1.3)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.legend()
    save_fig('fig_external_char.png')

if __name__ == '__main__':
    draw_u_curves()
    draw_angular_characteristics()
    draw_external_characteristics()
    print("Синхронные машины: Графики успешно сгенерированы в", SAVE_DIR)
