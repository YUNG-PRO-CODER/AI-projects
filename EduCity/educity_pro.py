import sys
import numpy as np
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import pyqtgraph as pg
from pyqtgraph import PlotWidget, mkPen
import time
import random
from datetime import datetime

INDIA_STATES = [
    "Andhra Pradesh", "Arunachal Pradesh", "Assam", "Bihar", "Chhattisgarh",
    "Goa", "Gujarat", "Haryana", "Himachal Pradesh", "Jharkhand",
    "Karnataka", "Kerala", "Madhya Pradesh", "Maharashtra", "Manipur",
    "Meghalaya", "Mizoram", "Nagaland", "Odisha", "Punjab",
    "Rajasthan", "Sikkim", "Tamil Nadu", "Telangana", "Tripura",
    "Uttar Pradesh", "Uttarakhand", "West Bengal"
]

class DynamicMLGenerator:
    def __init__(self):
        np.random.seed(42)
        self.state_vectors = self._init_state_vectors()
    
    def _init_state_vectors(self):
        vectors = {}
        for i, state in enumerate(INDIA_STATES):
            vector = np.array([
                1 + i * 0.1, np.sin(i) * 0.3 + 0.4, np.cos(i * 0.7) * 0.5,
                abs(np.sin(i * 1.2)) * 0.8, np.tanh(i * 0.3) * 0.6,
                random.uniform(0.2, 0.9), abs(np.cos(i * 0.9)) * 0.7,
                np.sin(i * 1.5) * 0.4 + 0.5, random.uniform(0.1, 0.8),
                i / len(INDIA_STATES)
            ])
            vectors[state] = vector
        return vectors
    
    def generate_neural_problem(self, state, t):
        vector = self.state_vectors[state]
        dropout_trend = 0.3 + np.tanh(vector[5] + np.sin(t * 0.8)) * 0.4
        literacy_gap = abs(vector[1] - vector[2]) * 100
        
        problem_types = [
            f"{dropout_trend*100:.1f}% student dropout predicted by LSTM models",
            f"Literacy gap of {literacy_gap:.1f}% detected by CNN analysis",
            f"Teacher absenteeism shows {vector[4]*100:.0f}% coverage gap",
            f"Digital divide reveals {vector[7]*100:.0f}% connectivity failure",
            f"Nutrition models predict {vector[6]*100:.0f}% cognitive decline",
            f"Infrastructure clustering shows {vector[3]*100:.0f}% school deficit"
        ]
        
        weights = np.abs(vector[:len(problem_types)])
        weights = weights / weights.sum()
        problem = np.random.choice(problem_types, p=weights)
        return f"🔴 ML-DETECTED: {problem}"
    
    def generate_xgboost_solution(self, state, t):
        vector = self.state_vectors[state]
        solution_accuracy = 0.75 + (np.sin(t + len(state)) * 0.25)
        impact_reduction = 0.4 + vector[0] * 0.3
        
        solution_templates = [
            f"✅ XGBoost models deployed - {solution_accuracy*100:.0f}% accuracy",
            f"✅ Transformer AI Tutors - {solution_accuracy*100:.0f}% comprehension",
            f"✅ CNN mobile learning pods - {solution_accuracy*100:.0f}% attendance",
            f"✅ LSTM flood prediction - {impact_reduction*100:.0f}% dropout prevention",
            f"✅ GAN tribal content - {solution_accuracy*100:.0f}% engagement"
        ]
        
        idx = int((t + len(state)) % len(solution_templates))
        return solution_templates[idx]
    
    def generate_students_affected(self, state, t):
        base_population = np.random.randint(8_000_000, 25_000_000)
        impact_factor = 0.3 + abs(np.sin(t + len(state))) * 0.7
        return int(base_population * impact_factor)

class IndiaEducationData:
    def __init__(self):
        self.time = time.time()
        self.total_students = 260_000_000
        self.ml_gen = DynamicMLGenerator()
    
    def get_live_data(self):
        self.time = time.time()
        t = self.time
        states_data = {}
        
        for state in INDIA_STATES:
            impact = 25 + (np.sin(t * 0.6 + hash(state) % 100 / 100) * 65)
            states_data[state] = {
                'impact': max(0, min(100, impact)),
                'students': self.ml_gen.generate_students_affected(state, t),
                'ml_problem': self.ml_gen.generate_neural_problem(state, t),
                'ml_solution': self.ml_gen.generate_xgboost_solution(state, t),
                'ml_accuracy': 72 + np.random.uniform(-5, 15),
                'deployment_time': datetime.now().strftime("%H:%M:%S")
            }
        
        impacts = [data['impact'] for data in states_data.values()]
        students_total = sum(data['students'] for data in states_data.values())
        
        metrics = {
            'total_students': min(280_000_000, students_total) / 10_000_000,  # In crores
            'states_covered': 28,
            'ai_solutions': 45_000 + int(t % 1000 * 80),
            'ml_accuracy': np.mean([data['ml_accuracy'] for data in states_data.values()]),
            'progress': min(100, (t % 7200) / 72)
        }
        
        return metrics, states_data

class IndiaEngine(QThread):
    dataReady = pyqtSignal(dict)
    
    def __init__(self):
        super().__init__()
        self.running = False
        self.data_gen = IndiaEducationData()
    
    def run(self):
        self.running = True
        while self.running:
            data = self.data_gen.get_live_data()
            self.dataReady.emit({
                'metrics': data[0],
                'states': data[1]
            })
            self.msleep(100)  
    
    def stop(self):
        self.running = False

class StateDetailWidget(QFrame):
    def __init__(self, state_data):
        super().__init__()
        self.state_data = state_data
        self.initUI()
    
    def initUI(self):
        self.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, 
                    stop:0 rgba(10,25,60,255), stop:1 rgba(20,40,90,255));
                border: 2px solid rgba(0,180,255,120); border-radius: 20px;
                padding: 25px;
            }
        """)
        
        layout = QVBoxLayout(self)
        layout.setSpacing(18)
        
        state_name = list(self.state_data.keys())[0]
        data = self.state_data[state_name]
        self.title = QLabel(f"🤖 {state_name} | ML Acc: {data['ml_accuracy']:.0f}% | {data['deployment_time']}")
        self.title.setStyleSheet("""
            color: #00ff88; font-size: 24px; font-weight: bold;
            padding: 18px; background: rgba(0,255,136,0.25);
            border: 3px solid #00ff88; border-radius: 18px;
        """)
        self.title.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.title)
        
        layout.addWidget(QLabel("🔴 NEURAL NETWORK PROBLEM:"))
        self.problem_text = QTextEdit()
        self.problem_text.setFixedHeight(140)
        self.problem_text.setStyleSheet("""
            QTextEdit { background: rgba(255,71,87,0.35); color: #ff6b6b; 
                       font-size: 15px; font-family: 'Consolas'; border: 3px solid #ff4757; 
                       border-radius: 15px; padding: 20px; }
        """)
        self.problem_text.setReadOnly(True)
        layout.addWidget(self.problem_text)
        
        layout.addWidget(QLabel("🟢 XGBOOST SOLUTION:"))
        self.solution_text = QTextEdit()
        self.solution_text.setFixedHeight(140)
        self.solution_text.setStyleSheet("""
            QTextEdit { background: rgba(0,255,136,0.35); color: #00ff88; 
                       font-size: 15px; font-family: 'Consolas'; border: 3px solid #00ff88; 
                       border-radius: 15px; padding: 20px; }
        """)
        self.solution_text.setReadOnly(True)
        layout.addWidget(self.solution_text)
        
        self.update_content()
    
    def update_content(self):
        state_name = list(self.state_data.keys())[0]
        data = self.state_data[state_name]
        self.problem_text.setPlainText(data['ml_problem'])
        self.solution_text.setPlainText(data['ml_solution'])
        self.title.setText(f"🤖 {state_name} | ML Acc: {data['ml_accuracy']:.0f}% | {data['deployment_time']}")

class VerticalStateTab(QPushButton):
    stateSelected = pyqtSignal(str)
    
    def __init__(self, state_name, index):
        super().__init__()
        self.state_name = state_name
        self.index = index
        self.initUI()
    
    def initUI(self):
        self.setCheckable(True)
        self.setFixedHeight(65)
        self.setText(f"📍 {self.state_name}")
        self.update_style()
        self.clicked.connect(self.toggle_expand)
    
    def update_style(self):
        if self.isChecked():
            self.setStyleSheet("""
                QPushButton { background: qlineargradient(90deg, #00ff88, #ffd700); 
                             color: black; font-size: 16px; font-weight: bold;
                             border-left: 8px solid #ffd700; border-radius: 15px;
                             padding: 15px 25px; }
            """)
        else:
            self.setStyleSheet("""
                QPushButton { background: qlineargradient(90deg, rgba(0,120,255,80), rgba(15,35,90,255));
                             color: #00bfff; font-size: 15px; font-weight: bold;
                             border-left: 6px solid rgba(0,180,255,60); border-radius: 15px;
                             padding: 15px 25px; }
            """)
    
    def toggle_expand(self):
        self.setChecked(True)
        self.stateSelected.emit(self.state_name)

class IndiaMetric(QFrame):
    def __init__(self, title, unit):
        super().__init__()
        self.title = title
        self.unit = unit
        self.value = 0
        self.setFixedSize(220, 90)
        self.setStyleSheet("""
            background: qlineargradient(45deg, rgba(5,55,135,80), rgba(15,35,90,255));
            border: 3px solid rgba(0,120,215,80); border-radius: 18px;
        """)
        self.initUI()
    
    def initUI(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 12, 12, 12)
        
        title_label = QLabel(self.title)
        title_label.setStyleSheet("color: #00bfff; font-size: 13px; font-weight: bold;")
        title_label.setAlignment(Qt.AlignCenter)
        
        self.value_label = QLabel("0")
        self.value_label.setStyleSheet("color: #00ff88; font-size: 26px; font-weight: bold;")
        self.value_label.setAlignment(Qt.AlignCenter)
        
        layout.addWidget(title_label)
        layout.addWidget(self.value_label)
    
    def setValue(self, value):
        self.value = value
        self.value_label.setText(f"{value:.1f}{self.unit}")

class IndiaDashboard(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("🇮🇳 INDIA EDUCATION ANALYSIS -created by Atharv-")
        self.setGeometry(50, 50, 1900, 1050)
        self.engine = None
        self.state_data = {}
        self.chart_data = []
        self.selected_state = None
        self.initUI()
    
    def initUI(self):
        self.setStyleSheet("""
            QMainWindow { background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                stop:0 rgba(135,31,31,255), stop:0.5 rgba(19,136,8,255), stop:1 rgba(0,51,153,255)); }
        """)
        
        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QHBoxLayout(central)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)
        
        left_panel = QFrame()
        left_panel.setFixedWidth(350)
        left_panel.setStyleSheet("""
            QFrame { background: rgba(10,20,50,240); border: 3px solid #ffd700; border-radius: 25px; }
        """)
        left_layout = QVBoxLayout(left_panel)
        left_layout.setSpacing(10)
        left_layout.setContentsMargins(20, 20, 20, 20)
        
        header_label = QLabel("🇮🇳 STATE AI/ML TABS (28 States)")
        header_label.setStyleSheet("""
            color: #ffd700; font-size: 20px; font-weight: bold; padding: 15px; 
            background: rgba(255,215,0,0.3); border-radius: 15px; border: 2px solid #ffd700;
        """)
        header_label.setAlignment(Qt.AlignCenter)
        left_layout.addWidget(header_label)
        
        self.state_tabs_scroll = QScrollArea()
        self.state_tabs_scroll.setWidgetResizable(True)
        self.state_tabs_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        tabs_widget = QWidget()
        self.tabs_layout = QVBoxLayout(tabs_widget)
        self.tabs_layout.setSpacing(5)
        self.state_tabs_scroll.setWidget(tabs_widget)
        self.state_tabs_scroll.setStyleSheet("QScrollArea { border: none; }")
        left_layout.addWidget(self.state_tabs_scroll)
        main_layout.addWidget(left_panel)
        
        right_panel = QFrame()
        right_panel.setStyleSheet("""
            QFrame { background: rgba(15,25,60,220); border: 3px solid #00bfff; border-radius: 25px; }
        """)
        right_layout = QVBoxLayout(right_panel)
        right_layout.setContentsMargins(25, 25, 25, 25)
        right_layout.setSpacing(20)
        
        header = QLabel("🤖 INDIA EDUCATION ANALYSIS • 28 STATES")
        header.setStyleSheet("""
            color: #ffd700; font-size: 36px; font-weight: bold; padding: 25px; 
            background: rgba(0,0,0,0.8); border: 4px solid #ffd700; border-radius: 25px;
        """)
        header.setAlignment(Qt.AlignCenter)
        right_layout.addWidget(header)
        
        self.detail_frame = QFrame()
        self.detail_frame.setMinimumHeight(450)
        self.detail_frame.setStyleSheet("""
            QFrame { background: rgba(20,30,70,255); border: 3px solid rgba(0,255,136,100); 
                    border-radius: 25px; }
        """)
        self.detail_layout = QVBoxLayout(self.detail_frame)
        
        self.welcome_label = QLabel("👈 CLICK ANY STATE TAB ON LEFT →\nDYNAMIC AI/ML Analysis Loads Here Instantly!")
        self.welcome_label.setStyleSheet("""
            color: #00ff88; font-size: 26px; font-weight: bold; padding: 80px; 
            background: rgba(0,255,136,0.1); border: 3px dashed #00ff88; border-radius: 25px;
        """)
        self.welcome_label.setAlignment(Qt.AlignCenter)
        self.detail_layout.addWidget(self.welcome_label, 1)
        right_layout.addWidget(self.detail_frame)
        
        metrics_layout = QHBoxLayout()
        self.metrics = [
            IndiaMetric("Total Students", "Cr"),
            IndiaMetric("AI Solutions", "K"),
            IndiaMetric("ML Accuracy", "%"),
            IndiaMetric("States Live", "")
        ]
        for metric in self.metrics:
            metrics_layout.addWidget(metric)
        metrics_layout.addStretch()
        right_layout.addLayout(metrics_layout)
        
        self.chart = pg.PlotWidget(title="📈 NATIONAL AI/ML PROGRESS (Real-time)")
        self.chart.setBackground('#0a0a1a')
        self.chart.showGrid(x=True, y=True, alpha=0.4)
        self.chart.setLabel('left', 'Progress %')
        self.chart.setLabel('bottom', 'Time Steps')
        self.curve = self.chart.plot([], [], pen=mkPen('#ffd700', width=4))
        right_layout.addWidget(self.chart)
        
        controls_layout = QHBoxLayout()
        self.status = QLabel("🔴 OFFLINE")
        self.status.setStyleSheet("""
            font-size: 22px; font-weight: bold; color: #ff4757; padding: 20px; 
            background: rgba(255,71,87,0.4); border: 4px solid #ff4757; border-radius: 22px;
        """)
        controls_layout.addWidget(self.status)
        controls_layout.addStretch()
        
        self.start_btn = QPushButton("🚀 START INDIA AI/ML")
        self.start_btn.clicked.connect(self.start_engine)
        self.start_btn.setStyleSheet("""
            QPushButton { background: qlineargradient(45deg, #00ff88, #ffd700); 
                         color: black; font-size: 22px; font-weight: bold; padding: 22px 45px; 
                         border-radius: 25px; border: 4px solid #ffd700; }
            QPushButton:hover { background: qlineargradient(45deg, #00ffaa, #ffed4a); 
                               border: 4px solid #ffffff; transform: scale(1.05); }
            QPushButton:pressed { background: qlineargradient(45deg, #00cc66, #ffcc00); }
        """)
        
        self.stop_btn = QPushButton("⏹️ STOP AI/ML")
        self.stop_btn.clicked.connect(self.stop_engine)
        self.stop_btn.setEnabled(False)
        self.stop_btn.setStyleSheet("""
            QPushButton { background: qlineargradient(45deg, #ff4757, #ff6b6b); 
                         color: white; font-size: 22px; font-weight: bold; padding: 22px 45px; 
                         border-radius: 25px; border: 4px solid #ff4757; }
            QPushButton:hover { background: qlineargradient(45deg, #ff6b6b, #ff8e8e); 
                               border: 4px solid #ffffff; transform: scale(1.05); }
            QPushButton:pressed { background: qlineargradient(45deg, #cc3333, #dd5555); }
        """)
        
        controls_layout.addWidget(self.start_btn)
        controls_layout.addWidget(self.stop_btn)
        right_layout.addLayout(controls_layout)
        
        main_layout.addWidget(right_panel)
        
        self.create_state_tabs()
    
    def create_state_tabs(self):
        for i, state in enumerate(INDIA_STATES):
            tab = VerticalStateTab(state, i)
            tab.stateSelected.connect(self.on_state_selected)
            self.tabs_layout.addWidget(tab)
    
    def on_state_selected(self, state_name):
        self.selected_state = state_name
        for i in reversed(range(self.detail_layout.count())):
            child = self.detail_layout.itemAt(i).widget()
            if child:
                child.setParent(None)
        
        state_detail = {state_name: self.state_data.get(state_name, {})}
        detail_widget = StateDetailWidget(state_detail)
        self.detail_layout.addWidget(detail_widget)
    
    def start_engine(self):
        if self.engine is None or not self.engine.isRunning():
            self.engine = IndiaEngine()
            self.engine.dataReady.connect(self.update_dashboard)
            self.engine.start()
            self.start_btn.setEnabled(False)
            self.stop_btn.setEnabled(True)
            self.status.setText("🟢 LIVE - AI/ML ENGINE RUNNING")
            self.status.setStyleSheet("""
                font-size: 22px; font-weight: bold; color: #00ff88; padding: 20px; 
                background: rgba(0,255,136,0.4); border: 4px solid #00ff88; border-radius: 22px;
            """)
    
    def stop_engine(self):
        if self.engine and self.engine.isRunning():
            self.engine.stop()
            self.engine.wait(1000)
            self.start_btn.setEnabled(True)
            self.stop_btn.setEnabled(False)
            self.status.setText("🔴 OFFLINE")
            self.status.setStyleSheet("""
                font-size: 22px; font-weight: bold; color: #ff4757; padding: 20px; 
                background: rgba(255,71,87,0.4); border: 4px solid #ff4757; border-radius: 22px;
            """)
    
    def update_dashboard(self, data):
        self.state_data = data['states']
        
        metrics = data['metrics']
        self.metrics[0].setValue(metrics['total_students'])
        self.metrics[1].setValue(metrics['ai_solutions'] / 1000)
        self.metrics[2].setValue(metrics['ml_accuracy'])
        self.metrics[3].setValue(metrics['states_covered'])
        
        self.chart_data.append(metrics['progress'])
        if len(self.chart_data) > 50:
            self.chart_data.pop(0)
        self.curve.setData(range(len(self.chart_data)), self.chart_data)
        
        if self.selected_state and self.selected_state in self.state_data:
            for i in range(self.tabs_layout.count()):
                tab = self.tabs_layout.itemAt(i).widget()
                if isinstance(tab, VerticalStateTab) and tab.state_name == self.selected_state:
                    tab.stateSelected.emit(self.selected_state)
                    break
    
    def closeEvent(self, event):
        if self.engine and self.engine.isRunning():
            self.engine.stop()
            self.engine.wait(1000)
        event.accept()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)
    
    dashboard = IndiaDashboard()
    dashboard.show()
    
    sys.exit(app.exec_())
        