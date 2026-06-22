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

def draw_pso_convergence():
    iterations = np.arange(1, 101)
    # Имитация функции сходимости (экспоненциальный спад издержек + случайный шум)
    base_cost = 15000
    initial_cost = 25000
    
    # Лучший результат стаи (gBest) - монотонно убывает
    gbest = base_cost + (initial_cost - base_cost) * np.exp(-iterations / 15.0)
    # Добавим ступеньки (имитация нахождения новых локальных минимумов)
    gbest[25:40] = gbest[25]
    gbest[40:] = gbest[40] - 500 * np.exp(-(iterations[40:] - 40) / 10.0)
    gbest[70:] = gbest[70]
    
    # Средний результат стаи
    avg_cost = gbest + 2000 * np.exp(-iterations / 30.0) + 500 * np.random.rand(100)
    
    plt.figure(figsize=(8, 5))
    plt.plot(iterations, avg_cost, 'g--', alpha=0.6, label='Среднее значение (Average Best)')
    plt.plot(iterations, gbest, 'b-', linewidth=2.5, label='Глобальный оптимум (gBest)')
    
    plt.title('График сходимости алгоритма PSO (Economic Load Dispatch)')
    plt.xlabel('Номер итерации')
    plt.ylabel('Целевая функция (Затраты $F$, у.е.)')
    plt.xlim(0, 100)
    plt.ylim(14000, 26000)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.legend()
    
    # Аннотация
    plt.annotate('Локальный минимум', xy=(30, gbest[30]), xytext=(40, gbest[30]+2000),
                 arrowprops=dict(facecolor='black', arrowstyle='->'))
    plt.annotate('Глобальный оптимум найден', xy=(75, gbest[75]), xytext=(50, gbest[75]-1000),
                 arrowprops=dict(facecolor='black', arrowstyle='->'))

    save_fig('fig_pso_convergence.png')

def draw_cloud_architecture():
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.axis('off')
    
    # Цвета
    c_edge = '#e1f5fe'
    c_cloud = '#e8eaf6'
    c_ai = '#fff3e0'
    
    # Уровни
    # 1. Edge Level
    rect_edge = patches.Rectangle((0.05, 0.1), 0.25, 0.8, fill=True, facecolor=c_edge, edgecolor='black', lw=1.5)
    ax.add_patch(rect_edge)
    ax.text(0.175, 0.85, "Полевой уровень\n(Edge)", ha='center', va='center', fontweight='bold')
    
    ax.text(0.175, 0.65, "PMU / WAMS\n(Микросекунды)", ha='center', va='center', bbox=dict(facecolor='white', edgecolor='gray', boxstyle='round,pad=0.5'))
    ax.text(0.175, 0.45, "IIoT Датчики\n(Вибрация/Темп.)", ha='center', va='center', bbox=dict(facecolor='white', edgecolor='gray', boxstyle='round,pad=0.5'))
    ax.text(0.175, 0.25, "SCADA (АСУ ТП)", ha='center', va='center', bbox=dict(facecolor='white', edgecolor='gray', boxstyle='round,pad=0.5'))
    
    # 2. Cloud Data Lake
    rect_cloud = patches.Rectangle((0.4, 0.1), 0.25, 0.8, fill=True, facecolor=c_cloud, edgecolor='black', lw=1.5)
    ax.add_patch(rect_cloud)
    ax.text(0.525, 0.85, "Облачная платформа\n(Data Pipeline)", ha='center', va='center', fontweight='bold')
    
    ax.text(0.525, 0.65, "Data Lake\n(Хранилище)", ha='center', va='center', bbox=dict(facecolor='white', edgecolor='blue', boxstyle='round,pad=0.5'))
    ax.text(0.525, 0.45, "ETL-процесс\n(Очистка данных)", ha='center', va='center', bbox=dict(facecolor='white', edgecolor='gray', boxstyle='round,pad=0.5'))
    ax.text(0.525, 0.25, "Обогащение\n(Погода, Рынок)", ha='center', va='center', bbox=dict(facecolor='white', edgecolor='gray', boxstyle='round,pad=0.5'))
    
    # 3. AI Engine
    rect_ai = patches.Rectangle((0.75, 0.1), 0.2, 0.8, fill=True, facecolor=c_ai, edgecolor='black', lw=1.5)
    ax.add_patch(rect_ai)
    ax.text(0.85, 0.85, "AI Engine\n(Аналитика)", ha='center', va='center', fontweight='bold')
    
    ax.text(0.85, 0.55, "DNN OPF\n(Управление перетоками)", ha='center', va='center', bbox=dict(facecolor='white', edgecolor='orange', boxstyle='round,pad=0.5'))
    ax.text(0.85, 0.35, "Predictive Maintenance\n(Поиск аномалий)", ha='center', va='center', bbox=dict(facecolor='white', edgecolor='orange', boxstyle='round,pad=0.5'))
    
    # Стрелки
    # Edge -> Cloud
    ax.arrow(0.3, 0.65, 0.08, 0, head_width=0.03, head_length=0.02, fc='k', ec='k', lw=1.5)
    ax.arrow(0.3, 0.45, 0.08, 0, head_width=0.03, head_length=0.02, fc='k', ec='k', lw=1.5)
    
    # Cloud -> AI
    ax.arrow(0.65, 0.55, 0.08, 0, head_width=0.03, head_length=0.02, fc='k', ec='k', lw=1.5)
    ax.arrow(0.65, 0.35, 0.08, 0, head_width=0.03, head_length=0.02, fc='k', ec='k', lw=1.5)
    
    # Feedback (AI -> SCADA)
    ax.annotate("", xy=(0.3, 0.25), xytext=(0.85, 0.25), arrowprops=dict(arrowstyle="->", color="red", lw=2, ls='dashed'))
    ax.text(0.575, 0.21, "Управляющие сигналы и Алерты", ha='center', va='center', color='red', fontsize=10)
    
    plt.title("Рис. 2 - Архитектура облачного предиктивного управления (IIoT + Cloud AI)", pad=10)
    save_fig('fig_cloud_architecture.png')

if __name__ == '__main__':
    draw_pso_convergence()
    draw_cloud_architecture()
    print("Графики для СПСЭ успешно сгенерированы в", SAVE_DIR)
