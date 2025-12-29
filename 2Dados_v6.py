"""
Base Modelagem Precificação
FASE 1: Dados Básicos
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime


st.set_page_config(
    page_title="Base Modelagem Precificação",
    layout="wide",
    initial_sidebar_state="expanded"
    
)



# O vídeo e o logotipo extraídos do DNA visual da Brivia
video_url = "https://cdn.prod.website-files.com/65c2dcb4330facd527e06bdd/66189f248c2e87b594826a44_Co%CC%81pia%20de%20BornBlackColor2-transcode.mp4"
logo_url = "https://cdn.prod.website-files.com/65c2dcb4330facd527e06bdd/6619a7597575e945de440959_brivia_group.svg"

st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;700&display=swap');

    .stApp {{
        background-color: #000000 !important;
    }}

    /* Container do Cabeçalho */
    .header-brivia {{
        display: flex;
        align-items: center;
        padding-bottom: 30px;
        margin-bottom: 20px;
        border-bottom: 1px solid rgba(255, 255, 255, 0.1);
    }}

    .logo-brivia {{
        height: 35px; 
        margin-right: 20px;
        filter: brightness(0) invert(1) !important;
    }}

    /* AVISO CUSTOMIZADO (Substitui o st.info azul) */
    .brivia-alerta {{
        padding: 15px;
        border-radius: 4px;
        background-color: rgba(255, 255, 255, 0.05);
        border-left: 5px solid #90513b; /* Barra lateral Vinho Brivia */
        color: #ffffff;
        font-family: 'Space Grotesk', sans-serif !important;
        font-size: 0.9rem;
        margin-bottom: 25px;
    }}

    #brivia-video-bg {{
        width: 100%;
        max-height: 300px;
        object-fit: cover;
        border-radius: 8px;
        margin-bottom: 30px;
    }}

    .stMainBlockContainer {{
        background-color: transparent !important;
    }}

    h1, h2, h3, label, p {{
        font-family: 'Space Grotesk', sans-serif !important;
        color: white !important;
    }}

    /* --- ESTILO DAS FASES --- */
    .fase-container {{
        padding: 12px;
        border-radius: 4px;
        text-align: center;
        font-family: 'Space Grotesk', sans-serif;
        font-size: 0.75rem;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        margin-bottom: 10px;
    }}

    /* FASE ATUAL: Borda Neon Vinho */
    .fase-atual {{
        background: linear-gradient(#000, #000) padding-box,
                    linear-gradient(135deg, #90513b, #ffffff) border-box;
        border: 2px solid transparent;
        color: #ffffff !important;
        font-weight: 700;
        box-shadow: 0 0 15px rgba(144, 81, 59, 0.4);
    }}

    .fase-ok {{
        border: 1px solid rgba(255, 255, 255, 0.3);
        color: rgba(255, 255, 255, 0.6);
        background-color: rgba(255, 255, 255, 0.02);
    }}

    .fase-espera {{
        border: 1px solid rgba(255, 255, 255, 0.1);
        color: rgba(255, 255, 255, 0.2);
    }}
</style>

<div class="header-brivia">
    <img src="{logo_url}" class="logo-brivia">
    <h1 style="margin:0; font-size: 1.8rem; letter-spacing: -1px;">Base Modelagem Precificação</h1>
</div>

<video autoplay loop muted playsinline id="brivia-video-bg">
    <source src="{video_url}" type="video/mp4">
</video>
""", unsafe_allow_html=True)
#Aqui eu estou definindo todos os dados

TIPOS_CONTRATO = ["Fee", "Projeto"]

TIPOS_SERVICO = [
    "Tecnologia",
    "Comunicação",
    "Tecnologia - Exportação",
    "Comunicação - Exportação"
]

#dependendo do serviço, vem uma empresa específica
EMPRESAS_TRIBUTACAO = {
    "Malagueta - Tecnologia": {"empresa": "Malagueta", "servico": "Tecnologia", "aliquota": 6.65},
    "Malagueta - Comunicação": {"empresa": "Malagueta", "servico": "Comunicação", "aliquota": 9.65},
    "Habanero - Tecnologia": {"empresa": "Habanero", "servico": "Tecnologia", "aliquota": 6.65},
    "Habanero - Comunicação": {"empresa": "Habanero", "servico": "Comunicação", "aliquota": 14.25},
    "Brivia - Tecnologia": {"empresa": "Brivia", "servico": "Tecnologia", "aliquota": 6.65},
    "Brivia - Comunicação": {"empresa": "Brivia", "servico": "Comunicação", "aliquota": 11.25},
    "Brivia - Tecnologia - Exportação": {"empresa": "Brivia", "servico": "Tecnologia - Exportação", "aliquota": 0.00},
    "Brivia - Comunicação - Exportação": {"empresa": "Brivia", "servico": "Comunicação - Exportação", "aliquota": 0.00},
    "Dez - Tecnologia": {"empresa": "Dez", "servico": "Tecnologia", "aliquota": 6.65},
    "Dez - Comunicação": {"empresa": "Dez", "servico": "Comunicação", "aliquota": 11.25},
    "Heads RS - Tecnologia": {"empresa": "Heads RS", "servico": "Tecnologia", "aliquota": 6.65},
    "Heads RS - Comunicação": {"empresa": "Heads RS", "servico": "Comunicação", "aliquota": 11.25},
    "Heads PR - Tecnologia": {"empresa": "Heads PR", "servico": "Tecnologia", "aliquota": 8.65},
    "Heads PR - Comunicação": {"empresa": "Heads PR", "servico": "Comunicação", "aliquota": 14.25},
    "Briviacom RS - Tecnologia": {"empresa": "Briviacom RS", "servico": "Tecnologia", "aliquota": 8.65},
    "Briviacom RS - Comunicação": {"empresa": "Briviacom RS", "servico": "Comunicação", "aliquota": 14.25},
    "Briviacom Brasília - Tecnologia": {"empresa": "Briviacom Brasília", "servico": "Tecnologia", "aliquota": 8.65},
    "Briviacom Brasília - Comunicação": {"empresa": "Briviacom Brasília", "servico": "Comunicação", "aliquota": 14.25},
}

COMISSAO_NB = [0, 1, 2, 3]
COMISSAO_PARCEIROS = [0, 1, 2, 3, 4, 5, 6, 7, 8]

LINHAS_RECEITA = [
    "Comissão de mídia",
    "Honorários de produção",
    "Comissão de ferramentas",
    "Bônus de veiculação (PIA)",
    "Outras receitas"
]

LINHAS_CUSTOS = [
    "Terceiros",
    "Materiais",
    "Viagens",
    "Outros custos"
]

GROSS_MARGIN_ALVO = 40.0



def init_session_state():
    """Inicializa todas as variáveis de sessão"""
    
    # para definirmos nossa fase atual
    if 'fase_atual' not in st.session_state:
        st.session_state.fase_atual = 1
    
    # Dados básicos
    if 'dados_basicos' not in st.session_state:
        st.session_state.dados_basicos = {
            'cliente': '',
            'descricao_contrato': '',
            'tipo_contrato': TIPOS_CONTRATO[0],
            'quantidade_meses': 12,
            'tipo_servico': TIPOS_SERVICO[0],
            'empresa_tributacao': '',
            'aliquota_imposto': 0.0,
            'comissao_nb': 0,
            'comissao_parceiros': 0,
        }
    
    # Receita Bruta
    if 'receita_bruta' not in st.session_state:
        st.session_state.receita_bruta = {
            linha: {'verba_total': 0.0, 'comissao_pct': 0.0}
            for linha in LINHAS_RECEITA
        }
    
    # Custos
    if 'custos' not in st.session_state:
        st.session_state.custos = {
            linha: {'valor_mensal': 0.0, 'observacoes': ''}
            for linha in LINHAS_CUSTOS
        }
    
    # Gross Margin
    if 'gross_margin' not in st.session_state:
        st.session_state.gross_margin = {
            'desconto': 0.0,
            'observacoes': ''
        }



def formatar_moeda(valor):
    """Formata valor em reais"""
    return f"R$ {valor:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')

def filtrar_empresas_por_servico(tipo_servico):
    """Filtra empresas compatíveis com o tipo de serviço selecionado"""
    empresas_filtradas = []
    for key, data in EMPRESAS_TRIBUTACAO.items():
        if data['servico'] == tipo_servico:
            empresas_filtradas.append(key)
    return empresas_filtradas

def validar_fase_1():
    """Valida se todos os campos obrigatórios da fase 1 estão preenchidos"""
    dados = st.session_state.dados_basicos
    
    campos_obrigatorios = [
        dados['cliente'].strip() != '',
        dados['descricao_contrato'].strip() != '',
        dados['empresa_tributacao'] != '',
        dados['quantidade_meses'] > 0
    ]
    
    return all(campos_obrigatorios)

def calcular_total_receita(verba_total, comissao_pct):
    """Calcula total da receita"""
    return verba_total * (comissao_pct / 100)

def calcular_valor_total_custo(valor_mensal, quantidade_meses):
    """Calcula valor total do custo"""
    return valor_mensal * quantidade_meses

def calcular_gross_margin_com_desconto(desconto):
    """Calcula gross margin com desconto"""
    return GROSS_MARGIN_ALVO - desconto

# ==================== INTERFACE PRINCIPAL ====================

def main():
    init_session_state()
    
        # Controle de fases concluídas
    if 'fase_max_concluida' not in st.session_state:
        st.session_state.fase_max_concluida = 1

    # Header
    


    
    # Indicador de fases (Estilo Brivia)
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.session_state.fase_atual == 1:
            st.markdown('<div class="fase-container fase-atual">Fase 1: Dados Básicos</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="fase-container fase-ok">Fase 1: Ok</div>', unsafe_allow_html=True)
    
    with col2:
        if st.session_state.fase_atual == 2:
            st.markdown('<div class="fase-container fase-atual">Fase 2: Equipe CLT</div>', unsafe_allow_html=True)
        elif st.session_state.fase_atual > 2:
            st.markdown('<div class="fase-container fase-ok">Fase 2: Ok</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="fase-container fase-espera">Fase 2: Aguardando</div>', unsafe_allow_html=True)
    
    with col3:
        if st.session_state.fase_atual == 3:
            st.markdown('<div class="fase-container fase-atual">Fase 3: Terceiros</div>', unsafe_allow_html=True)
        elif st.session_state.fase_atual > 3:
            st.markdown('<div class="fase-container fase-ok">Fase 3: Ok</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="fase-container fase-espera">Fase 3: Aguardando</div>', unsafe_allow_html=True)
    
    with col4:
        if st.session_state.fase_atual == 4:
            st.markdown('<div class="fase-container fase-atual">Fase 4: Ferramentas</div>', unsafe_allow_html=True)
        elif st.session_state.fase_atual > 4:
            st.markdown('<div class="fase-container fase-ok">Fase 4: Ok</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="fase-container fase-espera">Fase 4: Aguardando</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    def botao_voltar():
     if st.session_state.fase_atual > 1:
        fase_anterior = st.session_state.fase_atual - 1

        if fase_anterior <= st.session_state.fase_max_concluida:
            if st.button("<---", use_container_width=True):
                st.session_state.fase_atual = fase_anterior
                st.rerun()

    
    botao_voltar()
    

    # Renderizar fase atual
    if st.session_state.fase_atual == 1:
        renderizar_fase_1()
    #elif st.session_state.fase_atual == 2:
    #    renderizar_fase_2()
    #elif st.session_state.fase_atual == 3:
     #   renderizar_fase_3()
    #elif st.session_state.fase_atual == 4:
    #    renderizar_fase_4()



# ==================== FASE 1: DADOS BÁSICOS ====================

def renderizar_fase_1():
    st.header("FASE 1: Dados Básicos da Precificação")
    st.markdown('<div class="brivia-alerta">Preencha todos os campos obrigatórios para avançar para a próxima fase</div>', unsafe_allow_html=True)
    
    # 1. INFORMAÇÕES DO CLIENTE E CONTRATO
    st.subheader("Informações do Cliente e Contrato")
    
    col1, col2 = st.columns(2)
    
    with col1:
        cliente = st.text_input(
            "Cliente *",
            value=st.session_state.dados_basicos['cliente'],
            placeholder="Nome ou Razão Social do Cliente",
            help="Campo obrigatório"
        )
        st.session_state.dados_basicos['cliente'] = cliente
        
        tipo_contrato = st.selectbox(
            "Tipo de Contrato *",
            TIPOS_CONTRATO,
            index=TIPOS_CONTRATO.index(st.session_state.dados_basicos['tipo_contrato']),
            help="Campo obrigatório"
        )
        st.session_state.dados_basicos['tipo_contrato'] = tipo_contrato
        
        tipo_servico = st.selectbox(
            "Tipo de Serviço *",
            TIPOS_SERVICO,
            index=TIPOS_SERVICO.index(st.session_state.dados_basicos['tipo_servico']),
            help="Campo obrigatório"
        )
        st.session_state.dados_basicos['tipo_servico'] = tipo_servico
    
    with col2:
        descricao = st.text_area(
            "Descrição do Contrato *",
            value=st.session_state.dados_basicos['descricao_contrato'],
            placeholder="Descreva os serviços a serem prestados",
            help="Campo obrigatório",
            height=100
        )
        st.session_state.dados_basicos['descricao_contrato'] = descricao
        
        quantidade_meses = st.number_input(
            "Quantidade de Meses do Contrato *",
            min_value=1,
            max_value=60,
            value=st.session_state.dados_basicos['quantidade_meses'],
            help="Campo obrigatório"
        )
        st.session_state.dados_basicos['quantidade_meses'] = quantidade_meses
    
    st.markdown("---")
    
    # 2. TRIBUTAÇÃO
    st.subheader("Empresa para Tributação")
    
    # Filtrar empresas compatíveis
    empresas_disponiveis = filtrar_empresas_por_servico(tipo_servico)
    
    if empresas_disponiveis:
        col1, col2 = st.columns(2)
        
        with col1:
            # Se já tem empresa selecionada e é válida, manter
            if st.session_state.dados_basicos['empresa_tributacao'] in empresas_disponiveis:
                idx = empresas_disponiveis.index(st.session_state.dados_basicos['empresa_tributacao'])
            else:
                idx = 0
                st.session_state.dados_basicos['empresa_tributacao'] = empresas_disponiveis[0]
            
            empresa_selecionada = st.selectbox(
                "Empresa para Tributação *",
                empresas_disponiveis,
                index=idx,
                help="Empresas disponíveis para o tipo de serviço selecionado"
            )
            st.session_state.dados_basicos['empresa_tributacao'] = empresa_selecionada
            
            # Atualizar alíquota automaticamente
            aliquota = EMPRESAS_TRIBUTACAO[empresa_selecionada]['aliquota']
            st.session_state.dados_basicos['aliquota_imposto'] = aliquota
        
        with col2:
            st.metric(
                "Alíquota de Imposto",
                f"{aliquota:.2f}%",
                help="Calculado automaticamente com base na empresa selecionada"
            )
    else:
        st.warning("Nenhuma empresa disponível para o tipo de serviço selecionado")
    
    st.markdown("---")
    
    # 3. COMISSÕES
    st.subheader("Comissões")
    
    col1, col2 = st.columns(2)
    
    with col1:
        comissao_nb = st.selectbox(
            "Alíquota de Comissão NB (New Business)",
            COMISSAO_NB,
            index=COMISSAO_NB.index(st.session_state.dados_basicos['comissao_nb']),
            format_func=lambda x: f"{x}%",
            help="Comissão de novos negócios"
        )
        st.session_state.dados_basicos['comissao_nb'] = comissao_nb
    
    with col2:
        comissao_parceiros = st.selectbox(
            "Alíquota de Comissão Parceiros",
            COMISSAO_PARCEIROS,
            index=COMISSAO_PARCEIROS.index(st.session_state.dados_basicos['comissao_parceiros']),
            format_func=lambda x: f"{x}%",
            help="Comissão de parceiros"
        )
        st.session_state.dados_basicos['comissao_parceiros'] = comissao_parceiros
    
    st.markdown("---")
    
    # 4. RECEITA BRUTA
    st.subheader("Receita Bruta")
    st.caption("Informe as receitas adicionais advindas do contrato")
    
    total_receita_bruta = 0.0
    
    # Cabeçalho da tabela
    col1, col2, col3, col4 = st.columns([3, 2, 2, 2])
    with col1:
        st.markdown("**Tipo de Receita**")
    with col2:
        st.markdown("**Verba Total (R$)**")
    with col3:
        st.markdown("**Comissão (%)**")
    with col4:
        st.markdown("**Total da Receita (R$)**")
    
    # Linhas de receita
    for linha in LINHAS_RECEITA:
        col1, col2, col3, col4 = st.columns([3, 2, 2, 2])
        
        with col1:
            st.text(linha)
        
        with col2:
            verba = st.number_input(
                f"verba_{linha}",
                min_value=0.0,
                value=st.session_state.receita_bruta[linha]['verba_total'],
                step=1000.0,
                format="%.2f",
                label_visibility="collapsed",
                key=f"verba_{linha}"
            )
            st.session_state.receita_bruta[linha]['verba_total'] = verba
        
        with col3:
            comissao = st.number_input(
                f"comissao_{linha}",
                min_value=0.0,
                max_value=100.0,
                value=st.session_state.receita_bruta[linha]['comissao_pct'],
                step=0.5,
                format="%.2f",
                label_visibility="collapsed",
                key=f"comissao_{linha}"
            )
            st.session_state.receita_bruta[linha]['comissao_pct'] = comissao
        
        with col4:
            total_linha = calcular_total_receita(verba, comissao)
            total_receita_bruta += total_linha
            st.text(formatar_moeda(total_linha))
    
    # Total
    st.markdown("---")
    col1, col2, col3, col4 = st.columns([3, 2, 2, 2])
    with col1:
        st.markdown("**TOTAL RECEITA BRUTA**")
    with col4:
        st.markdown(f"**{formatar_moeda(total_receita_bruta)}**")
    
    st.markdown("---")
    
    # 5. CUSTOS
    st.subheader("Custos")
    st.caption("Informe os custos de viagens e outros custos extras")
    
    total_custos = 0.0
    
    # Cabeçalho da tabela
    col1, col2, col3, col4 = st.columns([2, 2, 2, 3])
    with col1:
        st.markdown("**Tipo de Custo**")
    with col2:
        st.markdown("**Valor Mensal (R$)**")
    with col3:
        st.markdown("**Valor Total (R$)**")
    with col4:
        st.markdown("**Observações**")
    
    # Linhas de custo
    for linha in LINHAS_CUSTOS:
        col1, col2, col3, col4 = st.columns([2, 2, 2, 3])
        
        with col1:
            st.text(linha)
        
        with col2:
            # Terceiros e Materiais são puxados de outras abas (disabled)
            if linha in ["Terceiros", "Materiais"]:
                st.text_input(
                    f"valor_{linha}",
                    value="(Calculado na próxima fase)",
                    disabled=True,
                    label_visibility="collapsed",
                    key=f"valor_{linha}_disabled"
                )
            else:
                valor_mensal = st.number_input(
                    f"valor_{linha}",
                    min_value=0.0,
                    value=st.session_state.custos[linha]['valor_mensal'],
                    step=100.0,
                    format="%.2f",
                    label_visibility="collapsed",
                    key=f"valor_{linha}"
                )
                st.session_state.custos[linha]['valor_mensal'] = valor_mensal
        
        with col3:
            if linha in ["Terceiros", "Materiais"]:
                st.text("-")
            else:
                valor_total = calcular_valor_total_custo(
                    st.session_state.custos[linha]['valor_mensal'],
                    quantidade_meses
                )
                total_custos += valor_total
                st.text(formatar_moeda(valor_total))
        
        with col4:
            obs = st.text_input(
                f"obs_{linha}",
                value=st.session_state.custos[linha]['observacoes'],
                placeholder="Observações...",
                label_visibility="collapsed",
                key=f"obs_{linha}"
            )
            st.session_state.custos[linha]['observacoes'] = obs
    
    # Total
    st.markdown("---")
    col1, col2, col3, col4 = st.columns([2, 2, 2, 3])
    with col1:
        st.markdown("**TOTAL CUSTOS**")
    with col3:
        st.markdown(f"**{formatar_moeda(total_custos)}**")
    
    st.markdown("---")
    
    # 6. GROSS MARGIN
    st.subheader("Gross Margin")
    
    
    col1, col2, col3 = st.columns([2, 2, 3])
    
    with col1:
        st.markdown("")
        st.markdown("")
        st.markdown("**Gross Margin Alvo**")
        st.markdown("")
        st.markdown("")
        st.markdown("**Desconto**")
        st.markdown("")
        st.markdown("")
        st.markdown("**Gross Margin com Desconto**")
    
    with col2:
        st.metric("", f"{GROSS_MARGIN_ALVO:.2f}%")
        
        desconto = st.number_input(
            "Desconto GM",
            min_value=0.0,
            max_value=100.0,
            value=st.session_state.gross_margin['desconto'],
            step=0.5,
            format="%.2f",
            label_visibility="collapsed"
        )
        st.session_state.gross_margin['desconto'] = desconto
        
        gm_final = calcular_gross_margin_com_desconto(desconto)
        if gm_final < 20:
            st.error(f"{gm_final:.2f}%")
        elif gm_final < 30:
            st.warning(f"{gm_final:.2f}%")
        else:
            st.success(f"{gm_final:.2f}%")
    
    with col3:
        st.text("")
        st.text("")
        st.text("")
        st.text("")
        st.text("")
        st.text("")
        obs_gm = st.text_area(
            "Observações GM",
            value=st.session_state.gross_margin['observacoes'],
            placeholder="Observações sobre gross margin...",
            label_visibility="collapsed",
            height=100
        )
        st.session_state.gross_margin['observacoes'] = obs_gm
    
    st.markdown("---")
    
    # RESUMO E VALIDAÇÃO
    st.subheader("Resumo da Fase 1")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Cliente", cliente if cliente else "Não preenchido")
        st.metric("Tipo de Contrato", tipo_contrato)
        st.metric("Duração", f"{quantidade_meses} meses")
    
    with col2:
        st.metric("Tipo de Serviço", tipo_servico)
        st.metric("Alíquota de Imposto", f"{st.session_state.dados_basicos['aliquota_imposto']:.2f}%")
        st.metric("Receita Bruta", formatar_moeda(total_receita_bruta))
    
    with col3:
        st.metric("Comissão NB", f"{comissao_nb}%")
        st.metric("Comissão Parceiros", f"{comissao_parceiros}%")
        st.metric("Custos Extras", formatar_moeda(total_custos))
    
    st.markdown("---")
    
    # BOTÃO DE AVANÇAR
    fase_valida = validar_fase_1()
    
    col1, col2, col3 = st.columns([2, 1, 2])
    
    with col2:
        if fase_valida:
            if st.button("Avançar para Equipe CLT", type="primary", use_container_width=True):
                st.session_state.fase_atual = 2
                st.rerun()
        else:
            st.button("Avançar para Equipe CLT", disabled=True, use_container_width=True)
            st.error("!!! Preencha todos os campos obrigatórios (*) para avançar")

if __name__ == "__main__":
    main()
