import pandas as pd
import numpy as np
import streamlit as st

def analise_exploratoria():
    st.title("📊 Análise Exploratória - Extratos Bancários de Partidos (2020)")
    
    # 1. Carregar dados
    st.header("1. Carregamento de Dados")
    try:
        extrato = pd.read_csv('extrato_bancario_partido_2020.csv', 
                             encoding='latin-1', sep=';', low_memory=False)
        st.success(f"✅ Dataset carregado com sucesso!")
        st.write(f"**Dimensões:** {extrato.shape[0]:,} linhas × {extrato.shape[1]} colunas")
    except Exception as e:
        st.error(f"❌ Erro ao carregar arquivo: {e}")
        return
    
    # 2. Informações básicas
    st.header("2. Informações Básicas")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total de Transações", f"{len(extrato):,}")
    with col2:
        st.metric("Partidos Únicos", extrato['SG_PARTIDO'].nunique())
    with col3:
        valor_total = extrato['VR_LANCAMENTO'].sum()
        st.metric("Valor Total Movimentado", f"R$ {valor_total:,.2f}")
    
    # 3. Estrutura das colunas
    st.header("3. Estrutura das Colunas")
    st.write("**Colunas disponíveis:**")
    for i, col in enumerate(extrato.columns, 1):
        st.write(f"{i}. `{col}`")
    
    # 4. Amostra dos dados
    st.header("4. Amostra dos Dados")
    st.dataframe(extrato.head(10), use_container_width=True)
    
    # 5. Análise de valores missing
    st.header("5. Valores Missing/Problemas")
    missing_data = extrato.isnull().sum()
    st.write("Valores missing por coluna:")
    st.dataframe(missing_data[missing_data > 0], use_container_width=True)
    
    # 6. Análise de tipos de lançamento
    st.header("6. Tipos de Lançamento")
    tipo_lancamento = extrato['TP_LANCAMENTO'].value_counts()
    st.write(tipo_lancamento)
    
    # 7. Partidos com mais movimentação
    st.header("7. Top 10 Partidos por Movimentação")
    movimentacao_partidos = extrato.groupby('SG_PARTIDO').agg({
        'VR_LANCAMENTO': ['sum', 'count']
    }).round(2)
    movimentacao_partidos.columns = ['Valor Total', 'Qtd Transações']
    st.dataframe(movimentacao_partidos.nlargest(10, 'Valor Total'), use_container_width=True)
    
    # 8. Análise de valores
    st.header("8. Estatísticas dos Valores")
    st.write(extrato['VR_LANCAMENTO'].describe())
    
    # 9. Verificar colunas críticas para nossas perguntas
    st.header("9. Colunas Críticas para Análise")
    colunas_criticas = ['DS_LANCAMENTO', 'NM_CONTRAPARTE', 'DS_FONTE_RECURSO', 'DS_TIPO_OPERACAO']
    for coluna in colunas_criticas:
        if coluna in extrato.columns:
            st.write(f"**{coluna}:** {extrato[coluna].nunique()} valores únicos")
            st.write(f"Exemplos: {extrato[coluna].dropna().head(5).tolist()}")
        else:
            st.warning(f"Coluna {coluna} não encontrada!")
    
    return extrato

# Executar análise
if __name__ == "__main__":
    df = analise_exploratoria()