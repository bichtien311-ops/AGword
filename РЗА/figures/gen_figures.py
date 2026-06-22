import os
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches

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

def draw_current_protection():
    # Ампер-секундная характеристика (Ступени МТЗ и ТО)
    fig, ax = plt.subplots(figsize=(8, 5))
    
    # Ступени:
    # МТЗ 3-й линии (наша защита)
    I_mtz = 200
    t_mtz = 1.5
    
    # ТО с выдержкой (II ступень)
    I_to2 = 800
    t_to2 = 0.5
    
    # Мгновенная ТО (I ступень)
    I_to1 = 2000
    t_to1 = 0.1
    
    ax.plot([0, I_mtz, I_mtz, I_to2, I_to2, I_to1, I_to1, 3000], 
            [t_mtz, t_mtz, t_to2, t_to2, t_to1, t_to1, 0.05, 0.05], 'b-', lw=2.5, label='Характеристика нашей защиты')
    
    # Смежная линия (для демонстрации ступени селективности)
    t_sm_mtz = 1.0
    t_sm_to1 = 0.1
    ax.plot([0, I_mtz, I_mtz, 1500, 1500, 3000], 
            [t_sm_mtz, t_sm_mtz, t_sm_to1, t_sm_to1, 0.02, 0.02], 'r--', lw=1.5, alpha=0.7, label='Смежный участок')
    
    # Аннотации
    ax.annotate(r'$\Delta t$ (ступень селективности)', xy=(100, 1.25), xytext=(300, 1.25), 
                arrowprops=dict(arrowstyle='<->', color='black'))
    
    ax.text(I_mtz + 50, t_mtz - 0.2, "III ступень\n(МТЗ)", color='blue')
    ax.text(I_to2 + 50, t_to2 + 0.1, "II ступень\n(ТО с выдержкой)", color='blue')
    ax.text(I_to1 + 50, t_to1 + 0.1, "I ступень\n(Мгновенная ТО)", color='blue')
    
    ax.set_title("Время-токовая характеристика ступенчатой токовой защиты")
    ax.set_xlabel("Ток КЗ, $I_к$ (А)")
    ax.set_ylabel("Время срабатывания, $t$ (с)")
    ax.set_xlim(0, 3000)
    ax.set_ylim(0, 2.0)
    ax.grid(True, ls=':')
    ax.legend()
    
    save_fig('fig_current_protection.png')

def draw_differential_brake():
    fig, ax = plt.subplots(figsize=(7, 5))
    
    I_torm = np.linspace(0, 10, 100)
    
    # Ток начала торможения
    I_t0 = 2.0
    # Базовый ток срабатывания
    I_s0 = 0.5
    # Коэффициент торможения
    k_t = 0.4
    
    I_sr = np.where(I_torm < I_t0, I_s0, I_s0 + k_t * (I_torm - I_t0))
    
    ax.plot(I_torm, I_sr, 'r-', lw=2.5, label='Характеристика срабатывания $I_{с.р} = f(I_{торм})$')
    ax.fill_between(I_torm, I_sr, 10, color='red', alpha=0.1, label='Зона срабатывания (внутреннее КЗ)')
    ax.fill_between(I_torm, 0, I_sr, color='green', alpha=0.1, label='Зона блокировки (внешнее КЗ)')
    
    # Имитация тока небаланса
    I_nb = np.where(I_torm < 1.0, 0.1, 0.1 + 0.2 * (I_torm - 1.0) ** 1.2)
    ax.plot(I_torm, I_nb, 'b--', lw=1.5, label='Максимальный ток небаланса $I_{нб.max}$')
    
    ax.set_title("Тормозная характеристика дифференциальной защиты")
    ax.set_xlabel("Ток торможения, $I_{торм}$ (о.е.)")
    ax.set_ylabel("Дифференциальный ток, $I_{диф}$ (о.е.)")
    ax.set_xlim(0, 8)
    ax.set_ylim(0, 5)
    ax.grid(True, ls=':')
    ax.legend(loc='upper left')
    
    save_fig('fig_differential_brake.png')

def draw_distance_characteristic():
    fig, ax = plt.subplots(figsize=(6, 6))
    
    # Полигональная характеристика (четырехугольник)
    # Точки: (R, X)
    R_d = 20 # Запас на дугу
    Z_L = 30 # Сопротивление линии
    phi_L = np.radians(70) # Угол линии
    
    p1 = (0, 0)
    p2 = (R_d, 0)
    p3 = (R_d + Z_L*np.cos(phi_L), Z_L*np.sin(phi_L))
    p4 = (Z_L*np.cos(phi_L) - 5, Z_L*np.sin(phi_L))
    p5 = (-10, -5) # Охват начала координат для направленности
    
    poly = patches.Polygon([p1, p2, p3, p4, p5], closed=True, fill=True, edgecolor='blue', facecolor='blue', alpha=0.2, lw=2)
    ax.add_patch(poly)
    
    # Вектор сопротивления линии
    ax.annotate('', xy=(Z_L*np.cos(phi_L), Z_L*np.sin(phi_L)), xytext=(0,0), arrowprops=dict(arrowstyle='->', color='black', lw=2))
    ax.text(Z_L*np.cos(phi_L) - 5, Z_L*np.sin(phi_L) + 2, r'$Z_{ЛЭП}$', fontsize=12, fontweight='bold')
    
    # Координатные оси
    ax.axhline(0, color='black', lw=1.5)
    ax.axvline(0, color='black', lw=1.5)
    
    # Аннотации границ
    ax.text(R_d/2, -2, 'Охват дуги $R_д$', color='blue')
    ax.text(p4[0]+2, p4[1]+2, 'Верхняя граница (Отсечка)', color='red')
    
    ax.set_xlim(-15, 45)
    ax.set_ylim(-10, 40)
    ax.set_title("Полигональная характеристика дистанционной защиты")
    ax.set_xlabel("Активное сопротивление, $R$ (Ом)")
    ax.set_ylabel("Реактивное сопротивление, $jX$ (Ом)")
    ax.grid(True, ls=':')
    
    save_fig('fig_distance_characteristic.png')

def draw_digital_substation():
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.axis('off')
    
    # Цвета
    c_station = '#e8f5e9'
    c_bay = '#e3f2fd'
    c_process = '#fff3e0'
    
    # 1. Station Level
    rect_station = patches.Rectangle((0.1, 0.75), 0.8, 0.2, fill=True, facecolor=c_station, edgecolor='black', lw=1.5)
    ax.add_patch(rect_station)
    ax.text(0.5, 0.9, "Уровень станции (Station Level)", ha='center', va='center', fontweight='bold', fontsize=12)
    ax.text(0.3, 0.82, "SCADA Сервер", ha='center', va='center', bbox=dict(facecolor='white', boxstyle='round,pad=0.4'))
    ax.text(0.7, 0.82, "АРМ Диспетчера", ha='center', va='center', bbox=dict(facecolor='white', boxstyle='round,pad=0.4'))
    
    # Station Bus
    ax.axhline(0.7, xmin=0.1, xmax=0.9, color='blue', lw=3, label='Шина станции (Ethernet)')
    ax.text(0.5, 0.72, "Шина Станции (MMS, GOOSE)", color='blue', ha='center', fontweight='bold')
    
    # 2. Bay Level
    rect_bay = patches.Rectangle((0.1, 0.4), 0.8, 0.25, fill=True, facecolor=c_bay, edgecolor='black', lw=1.5)
    ax.add_patch(rect_bay)
    ax.text(0.5, 0.6, "Уровень присоединения (Bay Level)", ha='center', va='center', fontweight='bold', fontsize=12)
    ax.text(0.25, 0.5, "Терминал РЗА (IED 1)\n(Защита линии)", ha='center', va='center', bbox=dict(facecolor='white', edgecolor='red', boxstyle='round,pad=0.4'))
    ax.text(0.5, 0.5, "Терминал РЗА (IED 2)\n(Защита тр-ра)", ha='center', va='center', bbox=dict(facecolor='white', edgecolor='red', boxstyle='round,pad=0.4'))
    ax.text(0.75, 0.5, "Контроллер (IED 3)\n(Автоматика)", ha='center', va='center', bbox=dict(facecolor='white', edgecolor='red', boxstyle='round,pad=0.4'))
    
    # Process Bus
    ax.axhline(0.35, xmin=0.1, xmax=0.9, color='green', lw=3, label='Шина процесса (Ethernet/ВОЛС)')
    ax.text(0.5, 0.37, "Шина Процесса (Sampled Values, GOOSE)", color='green', ha='center', fontweight='bold')
    
    # 3. Process Level
    rect_process = patches.Rectangle((0.1, 0.05), 0.8, 0.25, fill=True, facecolor=c_process, edgecolor='black', lw=1.5)
    ax.add_patch(rect_process)
    ax.text(0.5, 0.25, "Уровень процесса (Process Level)", ha='center', va='center', fontweight='bold', fontsize=12)
    ax.text(0.3, 0.15, "Оптические ТТ и ТН\n(SV поток)", ha='center', va='center', bbox=dict(facecolor='white', boxstyle='round,pad=0.4'))
    ax.text(0.7, 0.15, "Merging Unit (MU)\n(АЦП для старых ТТ)", ha='center', va='center', bbox=dict(facecolor='white', boxstyle='round,pad=0.4'))
    
    # Линии связи (Вертикальные)
    ax.arrow(0.3, 0.75, 0, -0.05, head_width=0.015, color='black', lw=1)
    ax.arrow(0.7, 0.75, 0, -0.05, head_width=0.015, color='black', lw=1)
    
    ax.arrow(0.25, 0.7, 0, -0.05, head_width=0.015, color='black', lw=1)
    ax.arrow(0.5, 0.7, 0, -0.05, head_width=0.015, color='black', lw=1)
    ax.arrow(0.75, 0.7, 0, -0.05, head_width=0.015, color='black', lw=1)
    
    ax.arrow(0.3, 0.4, 0, -0.05, head_width=0.015, color='black', lw=1)
    ax.arrow(0.5, 0.4, 0, -0.05, head_width=0.015, color='black', lw=1)
    ax.arrow(0.7, 0.4, 0, -0.05, head_width=0.015, color='black', lw=1)
    
    ax.arrow(0.3, 0.35, 0, -0.05, head_width=0.015, color='black', lw=1)
    ax.arrow(0.7, 0.35, 0, -0.05, head_width=0.015, color='black', lw=1)
    
    plt.title("Архитектура Цифровой Подстанции (МЭК 61850)", pad=10)
    save_fig('fig_digital_substation.png')

if __name__ == '__main__':
    draw_current_protection()
    draw_differential_brake()
    draw_distance_characteristic()
    draw_digital_substation()
    print("Графики РЗА успешно сгенерированы в", SAVE_DIR)
