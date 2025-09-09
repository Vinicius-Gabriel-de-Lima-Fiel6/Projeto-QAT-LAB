from PyQt6.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QHBoxLayout, QComboBox,
    QPushButton, QLineEdit, QMessageBox, QFormLayout
)
from PyQt6.QtCore import Qt
import numpy as np
import statistics
import matplotlib
matplotlib.use('QtAgg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qtagg import NavigationToolbar2QT
from scipy.interpolate import make_interp_spline
from mpl_toolkits.mplot3d import Axes3D
import webbrowser

class GraficosA(QWidget):
    def __init__(self):
        super().__init__()
        self.setLayout(QVBoxLayout(spacing=10))
        self.setStyleSheet("""
            QWidget { background-color: #fafafa; font-family: 'Segoe UI'; font-size: 12px; }
            QComboBox { min-width: 200px; max-width: 200px; }
            QLineEdit { min-height:24px; max-width:180px; border:1px solid #ccc; border-radius:4px; padding:4px; }
            QPushButton { background-color:#2979FF; color:white; padding:6px 12px; border:none; border-radius:4px; max-width:80px; }
            QPushButton:hover { background-color:#1565C0; }
            QLabel { font-weight:600; }
        """)
        self.current_curves = []
        menu = QHBoxLayout(spacing=10)
        menu.addWidget(QLabel("Escolha o gráfico:"))
        self.combo = QComboBox()
        self.combo.addItems([
            "Solubilidade", "Titulação", "Calibração", "Dispersão", "Histograma",
            "UV‑Vis", "Diagrama de Fases","Cromatograma", "Barras", "Regressão Linear", "Barras com Erro", "Cinética Química",
            "Arrhenius","Michaelis‑Menten", "Lineweaver‑Burk",
            "pKa Curve","Isoterma Adsorção", "Capacidade Térmica", "RMN Spectrum",
            "Mass Spectrum", "TGA","Adsorção Cinética", "Polarização"
        ])
         # ===== Botões para abrir GeoGebra e WolframAlpha
        link_buttons = QHBoxLayout()
        btn_geo = QPushButton("GeoGebra")
        btn_geo.clicked.connect(self._abrir_geogebra)
        btn_wolf = QPushButton("WolframAlpha")
        btn_wolf.clicked.connect(self._abrir_wolfram)
        w_s=QPushButton("Graf.Weibull")
        w_s.clicked.connect(self.siteWeibull)
        w_matlab=QPushButton("Graf.Matlab")
        w_matlab.clicked.connect(self._abrir_matlab)
        link_buttons.addWidget(w_matlab)
        link_buttons.addWidget(w_s)
        link_buttons.addWidget(btn_geo)
        link_buttons.addWidget(btn_wolf)
        self.layout().addLayout(link_buttons)
#============================================#=================================================#
        menu.addWidget(self.combo)
        self.layout().addLayout(menu)
        self.container = QWidget()
        self.container.setLayout(QVBoxLayout(spacing=10))
        self.layout().addWidget(self.container)
        self.figure = plt.figure(figsize=(6,4))
        self.ax = self.figure.add_subplot(111)
        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar2QT(self.canvas, self)
        self.container.layout().addWidget(self.canvas)
        self.container.layout().addWidget(self.toolbar)
        self.combo.currentTextChanged.connect(self._on_change)
        self._on_change(self.combo.currentText())
       
    def _clear_layout(self, layout):
        while layout.count():
            it = layout.takeAt(0)
            w = it.widget()
            if w: w.setParent(None); w.deleteLater()
            elif it.layout(): self._clear_layout(it.layout())

    def _on_change(self, name):
        self._clear_layout(self.container.layout())
        self.figure = plt.figure(figsize=(6,4))
        self.ax = self.figure.add_subplot(111)
        self.canvas = FigureCanvas(self.figure)
        self.current_curves = []
        form = QFormLayout(); form.setLabelAlignment(Qt.AlignmentFlag.AlignLeft)
        self.container.layout().addLayout(form)
        b = getattr(self, f"_build_{name.replace('‑','_').replace(' ','_')}", None)
        if b: b(form)
        btn = QPushButton("Plotar"); btn.clicked.connect(lambda: self._plot(name))
        self.container.layout().addWidget(btn)
        self.container.layout().addWidget(self.canvas)
        if self.toolbar: self.toolbar.setParent(None)
        self.toolbar = NavigationToolbar2QT(self.canvas, self)
        self.container.layout().addWidget(self.toolbar)

    def _plot(self, name):
        try:
            fn = getattr(self, f"_plot_{name.replace('‑','_').replace(' ','_')}", None)
            if fn: fn()
            self.ax.grid(True, which='both', linestyle='--', linewidth=0.5, alpha=0.6)
            self.canvas.draw()
        except Exception as e:
            QMessageBox.critical(self, "Erro", str(e))

    # 1 Solubilidade
    def _build_Solubilidade(self, form):
        self.eName=QLineEdit(); form.addRow("Composto:",self.eName)
        self.eTemp=QLineEdit(); form.addRow("Temperaturas (K):",self.eTemp)
        self.eSol=QLineEdit(); form.addRow("Solubilidade (g/100g H₂O):",self.eSol)
    def _plot_Solubilidade(self):
        name=self.eName.text().strip()
        t=list(map(float,self.eTemp.text().split(',')))
        s=list(map(float,self.eSol.text().split(',')))
        if not name or len(t)!=len(s): raise ValueError("Dados incorretos")
        if name not in self.current_curves: self.current_curves.append(name)
        x,y=np.array(t),np.array(s)
        if len(x)>=3:
            xs=np.linspace(x.min(),x.max(),300)
            ys=make_interp_spline(x,y,k=2)(xs); self.ax.plot(xs,ys,label=name)
        else:
            self.ax.plot(x,y,'-o',label=name)
        self.ax.set_title("Solubilidade",fontsize=14)
        self.ax.set_xlabel("Temperatura (K)"); self.ax.set_ylabel("Solubilidade")
        self.ax.legend()

    # 2 Titulação
    def _build_Titulação(self, form):
        self.ePh=QLineEdit(); form.addRow("pH:",self.ePh)
        self.eVol=QLineEdit(); form.addRow("Volume (mL):",self.eVol)
    def _plot_Titulação(self):
        p=list(map(float,self.ePh.text().split(',')))
        v=list(map(float,self.eVol.text().split(',')))
        if len(p)!=len(v): raise ValueError("verifique")
        self.ax.clear(); self.ax.plot(v,p,'-o',color='purple')
        self.ax.set_title("Titulação",fontsize=14)
        self.ax.set_xlabel("Volume (mL)"); self.ax.set_ylabel("pH")

    # 3 Calibração
    def _build_Calibração(self, form):
        self.eConc=QLineEdit(); form.addRow("Concentração:",self.eConc)
        self.eAbs=QLineEdit(); form.addRow("Absorbância:",self.eAbs)
    def _plot_Calibração(self):
        c=list(map(float,self.eConc.text().split(',')))
        a=list(map(float,self.eAbs.text().split(',')))
        if len(c)!=len(a): raise ValueError("verifique")
        coef=np.polyfit(c,a,1); f=np.poly1d(coef)
        self.ax.clear()
        self.ax.plot(c,a,'o'); self.ax.plot(c,f(c),'-')
        self.ax.set_title("Calibração",fontsize=14)
        self.ax.set_xlabel("Concentração"); self.ax.set_ylabel("Absorbância")

    # 4 Dispersão
    def _build_Dispersão(self, form):
        self.eX=QLineEdit(); form.addRow("X:",self.eX)
        self.eY=QLineEdit(); form.addRow("Y:",self.eY)
    def _plot_Dispersão(self):
        x=list(map(float,self.eX.text().split(',')))
        y=list(map(float,self.eY.text().split(',')))
        if len(x)!=len(y): raise ValueError()
        self.ax.clear(); self.ax.scatter(x,y,color='blue')
        self.ax.set_title("Dispersão",fontsize=14)
        self.ax.set_xlabel("X"); self.ax.set_ylabel("Y")

    # 5 Histograma
    def _build_Histograma(self, form):
        self.eData=QLineEdit(); form.addRow("Dados:",self.eData)
    def _plot_Histograma(self):
        d=list(map(float,self.eData.text().split(',')))
        self.ax.clear(); self.ax.hist(d,bins='auto',color='orange',edgecolor='black')
        self.ax.set_title("Histograma",fontsize=14)
        self.ax.set_xlabel("Valor"); self.ax.set_ylabel("Frequência")

    # 6 UV‑Vis
    def _build_UV_Vis(self, form):
        self.eW=QLineEdit(); form.addRow("λ (nm):",self.eW)
        self.eAbsUV=QLineEdit(); form.addRow("Absorbância:",self.eAbsUV)
    def _plot_UV_Vis(self):
        wl=list(map(float,self.eW.text().split(',')))
        a=list(map(float,self.eAbsUV.text().split(',')))
        if len(wl)!=len(a): raise ValueError()
        self.ax.clear(); self.ax.plot(wl,a,'-o',color='navy')
        self.ax.set_title("UV‑Vis",fontsize=14)
        self.ax.set_xlabel("λ (nm)"); self.ax.set_ylabel("Absorbância")

    # 7 Diagrama de Fases
    def _build_Diagrama_de_Fases(self, form):
        self.eT=QLineEdit(); form.addRow("Temperaturas (K):",self.eT)
        self.eP=QLineEdit(); form.addRow("Pressões (atm):",self.eP)
    def _plot_Diagrama_de_Fases(self):
        t=list(map(float,self.eT.text().split(',')))
        p=list(map(float,self.eP.text().split(',')))
        if len(t)!=len(p): raise ValueError()
        self.ax.clear(); self.ax.plot(t,p,'-o',color='darkgreen')
        self.ax.set_title("Diagrama de Fases",fontsize=14)
        self.ax.set_xlabel("T (K)"); self.ax.set_ylabel("P (atm)")




    


    # 11 Cromatograma
    def _build_Cromatograma(self, form):
        self.eRet=QLineEdit(); form.addRow("Retenção (min):",self.eRet)
        self.eInt=QLineEdit(); form.addRow("Intensidade:",self.eInt)
    def _plot_Cromatograma(self):
        r=list(map(float,self.eRet.text().split(',')))
        i=list(map(float,self.eInt.text().split(',')))
        if len(r)!=len(i): raise ValueError()
        self.ax.clear(); self.ax.plot(r,i,'-',color='brown')
        self.ax.set_title("Cromatograma",fontsize=14)
        self.ax.set_xlabel("Tempo (min)"); self.ax.set_ylabel("Intensidade")

    # 12 Barras
    def _build_Barras(self, form):
        self.eCats=QLineEdit(); form.addRow("Categorias (vírgula):",self.eCats)
        self.eVals=QLineEdit(); form.addRow("Valores:",self.eVals)
    def _plot_Barras(self):
        cats=self.eCats.text().split(',')
        vals=list(map(float,self.eVals.text().split(',')))
        self.ax.clear(); self.ax.bar(cats,vals,color='skyblue')
        self.ax.set_title("Barras",fontsize=14); self.ax.set_ylabel("Valor")

    # 13 Regressão Linear
    def _build_Regressão_Linear(self, form):
        self.eXre=QLineEdit(); form.addRow("X:",self.eXre)
        self.eYre=QLineEdit(); form.addRow("Y:",self.eYre)
    def _plot_Regressão_Linear(self):
        x=np.array(list(map(float,self.eXre.text().split(','))))
        y=np.array(list(map(float,self.eYre.text().split(','))))
        if x.size!=y.size: raise ValueError()
        coef=np.polyfit(x,y,1); f=np.poly1d(coef)
        self.ax.clear(); self.ax.scatter(x,y,color='magenta')
        self.ax.plot(x,f(x),'-',color='red')
        self.ax.set_title("Regressão Linear",fontsize=14); self.ax.legend(["Dados",f"y={coef[0]:.2f}x+{coef[1]:.2f}"])
        self.ax.set_xlabel("X"); self.ax.set_ylabel("Y")

    # 14 Barras com Erro
    def _build_Barras_com_Erro(self, form):
        self.eCats_e=QLineEdit(); form.addRow("Categorias:",self.eCats_e)
        self.eVals_e=QLineEdit(); form.addRow("Valores sequenciais:",self.eVals_e)
    def _plot_Barras_com_Erro(self):
        cats=self.eCats_e.text().split(',')
        vals=list(map(float,self.eVals_e.text().split(',')))
        n=len(vals)//len(cats); means,errs=[],[]
        for i,c in enumerate(cats):
            chunk=vals[i*n:(i+1)*n]
            means.append(statistics.mean(chunk)); errs.append(statistics.pstdev(chunk))
        self.ax.clear(); self.ax.bar(range(len(cats)),means,yerr=errs,capsize=5,color='lightgreen')
        self.ax.set_xticks(range(len(cats))); self.ax.set_xticklabels(cats)
        self.ax.set_title("Barras com Erro",fontsize=14); self.ax.set_ylabel("Média ± Desvio")

    # 15 Cinética Química
    def _build_Cinética_Química(self, form):
        self.eTK=QLineEdit(); form.addRow("Tempo (s):",self.eTK)
        self.eCK=QLineEdit(); form.addRow("Concentração:",self.eCK)
    def _plot_Cinética_Química(self):
        t=list(map(float,self.eTK.text().split(',')))
        c=list(map(float,self.eCK.text().split(',')))
        if len(t)!=len(c): raise ValueError()
        if self.combo.currentText()=="Cinética Química": self.ax.clear()
        self.ax.plot(t,c,'-o')
        self.ax.set_title("Cinética Química",fontsize=14)
        self.ax.set_xlabel("Tempo (s)"); self.ax.set_ylabel("Conc.")
  

    # 17 Arrhenius
    def _build_Arrhenius(self, form):
        self.eInvT = QLineEdit(); form.addRow("1/T (1/K):", self.eInvT)
        self.eLnK = QLineEdit(); form.addRow("ln k:", self.eLnK)
    def _plot_Arrhenius(self):
        invt = list(map(float, self.eInvT.text().split(',')))
        lnK = list(map(float, self.eLnK.text().split(',')))
        if len(invt) != len(lnK): raise ValueError()
        self.ax.clear()
        self.ax.plot(invt, lnK, '-o', color='darkred')
        self.ax.set_title("Gráfico de Arrhenius", fontsize=14)
        self.ax.set_xlabel("1/T (1/K)"); self.ax.set_ylabel("ln k")


   

    # 19 Michaelis–Menten
    def _build_Michaelis_Menten(self, form):
        self.eS = QLineEdit(); form.addRow("Concentração [S]:", self.eS)
        self.eV0 = QLineEdit(); form.addRow("Velocidade V₀:", self.eV0)
    def _plot_Michaelis_Menten(self):
        S = list(map(float, self.eS.text().split(',')))
        V0 = list(map(float, self.eV0.text().split(',')))
        if len(S) != len(V0): raise ValueError()
        self.ax.clear(); self.ax.plot(S, V0, '-o', color='blue')
        self.ax.set_title("Michaelis–Menten", fontsize=14)
        self.ax.set_xlabel("[S]"); self.ax.set_ylabel("V₀")

    # 20 Lineweaver–Burk
    def _build_Lineweaver_Burk(self, form):
        self.eInvS = QLineEdit(); form.addRow("1/[S]:", self.eInvS)
        self.eInvV = QLineEdit(); form.addRow("1/V₀:", self.eInvV)
    def _plot_Lineweaver_Burk(self):
        invS = list(map(float, self.eInvS.text().split(',')))
        invV = list(map(float, self.eInvV.text().split(',')))
        if len(invS) != len(invV): raise ValueError()
        self.ax.clear(); self.ax.plot(invS, invV, '-o', color='green')
        self.ax.set_title("Lineweaver–Burk", fontsize=14)
        self.ax.set_xlabel("1/[S]"); self.ax.set_ylabel("1/V₀")

    # 21 pKa Curve (log Ka vs pH)
    def _build_pKa_Curve(self, form):
        self.ePHpka = QLineEdit(); form.addRow("pH valores:", self.ePHpka)
        self.eLogKa = QLineEdit(); form.addRow("log Ka:", self.eLogKa)
    def _plot_pKa_Curve(self):
        ph = list(map(float, self.ePHpka.text().split(',')))
        logka = list(map(float, self.eLogKa.text().split(',')))
        self.ax.clear(); self.ax.plot(ph, logka, '-o', color='orange')
        self.ax.set_title("Curva de pKa", fontsize=14)
        self.ax.set_xlabel("pH"); self.ax.set_ylabel("log Ka")

  
  

    # 23 Isoterma de Adsorção
    def _build_Isoterma_Adsorção(self, form):
        self.eConcL = QLineEdit(); form.addRow("Concentração (mol/L):", self.eConcL)
        self.eAds = QLineEdit(); form.addRow("Adsorção ads:", self.eAds)
    def _plot_Isoterma_Adsorção(self):
        c = list(map(float, self.eConcL.text().split(',')))
        ads = list(map(float, self.eAds.text().split(',')))
        self.ax.clear(); self.ax.plot(c, ads, '-o', color='olive')
        self.ax.set_title("Isoterma de Adsorção", fontsize=14)
        self.ax.set_xlabel("Concentração"); self.ax.set_ylabel("Adsorção")

    # 24 Capacidade Térmica
    def _build_Capacidade_Térmica(self, form):
        self.eTcap = QLineEdit(); form.addRow("Temperatura (K):", self.eTcap)
        self.eCp = QLineEdit(); form.addRow("Cp (J/mol·K):", self.eCp)
    def _plot_Capacidade_Térmica(self):
        t = list(map(float, self.eTcap.text().split(',')))
        cp = list(map(float, self.eCp.text().split(',')))
        self.ax.clear(); self.ax.plot(t, cp, '-o', color='magenta')
        self.ax.set_title("Capacidade Térmica", fontsize=14)
        self.ax.set_xlabel("Temperatura"); self.ax.set_ylabel("Cp")

    # 25 RMN Spectrum
    def _build_RMN_Spectrum(self, form):
        self.eDelta = QLineEdit(); form.addRow("δ (ppm):", self.eDelta)
        self.eIntRMN = QLineEdit(); form.addRow("Intensidade:", self.eIntRMN)
    def _plot_RMN_Spectrum(self):
        dx = list(map(float, self.eDelta.text().split(',')))
        iod = list(map(float, self.eIntRMN.text().split(',')))
        self.ax.clear(); self.ax.plot(dx, iod, '-o', color='navy')
        self.ax.set_title("Espectro RMN", fontsize=14)
        self.ax.set_xlabel("δ (ppm)"); self.ax.set_ylabel("Intensidade")

    # 26 Mass Spectrum
    def _build_Mass_Spectrum(self, form):
        self.eMZ = QLineEdit(); form.addRow("m/z valores:", self.eMZ)
        self.eIntM = QLineEdit(); form.addRow("Intensidade:", self.eIntM)
    def _plot_Mass_Spectrum(self):
        mz = list(map(float, self.eMZ.text().split(',')))
        im = list(map(float, self.eIntM.text().split(',')))
        self.ax.clear(); self.ax.plot(mz, im, '-o', color='gray')
        self.ax.set_title("Espectro de Massa", fontsize=14)
        self.ax.set_xlabel("m/z"); self.ax.set_ylabel("Intensidade")

    # 27 TGA
    def _build_TGA(self, form):
        self.eTempTGA = QLineEdit(); form.addRow("Temperatura (°C):", self.eTempTGA)
        self.eMass = QLineEdit(); form.addRow("Massa (%):", self.eMass)
    def _plot_TGA(self):
        temp = list(map(float, self.eTempTGA.text().split(',')))
        m = list(map(float, self.eMass.text().split(',')))
        self.ax.clear(); self.ax.plot(temp, m, '-o', color='sienna')
        self.ax.set_title("TGA (Termogravimetria)", fontsize=14)
        self.ax.set_xlabel("Temperatura (°C)"); self.ax.set_ylabel("Massa (%)")

    # 29 Adsorção Cinética
    def _build_Adsorção_Cinética(self, form):
        self.eTK2 = QLineEdit(); form.addRow("Tempo (s):", self.eTK2)
        self.eAdsK = QLineEdit(); form.addRow("Adsorção:", self.eAdsK)
    def _plot_Adsorção_Cinética(self):
        t=list(map(float,self.eTK2.text().split(',')))
        ads=list(map(float,self.eAdsK.text().split(',')))
        self.ax.clear(); self.ax.plot(t, ads, '-o', color='olive')
        self.ax.set_title("Adsorção Cinética", fontsize=14)
        self.ax.set_xlabel("Tempo (s)"); self.ax.set_ylabel("Adsorção")

    # 30 Polarização Eletroquímica
    def _build_Polarização(self, form):
        self.ePot = QLineEdit(); form.addRow("Potencial (V):", self.ePot)
        self.eCurr = QLineEdit(); form.addRow("Corrente (A):", self.eCurr)
    def _plot_Polarização(self):
        pot=list(map(float,self.ePot.text().split(',')))
        cur=list(map(float,self.eCurr.text().split(',')))
        self.ax.clear(); self.ax.plot(pot, cur, '-o', color='darkblue')
        self.ax.set_title("Polarização Eletroquímica", fontsize=14)
        self.ax.set_xlabel("Potencial (V)"); self.ax.set_ylabel("Corrente (A)")
        
        
    def siteWeibull(self):
        webbrowser.open("https://www-acsu-buffalo-edu.translate.goog/~adamcunn/probability/weibull.html?_x_tr_sl=en&_x_tr_tl=pt&_x_tr_hl=pt&_x_tr_pto=tc")
    def _abrir_geogebra(self):
        webbrowser.open("https://www.geogebra.org/graphing")
    def _abrir_wolfram(self):
        webbrowser.open("https://www.wolframalpha.com/")
    def _abrir_matlab(self):
        webbrowser.open("https://matlab.mathworks.com/")
