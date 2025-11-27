import gdown
import os
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import plotly.graph_objects as go

# Baixar o arquivo do Google Drive antes de carregar
url = "https://drive.google.com/uc?id=1kUYPvgu-HCIdvdWVDYGCbbfEjEvOetzH"
output = "extrato_bancario_DASHBOARD.csv"

if not os.path.exists(output):
    st.info("Baixando base de dados do Google Drive...")
    gdown.download(url, output, quiet=False)
    st.success("Base de dados carregada com sucesso!")

# Agora sim, chama a função que usa o arquivo
@st.cache_data
def carregar_dados():
    """Carrega o dataset tratado para análise ou usa dados de demonstração."""
    try:
        df = pd.read_csv('extrato_bancario_DASHBOARD.csv', encoding='utf-8')
        df['DT_LANCAMENTO'] = pd.to_datetime(df['DT_LANCAMENTO'], errors='coerce')
    except Exception as e:
        st.warning(f"Usando dados de demonstração. O arquivo não foi encontrado. Erro: {e}")
        data = {
            'DT_LANCAMENTO': pd.to_datetime([
                '2020-01-15', '2020-02-20', '2020-03-10',
                '2020-04-05', '2020-05-25', '2020-06-01'
            ]),
            'NM_ESFERA': ['NACIONAL', 'ESTADUAL', 'MUNICIPAL', 'NACIONAL', 'ESTADUAL', 'MUNICIPAL'],
            'CATEGORIA_GASTO': ['PESSOAL', 'PROPAGANDA', 'OUTROS', 'ALUGUEL', 'PESSOAL', 'PROPAGANDA'],
            'SG_PARTIDO': ['PT', 'PSDB', 'MDB', 'PT', 'PSDB', 'MDB'],
            'NM_CONTRAPARTE': ['A', 'B', 'C', 'D', 'E', 'F'],
            'VR_LANCAMENTO_NUM': [500000.00, 200000.00, 50000.00, 300000.00, 150000.00, 75000.00]
        }
        df = pd.DataFrame(data)

    return df

# E aqui, de fato, chama a função:
df = carregar_dados()


# =============================================
# CONFIGURAÇÃO DE ESTILO CORPORATIVO
# =============================================
CORES = {
    'azul_escuro': '#0F4C75',
    'azul_medio': '#3282B8',
    'azul_claro': '#BBE1FA',
    'azul_muito_escuro': '#1B262C',
    'cinza_escuro': '#393E46',
    'cinza_medio': '#686D76',
    'cinza_claro': '#EEEEEE',
    'branco': '#FFFFFF',
    'amarelo_mostarda': "#FFC400",
    'laranja': "#FF9900",
    'gradiente_principal': ['#0F4C75', '#2E72A2', '#5D99C6', '#89CFF0', '#BBE1FA', '#FF9900', '#FFC400'],
    'gradiente_secundario': ['#1B262C', '#0F4C75', '#3282B8'],
    'mapa_cores_esferas': {
        'NACIONAL': '#0F4C75', # Azul Escuro
        'ESTADUAL': '#FF9900', # Laranja para contraste
        'MUNICIPAL': '#5D99C6', # Azul Médio-claro
        'DISTRITAL': '#3282B8', # Outro tom de azul
        'NAO INFORMADO': '#393E46' # Cinza Escuro
    }
}
TEMA_PLOTLY = {
    'plot_bgcolor': CORES['branco'],
    'paper_bgcolor': CORES['branco'],
    'font_color': '#333333',
    'font_family': "Inter, sans-serif",
    'titulo_cor': CORES['azul_escuro'],
    'legenda_cor': CORES['azul_escuro']
}

def configurar_estilo_azul_profissional():
    """Configura estilo visual com tema azul profissional e retorna cores."""
    
    st.set_page_config(
        page_title="Análise Financeira - Partidos Políticos",
        page_icon="📊",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Aplica CSS para o tema e estiliza o sidebar
    st.markdown(f"""
    <style>
    .stApp {{
        background: linear-gradient(135deg, {CORES['azul_escuro']} 0%, {CORES['azul_medio']} 50%, {CORES['azul_claro']} 100%);
        background-attachment: fixed;
    }}
    .main .block-container {{
        background-color: rgba(255, 255, 255);
        border-radius: 12px;
        padding: 2rem;
        margin: 1rem;
        box-shadow: 0 8px 32px rgba(0,0,0,0.15);
        border: 1px solid rgba(255, 255, 255, 0.5);
        color: {CORES['azul_muito_escuro']};
    }}
    /* Títulos do corpo principal mais claros e definidos */
    h1 {{ color: {CORES['branco']} !important; }}
    h2 {{ color: {CORES['azul_escuro']} !important; }}
    h3 {{ color: {CORES['amarelo_mostarda']} !important; }}
    h4 {{ color: {CORES['laranja']} !important; }}

    /* Estilização do Sidebar para harmonizar com o tema */
    .css-1d3f9ho {{ /* st.sidebar element */
        background-color: {CORES['azul_muito_escuro']} !important; 
        color: {CORES['branco']} !important;
        padding: 1rem;
        border-radius: 0 12px 12px 0;
    }}
    .css-1d3f9ho h3, .css-1d3f9ho h4 {{
        color: {CORES['azul_claro']} !important; 
    }}
    .css-1d3f9ho label, .css-1d3f9ho .st-cg {{ /* Labels e textos */
        color: {CORES['branco']} !important;
    }}
    </style>
    """, unsafe_allow_html=True)
    
    return CORES

# =============================================
# CARREGAMENTO DE DADOS
# =============================================


# =============================================
# CONFIGURAÇÃO DO TEMA PLOTLY
# =============================================

TEMA_PLOTLY = {
    'title_color': CORES['azul_escuro'],
    'font_color': CORES['azul_muito_escuro'], 
    'height': 500,
    'plot_bg': CORES['branco'],
    'paper_bg': CORES['branco']
}

@st.cache_data
def configurar_layout(fig, titulo):
    """
    Aplica um layout padrão (tema e centralização de título) à figura do Plotly.
    """
    titulo_cor = TEMA_PLOTLY.get('title_color', '#0F4C75')
    fonte_cor = TEMA_PLOTLY.get('font_color', 'black')
    paper_cor = TEMA_PLOTLY.get('paper_bg', 'white')
    plot_cor = TEMA_PLOTLY.get('plot_bg', 'white')

    fig.update_layout(
        title={
            'text': titulo,
            'y': 0.95, 
            'x': 0.5, 
            'xanchor': 'center',
            'yanchor': 'top',
            'font': dict(
                size=20,
                color=titulo_cor
            )
        },
        paper_bgcolor=paper_cor,
        plot_bgcolor=plot_cor,
        font=dict(
            color=fonte_cor
        ),
        height=TEMA_PLOTLY.get('height', 500),
        margin=dict(t=80, b=50, l=50, r=50) 
    )

    return fig

# =============================================
# FUNÇÕES ESPECÍFICAS PARA P1
# =============================================

@st.cache_data
def criar_grafico_barras_agrupadas_esferas(dados, cores):
    """GRÁFICO 1: Barras agrupadas - Gastos por categoria × esfera"""
    
    esfera_categoria = dados.groupby(['NM_ESFERA', 'CATEGORIA_GASTO'])['VR_LANCAMENTO_NUM'].sum().reset_index()
    
    top_categorias = dados.groupby('CATEGORIA_GASTO')['VR_LANCAMENTO_NUM'].sum().nlargest(6).index
    dados_filtrados = esfera_categoria[esfera_categoria['CATEGORIA_GASTO'].isin(top_categorias)]
    
    fig = px.bar(
        dados_filtrados,
        x='CATEGORIA_GASTO',
        y='VR_LANCAMENTO_NUM',
        color='NM_ESFERA',
        barmode='group',
        color_discrete_sequence=cores['gradiente_principal']
    )
    
    fig = configurar_layout(fig, 'COMPARAÇÃO DE GASTOS POR CATEGORIA ENTRE ESFERAS')
    
    fig.update_layout(
        xaxis=dict(
            title_text='CATEGORIA DE GASTO',
            linecolor=TEMA_PLOTLY['font_color'],
            gridcolor=TEMA_PLOTLY['font_color'],
            tickcolor=TEMA_PLOTLY['font_color'],
            tickfont=dict(color=TEMA_PLOTLY['font_color']),
            title_font=dict(color=TEMA_PLOTLY['font_color'])
        ),
        yaxis=dict(
            title_text='VALOR TOTAL (R$)',
            linecolor=TEMA_PLOTLY['font_color'],
            gridcolor=TEMA_PLOTLY['font_color'],
            tickcolor=TEMA_PLOTLY['font_color'],
            tickfont=dict(color=TEMA_PLOTLY['font_color']),
            title_font=dict(color=TEMA_PLOTLY['font_color'])
        ),
        legend=dict(
            font=dict(color=TEMA_PLOTLY['font_color']),
            title_text='Esfera',
            title=dict(
                font=dict(
                    color=TEMA_PLOTLY['font_color'],
                    weight='bold'   
                )
            )
        )
    )
    
    fig.update_xaxes(tickangle=45)
    fig.update_yaxes(tickformat=",.0f")
    
    return fig

@st.cache_data
def criar_grafico_treemap_esferas(dados, cores):
    """GRÁFICO 2: Treemap hierárquico - Esfera → Partido → Categoria"""

    hierarquia = dados.groupby(['NM_ESFERA', 'SG_PARTIDO', 'CATEGORIA_GASTO'])['VR_LANCAMENTO_NUM'].sum().reset_index()

    partidos_top_por_esfera = []
    for esfera in dados['NM_ESFERA'].unique():
        top_partidos = (
            dados[dados['NM_ESFERA'] == esfera]
            .groupby('SG_PARTIDO')['VR_LANCAMENTO_NUM'].sum()
            .nlargest(3).index
        )
        for partido in top_partidos:
            partidos_top_por_esfera.append((esfera, partido))

    mask = hierarquia.apply(lambda x: (x['NM_ESFERA'], x['SG_PARTIDO']) in partidos_top_por_esfera, axis=1)
    dados_filtrados = hierarquia[hierarquia['SG_PARTIDO'].isin(dados['SG_PARTIDO'].unique())]
  

    gradiente_laranja = [
        "#FF6F00",  # Esfera
        "#FFA726",  # Partido
        "#FFE082"   # Categoria
    ]

    fig = px.treemap(
        dados_filtrados,
        path=['NM_ESFERA', 'SG_PARTIDO', 'CATEGORIA_GASTO'],
        values='VR_LANCAMENTO_NUM',
        color='NM_ESFERA',
        color_discrete_sequence=gradiente_laranja
    )

    fig.data[0].marker.colors = [
        gradiente_laranja[min(len(p.split('/')) - 1, 2)]
        for p in fig.data[0].ids
    ]

    fig = configurar_layout(fig, 'Mapa de Árvore: Estrutura Hierárquica de Gastos (Esfera / Partido / Categoria)')

    fig.update_traces(
        textinfo='label+value',
        hovertemplate='<b>%{label}</b><br>R$ %{value:,.2f}<extra></extra>',
        marker=dict(line=dict(color=cores['cinza_medio'], width=1))
    )

    fig.update_layout(
        margin=dict(t=80, l=0, r=0, b=0)
    )

    fig.add_trace(go.Scatter(
        x=[None], y=[None],
        mode='markers',
        marker=dict(size=10, color=gradiente_laranja[0]),
        name='Esfera'
    ))
    fig.add_trace(go.Scatter(
        x=[None], y=[None],
        mode='markers',
        marker=dict(size=10, color=gradiente_laranja[1]),
        name='Partido'
    ))
    fig.add_trace(go.Scatter(
        x=[None], y=[None],
        mode='markers',
        marker=dict(size=10, color=gradiente_laranja[2]),
        name='Categoria'
    ))

    fig.update_layout(
        legend=dict(
            title=dict(
                text='<b>NÍVEL HIERÁRQUICO</b>',
                font=dict(size=13, color=cores['azul_escuro']),
                side='top'
            ),
            font=dict(color=cores['azul_muito_escuro'], size=12),
            orientation='h',
            yanchor='bottom',
            y=-0.25,
            xanchor='center',
            x=0.5,
            valign='middle',
            itemsizing='constant',
            itemwidth=50,
            traceorder='normal'
        )
    )
    
    fig.update_xaxes(
        showgrid=False,
        zeroline=False,
        color='black',
        title_font=dict(color='black', size=12),
        tickfont=dict(color='black', size=11)
    )

    fig.update_yaxes(
        showgrid=False,
        zeroline=False,
        color='black',
        title_font=dict(color='black', size=12),
        tickfont=dict(color='black', size=11)
    )

    return fig

@st.cache_data
def criar_grafico_comparacao_percentual(dados, cores):
    """GRÁFICO 3: Comparação percentual entre esferas"""
    
    total_por_esfera = dados.groupby('NM_ESFERA')['VR_LANCAMENTO_NUM'].sum()
    percentual_esfera = dados.groupby(['NM_ESFERA', 'CATEGORIA_GASTO'])['VR_LANCAMENTO_NUM'].sum().reset_index()
    percentual_esfera['PERCENTUAL'] = percentual_esfera.apply(
        lambda x: (x['VR_LANCAMENTO_NUM'] / total_por_esfera[x['NM_ESFERA']]) * 100, 
        axis=1
    )
    
    top_categorias = dados.groupby('CATEGORIA_GASTO')['VR_LANCAMENTO_NUM'].sum().nlargest(5).index
    dados_filtrados = percentual_esfera[percentual_esfera['CATEGORIA_GASTO'].isin(top_categorias)]
    
    fig = px.bar(
        dados_filtrados,
        x='NM_ESFERA',
        y='PERCENTUAL',
        color='CATEGORIA_GASTO',
        barmode='stack',
        color_discrete_sequence=cores['gradiente_principal']
    )
    
    fig = configurar_layout(fig, 'Composição Percentual: DISTRIBUIÇÃO DAS CATEGORIAS DE GASTOS POR ESFERA')
    
    fig.update_layout(
        xaxis=dict(
            title_text='ESFERA PARTIDÁRIA',
            linecolor=TEMA_PLOTLY['font_color'],
            gridcolor=TEMA_PLOTLY['font_color'],
            tickcolor=TEMA_PLOTLY['font_color'],
            tickfont=dict(color=TEMA_PLOTLY['font_color']),
            title_font=dict(color=TEMA_PLOTLY['font_color'])
        ),
        yaxis=dict(
            title_text='PERCENTUAL (%)',
            linecolor=TEMA_PLOTLY['font_color'],
            gridcolor=TEMA_PLOTLY['font_color'],
            tickcolor=TEMA_PLOTLY['font_color'],
            tickfont=dict(color=TEMA_PLOTLY['font_color']),
            title_font=dict(color=TEMA_PLOTLY['font_color'])
        ),
        legend=dict(
            title=dict(
                text='<b>CATEGORIAS DE GASTOS</b>',
                font=dict(size=13, color='black')
            ),
            font=dict(color='black', size=12),
            orientation='v',
            yanchor='middle',
            y=0.5,
            xanchor='left',
            x=1.02,
            bgcolor='rgba(255,255,255,0)',
            bordercolor='rgba(0,0,0,0)',
            traceorder='normal'
        )
    )
    
    fig.update_yaxes(ticksuffix="%")
    
    return fig

# =============================================
# FUNÇÕES ESPECÍFICAS PARA P2 - VERSÃO CORRIGIDA
# =============================================

@st.cache_data
def criar_scatter_tarifas_vs_gastos(dados, cores):
    """GRÁFICO 4: Scatter plot - Tarifas bancárias vs Gastos totais por partido (EM MILHÕES)"""

    # Agrupa por partido
    dados_agrupados = dados.groupby('SG_PARTIDO').agg({
        'VR_LANCAMENTO_NUM': 'sum'
    }).reset_index()
    dados_agrupados.columns = ['SG_PARTIDO', 'GASTO_TOTAL']

    # Calcula tarifas por partido
    tarifas_partido = dados[dados['CATEGORIA_GASTO'] == 'TARIFAS BANCÁRIAS'].groupby('SG_PARTIDO')['VR_LANCAMENTO_NUM'].sum().reset_index()
    tarifas_partido.columns = ['SG_PARTIDO', 'VALOR_TARIFAS']

    # Merge
    dados_agrupados = dados_agrupados.merge(tarifas_partido, on='SG_PARTIDO', how='left')
    dados_agrupados['VALOR_TARIFAS'] = dados_agrupados['VALOR_TARIFAS'].fillna(0)

    # Calcula percentual corretamente
    dados_agrupados['PERC_TARIFAS'] = (dados_agrupados['VALOR_TARIFAS'] / dados_agrupados['GASTO_TOTAL']) * 100

    # Filtra partidos com gastos significativos
    dados_agrupados = dados_agrupados[dados_agrupados['GASTO_TOTAL'] > 10000]

    # Converte para milhões
    dados_agrupados['GASTO_TOTAL_M'] = dados_agrupados['GASTO_TOTAL'] / 1_000_000
    dados_agrupados['VALOR_TARIFAS_M'] = dados_agrupados['VALOR_TARIFAS'] / 1_000_000

    # Cria scatter plot
    fig = px.scatter(
        dados_agrupados,
        x='GASTO_TOTAL_M',
        y='PERC_TARIFAS',
        size='PERC_TARIFAS',
        color='PERC_TARIFAS',
        hover_name='SG_PARTIDO',
        hover_data={
            'GASTO_TOTAL': ':.2f',
            'VALOR_TARIFAS': ':.2f',
            'PERC_TARIFAS': ':.2f',
        },
        color_continuous_scale=cores['gradiente_secundario'],
        size_max=40
    )

    fig = configurar_layout(fig, 'EFICIÊNCIA: TARIFAS BANCÁRIAS vs GASTOS TOTAIS POR PARTIDO')

    # ----------------------------- FAIXAS DE EFICIÊNCIA (fundo) -----------------------------
    fig.add_hrect(y0=0, y1=1, fillcolor="green", opacity=0.07, layer="below", line_width=0)
    fig.add_hrect(y0=1, y1=2, fillcolor="orange", opacity=0.07, layer="below", line_width=0)
    fig.add_hrect(y0=2, y1=3, fillcolor="red", opacity=0.07, layer="below", line_width=0)

    # ----------------------------- LINHAS DE REFERÊNCIA -----------------------------
    fig.add_hline(y=1, line=dict(color='green', width=2, dash='dash'), name='1% (Excelente)')
    fig.add_hline(y=2, line=dict(color='orange', width=2, dash='dash'), name='2% (Boa)')
    fig.add_hline(y=3, line=dict(color='red', width=2, dash='dash'), name='3% (Alerta)')

    # ----------------------------- AJUSTE DOS EIXOS -----------------------------
    fig.update_xaxes(
        title_text='GASTOS TOTAIS (Milhões de R$)',
        type="log",
        tickformat=",.1f",
        showline=True,
        linewidth=2,
        linecolor="black",
        tickfont=dict(color="black"),
        title_font=dict(color="black")
    )

    fig.update_yaxes(
        title_text='PERCENTUAL DE TARIFAS BANCÁRIAS (%)',
        ticksuffix="%",
        range=[0, dados_agrupados['PERC_TARIFAS'].max() * 1.25],  # Aumenta limite e evita ponto cortado
        showline=True,
        linewidth=2,
        linecolor="black",
        tickfont=dict(color="black"),
        title_font=dict(color="black")
    )
    fig.update_coloraxes(
        colorbar=dict(
            title="% Tarifas",
            tickfont=dict(color="black")
        )
    )
    return fig


@st.cache_data
def criar_ranking_eficiencia(dados, cores):
    """GRÁFICO 5: Ranking de eficiência - Menor % em tarifas bancárias"""
    
    # Calcula totais por partido
    totais_partido = dados.groupby('SG_PARTIDO')['VR_LANCAMENTO_NUM'].sum().reset_index()
    totais_partido.columns = ['SG_PARTIDO', 'TOTAL_GASTO']
    
    # Calcula tarifas por partido
    tarifas_partido = dados[dados['CATEGORIA_GASTO'] == 'TARIFAS BANCÁRIAS'].groupby('SG_PARTIDO')['VR_LANCAMENTO_NUM'].sum().reset_index()
    tarifas_partido.columns = ['SG_PARTIDO', 'TOTAL_TARIFAS']
    
    # Merge e cálculo de percentual
    eficiencia = totais_partido.merge(tarifas_partido, on='SG_PARTIDO', how='left')
    eficiencia['TOTAL_TARIFAS'] = eficiencia['TOTAL_TARIFAS'].fillna(0)
    eficiencia['PERC_TARIFAS'] = (eficiencia['TOTAL_TARIFAS'] / eficiencia['TOTAL_GASTO']) * 100
    
    # Ordena por eficiência (menor percentual primeiro)
    eficiencia = eficiencia.sort_values('PERC_TARIFAS', ascending=True)
    
    # Filtra partidos com gastos significativos (pelo menos R$ 50.000)
    eficiencia = eficiencia[eficiencia['TOTAL_GASTO'] > 50000]
    
    # Seleciona top 15 mais eficientes
    eficiencia = eficiencia.head(15)
    
    fig = px.bar(
        eficiencia,
        y='SG_PARTIDO',
        x='PERC_TARIFAS',
        orientation='h',
        color='PERC_TARIFAS',
        color_continuous_scale=['#00A86B', '#32CD32', '#90EE90'],  # Tons de verde para eficiência
        hover_data={
            'TOTAL_GASTO': ':.2f',
            'TOTAL_TARIFAS': ':.2f',
            'PERC_TARIFAS': ':.2f'
        }
    )
    
    fig = configurar_layout(fig, 'RANKING DE EFICIÊNCIA: MENOR % DE TARIFAS BANCÁRIAS')
    
    fig.update_layout(
        yaxis=dict(
            title_text='PARTIDO',
            linecolor=TEMA_PLOTLY['font_color'],
            gridcolor=TEMA_PLOTLY['font_color'],
            tickcolor=TEMA_PLOTLY['font_color'],
            tickfont=dict(color=TEMA_PLOTLY['font_color']),
            title_font=dict(color=TEMA_PLOTLY['font_color']),
            categoryorder='array',
            categoryarray=eficiencia['SG_PARTIDO'].tolist()[::-1]
        ),
        xaxis=dict(
            title_text='PERCENTUAL DE TARIFAS BANCÁRIAS (%)',
            linecolor=TEMA_PLOTLY['font_color'],
            gridcolor=TEMA_PLOTLY['font_color'],
            tickcolor=TEMA_PLOTLY['font_color'],
            tickfont=dict(color=TEMA_PLOTLY['font_color']),
            title_font=dict(color=TEMA_PLOTLY['font_color'])
        ),
        coloraxis_colorbar=dict(
            title="% Tarifas"
        )
    )
    
    fig.update_xaxes(ticksuffix="%")
    
    return fig
@st.cache_data
def criar_indice_diversificacao_fornecedores(dados, cores):
    """GRÁFICO 6: Índice de diversificação de fornecedores por partido"""
    
    # Calcula métricas por partido
    diversificacao = dados.groupby('SG_PARTIDO').agg({
        'NM_CONTRAPARTE': 'nunique',  # Número único de fornecedores
        'VR_LANCAMENTO_NUM': 'sum',   # Total gasto
        'DT_LANCAMENTO': 'count'      # Número de transações
    }).reset_index()
    
    diversificacao.columns = ['SG_PARTIDO', 'QTD_FORNECEDORES', 'TOTAL_GASTO', 'QTD_TRANSACOES']
    
    # Calcula o índice de diversificação (fornecedores por milhão de reais)
    diversificacao['INDICE_DIVERSIFICACAO'] = (diversificacao['QTD_FORNECEDORES'] / diversificacao['TOTAL_GASTO']) * 1_000_000
    
    # Filtra partidos com gastos significativos (pelo menos R$ 100.000)
    diversificacao = diversificacao[diversificacao['TOTAL_GASTO'] > 100000]
    
    # Ordena por índice de diversificação (maior = mais diversificado)
    diversificacao = diversificacao.sort_values('INDICE_DIVERSIFICACAO', ascending=False)
    
    # Seleciona top 15 partidos mais diversificados
    diversificacao = diversificacao.head(15)
    
    fig = px.bar(
        diversificacao,
        y='SG_PARTIDO',
        x='INDICE_DIVERSIFICACAO',
        orientation='h',
        color='INDICE_DIVERSIFICACAO',
        color_continuous_scale=cores['gradiente_principal'],
        hover_data={
            'QTD_FORNECEDORES': True,
            'TOTAL_GASTO': ':.2f',
            'QTD_TRANSACOES': True,
            'INDICE_DIVERSIFICACAO': ':.2f'
        }
    )
    
    fig = configurar_layout(fig, 'DIVERSIFICAÇÃO: ÍNDICE DE FORNECEDORES POR PARTIDO')
    
    fig.update_layout(
        yaxis=dict(
            title_text='PARTIDO',
            linecolor=TEMA_PLOTLY['font_color'],
            gridcolor=TEMA_PLOTLY['font_color'],
            tickcolor=TEMA_PLOTLY['font_color'],
            tickfont=dict(color=TEMA_PLOTLY['font_color']),
            title_font=dict(color=TEMA_PLOTLY['font_color']),
            categoryorder='total ascending'
        ),
        xaxis=dict(
            title_text='ÍNDICE DE DIVERSIFICAÇÃO (Fornecedores por Milhão de R$)',
            linecolor=TEMA_PLOTLY['font_color'],
            gridcolor=TEMA_PLOTLY['font_color'],
            tickcolor=TEMA_PLOTLY['font_color'],
            tickfont=dict(color=TEMA_PLOTLY['font_color']),
            title_font=dict(color=TEMA_PLOTLY['font_color'])
        ),
        coloraxis_colorbar=dict(
            title="Índice"
        )
    )
    
    return fig

# =============================================
# LAYOUT PRINCIPAL
# =============================================

def main():
    global CORES 
    CORES = configurar_estilo_azul_profissional()
    
    TEMA_PLOTLY.update({
        'title_color': CORES['azul_escuro'],
        'font_color': CORES['azul_muito_escuro'],
        'plot_bg': CORES['branco'],
        'paper_bg': CORES['branco']
    })
    
    # Carrega dados dentro do main (garante que 'dados' exista antes de usar)
    dados = carregar_dados()
    if dados is None:
        return

    
# REMOVE TODOS OS "NÃO INFORMADO" DO DATAFRAME
    dados = dados[
        ~dados['NM_ESFERA'].str.contains("NÃO INFORMADO", case=False, na=False) &
        ~dados['CATEGORIA_GASTO'].str.contains("NÃO INFORMADO", case=False, na=False) &
        ~dados['SG_PARTIDO'].str.contains("NÃO INFORMADO", case=False, na=False)
    ]
    
    if dados is None:
        return
    # Sidebar
    with st.sidebar:
        st.markdown("### CONTROLES DE ANÁLISE")
        
        # ---- Filtro Esferas ----
        lista_esferas = sorted(dados['NM_ESFERA'].unique())
        opcoes_esferas = ["Todas as esferas"] + lista_esferas

        esferas_sel = st.multiselect("Selecione as Esferas:", opcoes_esferas, default=["Todas as esferas"])
        esferas = lista_esferas if "Todas as esferas" in esferas_sel else esferas_sel
        
        # ---- Filtro Categorias ----
        lista_categorias = sorted(dados['CATEGORIA_GASTO'].unique())
        opcoes_categorias = ["Todas as categorias"] + lista_categorias

        categorias_sel = st.multiselect("Selecione as Categorias:", opcoes_categorias, default=["Todas as categorias"])
        categorias = lista_categorias if "Todas as categorias" in categorias_sel else categorias_sel

        # ---- Filtro Partidos ----
        lista_partidos = sorted(dados['SG_PARTIDO'].unique())
        opcoes_partidos = ["Todos os partidos"] + lista_partidos

        partidos_sel = st.multiselect("Selecione os Partidos:", opcoes_partidos, default=["Todos os partidos"])
        partidos = lista_partidos if "Todos os partidos" in partidos_sel else partidos_sel

        st.markdown("---")
        st.markdown("### RESUMO GERAL")
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Valor Total", f"R$ {dados['VR_LANCAMENTO_NUM'].sum():,.2f}")
            st.metric("Partidos", dados['SG_PARTIDO'].nunique())
        with col2:
            st.metric("Transações", f"{len(dados):,}")
            st.metric("Fornecedores", dados['NM_CONTRAPARTE'].nunique())


        # Filtragem de dados
        dados_filt = dados.copy()
        dados_filt = dados_filt[dados_filt['NM_ESFERA'].isin(esferas)]
        dados_filt = dados_filt[dados_filt['CATEGORIA_GASTO'].isin(categorias)]
        dados_filt = dados_filt[dados_filt['SG_PARTIDO'].isin(partidos)]
            

    # Conteúdo principal
    st.title("ANÁLISE FINANCEIRA DE PARTIDOS POLÍTICOS")
    st.markdown("Dashboard de Transparência - Dados TSE 2020")
    
    st.markdown("### VISÃO GERAL FILTRADA")
    st.metric(
        "VALOR TOTAL ANALISADO", 
        f"R$ {dados_filt['VR_LANCAMENTO_NUM'].sum():,.2f}",
        delta=f"{len(dados_filt):,} transações"
    )

    # =============================================
    # SEÇÃO P1 - COMPARAÇÃO ENTRE ESFERAS
    # =============================================
    
    st.markdown("---")
    st.markdown("### P1: Como os padrões de gastos diferem entre as esferas partidárias?")
    
    st.markdown("""
    **Objetivo:** Comparar os padrões de gastos entre esferas municipais, estaduais e nacionais para identificar 
    diferenças na alocação de recursos e estratégias financeiras.
    """)

    # GRÁFICO 1
    st.markdown("#### Gráfico de Barras Agrupadas: GASTOS POR CATEGORIA ENTRE ESFERAS")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.plotly_chart(criar_grafico_barras_agrupadas_esferas(dados_filt, CORES), use_container_width=True)
    
    with col2:
        st.markdown("**Insights:**")
        st.markdown("""
        - Comparação de volume em cada categoria: As Transferências são a categoria com maior volume de gastos, superando todas as demais em todas as esferas.
        - Padrões dominantes: A esfera Nacional concentra a maior parte dos recursos, enquanto Distrital e Estadual apresentam volumes mais modestos e equilibrados.
        - Diferenças entre esferas: A distância entre as barras evidencia desigualdade na distribuição de recursos entre os níveis partidários, com predominância nacional e baixa participação municipal.
        """)

    st.markdown("***Gráfico 1: Comparação de gastos por categoria entre esferas***")
    st.markdown("O gráfico apresenta o volume total de gastos em cada categoria, distribuído entre as esferas partidárias (Distrital, Estadual, Municipal, Nacional e Não Informado)." \
    "Cada grupo de barras representa uma categoria de despesa, e as cores indicam a esfera correspondente.")

    # GRÁFICO 2
    st.markdown("#### Mapa de Árvore: ESTRUTURA HIERÁRQUICA POR ESFERA, PARTIDO e CATEGORIA")

    col1, col2 = st.columns([3, 1])

    with col1:
        st.plotly_chart(criar_grafico_treemap_esferas(dados_filt, CORES), use_container_width=True)

    with col2:
        st.markdown("**Insights:**")
        st.markdown("""
        - Hierarquia de gastos: O gráfico revela a estrutura hierárquica dos gastos públicos, mostrando a distribuição dos valores entre esferas, partidos e categorias.
        - Predomínio nacional: A Esfera Nacional concentra a maior parte dos recursos, destacando-se especialmente nas categorias de Transferências e Outras Despesas.
        - Partidos de maior participação: Partidos como PT, MDB e PSDB dominam os maiores blocos de gastos, indicando maior presença financeira.
        - Diversificação regional: As esferas Estadual e Municipal apresentam distribuição mais equilibrada entre partidos e tipos de despesa, sugerindo maior pulverização dos recursos.
        """)

    st.markdown("***Gráfico 2: Estrutura Hierárquica de Gastos***")
    st.markdown("Este mapa de árvore mostra como os gastos se organizam hierarquicamente, da Esfera ao Partido e à Categoria de gasto." \
    "Cada bloco representa o valor total movimentado, e seu tamanho indica a proporção do gasto em relação ao total." \
    "As cores em tons de laranja e amarelo representam os níveis hierárquicos — Esfera, Partido e Categoria —, facilitando a visualização das camadas de alocação de recursos.")

    # GRÁFICO 3
    st.markdown("#### Composição Percentual: DISTRIBUIÇÃO DAS CATEGORIAS DE GASTOS POR ESFERA")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.plotly_chart(criar_grafico_comparacao_percentual(dados_filt, CORES), use_container_width=True)
    
    with col2:
        st.markdown("**Insights:**")
        st.markdown("""
        - Proporção de cada categoria: O gráfico evidencia o peso relativo de cada tipo de gasto dentro de cada esfera. As Transferências dominam a composição, especialmente na esfera Nacional.
        - Balanceamento de gastos: As esferas Municipal e Distrital apresentam distribuições mais equilibradas entre as categorias, indicando maior diversidade de despesas.
        - Foco estratégico: A Esfera Nacional concentra recursos em Transferências e Pagamentos, refletindo foco em repasses e obrigações centrais, enquanto níveis locais tendem a pulverizar gastos em áreas operacionais.
        """)
    
    st.markdown("***Gráfico 3: Composição Percentual por Esfera***")
    st.markdown("Mostra a proporção das principais categorias de gasto dentro de cada esfera partidária." \
    "Cada barra representa 100% dos gastos da esfera, segmentada por categoria (cores)." \
    "Os tons de azul indicam o peso relativo de cada despesa, permitindo comparar estruturas de gasto e prioridades financeiras entre as esferas Distrital, Estadual, Municipal e Nacional.")

    # =============================================
    # SEÇÃO P2 - EFICIÊNCIA NA GESTÃO
    # =============================================
    
    st.markdown("---")
    st.markdown("### P2: Quais partidos são mais eficientes na gestão (menos tarifas bancárias, mais gastos diretos)?")
    
    st.markdown("""
    **Objetivo:** Identificar os partidos com melhor gestão financeira através da análise da relação entre 
    tarifas bancárias e gastos totais, considerando eficiência operacional.
    """)

    # GRÁFICO 4
    st.markdown("#### Gráfico de Dispersão: TARIFAS BANCÁRIAS vs GASTOS TOTAIS")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.plotly_chart(criar_scatter_tarifas_vs_gastos(dados_filt, CORES), use_container_width=True)
    
    with col2:
        # No lugar dos insights atuais, use:
        st.markdown("**Insights:**")
        st.markdown("""    
        - Partidos pequenos têm proporcionalmente maior gasto com tarifas.
        - As bolhas grandes estão concentradas em valores baixos de gasto total (próximo de zero):Isso significa que partidos com pouco orçamento acabam pagando tarifas bancárias altas em proporção.
        - Partidos grandes são muito mais eficientes (<1%).
        """)

    st.markdown("***Gráfico 4: Análise de Dispersão - Eficiência Financeira***")
    st.markdown("""
    Cada ponto representa um **partido**, onde:
    - Eixo X: Volume total de gastos (em milhões de R$)
    - Eixo Y: Valor absoluto em tarifas bancárias (em milhões de R$)
    - Tamanho das bolhas: Percentual de tarifas sobre o total de gastos
    - Linhas tracejadas de referência:
    - Verde (1%) → Eficiência excelente
    - Laranja (1%–2%) → Eficiência boa/moderada
    - Vermelha (2%–3%) → Eficiência regular
    - Acima de 3% → Eficiência baixa (alerta)
    - Posição relativa:
    - Abaixo da linha verde: desempenho exemplar
    - Entre as linhas: desempenho aceitável, mas com margem de melhoria
    """)

    # GRÁFICO 5
    st.markdown("#### Ranking de Eficiência: MENOR % DE TARIFAS BANCÁRIAS")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.plotly_chart(criar_ranking_eficiencia(dados_filt, CORES), use_container_width=True)
    
    with col2:
        # No lugar dos insights atuais do ranking, use:
        st.markdown("**Insights:**")
        st.markdown("""    
        - **Top eficientes:** AVANTE, PROS e PODE — apresentam a menor incidência de tarifas.
        - **Referência setorial:** serve como benchmark para outras legendas buscarem eficiência.
        - **Meta ideal:** percentual abaixo de 2% é considerado excelente, e todos estão bem abaixo disso, o que demonstra bom desempenho geral.
        - **Oportunidade:** partidos acima de 0,03% podem revisar práticas bancárias para reduzir custos.
        """)

    st.markdown("***Gráfico 5: Ranking de Eficiência Financeira***")
    st.markdown("""
    Ranking horizontal dos partidos com **menor percentual de tarifas bancárias** em relação aos gastos totais.  
    - **Barras verdes** = partidos mais eficientes (menor % de tarifas)
    - **Ordenação** = do mais eficiente (topo) para o menos eficiente
    - **Dados hover** = mostram valores absolutos de gastos totais e tarifas
    - **Filtro aplicado** = apenas partidos com gastos superiores a R$ 50.000
    """)

    # =============================================
    # SEÇÃO P3 - DIVERSIFICAÇÃO DE FORNECEDORES
    # =============================================

    st.markdown("---")
    st.markdown("### P3: Como a concentração de gastos por fornecedor varia entre os partidos (análise de diversificação)?")

    st.markdown("""
    **Objetivo:** Analisar a concentração ou diversificação dos gastos entre fornecedores, 
    identificando partidos que distribuem melhor seus recursos ou concentram em poucos contratados.
    """)

    # GRÁFICO 6
    st.markdown("#### Índice de Diversificação: FORNECEDORES POR MILHÃO DE REAIS")

    col1, col2 = st.columns([3, 1])

    with col1:
        st.plotly_chart(criar_indice_diversificacao_fornecedores(dados_filt, CORES), use_container_width=True)

    with col2:
        st.markdown("**Insights:**")
        st.markdown("""        
        - **Diversificação de fornecedores:** O gráfico mostra o quanto cada partido distribui seus gastos entre diferentes fornecedores, revelando o nível de pulverização dos contratos.
        - **Maior índice = maior diversificação:** Partidos como PSTU e PRTB demonstram ampla dispersão dos gastos, o que indica baixo risco de concentração e maior transparência.
        - **Menor índice = maior concentração:** Partidos com índices menores concentram seus gastos em poucos fornecedores, o que pode indicar dependência operacional ou centralização financeira.
        """)

    st.markdown("***Gráfico 6: Índice de Diversificação de Fornecedores***")
    st.markdown("""
    O índice mostra **quantos fornecedores diferentes** cada partido utiliza **por milhão de reais gasto**:
    - **Barras maiores** = Partidos mais diversificados (mais fornecedores por volume)
    - **Barras menores** = Partidos mais concentrados (menos fornecedores por volume)
    - **Cores** = Intensidade do índice de diversificação
    """)

    # =============================================
    # INFORMAÇÕES TÉCNICAS - P1, P2 & P3
    # =============================================

    st.markdown("---")
    st.markdown("#### INFORMAÇÕES TÉCNICAS - P1, P2 & P3")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("**FILTROS APLICADOS:**")
        st.markdown(f"- Esferas: {len(esferas)}")
        st.markdown(f"- Categorias: {len(categorias)}")
        st.markdown(f"- Partidos filtrados: {len(partidos)} selecionados")


    with col2:
        st.markdown("**GRÁFICOS UTILIZADOS:**")
        st.markdown("- P1: Barras Agrupadas, Treemap, Composição")
        st.markdown("- P2: Scatter Plot, Ranking Horizontal") 
        st.markdown("- P3: Índice de Diversificação")

    with col3:
        st.markdown("**DADOS DA ANÁLISE:**")
        if not dados_filt.empty and pd.notna(dados_filt['DT_LANCAMENTO']).any():
            st.markdown(f"- Período: {dados_filt['DT_LANCAMENTO'].min().strftime('%d/%m/%Y')} a {dados_filt['DT_LANCAMENTO'].max().strftime('%d/%m/%Y')}")
        else:
            st.markdown("- Período: N/A")
            
        st.markdown(f"- Transações: {len(dados_filt):,}")
        st.markdown(f"- Partidos analisados: {dados_filt['SG_PARTIDO'].nunique()}")
        st.markdown(f"- Fornecedores únicos: {dados_filt['NM_CONTRAPARTE'].nunique()}")

    # Rodapé
    st.markdown("---")
    st.markdown(
        "<div style='text-align: center; color: #393E46;'>"
        "Fonte: TSE — Dados Abertos 2020"
        #f"Gerado em: {pd.Timestamp.now().strftime('%d/%m/%Y às %H:%M')}"
        "</div>", 
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()