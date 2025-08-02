from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QHBoxLayout, QLabel
import webbrowser

class EngineeringToolsPage(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()

        # Título da aba
        # Categoria: Simuladores de Reações Químicas
        self.create_category("Simuladores de Reações Químicas", [
            ("ChemPy - Biblioteca Python para Cálculos Químicos", "https://chemPy.readthedocs.io/"),
            ("ChemSpider - Banco de Dados de Química", "http://www.chemspider.com/")
        ], layout)

        # Categoria: Sistemas de IA e Otimização
        self.create_category("Sistemas de IA e Otimização", [
            ("OpenAI - ChatGPT para Modelos Químicos", "https://chatgpt.openai.com/"),
            ("MATLAB-simulação matemátoca de processso","https://www.mathworks.com/products/matlab.html")
        ], layout)

        # Categoria: Periódicos Científicos
        self.create_category("Periódicos Científicos", [
            ("Periódicos CAPES", "https://www.periodicos.capes.gov.br/"),
            ("Elsevier Journals", "https://www.journals.elsevier.com/"),
            ("SpringerLink - Artigos Científicos", "https://link.springer.com/")
        ], layout)

        # Categoria: Laboratórios Virtuais
        self.create_category("Laboratórios Virtuais", [
            ("Labster - Simulações de Laboratório", "https://www.labster.com/"),
            ("DeepChem","https://deepchem.io")
        ], layout)

        # Categoria: Simuladores de Processos Químicos
        self.create_category("Simuladores de Processos Químicos", [
            ("Aspen Plus - Simulação de Processos", "https://www.aspentech.com/en/resources/aspen-plus"),
            ("HYSYS - Simulação de Processos", "https://www.aspentech.com/en/resources/hysys")
        ], layout)

        # Botão de voltar para a aba principal
        
        
        

        self.setLayout(layout)

    def create_category(self, category_name, links, layout):
        category_label = QLabel(category_name)
        category_label.setStyleSheet("font-size: 16px; font-weight: bold; color: #00FFFF; margin-top: 10px;")
        layout.addWidget(category_label)

        button_layout = QVBoxLayout()

        for name, url in links:
            button = QPushButton(name)
            button.clicked.connect(lambda _, link=url: self.open_link(link))
            button.setStyleSheet("""
                QPushButton {
                    background-color: #2D2D2D;
                    color: #FFFFFF;
                    padding: 10px;
                    font-size: 14px;
                    text-align: left;
                    border: none;
                }
                QPushButton:hover {
                    background-color: #444444;
                    color: #00FFFF;
                }
            """)
            button_layout.addWidget(button)

        layout.addLayout(button_layout)

    def open_link(self, url):
        webbrowser.open(url)

    def back_to_main(self):
        # Lógica para voltar para a página principal
        print("Voltando para a página principal.")