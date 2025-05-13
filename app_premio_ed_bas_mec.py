import streamlit as st
import pandas as pd

# Configuração da página
st.set_page_config(page_title="Prêmio MEC Educação Básica", layout="wide")

st.title("Prêmio MEC Educação Básica")
tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs(['Educação infantil', 'Alfabetização', 'Fundamental AI',
         'Fundamental AF', 'Médio', 'Enem', 'TI', 'Médio EPT'])
# Carregando pipos dados
@st.cache_data
def load_data():
    df_microdados = pd.read_csv('microdados_ed_basica_2024/dados/microdados_ed_basica_2024_resumido.csv', sep=';', encoding='latin1')
    df_sinopse = pd.read_excel('sinopse/dados_creche.xlsx', sheet_name='total')
    # df_pop = pd.read_excel('insumos/populacao_municipio_2022_2024.xlsx')
    df_ideb_esc_ai = pd.read_csv('ideb/tratado/ideb_esc_ai.csv', sep=';', encoding='latin1')
    df_ideb_esc_af = pd.read_csv('ideb/tratado/ideb_esc_af.csv', sep=';', encoding='latin1')    
    df_ideb_esc_af = pd.read_csv('ideb/tratado/ideb_esc_af.csv', sep=';', encoding='latin1')
    df_ideb_esc_em = pd.read_csv('ideb/tratado/ideb_esc_em.csv', sep=';', encoding='latin1')
    df_ideb_mun_ai = pd.read_csv('ideb/tratado/ideb_mun_ai.csv', sep=';', encoding='latin1')
    df_ideb_mun_af = pd.read_csv('ideb/tratado/ideb_mun_af.csv', sep=';', encoding='latin1')
    df_ideb_mun_em = pd.read_csv('ideb/tratado/ideb_mun_em.csv', sep=';', encoding='latin1')
    df_ideb_uf_ai = pd.read_csv('ideb/tratado/ideb_uf_ai.csv', sep=';', encoding='latin1')
    df_ideb_uf_af = pd.read_csv('ideb/tratado/ideb_uf_af.csv', sep=';', encoding='latin1')
    df_ideb_uf_em = pd.read_csv('ideb/tratado/ideb_uf_em.csv', sep=';', encoding='latin1')
    df_inse_esc = pd.read_excel('inse/INSE_2021_escolas.xlsx')
    df_inse_mun = pd.read_excel('inse/INSE_2021_municipios.xlsx')
    df_inse_uf = pd.read_excel('inse/INSE_2021_estados.xlsx')
    return df_microdados, df_sinopse, df_ideb_esc_ai, df_ideb_esc_af, df_ideb_esc_em, df_ideb_mun_ai, df_ideb_mun_af, df_ideb_mun_em, df_ideb_uf_ai, df_ideb_uf_af, df_ideb_uf_em, df_inse_esc, df_inse_mun, df_inse_uf

microdados, sinopse, ideb_esc_ai, ideb_esc_af, ideb_esc_em, ideb_mun_ai, ideb_mun_af, ideb_mun_em, ideb_uf_ai, ideb_uf_af, ideb_uf_em, inse_esc, inse_mun, inse_uf = load_data()

# Primeira seção/aba: Top 5 municípios por região
with tab1:
    st.header("Educação infantil")

    f'''**Fontes e filtros utilizados**:\n
    Sinopse do Censo da Educação Básica 2024
    - Matriculados na creche total ou de 0 a 3 anos: T_CRECHE ou T_CRECHE_0_3
    - Preenchimento de informações de raça/cor: P_RACA_COR
    Censo Demográfico 2022
    - População total de 0 a 3 anos: POP_0_3_CENSO22
    Projeção Populacional 2024
    - População total de 0 a 3 anos: POP_0_3_PROJ24'''

    col1, col2, col3 = st.columns(3)
    # Adicionando um seletor para escolher a taxa de cobertura
    with col1:
        tx_cobertura_opcao = st.radio(
        "Escolha a cobertura para ordenação:",
        options=['Censo Demográfico 2022', 'Projeção Populacional 2024'],
        index=0
    )
    
    with col2:
        botao_creche = st.radio(
        "Escolha a variável a ser utilizada:",
        options=['Total de matriculados na crecre', 'Total de matriculados na creche de 0 a 3 anos'],
        index=0
    )

    with col3:
        limiar = st.slider(
            "Selecione o limiar mínimo para o percentual de preenchimento das informações de raça/cor:",
            min_value=0,
            max_value=100,
            value=0,  # Valor padrão (90%)
            step=1,
            format="%d%%"
        ) / 100  # Converte para decimal (0.90)

    # Aplica o filtro
    df_filtrado = sinopse[sinopse['P_RACA_COR'] > limiar]

    # Definindo a coluna de população conforme a taxa escolhida
    if tx_cobertura_opcao == 'Censo Demográfico 2024':
        pop_col = 'POP_0_3_CENSO22'
    else:
        pop_col = 'POP_0_3_PROJ24'
    
    if botao_creche == 'Total de matriculados na crecre':
        var_creche = 'T_CRECHE'
    else:
        var_creche = 'T_CRECHE_0_3'

    # Calculando a razão entre T_CRECHE_0_3 e pop_col
    df_filtrado['P_COBERTURA_CALC'] = (df_filtrado[var_creche] / df_filtrado[pop_col]).clip(upper=1)

    # Agrupando e selecionando os 5 primeiros por região com base na taxa escolhida
    top_municipios = (
        df_filtrado
        # Ordena por região e taxa de cobertura (decrescente)
        .sort_values(['NO_REGIAO', 'P_COBERTURA_CALC', var_creche], 
                     ascending=[True, False, False])
        # Agrupa por região e mantém os 5 maiores de cada grupo
        .groupby('NO_REGIAO', as_index=False)
        .head(5)
        # Seleciona colunas relevantes
        [['NO_REGIAO', 'NO_UF', 'CO_MUNICIPIO', 'NO_MUNICIPIO', var_creche, 
        pop_col, 'P_COBERTURA_CALC', 'P_RACA_COR']]
    )

    # Formatando as colunas de percentual com 1 casa decimal
    top_municipios['P_COBERTURA_CALC'] = (top_municipios['P_COBERTURA_CALC'] * 100).round(1).astype(str) + '%'
    top_municipios['P_RACA_COR'] = (top_municipios['P_RACA_COR'] * 100).round(1).astype(str) + '%'


    st.dataframe(top_municipios, use_container_width=True, hide_index=True)

with tab2:
    st.header('Alfabetização')

with tab3:
    st.header('Fundamental AI')

    f'''**Fontes e filtros utilizados**:\n
    Censo da Educação Básica 2024
    - Tipo de dependência: municipal (TP_DEPENDENCIA == 3)
    - Indicador de oferta do fundamental anos iniciais (IN_FUND_AI == 1)
    - Matriculados nos anos iniciais: QT_MAT_FUND_AI
    IDEB 2023 (VL_OBSERVADO_2023)
    - Rede: Municipal
    INSE 2021 (MEDIA_INSE)'''

    st.title('Escolas municipais')


    df_ind3 = microdados[(microdados.TP_DEPENDENCIA == 3) & (microdados.IN_FUND_AI == 1)]
    # agrupar por CO_MUNICIPIO e calcular a soma de QT_MAT_FUND_AI
    # df_ind3 = df_ind3.groupby(['CO_MUNICIPIO', 'NO_MUNICIPIO', 'NO_UF', 'NO_REGIAO'], as_index=False).agg({'QT_MAT_FUND_AI': 'sum'})
    # tira as duplicatas
    ideb_esc_ai_mun = ideb_esc_ai[ideb_esc_ai.REDE.str.startswith('Municipal')]
    # juntar com ideb_esc_ai por CO_ENTIDADE e ID_ESCOLA (merge)
    df_ind3 = pd.merge(df_ind3, ideb_esc_ai_mun, 
                       left_on='CO_ENTIDADE', right_on='ID_ESCOLA', how='left')
    df_ind3 = pd.merge(df_ind3, inse_esc[['ID_ESCOLA', 'MEDIA_INSE']],
                       left_on='CO_ENTIDADE', right_on='ID_ESCOLA', how='left')
    # Agrupando e selecionando os 5 primeiros por região com base na taxa escolhida
    top_municipios_ind3 = (
        df_ind3
        # Ordena por região e taxa de cobertura (decrescente)
        .sort_values(['NO_REGIAO', 'VL_OBSERVADO_2023', 'QT_MAT_FUND_AI'],
        ascending=[True, False, False])
        # Agrupa por região e mantém os 5 maiores de cada grupo
        .groupby('NO_REGIAO', as_index=False)
        .head(5)
        # Seleciona colunas relevantes
        [['NO_REGIAO', 'NO_UF', 'CO_MUNICIPIO', 'NO_MUNICIPIO', 'CO_ENTIDADE', 'NO_ENTIDADE', 'QT_MAT_FUND_AI', 'VL_OBSERVADO_2023', 'MEDIA_INSE']]
    )

    st.dataframe(top_municipios_ind3, use_container_width=True, hide_index=True)
    # teste = df_ind3[df_ind3.NO_ENTIDADE == 'ESCOLA MOCINHA RODRIGUES']
    # st.dataframe(teste[['NO_REGIAO', 'CO_MUNICIPIO', 'NO_MUNICIPIO', 'CO_ENTIDADE', 'NO_ENTIDADE', 'QT_MAT_FUND_AI', 'VL_OBSERVADO_2023', 'MEDIA_INSE']])
    # # st.dataframe(ideb_mun_ai)

    # teste2 = microdados[microdados.NO_ENTIDADE == 'ESCOLA MOCINHA RODRIGUES']
    # st.dataframe(teste2[['NO_REGIAO', 'CO_MUNICIPIO', 'NO_MUNICIPIO', 'CO_ENTIDADE', 'NO_ENTIDADE', 'TP_DEPENDENCIA', 'QT_MAT_FUND_AI']])
    st.title('Redes municipais')

    df_ind3b = microdados[(microdados.TP_DEPENDENCIA == 3) & (microdados.IN_FUND_AI == 1)]
    # agrupar por CO_MUNICIPIO e calcular a soma de QT_MAT_FUND_AI
    df_ind3b = df_ind3b.groupby(['CO_MUNICIPIO', 'NO_MUNICIPIO', 'NO_UF', 'NO_REGIAO'], as_index=False).agg({'QT_MAT_FUND_AI': 'sum'})
    # tira as duplicatas
    ideb_mun_ai_mun = ideb_mun_ai[ideb_mun_ai.REDE.str.startswith('Municipal')]
    # tira as duplicatas inse
    inse_mun_mun = inse_mun[(inse_mun.TP_TIPO_REDE == 3) & (inse_mun.TP_LOCALIZACAO == 0)]
    # juntar com ideb_esc_ai por CO_ENTIDADE e ID_ESCOLA (merge)
    df_ind3b = pd.merge(df_ind3b, ideb_mun_ai_mun, 
                       left_on='CO_MUNICIPIO', right_on='CO_MUNICIPIO', how='left')
    df_ind3b = pd.merge(df_ind3b, inse_mun_mun[['CO_MUNICIPIO', 'MEDIA_INSE']],
                       left_on='CO_MUNICIPIO', right_on='CO_MUNICIPIO', how='left')
    # Agrupando e selecionando os 5 primeiros por região com base na taxa escolhida
    top_municipios_ind3b = (
        df_ind3b
        # Ordena por região e taxa de cobertura (decrescente)
        .sort_values(['NO_REGIAO', 'VL_OBSERVADO_2023', 'QT_MAT_FUND_AI'], 
                     ascending=[True, False, False])
        # Agrupa por região e mantém os 5 maiores de cada grupo
        .groupby('NO_REGIAO', as_index=False)
        .head(5)
        # Seleciona colunas relevantes
        [['NO_REGIAO', 'NO_UF', 'CO_MUNICIPIO', 'NO_MUNICIPIO', 'QT_MAT_FUND_AI', 'VL_OBSERVADO_2023', 'MEDIA_INSE']]
    )

    st.dataframe(top_municipios_ind3b, use_container_width=True, hide_index=True)

    st.title('Estado - redes públicas')

    df_ind3c = microdados[(microdados.TP_DEPENDENCIA == 3) & (microdados.IN_FUND_AI == 1)]
    # # agrupar por CO_MUNICIPIO e calcular a soma de QT_MAT_FUND_AI
    df_ind3c = df_ind3c.groupby(['NO_UF', 'CO_UF'], as_index=False).agg({'QT_MAT_FUND_AI': 'sum'})
    
    # arruma ideb
    ideb_uf_ai_uf = ideb_uf_ai[ideb_uf_ai.REDE.str.startswith('Pública')]
    # Dicionário de mapeamento do nome do estado para o código IBGE
    uf_codigos = {
        'Rondônia': 11,
        'Acre': 12,
        'Amazonas': 13,
        'Roraima': 14,
        'Pará': 15,
        'Amapá': 16,
        'Tocantins': 17,
        'Maranhão': 21,
        'Piauí': 22,
        'Ceará': 23,
        'R. G. do Norte': 24,  # Rio Grande do Norte
        'Paraíba': 25,
        'Pernambuco': 26,
        'Alagoas': 27,
        'Sergipe': 28,
        'Bahia': 29,
        'Minas Gerais': 31,
        'Espírito Santo': 32,
        'Rio de Janeiro': 33,
        'São Paulo': 35,
        'Paraná': 41,
        'Santa Catarina': 42,
        'R. G. do Sul': 43,    # Rio Grande do Sul
        'M. G. do Sul': 50,    # Mato Grosso do Sul
        'Mato Grosso': 51,
        'Goiás': 52,
        'Distrito Federal': 53,
    }
    # Supondo que seu DataFrame se chame df e a coluna seja 'NO_UF'
    ideb_uf_ai_uf['CO_UF'] = ideb_uf_ai_uf['SG_UF'].map(uf_codigos)
    ideb_uf_ai_uf.dropna(subset=['CO_UF'], inplace=True)

    # tira as duplicatas inse
    inse_uf_uf = inse_uf[(inse_uf.TP_TIPO_REDE == 2) & (inse_uf.TP_LOCALIZACAO == 0) & (inse_uf.TP_CAPITAL == 0)]
    # # juntar com ideb_esc_ai por CO_ENTIDADE e ID_ESCOLA (merge)
    df_ind3c = pd.merge(df_ind3c, ideb_uf_ai_uf, 
                       left_on='CO_UF', right_on='CO_UF', how='left')
    df_ind3c = pd.merge(df_ind3c, inse_uf_uf[['CO_UF', 'MEDIA_INSE']],
                       left_on='CO_UF', right_on='CO_UF', how='left')
    
    # st.dataframe(top_municipios_ind3c, use_container_width=True, hide_index=True)
    result = df_ind3c.sort_values(
        ['VL_OBSERVADO_2023', 'MEDIA_INSE'],
        ascending=[False, True]
    ).head(10)
    st.dataframe(result[['NO_UF', 'QT_MAT_FUND_AI', 'VL_OBSERVADO_2023', 'MEDIA_INSE']], 
                 use_container_width=True, hide_index=True)

with tab4:
    st.header('Fundamental AF')

    f'''**Fontes e filtros utilizados**:\n
    Censo da Educação Básica 2024
    - Tipo de dependência: municipal (TP_DEPENDENCIA == 3)
    - Indicador de oferta do fundamental anos finais (IN_FUND_AF == 1)
    - Matriculados nos anos finais: QT_MAT_FUND_AF
    IDEB 2023 (VL_OBSERVADO_2023)
    - Rede: Municipal
    INSE 2021 (MEDIA_INSE)'''

    st.title('Escolas municipais')

    df_ind4 = microdados[(microdados.TP_DEPENDENCIA == 3) & (microdados.IN_FUND_AF == 1)]
    # tira as duplicatas
    ideb_esc_af_mun = ideb_esc_af[ideb_esc_af.REDE.str.startswith('Municipal')]
    # juntar com ideb_esc_ai por CO_ENTIDADE e ID_ESCOLA (merge)
    df_ind4 = pd.merge(df_ind4, ideb_esc_af_mun, 
                       left_on='CO_ENTIDADE', right_on='ID_ESCOLA', how='left')
    df_ind4 = pd.merge(df_ind4, inse_esc[['ID_ESCOLA', 'MEDIA_INSE']],
                       left_on='CO_ENTIDADE', right_on='ID_ESCOLA', how='left')
    # Agrupando e selecionando os 5 primeiros por região com base na taxa escolhida
    top_municipios_ind4 = (
        df_ind4
        # Ordena por região e taxa de cobertura (decrescente)
        .sort_values(['NO_REGIAO', 'VL_OBSERVADO_2023', 'QT_MAT_FUND_AF'],
        ascending=[True, False, False])
        # Agrupa por região e mantém os 5 maiores de cada grupo
        .groupby('NO_REGIAO', as_index=False)
        .head(5)
        # Seleciona colunas relevantes
        [['NO_REGIAO', 'NO_UF', 'CO_MUNICIPIO', 'NO_MUNICIPIO', 'CO_ENTIDADE', 'NO_ENTIDADE', 'QT_MAT_FUND_AF', 'VL_OBSERVADO_2023', 'MEDIA_INSE']]
    )

    st.dataframe(top_municipios_ind4, use_container_width=True, hide_index=True)
    # teste = df_ind3[df_ind3.NO_ENTIDADE == 'ESCOLA MOCINHA RODRIGUES']
    # st.dataframe(teste[['NO_REGIAO', 'CO_MUNICIPIO', 'NO_MUNICIPIO', 'CO_ENTIDADE', 'NO_ENTIDADE', 'QT_MAT_FUND_AI', 'VL_OBSERVADO_2023', 'MEDIA_INSE']])
    # # st.dataframe(ideb_mun_ai)

    # teste2 = microdados[microdados.NO_ENTIDADE == 'ESCOLA MOCINHA RODRIGUES']
    # st.dataframe(teste2[['NO_REGIAO', 'CO_MUNICIPIO', 'NO_MUNICIPIO', 'CO_ENTIDADE', 'NO_ENTIDADE', 'TP_DEPENDENCIA', 'QT_MAT_FUND_AI']])
    st.title('Redes municipais')

    df_ind4b = microdados[(microdados.TP_DEPENDENCIA == 3) & (microdados.IN_FUND_AF == 1)]
    # agrupar por CO_MUNICIPIO e calcular a soma de QT_MAT_FUND_AI
    df_ind4b = df_ind4b.groupby(['CO_MUNICIPIO', 'NO_MUNICIPIO', 'NO_UF', 'NO_REGIAO'], as_index=False).agg({'QT_MAT_FUND_AF': 'sum'})
    # tira as duplicatas
    ideb_mun_af_mun = ideb_mun_af[ideb_mun_af.REDE.str.startswith('Municipal')]
    # tira as duplicatas inse
    inse_mun_mun = inse_mun[(inse_mun.TP_TIPO_REDE == 3) & (inse_mun.TP_LOCALIZACAO == 0)]
    # juntar com ideb_esc_ai por CO_ENTIDADE e ID_ESCOLA (merge)
    df_ind4b = pd.merge(df_ind4b, ideb_mun_af_mun, 
                       left_on='CO_MUNICIPIO', right_on='CO_MUNICIPIO', how='left')
    df_ind4b = pd.merge(df_ind4b, inse_mun_mun[['CO_MUNICIPIO', 'MEDIA_INSE']],
                       left_on='CO_MUNICIPIO', right_on='CO_MUNICIPIO', how='left')
    # Agrupando e selecionando os 5 primeiros por região com base na taxa escolhida
    top_municipios_ind4b = (
        df_ind4b
        # Ordena por região e taxa de cobertura (decrescente)
        .sort_values(['NO_REGIAO', 'VL_OBSERVADO_2023', 'QT_MAT_FUND_AF'], 
                     ascending=[True, False, False])
        # Agrupa por região e mantém os 5 maiores de cada grupo
        .groupby('NO_REGIAO', as_index=False)
        .head(5)
        # Seleciona colunas relevantes
        [['NO_REGIAO', 'NO_UF', 'CO_MUNICIPIO', 'NO_MUNICIPIO', 'QT_MAT_FUND_AF', 'VL_OBSERVADO_2023', 'MEDIA_INSE']]
    )

    st.dataframe(top_municipios_ind4b, use_container_width=True, hide_index=True)

    st.title('Estado - redes públicas')

    df_ind4c = microdados[(microdados.TP_DEPENDENCIA == 3) & (microdados.IN_FUND_AF == 1)]
    # # agrupar por CO_MUNICIPIO e calcular a soma de QT_MAT_FUND_AI
    df_ind4c = df_ind4c.groupby(['NO_UF', 'CO_UF'], as_index=False).agg({'QT_MAT_FUND_AF': 'sum'})
    
    # arruma ideb
    ideb_uf_af_uf = ideb_uf_af[ideb_uf_af.REDE.str.startswith('Pública')]
    # Dicionário de mapeamento do nome do estado para o código IBGE
    uf_codigos = {
        'Rondônia': 11,
        'Acre': 12,
        'Amazonas': 13,
        'Roraima': 14,
        'Pará': 15,
        'Amapá': 16,
        'Tocantins': 17,
        'Maranhão': 21,
        'Piauí': 22,
        'Ceará': 23,
        'R. G. do Norte': 24,  # Rio Grande do Norte
        'Paraíba': 25,
        'Pernambuco': 26,
        'Alagoas': 27,
        'Sergipe': 28,
        'Bahia': 29,
        'Minas Gerais': 31,
        'Espírito Santo': 32,
        'Rio de Janeiro': 33,
        'São Paulo': 35,
        'Paraná': 41,
        'Santa Catarina': 42,
        'R. G. do Sul': 43,    # Rio Grande do Sul
        'M. G. do Sul': 50,    # Mato Grosso do Sul
        'Mato Grosso': 51,
        'Goiás': 52,
        'Distrito Federal': 53,
    }
    # Supondo que seu DataFrame se chame df e a coluna seja 'NO_UF'
    ideb_uf_af_uf['CO_UF'] = ideb_uf_af_uf['SG_UF'].map(uf_codigos)
    ideb_uf_af_uf.dropna(subset=['CO_UF'], inplace=True)

    # tira as duplicatas inse
    inse_uf_uf = inse_uf[(inse_uf.TP_TIPO_REDE == 2) & (inse_uf.TP_LOCALIZACAO == 0) & (inse_uf.TP_CAPITAL == 0)]
    # # juntar com ideb_esc_ai por CO_ENTIDADE e ID_ESCOLA (merge)
    df_ind4c = pd.merge(df_ind4c, ideb_uf_af_uf, 
                       left_on='CO_UF', right_on='CO_UF', how='left')
    df_ind4c = pd.merge(df_ind4c, inse_uf_uf[['CO_UF', 'MEDIA_INSE']],
                       left_on='CO_UF', right_on='CO_UF', how='left')
    
    # st.dataframe(top_municipios_ind3c, use_container_width=True, hide_index=True)
    result4c = df_ind4c.sort_values(
        ['VL_OBSERVADO_2023', 'MEDIA_INSE'],
        ascending=[False, True]
    ).head(10)
    st.dataframe(result4c[['NO_UF', 'QT_MAT_FUND_AF', 'VL_OBSERVADO_2023', 'MEDIA_INSE']], 
                 use_container_width=True, hide_index=True)

with tab5:
    st.header('Ensino médio')

    f'''**Fontes e filtros utilizados**:\n
    Censo da Educação Básica 2024
    - Tipo de dependência: estadual (TP_DEPENDENCIA == 2)
    - Indicador de oferta do ensino médio (IN_MED == 1)
    - Matriculados no ensino médio: QT_MAT_MED
    IDEB 2023 (VL_OBSERVADO_2023)
    - Rede: Estadual
    INSE 2021 (MEDIA_INSE)'''

    st.title('Escolas estaduais')

    botao_vinculo = st.radio(
        "Incluir escolas vinculadas a Secretaria de Segurança Pública/Forças Armadas/Militar?",
        options=['Sim', 'Não'],
        index=0
    )

    df_ind5 = microdados[(microdados.TP_DEPENDENCIA == 2) & (microdados.IN_MED == 1)]
    # tira as duplicatas
    ideb_esc_em_mun = ideb_esc_em[ideb_esc_em.REDE.str.startswith('Estadual')]
    # juntar com ideb_esc_ai por CO_ENTIDADE e ID_ESCOLA (merge)
    df_ind5 = pd.merge(df_ind5, ideb_esc_em_mun, 
                       left_on='CO_ENTIDADE', right_on='ID_ESCOLA', how='left')
    df_ind5 = pd.merge(df_ind5, inse_esc[['ID_ESCOLA', 'MEDIA_INSE']],
                       left_on='CO_ENTIDADE', right_on='ID_ESCOLA', how='left')
    
    if botao_vinculo == 'Não':
        df_ind5 = df_ind5[df_ind5.IN_VINCULO_SEGURANCA_PUBLICA != 1]  

    # Agrupando e selecionando os 5 primeiros por região com base na taxa escolhida
    top_municipios_ind5 = (
        df_ind5
        # Ordena por região e taxa de cobertura (decrescente)
        .sort_values(['NO_REGIAO', 'VL_OBSERVADO_2023', 'QT_MAT_MED'],
        ascending=[True, False, False])
        # Agrupa por região e mantém os 5 maiores de cada grupo
        .groupby('NO_REGIAO', as_index=False)
        .head(5)
        # Seleciona colunas relevantes
        [['NO_REGIAO', 'NO_UF', 'CO_MUNICIPIO', 'NO_MUNICIPIO', 'CO_ENTIDADE', 'NO_ENTIDADE', 'QT_MAT_MED', 'VL_OBSERVADO_2023', 'MEDIA_INSE']]
    )

    st.dataframe(top_municipios_ind5, use_container_width=True, hide_index=True)

    st.title('Estado - redes estaduais')
    df_ind5c = microdados[(microdados.TP_DEPENDENCIA == 2) & (microdados.IN_MED == 1)]
    # # agrupar por CO_MUNICIPIO e calcular a soma de QT_MAT_FUND_AI
    df_ind5c = df_ind5c.groupby(['NO_UF', 'CO_UF'], as_index=False).agg({'QT_MAT_MED': 'sum'})
    
    # arruma ideb
    ideb_uf_em_uf = ideb_uf_em[ideb_uf_em.REDE.str.startswith('Estadual')]
    # Dicionário de mapeamento do nome do estado para o código IBGE
    uf_codigos = {
        'Rondônia': 11,
        'Acre': 12,
        'Amazonas': 13,
        'Roraima': 14,
        'Pará': 15,
        'Amapá': 16,
        'Tocantins': 17,
        'Maranhão': 21,
        'Piauí': 22,
        'Ceará': 23,
        'R. G. do Norte': 24,  # Rio Grande do Norte
        'Paraíba': 25,
        'Pernambuco': 26,
        'Alagoas': 27,
        'Sergipe': 28,
        'Bahia': 29,
        'Minas Gerais': 31,
        'Espírito Santo': 32,
        'Rio de Janeiro': 33,
        'São Paulo': 35,
        'Paraná': 41,
        'Santa Catarina': 42,
        'R. G. do Sul': 43,    # Rio Grande do Sul
        'M. G. do Sul': 50,    # Mato Grosso do Sul
        'Mato Grosso': 51,
        'Goiás': 52,
        'Distrito Federal': 53,
    }
    # Supondo que seu DataFrame se chame df e a coluna seja 'NO_UF'
    ideb_uf_em_uf['CO_UF'] = ideb_uf_em_uf['SG_UF'].map(uf_codigos)
    ideb_uf_em_uf.dropna(subset=['CO_UF'], inplace=True)

    # tira as duplicatas inse
    inse_uf_uf = inse_uf[(inse_uf.TP_TIPO_REDE == 6) & (inse_uf.TP_LOCALIZACAO == 0) & (inse_uf.TP_CAPITAL == 0)]
    # # juntar com ideb_esc_ai por CO_ENTIDADE e ID_ESCOLA (merge)
    df_ind5c = pd.merge(df_ind5c, ideb_uf_em_uf, 
                       left_on='CO_UF', right_on='CO_UF', how='left')
    df_ind5c = pd.merge(df_ind5c, inse_uf_uf[['CO_UF', 'MEDIA_INSE']],
                       left_on='CO_UF', right_on='CO_UF', how='left')
      
    # st.dataframe(top_municipios_ind3c, use_container_width=True, hide_index=True)
    result5c = df_ind5c.sort_values(
        ['VL_OBSERVADO_2023', 'MEDIA_INSE'],
        ascending=[False, True]
    ).head(10)
    st.dataframe(result5c[['NO_UF', 'QT_MAT_MED', 'VL_OBSERVADO_2023', 'MEDIA_INSE']], 
                 use_container_width=True, hide_index=True)
    
    # st.dataframe(microdados[microdados.CO_ENTIDADE == 43361340])