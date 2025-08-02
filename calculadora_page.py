from PyQt6.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QComboBox,
    QLineEdit, QPushButton, QMessageBox, QFormLayout, QFrame
)
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt
import math

class CalculadoraQuimicaPage(QWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("""
            QWidget {
                background-color: #1e1e1e;
                color: #ffffff;
                font-family: Arial;
                font-size: 14px;
            }
            QComboBox, QLineEdit {
                background-color: #2e2e2e;
                color: #ffffff;
                padding: 6px;
                border-radius: 6px;
                border: 1px solid #555;
            }
            QPushButton {
                background-color: #007acc;
                color: white;
                padding: 8px 20px;
                font-weight: bold;
                border-radius: 6px;
            }
            QPushButton:hover {
                background-color: #005f99;
            }
        """)

        
        layout_principal = QVBoxLayout()
        layout_principal.setAlignment(Qt.AlignmentFlag.AlignTop)
        layout_principal.setSpacing(25)
        layout_principal.setContentsMargins(30, 20, 30, 20)

        self.title = QLabel("Calculadora")
        self.title.setStyleSheet("font-size: 20px; font-weight: bold; background-color: transparent; color: #00FFFF;")
        layout_principal.addWidget(self.title)

        self.blocos = [
            ("🧪 Cálculos Químicos", self.atualizar_campos_quimica, self.calcular_quimica, "combo_quimica", "form_quimica", "resultado_quimica", [
                "Molaridade", "Molalidade", "Normalidade", "% em massa", "% em volume", "% m/v",
                "PPM", "PPB", "Fração molar", "Fração em massa", "Fração em volume",
                "Densidade", "Massa molar", "Concentração comum", "Concentração em mol/L",
                "Concentração equivalente", "Título em massa", "Título em volume",
                "Massa específica", "Volume molar (CNTP)", "Pressão osmótica", "pH", "pOH",
                "Ka", "Kb", "Kw", "Equivalente grama", "Peso equivalente", "Grau de ionização",
                "Número de oxidação", "Constante de dissociação", "Capacidade térmica",
                "Calor sensível", "Calor latente", "Solubilidade", "Rendimento da reação",
                "Pureza", "Diluição (C1V1 = C2V2)", "Velocidade da reação",
                "Número de Avogadro"
            ]),
            ("🔁 Conversões SI", self.atualizar_campos_conv, self.calcular_conv, "combo_convert", "form_conv", "resultado_conv", [
                "g para kg", "kg para g", "mg para g", "g para mg",
                "L para mL", "mL para L", "cm³ para mL", "mL para cm³",
                "m/s para km/h", "km/h para m/s", "atm para mmHg", "mmHg para atm",
                "atm para Pa", "Pa para atm", "J para cal", "cal para J",
                "°C para K", "K para °C", "cm² para m²", "m² para cm²"
            ]),
            ("📘 Cálculos Avançados", self.atualizar_campos_extra, self.calcular_extra, "combo_extra", "form_extra", "resultado_extra", [
                "Energia livre de Gibbs", "Lei dos gases ideais", "Volume em gases ideais",
                "Equilíbrio químico (Kp)", "Equilíbrio químico (Kc)", "Lei de Hess",
                "Velocidade média (m/s)", "Força (2ª lei de Newton)", "Trabalho de uma força",
                "Ponto de fusão estimado (°C)", "Ponto de ebulição estimado (°C)",
                "Entalpia de fusão (kJ/mol)", "Entalpia de vaporização (kJ/mol)",
                "Entropia (J/mol·K)", "Energia de ligação (kJ/mol)", "Ponto crítico estimado",
                "Temperatura de autoignição", "Índice de refração estimado",
                "Condutividade elétrica (S/m)"
            ])
        ]

        for titulo, atualiza, calcula, combo_attr, form_attr, resultado_attr, opcoes in self.blocos:
            bloco = QFrame()
            bloco.setStyleSheet("QFrame { background-color: #2b2b3d; border-radius: 12px; }")
            bloco_layout = QVBoxLayout(bloco)
            bloco_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
            bloco_layout.setContentsMargins(20, 20, 20, 20)
            bloco_layout.setSpacing(15)

            label = QLabel(titulo)
            label.setFont(QFont("Arial", 16, QFont.Weight.Bold))
            label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            bloco_layout.addWidget(label)

            combo = QComboBox()
            combo.addItems(opcoes)
            combo.setFixedWidth(250)
            bloco_layout.addWidget(combo, alignment=Qt.AlignmentFlag.AlignCenter)

            form = QFormLayout()
            bloco_layout.addLayout(form)

            btn = QPushButton("Calcular" if "quimica" in combo_attr else "Converter")
            btn.clicked.connect(calcula)
            bloco_layout.addWidget(btn, alignment=Qt.AlignmentFlag.AlignCenter)

            resultado = QLabel("Resultado:")
            resultado.setAlignment(Qt.AlignmentFlag.AlignCenter)
            bloco_layout.addWidget(resultado)

            setattr(self, combo_attr, combo)
            setattr(self, form_attr, form)
            setattr(self, resultado_attr, resultado)

            combo.currentIndexChanged.connect(atualiza)
            layout_principal.addWidget(bloco)

        self.setLayout(layout_principal)
        self.atualizar_campos_quimica()
        self.atualizar_campos_conv()
        self.atualizar_campos_extra()

    def atualizar_formulario(self, layout, campos):
        parent = layout.parentWidget()
        parent.entradas = []
        while layout.rowCount():
            layout.removeRow(0)
        for campo in campos:
            entrada = QLineEdit()
            entrada.setPlaceholderText(campo)
            layout.addRow(campo, entrada)
            parent.entradas.append(entrada)

    def atualizar_campos_quimica(self):
        campos = {
            "Molaridade": ["Mol", "L"],
            "Molalidade": ["Mol", "kg"],
            "Densidade": ["g", "mL"],
            "pH": ["[H⁺]"],
            "Diluição (C1V1 = C2V2)": ["C1", "V1", "C2 ou V2"]
        }
        chave = self.combo_quimica.currentText()
        self.atualizar_formulario(self.form_quimica, campos.get(chave, ["Valor 1", "Valor 2"]))

    def atualizar_campos_conv(self):
        self.atualizar_formulario(self.form_conv, ["Valor"])

    def atualizar_campos_extra(self):
        campos = {
            "Energia livre de Gibbs": ["ΔH", "T", "ΔS"],
            "Volume em gases ideais": ["n", "R", "T", "P"]
        }
        chave = self.combo_extra.currentText()
        self.atualizar_formulario(self.form_extra, campos.get(chave, ["Valor 1", "Valor 2"]))

    def calcular_quimica(self):
        try:
            v = [float(e.text()) for e in self.form_quimica.parent().entradas]
            op = self.combo_quimica.currentText()
            resultado = {
                "Molaridade": lambda mol, vol: mol / vol,
                "Molalidade": lambda mol, kg: mol / kg,
                "Densidade": lambda m, v: m / v,
                "pH": lambda H: -1 * math.log10(H),
                "Diluição (C1V1 = C2V2)": lambda C1, V1, C2=None, V2=None: C1 * V1 / C2 if V2 is None else C1 * V1 / V2 if C2 is None else None,
            }.get(op, lambda *x: sum(x))  # padrão: soma
            self.resultado_quimica.setText(f"Resultado: {resultado(*v):.4g}")
        except Exception as e:
            QMessageBox.critical(self, "Erro no cálculo químico", str(e))

    def calcular_conv(self):
        try:
            val = float(self.form_conv.parent().entradas[0].text())
            op = self.combo_convert.currentText()
            resultado = {
                "g para kg": lambda g: g / 1000,
                "kg para g": lambda kg: kg * 1000,
                "°C para K": lambda c: c + 273.15,
                "K para °C": lambda k: k - 273.15
            }.get(op, lambda x: x)
            self.resultado_conv.setText(f"Resultado: {resultado(val):.4g}")
        except Exception as e:
            QMessageBox.critical(self, "Erro na conversão", str(e))

    def calcular_extra(self):
        try:
            v = [float(e.text()) for e in self.form_extra.parent().entradas]
            op = self.combo_extra.currentText()
            resultado = {
                "Energia livre de Gibbs": lambda dh, t, ds: dh - t * ds,
                "Volume em gases ideais": lambda n, R, T, P: (n * R * T) / P
            }.get(op, lambda *x: sum(x))
            self.resultado_extra.setText(f"Resultado: {resultado(*v):.4g}")
        except Exception as e:
            QMessageBox.critical(self, "Erro nos cálculos avançados", str(e))
