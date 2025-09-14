// Sistema de Gráficos Científicos
let currentGraphType = 'solubilidade';
let currentCurves = [];

// Configurações dos tipos de gráfico
const graphConfigs = {
    solubilidade: {
        title: 'Solubilidade',
        fields: [
            { name: 'composto', label: 'Composto:', type: 'text', placeholder: 'Nome do composto' },
            { name: 'temperaturas', label: 'Temperaturas (K):', type: 'text', placeholder: '273,298,323,348 (separados por vírgula)' },
            { name: 'solubilidade', label: 'Solubilidade (g/100g H₂O):', type: 'text', placeholder: '10,15,25,40 (separados por vírgula)' }
        ],
        xLabel: 'Temperatura (K)',
        yLabel: 'Solubilidade (g/100g H₂O)'
    },
    titulacao: {
        title: 'Titulação',
        fields: [
            { name: 'volume', label: 'Volume (mL):', type: 'text', placeholder: '0,5,10,15,20,25 (separados por vírgula)' },
            { name: 'ph', label: 'pH:', type: 'text', placeholder: '2.1,3.5,7.0,10.5,11.8,12.2 (separados por vírgula)' }
        ],
        xLabel: 'Volume (mL)',
        yLabel: 'pH'
    },
    calibracao: {
        title: 'Calibração',
        fields: [
            { name: 'concentracao', label: 'Concentração:', type: 'text', placeholder: '0,1,2,3,4,5 (separados por vírgula)' },
            { name: 'absorbancia', label: 'Absorbância:', type: 'text', placeholder: '0,0.2,0.4,0.6,0.8,1.0 (separados por vírgula)' }
        ],
        xLabel: 'Concentração',
        yLabel: 'Absorbância'
    },
    dispersao: {
        title: 'Dispersão',
        fields: [
            { name: 'x', label: 'Valores X:', type: 'text', placeholder: '1,2,3,4,5,6 (separados por vírgula)' },
            { name: 'y', label: 'Valores Y:', type: 'text', placeholder: '2,4,1,5,3,6 (separados por vírgula)' }
        ],
        xLabel: 'X',
        yLabel: 'Y'
    },
    histograma: {
        title: 'Histograma',
        fields: [
            { name: 'dados', label: 'Dados:', type: 'text', placeholder: '1,2,2,3,3,3,4,4,5 (separados por vírgula)' }
        ],
        xLabel: 'Valor',
        yLabel: 'Frequência'
    },
    uv_vis: {
        title: 'UV-Vis',
        fields: [
            { name: 'comprimento_onda', label: 'λ (nm):', type: 'text', placeholder: '200,250,300,350,400,450,500 (separados por vírgula)' },
            { name: 'absorbancia', label: 'Absorbância:', type: 'text', placeholder: '0.1,0.3,0.8,1.2,0.9,0.4,0.1 (separados por vírgula)' }
        ],
        xLabel: 'λ (nm)',
        yLabel: 'Absorbância'
    },
    diagrama_fases: {
        title: 'Diagrama de Fases',
        fields: [
            { name: 'temperatura', label: 'Temperatura (K):', type: 'text', placeholder: '273,298,323,348,373 (separados por vírgula)' },
            { name: 'pressao', label: 'Pressão (atm):', type: 'text', placeholder: '1,2,5,10,20 (separados por vírgula)' }
        ],
        xLabel: 'Temperatura (K)',
        yLabel: 'Pressão (atm)'
    },
    cromatograma: {
        title: 'Cromatograma',
        fields: [
            { name: 'tempo_retencao', label: 'Tempo de Retenção (min):', type: 'text', placeholder: '1,2,3,4,5,6 (separados por vírgula)' },
            { name: 'intensidade', label: 'Intensidade:', type: 'text', placeholder: '100,500,200,800,300,150 (separados por vírgula)' }
        ],
        xLabel: 'Tempo (min)',
        yLabel: 'Intensidade'
    },
    barras: {
        title: 'Gráfico de Barras',
        fields: [
            { name: 'categorias', label: 'Categorias:', type: 'text', placeholder: 'A,B,C,D (separados por vírgula)' },
            { name: 'valores', label: 'Valores:', type: 'text', placeholder: '10,20,15,25 (separados por vírgula)' }
        ],
        xLabel: 'Categorias',
        yLabel: 'Valores'
    },
    regressao_linear: {
        title: 'Regressão Linear',
        fields: [
            { name: 'x', label: 'Valores X:', type: 'text', placeholder: '1,2,3,4,5 (separados por vírgula)' },
            { name: 'y', label: 'Valores Y:', type: 'text', placeholder: '2,4,6,8,10 (separados por vírgula)' }
        ],
        xLabel: 'X',
        yLabel: 'Y'
    },
    cinetica_quimica: {
        title: 'Cinética Química',
        fields: [
            { name: 'tempo', label: 'Tempo (s):', type: 'text', placeholder: '0,10,20,30,40,50 (separados por vírgula)' },
            { name: 'concentracao', label: 'Concentração:', type: 'text', placeholder: '1.0,0.8,0.6,0.4,0.2,0.1 (separados por vírgula)' }
        ],
        xLabel: 'Tempo (s)',
        yLabel: 'Concentração'
    },
    arrhenius: {
        title: 'Gráfico de Arrhenius',
        fields: [
            { name: 'inv_temperatura', label: '1/T (1/K):', type: 'text', placeholder: '0.003,0.0032,0.0034,0.0036 (separados por vírgula)' },
            { name: 'ln_k', label: 'ln k:', type: 'text', placeholder: '-5,-4,-3,-2 (separados por vírgula)' }
        ],
        xLabel: '1/T (1/K)',
        yLabel: 'ln k'
    },
    michaelis_menten: {
        title: 'Michaelis-Menten',
        fields: [
            { name: 'concentracao_s', label: 'Concentração [S]:', type: 'text', placeholder: '0.1,0.2,0.5,1.0,2.0,5.0 (separados por vírgula)' },
            { name: 'velocidade', label: 'Velocidade V₀:', type: 'text', placeholder: '0.05,0.09,0.17,0.25,0.33,0.42 (separados por vírgula)' }
        ],
        xLabel: '[S]',
        yLabel: 'V₀'
    },
    lineweaver_burk: {
        title: 'Lineweaver-Burk',
        fields: [
            { name: 'inv_s', label: '1/[S]:', type: 'text', placeholder: '10,5,2,1,0.5,0.2 (separados por vírgula)' },
            { name: 'inv_v', label: '1/V₀:', type: 'text', placeholder: '20,11,6,4,3,2.4 (separados por vírgula)' }
        ],
        xLabel: '1/[S]',
        yLabel: '1/V₀'
    },
    pka_curve: {
        title: 'Curva de pKa',
        fields: [
            { name: 'ph', label: 'pH:', type: 'text', placeholder: '1,2,3,4,5,6,7,8,9,10 (separados por vírgula)' },
            { name: 'log_ka', label: 'log Ka:', type: 'text', placeholder: '-1,-2,-3,-4,-5,-6,-7,-8,-9,-10 (separados por vírgula)' }
        ],
        xLabel: 'pH',
        yLabel: 'log Ka'
    },
    isoterma_adsorcao: {
        title: 'Isoterma de Adsorção',
        fields: [
            { name: 'concentracao', label: 'Concentração (mol/L):', type: 'text', placeholder: '0.1,0.2,0.3,0.4,0.5 (separados por vírgula)' },
            { name: 'adsorcao', label: 'Adsorção:', type: 'text', placeholder: '0.05,0.09,0.12,0.14,0.15 (separados por vírgula)' }
        ],
        xLabel: 'Concentração (mol/L)',
        yLabel: 'Adsorção'
    },
    capacidade_termica: {
        title: 'Capacidade Térmica',
        fields: [
            { name: 'temperatura', label: 'Temperatura (K):', type: 'text', placeholder: '200,250,300,350,400 (separados por vírgula)' },
            { name: 'cp', label: 'Cp (J/mol·K):', type: 'text', placeholder: '25,28,32,36,40 (separados por vírgula)' }
        ],
        xLabel: 'Temperatura (K)',
        yLabel: 'Cp (J/mol·K)'
    },
    rmn_spectrum: {
        title: 'Espectro RMN',
        fields: [
            { name: 'delta', label: 'δ (ppm):', type: 'text', placeholder: '0,1,2,3,4,5,6,7,8 (separados por vírgula)' },
            { name: 'intensidade', label: 'Intensidade:', type: 'text', placeholder: '0.1,0.3,0.8,1.0,0.6,0.4,0.2,0.5,0.9 (separados por vírgula)' }
        ],
        xLabel: 'δ (ppm)',
        yLabel: 'Intensidade'
    },
    mass_spectrum: {
        title: 'Espectro de Massa',
        fields: [
            { name: 'mz', label: 'm/z:', type: 'text', placeholder: '50,75,100,125,150,175,200 (separados por vírgula)' },
            { name: 'intensidade', label: 'Intensidade:', type: 'text', placeholder: '10,30,100,20,50,15,5 (separados por vírgula)' }
        ],
        xLabel: 'm/z',
        yLabel: 'Intensidade'
    },
    tga: {
        title: 'TGA (Termogravimetria)',
        fields: [
            { name: 'temperatura', label: 'Temperatura (°C):', type: 'text', placeholder: '25,100,200,300,400,500 (separados por vírgula)' },
            { name: 'massa', label: 'Massa (%):', type: 'text', placeholder: '100,95,85,70,50,30 (separados por vírgula)' }
        ],
        xLabel: 'Temperatura (°C)',
        yLabel: 'Massa (%)'
    },
    adsorcao_cinetica: {
        title: 'Adsorção Cinética',
        fields: [
            { name: 'tempo', label: 'Tempo (s):', type: 'text', placeholder: '0,60,120,180,240,300 (separados por vírgula)' },
            { name: 'adsorcao', label: 'Adsorção:', type: 'text', placeholder: '0,0.2,0.35,0.45,0.5,0.52 (separados por vírgula)' }
        ],
        xLabel: 'Tempo (s)',
        yLabel: 'Adsorção'
    },
    polarizacao: {
        title: 'Polarização Eletroquímica',
        fields: [
            { name: 'potencial', label: 'Potencial (V):', type: 'text', placeholder: '-1.0,-0.5,0,0.5,1.0,1.5 (separados por vírgula)' },
            { name: 'corrente', label: 'Corrente (A):', type: 'text', placeholder: '-0.1,-0.05,0,0.05,0.1,0.2 (separados por vírgula)' }
        ],
        xLabel: 'Potencial (V)',
        yLabel: 'Corrente (A)'
    }
};

// Função para mudar o tipo de gráfico
function changeGraphType() {
    const select = document.getElementById('graphType');
    currentGraphType = select.value;
    generateForm();
}

// Função para gerar o formulário dinamicamente
function generateForm() {
    const formContainer = document.getElementById('graphForm');
    const config = graphConfigs[currentGraphType];
    
    let formHTML = `<h3>${config.title}</h3>`;
    
    config.fields.forEach(field => {
        formHTML += `
            <div class="form-group">
                <label for="${field.name}">${field.label}</label>
                <input type="${field.type}" id="${field.name}" placeholder="${field.placeholder}">
            </div>
        `;
    });
    
    formContainer.innerHTML = formHTML;
}

// Função para plotar o gráfico
function plotGraph() {
    try {
        const config = graphConfigs[currentGraphType];
        const data = {};
        
        // Coletar dados do formulário
        config.fields.forEach(field => {
            const element = document.getElementById(field.name);
            if (field.type === 'text' && field.name !== 'composto' && field.name !== 'categorias') {
                data[field.name] = element.value.split(',').map(v => parseFloat(v.trim()));
            } else {
                data[field.name] = element.value;
            }
        });
        
        // Plotar baseado no tipo
        switch(currentGraphType) {
            case 'solubilidade':
                plotSolubilidade(data);
                break;
            case 'titulacao':
                plotTitulacao(data);
                break;
            case 'calibracao':
                plotCalibracao(data);
                break;
            case 'dispersao':
                plotDispersao(data);
                break;
            case 'histograma':
                plotHistograma(data);
                break;
            case 'uv_vis':
                plotUVVis(data);
                break;
            case 'diagrama_fases':
                plotDiagramaFases(data);
                break;
            case 'cromatograma':
                plotCromatograma(data);
                break;
            case 'barras':
                plotBarras(data);
                break;
            case 'regressao_linear':
                plotRegressaoLinear(data);
                break;
            case 'cinetica_quimica':
                plotCineticaQuimica(data);
                break;
            case 'arrhenius':
                plotArrhenius(data);
                break;
            case 'michaelis_menten':
                plotMichaelisMenten(data);
                break;
            case 'lineweaver_burk':
                plotLineweaverBurk(data);
                break;
            case 'pka_curve':
                plotPkaCurve(data);
                break;
            case 'isoterma_adsorcao':
                plotIsotermaAdsorcao(data);
                break;
            case 'capacidade_termica':
                plotCapacidadeTermica(data);
                break;
            case 'rmn_spectrum':
                plotRMNSpectrum(data);
                break;
            case 'mass_spectrum':
                plotMassSpectrum(data);
                break;
            case 'tga':
                plotTGA(data);
                break;
            case 'adsorcao_cinetica':
                plotAdsorcaoCinetica(data);
                break;
            case 'polarizacao':
                plotPolarizacao(data);
                break;
        }
        
        showNotification('Gráfico plotado com sucesso!', 'success');
    } catch (error) {
        showNotification('Erro ao plotar gráfico: ' + error.message, 'error');
    }
}

// Funções específicas para cada tipo de gráfico
function plotSolubilidade(data) {
    const trace = {
        x: data.temperaturas,
        y: data.solubilidade,
        mode: 'lines+markers',
        name: data.composto || 'Composto',
        line: { color: 'blue' }
    };
    
    const layout = {
        title: 'Solubilidade vs Temperatura',
        xaxis: { title: 'Temperatura (K)' },
        yaxis: { title: 'Solubilidade (g/100g H₂O)' },
        grid: true
    };
    
    Plotly.newPlot('plotlyGraph', [trace], layout);
}

function plotTitulacao(data) {
    const trace = {
        x: data.volume,
        y: data.ph,
        mode: 'lines+markers',
        line: { color: 'purple' }
    };
    
    const layout = {
        title: 'Curva de Titulação',
        xaxis: { title: 'Volume (mL)' },
        yaxis: { title: 'pH' }
    };
    
    Plotly.newPlot('plotlyGraph', [trace], layout);
}

function plotCalibracao(data) {
    // Calcular regressão linear
    const n = data.concentracao.length;
    const sumX = data.concentracao.reduce((a, b) => a + b, 0);
    const sumY = data.absorbancia.reduce((a, b) => a + b, 0);
    const sumXY = data.concentracao.reduce((sum, x, i) => sum + x * data.absorbancia[i], 0);
    const sumXX = data.concentracao.reduce((sum, x) => sum + x * x, 0);
    
    const slope = (n * sumXY - sumX * sumY) / (n * sumXX - sumX * sumX);
    const intercept = (sumY - slope * sumX) / n;
    
    const lineX = [Math.min(...data.concentracao), Math.max(...data.concentracao)];
    const lineY = lineX.map(x => slope * x + intercept);
    
    const trace1 = {
        x: data.concentracao,
        y: data.absorbancia,
        mode: 'markers',
        name: 'Dados',
        marker: { color: 'blue' }
    };
    
    const trace2 = {
        x: lineX,
        y: lineY,
        mode: 'lines',
        name: `y = ${slope.toFixed(3)}x + ${intercept.toFixed(3)}`,
        line: { color: 'red' }
    };
    
    const layout = {
        title: 'Curva de Calibração',
        xaxis: { title: 'Concentração' },
        yaxis: { title: 'Absorbância' }
    };
    
    Plotly.newPlot('plotlyGraph', [trace1, trace2], layout);
}

function plotDispersao(data) {
    const trace = {
        x: data.x,
        y: data.y,
        mode: 'markers',
        marker: { color: 'blue', size: 8 }
    };
    
    const layout = {
        title: 'Gráfico de Dispersão',
        xaxis: { title: 'X' },
        yaxis: { title: 'Y' }
    };
    
    Plotly.newPlot('plotlyGraph', [trace], layout);
}

function plotHistograma(data) {
    const trace = {
        x: data.dados,
        type: 'histogram',
        marker: { color: 'orange' }
    };
    
    const layout = {
        title: 'Histograma',
        xaxis: { title: 'Valor' },
        yaxis: { title: 'Frequência' }
    };
    
    Plotly.newPlot('plotlyGraph', [trace], layout);
}

function plotUVVis(data) {
    const trace = {
        x: data.comprimento_onda,
        y: data.absorbancia,
        mode: 'lines+markers',
        line: { color: 'navy' }
    };
    
    const layout = {
        title: 'Espectro UV-Vis',
        xaxis: { title: 'λ (nm)' },
        yaxis: { title: 'Absorbância' }
    };
    
    Plotly.newPlot('plotlyGraph', [trace], layout);
}

function plotDiagramaFases(data) {
    const trace = {
        x: data.temperatura,
        y: data.pressao,
        mode: 'lines+markers',
        line: { color: 'darkgreen' }
    };
    
    const layout = {
        title: 'Diagrama de Fases',
        xaxis: { title: 'Temperatura (K)' },
        yaxis: { title: 'Pressão (atm)' }
    };
    
    Plotly.newPlot('plotlyGraph', [trace], layout);
}

function plotCromatograma(data) {
    const trace = {
        x: data.tempo_retencao,
        y: data.intensidade,
        mode: 'lines',
        line: { color: 'brown' }
    };
    
    const layout = {
        title: 'Cromatograma',
        xaxis: { title: 'Tempo de Retenção (min)' },
        yaxis: { title: 'Intensidade' }
    };
    
    Plotly.newPlot('plotlyGraph', [trace], layout);
}

function plotBarras(data) {
    const categorias = data.categorias.split(',').map(c => c.trim());
    
    const trace = {
        x: categorias,
        y: data.valores,
        type: 'bar',
        marker: { color: 'skyblue' }
    };
    
    const layout = {
        title: 'Gráfico de Barras',
        xaxis: { title: 'Categorias' },
        yaxis: { title: 'Valores' }
    };
    
    Plotly.newPlot('plotlyGraph', [trace], layout);
}

function plotRegressaoLinear(data) {
    // Calcular regressão linear
    const n = data.x.length;
    const sumX = data.x.reduce((a, b) => a + b, 0);
    const sumY = data.y.reduce((a, b) => a + b, 0);
    const sumXY = data.x.reduce((sum, x, i) => sum + x * data.y[i], 0);
    const sumXX = data.x.reduce((sum, x) => sum + x * x, 0);
    
    const slope = (n * sumXY - sumX * sumY) / (n * sumXX - sumX * sumX);
    const intercept = (sumY - slope * sumX) / n;
    
    const lineX = [Math.min(...data.x), Math.max(...data.x)];
    const lineY = lineX.map(x => slope * x + intercept);
    
    const trace1 = {
        x: data.x,
        y: data.y,
        mode: 'markers',
        name: 'Dados',
        marker: { color: 'magenta' }
    };
    
    const trace2 = {
        x: lineX,
        y: lineY,
        mode: 'lines',
        name: `y = ${slope.toFixed(2)}x + ${intercept.toFixed(2)}`,
        line: { color: 'red' }
    };
    
    const layout = {
        title: 'Regressão Linear',
        xaxis: { title: 'X' },
        yaxis: { title: 'Y' }
    };
    
    Plotly.newPlot('plotlyGraph', [trace1, trace2], layout);
}

function plotCineticaQuimica(data) {
    const trace = {
        x: data.tempo,
        y: data.concentracao,
        mode: 'lines+markers',
        line: { color: 'green' }
    };
    
    const layout = {
        title: 'Cinética Química',
        xaxis: { title: 'Tempo (s)' },
        yaxis: { title: 'Concentração' }
    };
    
    Plotly.newPlot('plotlyGraph', [trace], layout);
}

function plotArrhenius(data) {
    const trace = {
        x: data.inv_temperatura,
        y: data.ln_k,
        mode: 'lines+markers',
        line: { color: 'darkred' }
    };
    
    const layout = {
        title: 'Gráfico de Arrhenius',
        xaxis: { title: '1/T (1/K)' },
        yaxis: { title: 'ln k' }
    };
    
    Plotly.newPlot('plotlyGraph', [trace], layout);
}

function plotMichaelisMenten(data) {
    const trace = {
        x: data.concentracao_s,
        y: data.velocidade,
        mode: 'lines+markers',
        line: { color: 'blue' }
    };
    
    const layout = {
        title: 'Michaelis-Menten',
        xaxis: { title: '[S]' },
        yaxis: { title: 'V₀' }
    };
    
    Plotly.newPlot('plotlyGraph', [trace], layout);
}

function plotLineweaverBurk(data) {
    const trace = {
        x: data.inv_s,
        y: data.inv_v,
        mode: 'lines+markers',
        line: { color: 'green' }
    };
    
    const layout = {
        title: 'Lineweaver-Burk',
        xaxis: { title: '1/[S]' },
        yaxis: { title: '1/V₀' }
    };
    
    Plotly.newPlot('plotlyGraph', [trace], layout);
}

function plotPkaCurve(data) {
    const trace = {
        x: data.ph,
        y: data.log_ka,
        mode: 'lines+markers',
        line: { color: 'orange' }
    };
    
    const layout = {
        title: 'Curva de pKa',
        xaxis: { title: 'pH' },
        yaxis: { title: 'log Ka' }
    };
    
    Plotly.newPlot('plotlyGraph', [trace], layout);
}

function plotIsotermaAdsorcao(data) {
    const trace = {
        x: data.concentracao,
        y: data.adsorcao,
        mode: 'lines+markers',
        line: { color: 'olive' }
    };
    
    const layout = {
        title: 'Isoterma de Adsorção',
        xaxis: { title: 'Concentração (mol/L)' },
        yaxis: { title: 'Adsorção' }
    };
    
    Plotly.newPlot('plotlyGraph', [trace], layout);
}

function plotCapacidadeTermica(data) {
    const trace = {
        x: data.temperatura,
        y: data.cp,
        mode: 'lines+markers',
        line: { color: 'magenta' }
    };
    
    const layout = {
        title: 'Capacidade Térmica',
        xaxis: { title: 'Temperatura (K)' },
        yaxis: { title: 'Cp (J/mol·K)' }
    };
    
    Plotly.newPlot('plotlyGraph', [trace], layout);
}

function plotRMNSpectrum(data) {
    const trace = {
        x: data.delta,
        y: data.intensidade,
        mode: 'lines+markers',
        line: { color: 'navy' }
    };
    
    const layout = {
        title: 'Espectro RMN',
        xaxis: { title: 'δ (ppm)' },
        yaxis: { title: 'Intensidade' }
    };
    
    Plotly.newPlot('plotlyGraph', [trace], layout);
}

function plotMassSpectrum(data) {
    const trace = {
        x: data.mz,
        y: data.intensidade,
        type: 'bar',
        marker: { color: 'gray' }
    };
    
    const layout = {
        title: 'Espectro de Massa',
        xaxis: { title: 'm/z' },
        yaxis: { title: 'Intensidade' }
    };
    
    Plotly.newPlot('plotlyGraph', [trace], layout);
}

function plotTGA(data) {
    const trace = {
        x: data.temperatura,
        y: data.massa,
        mode: 'lines+markers',
        line: { color: 'sienna' }
    };
    
    const layout = {
        title: 'TGA (Termogravimetria)',
        xaxis: { title: 'Temperatura (°C)' },
        yaxis: { title: 'Massa (%)' }
    };
    
    Plotly.newPlot('plotlyGraph', [trace], layout);
}

function plotAdsorcaoCinetica(data) {
    const trace = {
        x: data.tempo,
        y: data.adsorcao,
        mode: 'lines+markers',
        line: { color: 'olive' }
    };
    
    const layout = {
        title: 'Adsorção Cinética',
        xaxis: { title: 'Tempo (s)' },
        yaxis: { title: 'Adsorção' }
    };
    
    Plotly.newPlot('plotlyGraph', [trace], layout);
}

function plotPolarizacao(data) {
    const trace = {
        x: data.potencial,
        y: data.corrente,
        mode: 'lines+markers',
        line: { color: 'darkblue' }
    };
    
    const layout = {
        title: 'Polarização Eletroquímica',
        xaxis: { title: 'Potencial (V)' },
        yaxis: { title: 'Corrente (A)' }
    };
    
    Plotly.newPlot('plotlyGraph', [trace], layout);
}

// Função de notificação
function showNotification(message, type) {
    const notification = document.createElement('div');
    notification.className = `notification ${type}`;
    notification.textContent = message;
    
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        padding: 15px 20px;
        border-radius: 5px;
        color: white;
        font-weight: bold;
        z-index: 1000;
        animation: slideIn 0.3s ease;
    `;
    
    if (type === 'success') {
        notification.style.backgroundColor = '#4CAF50';
    } else {
        notification.style.backgroundColor = '#f44336';
    }
    
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.remove();
    }, 3000);
}

// Inicializar quando a página carregar
document.addEventListener('DOMContentLoaded', function() {
    generateForm();
});