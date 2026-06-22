# -*- coding: utf-8 -*-
"""Финальная сборка учебного пособия «Оптимизация СПСЭ»."""
import sys, os, re
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "execution"))

from word_builder import create_document, DocumentMetadata, DocType
from datetime import datetime

ROOT = os.path.dirname(__file__)
MASTER = os.path.join(ROOT, "data", "master_spse.md")
OUT = os.path.join(ROOT, "Результаты", "методичка_СПСЭ.docx")

if not os.path.exists(os.path.join(ROOT, "Результаты")):
    os.makedirs(os.path.join(ROOT, "Результаты"))

with open(MASTER, encoding="utf-8") as f:
    full = f.read()

introduction = (
    "Учебное пособие «Оптимизация систем промышленного электроснабжения» "
    "посвящено конвергенции традиционной энергетики и передовых ИТ-решений. "
    "В эпоху Четвертой промышленной революции (Индустрия 4.0) классические "
    "методы расчета режимов энергосистем уже не способны обеспечить требуемую "
    "гибкость и скорость принятия решений. Пособие подробно рассматривает "
    "переход от локальных SCADA-систем к распределенным облачным архитектурам, "
    "использующим промышленный интернет вещей (IIoT) и технологии больших "
    "данных. Особое внимание уделено строгим математическим моделям "
    "экономического распределения нагрузки (ELD) и оптимального перетока мощности "
    "(OPF), а также современным метаэвристическим алгоритмам (PSO) и нейросетевым "
    "прокси-моделям, способным решать эти нелинейные задачи в реальном времени. "
    "Практическая ценность материала подкрепляется детальным разбором успешного "
    "мирового опыта на примере глобального оператора National Grid."
)

conclusion = (
    "Подводя итоги, можно утверждать, что внедрение систем предиктивной "
    "аналитики и облачного ИИ является единственным путем обеспечения "
    "глобальной конкурентоспособности промышленных предприятий. Приведенные "
    "в пособии математические модели и алгоритмы машинного обучения (включая "
    "глубокие нейронные сети для аппроксимации OPF) наглядно демонстрируют, "
    "как цифровые технологии снижают капитальные затраты (CAPEX) за счет "
    "динамического рейтинга линий и интеллектуального размещения FACTS. "
    "Операционные затраты (OPEX) радикально сокращаются благодаря переходу "
    "от планово-предупредительных ремонтов к предиктивному обслуживанию, "
    "что было блестяще подтверждено кейсами National Grid и стартапа Avathon. "
    "Будущее промышленных энергосистем неразрывно связано с созданием "
    "автономных киберфизических комплексов, где ИИ-платформы в квазиреальном "
    "времени управляют потоками мощности, обеспечивая абсолютную "
    "энергоэффективность и надежность."
)

sources = [
    "Идельчик В.И. Электрические системы и сети: Учебник для вузов. — М.: Энергоатомиздат, 1989.",
    "Bose, A. (2017). Smart Transmission Grid Applications and Their Supporting Infrastructure. IEEE Transactions on Smart Grid, 1(1), 11-19.",
    "National Grid Case Study. (2024). Leveraging Apptio for TBM and NiCE CXone for Cloud Contact Centers.",
    "Avathon (SparkCognition) Report. (2025). Predictive Maintenance for Grain LNG Terminal: Eliminating Alarm Fatigue.",
    "Gomez-Exposito, A., Conejo, A. J., & Canizares, C. (2018). Electric Energy Systems: Analysis and Operation. CRC Press.",
    "Frank, S., Steponavice, I., & Rebennack, S. (2012). Optimal power flow: A bibliographic survey. Energy Systems, 3(3), 221-258."
]

meta = DocumentMetadata(
    title="Оптимизация систем промышленного электроснабжения",
    university="",
    author="",
    discipline="",
    city="",
    year=str(datetime.now().year),
)

create_document(
    doc_type=DocType.STUDY_GUIDE,
    raw_content=full,
    metadata=meta,
    output_path=OUT,
    sources=sources,
    introduction=introduction,
    conclusion=conclusion,
)
print("OK:", OUT)
