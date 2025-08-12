# -*- coding: utf-8 -*-
import sys, re
import pandas as pd
from unidecode import unidecode
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from PyQt6.QtCore import Qt, QRect
from PyQt6.QtWidgets import (
    QApplication, QWidget, QPlainTextEdit, QLineEdit, QPushButton, QFrame, QMessageBox
)
import webbrowser


CSV_URL = "https://raw.githubusercontent.com/tmelo-uea/cursos/main/dataset.csv"  # mesmo banco de dados


# ------------------------- util: NLP simples (sem NLTK) -------------------------
_PT_STOPWORDS = {
    
    'a', 'à', 'ao', 'aos', 'às', 'as', 'o', 'os', 'da', 'das', 'de', 'do', 'dos', 'e', 'é', 'em', 'no', 'na', 'nos', 'nas', 'que', 'com', 'para', 'por', 
    'um', 'uma', 'uns', 'umas', 'se', 'sem', 'há', 'houve', 'era', 'ser', 'são', 'sou', 'está', 'estão', 'estar', 'foi', 'fui', 'vai', 'vão', 'vamos', 'como', 
    'mas', 'ou', 'quando', 'onde', 'porque', 'porquê', 'me', 'te', 'seu', 'sua', 'seus', 'suas', 'minha', 'meu', 'minhas', 'meus', 'lhe', 'eles', 'elas', 'ele', 
    'ela', 'você', 'vocês', 'depois', 'antes', 'muito', 'muita', 'muitos', 'muitas', 'também', 'já', 'não', 'sim', 'isso', 'isto', 'aquela', 'aquelas', 'aquilo', 
    'este', 'estes', 'estas', 'essa', 'essas', 'esse', 'esses', 'em', 'nem', 'mas', 'assim', 'também', 'ainda', 'logo', 'entre', 'apenas', 'ou', 'além', 'como', 
    'quanto', 'qual', 'quantos', 'quais', 'qualquer', 'algum', 'alguma', 'alguns', 'algumas', 'mesmo', 'mesma', 'mesmas', 'próprio', 'própria', 'próprios', 'próprias', 
    'nós', 'nosso', 'nossos', 'nossa', 'nossas', 'que', 'qual', 'quem', 'se', 'tudo', 'todos', 'todas', 'alguns', 'aquelas', 'aquela', 'algumas', 'nenhum', 'nenhuma', 
    'ninguém', 'tanto', 'tantos', 'tanta', 'tantas', 'sobre', 'até', 'outro', 'outra', 'outros', 'outras', 'logo', 'mesmo', 'assim', 'não', 'também', 'demais', 'fora', 
    'aqui', 'lá', 'dentro', 'fora', 'então', 'já', 'mais', 'menos', 'em vez', 'fazendo', 'faz', 'fez', 'feito', 'tem', 'ter', 'tinha', 'tenho', 'temos', 'fui', 'ir', 'ficar', 
    'voltar', 'deixar', 'agora', 'ainda', 'então', 'contudo', 'desse', 'dessa', 'desses', 'dessas', 'cada', 'qualquer', 'porque', 'porquê', 'porém', 'seja', 'se', 'os', 
    'àquela', 'nós', 'você', 'que', 'aqueles', 'muitas', 'muitos', 'pelo', 'pelos', 'pela', 'pelas', 'um', 'uma', 'uns', 'umas', 'do', 'da', 'dos', 'das', 'na', 'nas', 
    'no', 'nos', 'por', 'para', 'até', 'entre', 'acima', 'abaixo', 'algumas', 'somente', 'agora', 'passado', 'lá', 'devido', 'daquele', 'daquelas', 'de todas', 'muito', 
    'mas', 'menos', 'maior', 'menor', 'maiores', 'menores', 'novos', 'velhos', 'futuro', 'conforme', 'tudo', 'tal', 'é', 'não', 'não','mas', 'porque', 'pode','tem', 
    'alguns','alguma','outro','de','fez', 'maior', 'devido', 'ainda','tal','assim','começar', 'isso', 'lugar','quanto', 'para','cada','esse','muitas','menos',
    'menores','porém','novo', 'último', 'determinados', 'mesmo', 'esses','isso', 'não', 'então', 'contudo', 'passado', 'pra', 'ir','este','essas','ele', 'mesmo',
    'essa','este','cada','alguma','todas','uma','mesmo','porque','sim','aquilo','esses','ninguém','tão','quem','quando','como','sim','toda','as','muito','alguns',
    'com','quem','você','porém','também','está','os','esses','porém','não','havia','portanto','ainda','as','do','uma','com','tão','outros','aquela','como', 
    
}

_token_re = re.compile(r"[A-Za-zÀ-ÖØ-öø-ÿ0-9]+")

def preprocess(text: str) -> str:
    if not isinstance(text, str):
        return ""
    text = unidecode(text.lower())
    tokens = _token_re.findall(text)
    tokens = [t for t in tokens if t not in _PT_STOPWORDS and len(t) > 1]
    return " ".join(tokens)


# ------------------------- App -------------------------
class ChatbotApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Chatbot + Botões Flutuantes")
        self.resize(920, 580)

        # --- Chat container central ---
        self.chat_container = QFrame(self)
        self.chat_container.setStyleSheet("QFrame{background:#f4f6f8;border-radius:12px;border:1px solid #e1e5ea;}")

        # área de conversa
        self.chat_area = QPlainTextEdit(self.chat_container)
        self.chat_area.setReadOnly(True)
        self.chat_area.setStyleSheet("QPlainTextEdit{border:none;background:transparent;font:12pt 'Segoe UI';}")

        # entrada + enviar
        self.input = QLineEdit(self.chat_container)
        self.input.setPlaceholderText("Digite sua pergunta…")
        self.input.returnPressed.connect(self.on_send)
        self.btn_send = QPushButton("Enviar", self.chat_container)
        self.btn_send.clicked.connect(self.on_send)
        self.btn_send.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_send.setStyleSheet(
            "QPushButton{background:#0ea5e9;color:white;border:none;border-radius:8px;padding:8px 14px;}"
            "QPushButton:hover{background:#0284c7;}"
        )

        # cria botões flutuantes (filhos da janela, não do layout)
        self.float_buttons = []
        self._make_float_buttons()

        # carrega dados + modelo
        self._load_dataset_and_model()

        # primeiro layout/posicionamento
        self._layout_children()

    # --------- dados/modelo ---------
    def _load_dataset_and_model(self):
        try:
            df = pd.read_csv(CSV_URL, delimiter=';')
        except Exception as e:
            QMessageBox.critical(self, "Erro ao ler CSV",
                                 f"Não consegui carregar o CSV do GitHub.\n\n{e}\n\n"
                                 f"URL: {CSV_URL}")
            # fallback mínimo para não quebrar a UI
            df = pd.DataFrame({"Pergunta": ["olá"], "Resposta": ["Olá! Como posso ajudar?"]})

        # valida colunas
        for col in ("Pergunta", "Resposta"):
            if col not in df.columns:
                raise RuntimeError(f"CSV precisa ter as colunas 'Pergunta' e 'Resposta'. Faltou: {col}")

        # preprocess
        df["Pergunta_Preprocessado"] = df["Pergunta"].map(preprocess)
        self.df = df

        # vetorização
        self.vectorizer = TfidfVectorizer()
        self.tfidf_matrix = self.vectorizer.fit_transform(self.df["Pergunta_Preprocessado"])

    def _answer(self, user_text: str) -> str:
        if not user_text.strip():
            return ""
        q = preprocess(user_text)
        if not q:
            return "Pode reformular sua pergunta? 🙂"
        q_vec = self.vectorizer.transform([q])
        sims = cosine_similarity(q_vec, self.tfidf_matrix)[0]
        idx = int(sims.argmax())
        return str(self.df["Resposta"].iloc[idx])

    # --------- UI helpers ---------
    def _make_float_buttons(self):
        links = [
            ("ChemPy Docs", "https://chempy.readthedocs.io/"),
            ("ChemSpider", "http://www.chemspider.com/"),
            ("SpringerLink", "https://link.springer.com/"),
            ("OpenAI ChatGPT", "https://chat.openai.com/"),
        ]
        style = (
            "QPushButton{background:#1f2937;color:#e5e7eb;border-radius:8px;padding:8px 10px;}"
            "QPushButton:hover{background:#374151;color:#67e8f9;}"
        )
        for text, url in links:
            b = QPushButton(text, self)
            b.setStyleSheet(style)
            b.setCursor(Qt.CursorShape.PointingHandCursor)
            b.clicked.connect(lambda _, u=url: webbrowser.open(u))
            b.resize(170, 38)
            self.float_buttons.append(b)

    def _layout_children(self):
        # centraliza o chat_container e posiciona filhos internos
        w, h = self.width(), self.height()
        cw, ch = 600, 360  # tamanho do container
        cx = (w - cw) // 2
        cy = (h - ch) // 2
        self.chat_container.setGeometry(QRect(cx, cy, cw, ch))

        # internos do container
        pad = 12
        self.chat_area.setGeometry(pad, pad, cw - 2*pad, ch - 100)
        self.input.setGeometry(pad, ch - 76, cw - 2*pad - 110, 40)
        self.btn_send.setGeometry(cw - pad - 100, ch - 76, 100, 40)

        # botões flutuantes ao redor do container (quatro cantos)
        gap = 14
        bx, by = self.chat_container.x(), self.chat_container.y()
        bw, bh = self.float_buttons[0].width(), self.float_buttons[0].height()

        # TL, TR, BL, BR (fora dos cantos do container)
        positions = [
            (bx - bw - gap,            by),                # topo-esquerda
            (bx + self.chat_container.width() + gap, by),  # topo-direita
            (bx - bw - gap,            by + self.chat_container.height() - bh),  # baixo-esquerda
            (bx + self.chat_container.width() + gap, by + self.chat_container.height() - bh),  # baixo-direita
        ]
        for btn, (px, py) in zip(self.float_buttons, positions):
            btn.move(px, py)
            btn.show()

    # redimensionou? reposiciona tudo
    def resizeEvent(self, event):
        super().resizeEvent(event)
        self._layout_children()

    # enviar
    def on_send(self):
        text = self.input.text().strip()
        if not text:
            return
        self.chat_area.appendPlainText(f"Você: {text}")
        try:
            resp = self._answer(text)
        except Exception as e:
            resp = f"[erro] {e}"
        self.chat_area.appendPlainText(f"Bot: {resp}\n")
        self.input.clear()


# ------------------------- main -------------------------
