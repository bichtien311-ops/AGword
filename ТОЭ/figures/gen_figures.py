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

def draw_phasor_diagram():
    fig, ax = plt.subplots(figsize=(6, 6))
    
    # Напряжение как базовый вектор
    U = np.array([4, 0])
    
    # Индуктивная нагрузка: ток отстает на угол phi (например, 45 град)
    phi = np.radians(-45)
    I_mag = 2.5
    I = np.array([I_mag * np.cos(phi), I_mag * np.sin(phi)])
    
    # Реактивная и активная составляющие тока
    I_a = np.array([I[0], 0])
    I_r = np.array([0, I[1]])
    
    ax.annotate('', xy=U, xytext=(0, 0), arrowprops=dict(color='blue', width=2, headwidth=8))
    ax.text(U[0]/2, 0.2, r'$\dot{U}$', color='blue', fontsize=14)
    
    ax.annotate('', xy=I, xytext=(0, 0), arrowprops=dict(color='red', width=2, headwidth=8))
    ax.text(I[0]/2, I[1]/2 - 0.3, r'$\dot{I}$', color='red', fontsize=14)
    
    ax.annotate('', xy=I_a, xytext=(0, 0), arrowprops=dict(color='black', width=1, headwidth=5, ls='--'))
    ax.text(I_a[0]/2, 0.2, r'$I_a$', color='black')
    
    ax.annotate('', xy=I, xytext=I_a, arrowprops=dict(color='black', width=1, headwidth=5, ls='--'))
    ax.text(I[0]+0.1, I[1]/2, r'$I_r$', color='black')
    
    # Дуга для угла phi
    arc = matplotlib.patches.Arc((0,0), 1.5, 1.5, angle=0, theta1=-45, theta2=0, color='green', lw=2)
    ax.add_patch(arc)
    ax.text(0.8, -0.4, r'$\varphi$', color='green', fontsize=14)
    
    ax.set_xlim(-1, 5)
    ax.set_ylim(-3, 3)
    ax.grid(True, linestyle=':')
    ax.axhline(0, color='black', lw=1)
    ax.axvline(0, color='black', lw=1)
    ax.set_title("Векторная диаграмма (индуктивная нагрузка)")
    
    save_fig('fig_phasor_diagram.png')

def draw_three_phase():
    t = np.linspace(0, 2*np.pi, 300)
    eA = np.sin(t)
    eB = np.sin(t - 2*np.pi/3)
    eC = np.sin(t + 2*np.pi/3)
    
    plt.figure(figsize=(8, 4))
    plt.plot(t, eA, 'r-', lw=2, label=r'$e_A(t)$')
    plt.plot(t, eB, 'g--', lw=2, label=r'$e_B(t)$')
    plt.plot(t, eC, 'b-.', lw=2, label=r'$e_C(t)$')
    
    plt.axhline(0, color='black', lw=1)
    plt.xticks([0, np.pi/2, np.pi, 3*np.pi/2, 2*np.pi], 
               ['0', r'$\pi/2$', r'$\pi$', r'$3\pi/2$', r'$2\pi$'])
    plt.title("Трехфазная система ЭДС")
    plt.xlabel(r'$\omega t$')
    plt.ylabel("ЭДС, о.е.")
    plt.legend(loc='upper right')
    plt.grid(True, ls=':')
    
    save_fig('fig_three_phase.png')

def draw_transients_combined():
    t = np.linspace(0, 5, 500)
    
    # RC заряд
    tau = 1.0
    uC = 1 - np.exp(-t/tau)
    
    # RLC колебательный разряд
    delta = 0.5
    omega0 = 5.0
    omega = np.sqrt(omega0**2 - delta**2)
    i_rlc = np.exp(-delta * t) * np.cos(omega * t)
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))
    
    ax1.plot(t, uC, 'b-', lw=2)
    ax1.axhline(1, color='r', ls='--')
    ax1.set_title(r'Заряд конденсатора $u_C(t)$')
    ax1.set_xlabel(r'$t/\tau$')
    ax1.set_ylabel(r'$u_C / U$')
    ax1.grid(True, ls=':')
    
    ax2.plot(t, i_rlc, 'g-', lw=2)
    ax2.plot(t, np.exp(-delta * t), 'k--', lw=1, alpha=0.5)
    ax2.plot(t, -np.exp(-delta * t), 'k--', lw=1, alpha=0.5)
    ax2.set_title(r'Разряд RLC контура $i(t)$')
    ax2.set_xlabel('Время $t$')
    ax2.grid(True, ls=':')
    ax2.axhline(0, color='black', lw=1)
    
    save_fig('fig_transients_combined.png')

def draw_dipole_field():
    x = np.linspace(-2, 2, 50)
    y = np.linspace(-2, 2, 50)
    X, Y = np.meshgrid(x, y)
    
    # Заряды
    q1, pos1 = 1, np.array([-0.5, 0])
    q2, pos2 = -1, np.array([0.5, 0])
    
    def E_field(q, pos, X, Y):
        dx = X - pos[0]
        dy = Y - pos[1]
        r = np.sqrt(dx**2 + dy**2)
        r[r < 0.1] = 0.1 # Защита от деления на 0
        Ex = q * dx / r**3
        Ey = q * dy / r**3
        return Ex, Ey

    def Potential(q, pos, X, Y):
        r = np.sqrt((X - pos[0])**2 + (Y - pos[1])**2)
        r[r < 0.1] = 0.1
        return q / r

    Ex1, Ey1 = E_field(q1, pos1, X, Y)
    Ex2, Ey2 = E_field(q2, pos2, X, Y)
    Ex, Ey = Ex1 + Ex2, Ey1 + Ey2
    
    V = Potential(q1, pos1, X, Y) + Potential(q2, pos2, X, Y)
    
    plt.figure(figsize=(6, 6))
    
    # Силовые линии E
    plt.streamplot(X, Y, Ex, Ey, color='gray', linewidth=1, density=1.5, arrowstyle='->', arrowsize=1.5)
    
    # Эквипотенциали
    levels = np.array([-2, -1, -0.5, -0.2, 0, 0.2, 0.5, 1, 2])
    plt.contour(X, Y, V, levels=levels, colors='blue', alpha=0.5, linestyles='dashed')
    
    # Сами заряды
    plt.plot(pos1[0], pos1[1], 'ro', markersize=10)
    plt.text(pos1[0], pos1[1]+0.15, '+q', color='red', ha='center', fontweight='bold')
    plt.plot(pos2[0], pos2[1], 'bo', markersize=10)
    plt.text(pos2[0], pos2[1]+0.15, '-q', color='blue', ha='center', fontweight='bold')
    
    plt.title("Электрическое поле диполя")
    plt.xlim(-2, 2)
    plt.ylim(-2, 2)
    plt.gca().set_aspect('equal')
    
    save_fig('fig_dipole_field.png')

if __name__ == '__main__':
    draw_phasor_diagram()
    draw_three_phase()
    draw_transients_combined()
    draw_dipole_field()
    print("Графики ТОЭ успешно сгенерированы в", SAVE_DIR)
