from PyQt6.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QComboBox,
    QLineEdit, QPushButton, QMessageBox, QFormLayout, QHBoxLayout
)
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt
import webbrowser
import math


class CalculadoraQuimicaPage(QWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("background-color: #2D2D2D;")

        layout_principal = QVBoxLayout()
        layout_principal.setAlignment(Qt.AlignmentFlag.AlignTop)

        # ====== 1. BLOCO: Cálculos Químicos ======
        bloco1 = self.blocos_titulo("🧪 Calculadora Química")
        self.combo_quimica = self.novo_combo([
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
        ])
        self.combo_quimica.currentIndexChanged.connect(
            self.atualizar_campos_quimica)
        bloco1.addWidget(self.combo_quimica,
                         alignment=Qt.AlignmentFlag.AlignHCenter)

        self.form_quimica = QFormLayout()
        bloco1.addLayout(self.form_quimica)

        self.btn_quimica = self.novo_botao("Calcular", self.calcular_quimica)
        bloco1.addWidget(self.btn_quimica,
                         alignment=Qt.AlignmentFlag.AlignHCenter)

        self.resultado_quimica = self.novo_resultado()
        bloco1.addWidget(self.resultado_quimica)

        layout_principal.addLayout(bloco1)

        # ====== 2. BLOCO: Conversões SI ======
        bloco2 = self.blocos_titulo("🔁 Conversões de Unidades (SI)")
        self.combo_convert = self.novo_combo([
            "g para kg",
            "kg para g",
            "mg para g",
            "g para mg",
            "L para mL",
            "mL para L",
            "cm³ para mL",
            "mL para cm³",
            "m/s para km/h",
            "km/h para m/s",
            "atm para mmHg",
            "mmHg para atm",
            "atm para Pa",
            "Pa para atm",
            "J para cal",
            "cal para J",
            "°C para K",
            "K para °C",
            "cm² para m²",
            "m² para cm²",
        ])
        self.combo_convert.currentIndexChanged.connect(
            self.atualizar_campos_conv)
        bloco2.addWidget(self.combo_convert,
                         alignment=Qt.AlignmentFlag.AlignHCenter)

        self.form_conv = QFormLayout()
        bloco2.addLayout(self.form_conv)

        self.btn_conv = self.novo_botao("Converter", self.calcular_conv)
        bloco2.addWidget(
            self.btn_conv, alignment=Qt.AlignmentFlag.AlignHCenter)

        self.resultado_conv = self.novo_resultado()
        bloco2.addWidget(self.resultado_conv)

        layout_principal.addLayout(bloco2)

        # ====== 3. BLOCO: Cálculos Avançados ======
        bloco3 = self.blocos_titulo("📘 Cálculos Avançados")
        self.combo_extra = self.novo_combo([
            "Energia livre de Gibbs",
            "Lei dos gases ideais",
            "Volume em gases ideais",
            "Equilíbrio químico (Kp)",
            "Equilíbrio químico (Kc)",
            "Lei de Hess",
            "Velocidade média (m/s)",
            "Força (2ª lei de Newton)",
            "Trabalho de uma força",

            # Bloco 3 (físico-químicos e estimativas):
            "Ponto de fusão estimado (°C)",
            "Ponto de ebulição estimado (°C)",
            "Entalpia de fusão (kJ/mol)",
            "Entalpia de vaporização (kJ/mol)",
            "Entropia (J/mol·K)",
            "Energia de ligação (kJ/mol)",
            "Ponto crítico estimado",
            "Temperatura de autoignição",
            "Índice de refração estimado",
            "Condutividade elétrica (S/m)",
        ])
        self.combo_extra.currentIndexChanged.connect(
            self.atualizar_campos_extra)
        bloco3.addWidget(self.combo_extra,
                         alignment=Qt.AlignmentFlag.AlignHCenter)

        self.form_extra = QFormLayout()
        bloco3.addLayout(self.form_extra)

        self.btn_extra = self.novo_botao("Calcular", self.calcular_extra)
        bloco3.addWidget(
            self.btn_extra, alignment=Qt.AlignmentFlag.AlignHCenter)

        self.resultado_extra = self.novo_resultado()
        bloco3.addWidget(self.resultado_extra)

        layout_principal.addLayout(bloco3)

        # Finalizando layout
        self.setLayout(layout_principal)
        self.atualizar_campos_quimica()
        self.atualizar_campos_conv()
        self.atualizar_campos_extra()
        # -----------------Botao calculadora-------------#
        self.setLayout(layout_principal)
        btn_calc = QPushButton("Calculadora online")
        btn_calc.clicked.connect(self._abrir_calc)
        layout_principal.addWidget(btn_calc)
        btn_calc.setStyleSheet("""
        QPushButton {
        font-size: 11px;
        padding: 4px 8px;
        min-width: 80px;
        max-width: 120px;
        }
       """)

    # ======= Componentes de Interface ========
    def blocos_titulo(self, texto):
        layout = QVBoxLayout()
        label = QLabel(texto)
        label.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        label.setStyleSheet("color: #FFFFFF")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(label)
        return layout

    def novo_combo(self, opcoes):
        combo = QComboBox()
        combo.addItems(opcoes)
        combo.setFixedWidth(250)
        combo.setStyleSheet("padding: 6px; font-size: 14px; color: #FFFFFF")
        return combo

    def novo_botao(self, texto, funcao):
        botao = QPushButton(texto)
        botao.clicked.connect(funcao)
        botao.setStyleSheet("""
            QPushButton {
                background-color: #007ACC;
                color: #FFFFFF;
                padding: 8px 20px;
                font-weight: bold;
                font-size: 14px;
                border-radius: 6px;
            }
            QPushButton:hover {
                background-color: #005F99;
            }
        """)  # FFFFFF é o HEX code pra branco
        return botao

    def novo_resultado(self):
        label = QLabel("Resultado: ")
        label.setFont(QFont("Arial", 12))
        label.setStyleSheet("color: #cccccc; font-weight: bold;")
        # Assim centraliza o resultado, ele "descola" da linha e fica mais "bonito"
        label.setContentsMargins(0, 8, 0, 8)
        label.setAlignment(Qt.AlignmentFlag.AlignHCenter |
                           Qt.AlignmentFlag.AlignVCenter)
        return label

    def atualizar_campos_quimica(self):
        campos = {
            "Molaridade": ["Moles do soluto (mol)", "Volume da solução (L)"],
            "Molalidade": ["Moles do soluto (mol)", "Massa do solvente (kg)"],
            "Normalidade": ["Equivalentes do soluto", "Volume da solução (L)"],
            "% em massa": ["Massa do soluto (g)", "Massa da solução (g)"],
            "% em volume": ["Volume do soluto (mL)", "Volume da solução (mL)"],
            "% m/v": ["Massa do soluto (g)", "Volume da solução (mL)"],
            "PPM": ["Massa do soluto (mg)", "Massa da solução (kg)"],
            "PPB": ["Massa do soluto (µg)", "Massa da solução (kg)"],
            "Fração molar": ["Moles do componente A", "Moles totais da mistura"],
            "Fração em massa": ["Massa do componente A (g)", "Massa total da mistura (g)"],
            "Fração em volume": ["Volume do componente A (mL)", "Volume total da mistura (mL)"],
            "Densidade": ["Massa (g)", "Volume (mL)"],
            "Massa molar": ["Massa (g)", "Quantidade de substância (mol)"],
            "Concentração comum": ["Massa do soluto (g)", "Volume da solução (L)"],
            "Concentração em mol/L": ["Quantidade de matéria (mol)", "Volume da solução (L)"],
            "Concentração equivalente": ["Número de equivalentes", "Volume (L)"],
            "Título em massa": ["Massa do soluto (g)", "Massa da solução (g)"],
            "Título em volume": ["Volume do soluto (mL)", "Volume da solução (mL)"],
            "Massa específica": ["Massa (g)", "Volume (cm³)"],
            "Volume molar (CNTP)": ["Quantidade de matéria (mol)"],
            "Pressão osmótica": ["Molaridade (mol/L)", "Temperatura (K)"],
            "pH": ["Concentração de H⁺ (mol/L)"],
            "pOH": ["Concentração de OH⁻ (mol/L)"],
            "Ka": ["[H⁺]", "[A⁻]", "[HA]"],
            "Kb": ["[OH⁻]", "[B⁺]", "[BOH]"],
            "Kw": ["[H⁺]", "[OH⁻]"],
            "Equivalente grama": ["Massa (g)", "Peso equivalente (g/eq)"],
            "Peso equivalente": ["Massa molar (g/mol)", "Número de elétrons ou íons trocados"],
            "Grau de ionização": ["Concentração ionizada", "Concentração inicial"],
            "Número de oxidação": ["Número total de elétrons ganhos ou perdidos", "Número de átomos"],
            "Constante de dissociação": ["Concentração dos produtos", "Concentração dos reagentes"],
            "Capacidade térmica": ["Calor (J)", "Variação de temperatura (°C)"],
            "Calor sensível": ["Massa (g)", "Capacidade térmica (J/g°C)", "ΔT (°C)"],
            "Calor latente": ["Massa (g)", "Calor latente (J/g)"],
            "Solubilidade": ["Massa dissolvida (g)", "Volume do solvente (L)"],
            "Rendimento da reação": ["Massa experimental (g)", "Massa teórica (g)"],
            "Pureza": ["Massa da substância pura (g)", "Massa total da amostra (g)"],
            "Diluição (C1V1 = C2V2)": ["C1", "V1", "C2 ou V2 (preencher 3 de 4 valores)"],
            "Velocidade da reação": ["Variação da concentração (mol/L)", "Variação do tempo (s)"],
            "Número de Avogadro": ["Número de partículas", "Número de mols"]
        }
        self.atualizar_formulario(
            self.form_quimica, campos[self.combo_quimica.currentText()])

    def atualizar_campos_conv(self):
        self.atualizar_formulario(self.form_conv, ["Valor"])

    def atualizar_campos_extra(self):
        campos = {
            "Energia livre de Gibbs": ["ΔH (kJ/mol)", "T (K)", "ΔS (J/mol·K)"],
            "Lei dos gases ideais": ["n (mol)", "R (0.0821)", "T (K)", "P (atm)", "V (L)"],
            "Volume em gases ideais": ["n (mol)", "R", "T (K)", "P (atm)"],
            "Equilíbrio químico (Kp)": ["Pressão produtos", "Pressão reagentes"],
            "Equilíbrio químico (Kc)": ["[produtos]", "[reagentes]"],
            "Lei de Hess": ["ΔH1", "ΔH2", "ΔH3"],
            "Velocidade média (m/s)": ["d (m)", "Δt (s)"],
            "Força (2ª lei de Newton)": ["m (kg)", "a (m/s²)"],
            "Trabalho de uma força": ["F (N)", "d (m)", "cos(θ)"],

            # Bloco 3 (físico-químicos e estimativas):
            "Ponto de fusão estimado (°C)": ["Composto", "Estimativa"],
            "Ponto de ebulição estimado (°C)": ["Composto", "Estimativa"],
            "Entalpia de fusão (kJ/mol)": ["Composto", "ΔHfus"],
            "Entalpia de vaporização (kJ/mol)": ["Composto", "ΔHvap"],
            "Entropia (J/mol·K)": ["Composto", "S"],
            "Energia de ligação (kJ/mol)": ["Ligação", "Energia"],
            "Ponto crítico estimado": ["Tc (K)", "Pc (atm)"],
            "Temperatura de autoignição": ["Composto", "Temperatura"],
            "Índice de refração estimado": ["Composto", "Índice n"],
            "Condutividade elétrica (S/m)": ["Material", "Condutividade"],
        }
        self.atualizar_formulario(
            self.form_extra, campos[self.combo_extra.currentText()])

    def atualizar_formulario(self, layout, campos):
        for i in reversed(range(layout.rowCount())):
            layout.removeRow(i)
        layout.parent().entradas = []
        for label in campos:
            entrada = QLineEdit()
            entrada.setPlaceholderText(label)
            entrada.setFixedWidth(200)
            entrada.setStyleSheet(
                "padding: 5px; font-size: 13px; color: #FFFFFF")

            layout.parent().entradas.append(entrada)
            label_widget = QLabel(label)
            label_widget.setStyleSheet(
                "color: #FFFFFF; font-size: 13px; font-weight: bold;")
            layout.addRow(label_widget, entrada)

    # ========= Cálculos ==========

    def calcular_quimica(self):
        try:
            v = [float(e.text()) for e in self.form_quimica.parent().entradas]
            op = self.combo_quimica.currentText()
            f = {
                "Molaridade": lambda mol, vol: mol / vol,
                "Molalidade": lambda mol, kg: mol / kg,
                "Normalidade": lambda eq, vol: eq / vol,
                "% em massa": lambda ms, msol: (ms / msol) * 100,
                "% em volume": lambda vs, vsol: (vs / vsol) * 100,
                "% m/v": lambda ms, vsol: (ms / vsol) * 100,
                "PPM": lambda mg, kg: (mg / (kg * 1e6)) * 1e6,
                "PPB": lambda ug, kg: (ug / (kg * 1e9)) * 1e9,
                "Fração molar": lambda molA, molTot: molA / molTot,
                "Fração em massa": lambda mA, mTot: mA / mTot,
                "Fração em volume": lambda vA, vTot: vA / vTot,
                "Densidade": lambda m, v: m / v,
                "Massa molar": lambda m, mol: m / mol,
                "Concentração comum": lambda m, v: m / v,
                "Concentração em mol/L": lambda mol, vol: mol / vol,
                "Concentração equivalente": lambda eq, vol: eq / vol,
                "Título em massa": lambda mSol, mTot: mSol / mTot,
                "Título em volume": lambda vSol, vTot: vSol / vTot,
                "Massa específica": lambda m, v: m / v,
                "Volume molar (CNTP)": lambda mol: mol * 22.4,
                "Pressão osmótica": lambda M, T: 0.0821 * M * T,
                "pH": lambda H: -1 * (math.log10(H)),
                "pOH": lambda OH: -1 * (math.log10(OH)),
                "Ka": lambda H, A, HA: (H * A) / HA,
                "Kb": lambda OH, B, BOH: (OH * B) / BOH,
                "Kw": lambda H, OH: H * OH,
                "Equivalente grama": lambda m, peq: m / peq,
                "Peso equivalente": lambda mm, n: mm / n,
                "Grau de ionização": lambda ci, c0: (ci / c0) * 100,
                "Número de oxidação": lambda ne, na: ne / na,
                "Constante de dissociação": lambda prod, reag: prod / reag,
                "Capacidade térmica": lambda q, dt: q / dt,
                "Calor sensível": lambda m, c, dt: m * c * dt,
                "Calor latente": lambda m, L: m * L,
                "Solubilidade": lambda mSol, vol: mSol / vol,
                "Rendimento da reação": lambda exp, teo: (exp / teo) * 100,
                "Pureza": lambda mp, mt: (mp / mt) * 100,
                "Diluição (C1V1 = C2V2)": lambda C1, V1, C2=None, V2=None: C1 * V1 / C2 if V2 is None else C1 * V1 / V2 if C2 is None else None,
                "Velocidade da reação": lambda dc, dt: dc / dt,
                "Número de Avogadro": lambda Np, mol: Np / mol
            }[op]
            self.resultado_quimica.setText(f"Resultado: {f(*v):.4g}")
        except Exception as e:
            QMessageBox.critical(self, "Erro", str(e))

    def calcular_conv(self):
        try:
            val = float(self.form_conv.parent().entradas[0].text())
            op = self.combo_convert.currentText()
            f = {
                "g para kg": lambda g: g / 1000,
                "kg para g": lambda kg: kg * 1000,
                "mg para g": lambda mg: mg / 1000,
                "g para mg": lambda g: g * 1000,
                "L para mL": lambda L: L * 1000,
                "mL para L": lambda mL: mL / 1000,
                "cm³ para mL": lambda cm3: cm3 * 1.0,
                "mL para cm³": lambda mL: mL * 1.0,
                "m/s para km/h": lambda ms: ms * 3.6,
                "km/h para m/s": lambda kmh: kmh / 3.6,
                "atm para mmHg": lambda atm: atm * 760,
                "mmHg para atm": lambda mmHg: mmHg / 760,
                "atm para Pa": lambda atm: atm * 101325,
                "Pa para atm": lambda pa: pa / 101325,
                "J para cal": lambda j: j / 4.184,
                "cal para J": lambda cal: cal * 4.184,
                "°C para K": lambda c: c + 273.15,
                "K para °C": lambda k: k - 273.15,
                "cm² para m²": lambda cm2: cm2 / 10000,
                "m² para cm²": lambda m2: m2 * 10000
            }[op]
            self.resultado_conv.setText(f"Resultado: {f(val):.4g}")
        except Exception as e:
            QMessageBox.critical(self, "Erro", str(e))

    def calcular_extra(self):
        try:
            v = [float(e.text()) for e in self.form_extra.parent().entradas]
            op = self.combo_extra.currentText()
            f = {
                "Energia livre de Gibbs": lambda dh, t, ds: dh - t * ds,
                "Lei dos gases ideais": lambda n, R, T, V: (n * R * T) / V,
                "Pressão em gases ideais": lambda n, R, T, V: (n * R * T) / V,
                "Volume em gases ideais": lambda n, R, T, P: (n * R * T) / P,
                "Equilíbrio químico (Kc)": lambda p, r: p / r,
                "Equilíbrio químico (Kp)": lambda pp, pr: pp / pr,
                "Lei de Hess": lambda dh1, dh2, dh3: dh1 + dh2 + dh3,
                "Velocidade média": lambda dx, dt: dx / dt,
                "Força (2ª Lei de Newton)": lambda m, a: m * a,
                "Trabalho de uma força": lambda f, d, cos: f * d * cos
            }[op]
            self.resultado_extra.setText(f"Resultado: {f(*v):.4g}")
        except Exception as e:
            QMessageBox.critical(self, "Erro", str(e))

    def _abrir_calc(self):
        webbrowser.open("https://www.calculadoraonline.com.br/cientifica")
