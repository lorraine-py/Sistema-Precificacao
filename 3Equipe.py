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
    page_title="Precificação",
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
        position: fixed;
        top: 0;
        right: 0;
        width: 80vw;
        height: 90vh;
        object-fit: cover;
        z-index: 0;
        pointer-events: none;
        -webkit-mask-image: radial-gradient(circle at 80% 50%, black 0%, transparent 75%);
        mask-image: radial-gradient(circle at 80% 50%, black 0%, transparent 75%);
    }}

    .stMainBlockContainer {{
        position: relative;
        z-index: 1;
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
    <h1 style="margin:0; font-size: 1.8rem; letter-spacing: -1px;">Precificação</h1>
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

# ==================== BASE DE DADOS COMPLETA (MERCER) ====================

BASE_SALARIAL = {
    "Gerente de DBM": {
        "1. Junior": {"mercado": 12875, "minima": 9000, "brivia": 12480},
        "2. Pleno": {"mercado": 13450, "minima": 11500, "brivia": 12480},
        "3. Sênior": {"mercado": 16325, "minima": 14000, "brivia": 14961},
        "4. Líder": {"mercado": 16325, "minima": 14000, "brivia": 14961},
        "5. Head": {"mercado": 20000, "minima": 17000, "brivia": 19360},
        "6. Especialista": {"mercado": 21125, "minima": 18500, "brivia": 19360},
    },
    "CRM Planner": {
        "1. Junior": {"mercado": 6600, "minima": 5500, "brivia": 6044},
        "2. Pleno": {"mercado": 11000, "minima": 9000, "brivia": 8685},
        "3. Sênior": {"mercado": 13250, "minima": 11000, "brivia": 12480},
        "4. Líder": {"mercado": 14250, "minima": 12000, "brivia": 12480},
        "5. Head": {"mercado": 16375, "minima": 14000, "brivia": 14961},
        "6. Especialista": {"mercado": 17375, "minima": 15000, "brivia": 14961},
    },
    "Arquiteto do Salesforce": {
        "1. Junior": {"mercado": 14980, "minima": 12000, "brivia": 12480},
        "2. Pleno": {"mercado": 14250, "minima": 12000, "brivia": 14961},
        "3. Sênior": {"mercado": 16375, "minima": 14000, "brivia": 14961},
        "4. Líder": {"mercado": 18125, "minima": 15500, "brivia": 14961},
        "5. Head": {"mercado": 20375, "minima": 18000, "brivia": 19360},
        "6. Especialista": {"mercado": 22375, "minima": 20000, "brivia": 19360},
    },
    "Desenvolvedor do Salesforce": {
        "1. Junior": {"mercado": 8738, "minima": 7000, "brivia": 6044},
        "2. Pleno": {"mercado": 11000, "minima": 9000, "brivia": 7245},
        "3. Sênior": {"mercado": 13250, "minima": 11000, "brivia": 10411},
        "4. Líder": {"mercado": 15000, "minima": 12500, "brivia": 10411},
        "5. Head": {"mercado": 17375, "minima": 15000, "brivia": 12480},
        "6. Especialista": {"mercado": 17625, "minima": 16000, "brivia": 14961},
    },
    "Consultor do Salesforce": {
        "1. Junior": {"mercado": 7615, "minima": 6100, "brivia": 6044},
        "2. Pleno": {"mercado": 11750, "minima": 9500, "brivia": 7245},
        "3. Sênior": {"mercado": 13750, "minima": 11500, "brivia": 10411},
        "4. Líder": {"mercado": 15375, "minima": 13000, "brivia": 10411},
        "5. Head": {"mercado": 17625, "minima": 15000, "brivia": 12480},
        "6. Especialista": {"mercado": 19375, "minima": 17000, "brivia": 14961},
    },
    "Administrador do Salesforce": {
        "1. Junior": {"mercado": 7116, "minima": 5700, "brivia": 6044},
        "2. Pleno": {"mercado": 10500, "minima": 8500, "brivia": 7245},
        "3. Sênior": {"mercado": 12000, "minima": 10000, "brivia": 10411},
        "4. Líder": {"mercado": 13750, "minima": 11500, "brivia": 10411},
        "5. Head": {"mercado": 15500, "minima": 13000, "brivia": 12480},
        "6. Especialista": {"mercado": 15875, "minima": 14000, "brivia": 14961},
    },
    "Analista de Conteúdo": {
        "1. Junior": {"mercado": 4300, "minima": 3500, "brivia": 4206},
        "2. Pleno": {"mercado": 6700, "minima": 5500, "brivia": 6044},
        "3. Sênior": {"mercado": 8500, "minima": 7000, "brivia": 7245},
        "4. Líder": {"mercado": 10375, "minima": 8500, "brivia": 10411},
        "5. Head": {"mercado": 13375, "minima": 11000, "brivia": 12480},
        "6. Especialista": {"mercado": 12250, "minima": 10000, "brivia": 12480},
    },
    "Analista de CRM": {
        "1. Junior": {"mercado": 6000, "minima": 4500, "brivia": 4206},
        "2. Pleno": {"mercado": 8125, "minima": 6500, "brivia": 6044},
        "3. Sênior": {"mercado": 10750, "minima": 8500, "brivia": 7245},
        "4. Líder": {"mercado": 12375, "minima": 10000, "brivia": 10411},
        "5. Head": {"mercado": 15750, "minima": 13000, "brivia": 12480},
        "6. Especialista": {"mercado": 13250, "minima": 11000, "brivia": 12480},
    },
    "Analista de Dados": {
        "1. Junior": {"mercado": 6625, "minima": 5000, "brivia": 6044},
        "2. Pleno": {"mercado": 8625, "minima": 7000, "brivia": 7245},
        "3. Sênior": {"mercado": 11250, "minima": 9000, "brivia": 10411},
        "4. Líder": {"mercado": 13250, "minima": 11000, "brivia": 12480},
        "5. Head": {"mercado": 16375, "minima": 14000, "brivia": 14961},
        "6. Especialista": {"mercado": 14250, "minima": 12000, "brivia": 12480},
    },
    "Analista de DBM": {
        "1. Junior": {"mercado": 5300, "minima": 4100, "brivia": 4206},
        "2. Pleno": {"mercado": 7500, "minima": 5900, "brivia": 6044},
        "3. Sênior": {"mercado": 10200, "minima": 8000, "brivia": 7245},
        "4. Líder": {"mercado": 12800, "minima": 10500, "brivia": 10411},
        "5. Head": {"mercado": 16000, "minima": 13200, "brivia": 12480},
        "6. Especialista": {"mercado": 13800, "minima": 11500, "brivia": 12480},
    },
    "Analista de Estratégia": {
        "1. Junior": {"mercado": 6000, "minima": 4500, "brivia": 4206},
        "2. Pleno": {"mercado": 8125, "minima": 6500, "brivia": 6044},
        "3. Sênior": {"mercado": 10750, "minima": 8500, "brivia": 7245},
        "4. Líder": {"mercado": 12250, "minima": 10000, "brivia": 10411},
        "5. Head": {"mercado": 15375, "minima": 13000, "brivia": 12480},
        "6. Especialista": {"mercado": 13250, "minima": 11000, "brivia": 12480},
    },
    "Analista de Inbound": {
        "1. Junior": {"mercado": 5200, "minima": 4000, "brivia": 4206},
        "2. Pleno": {"mercado": 6700, "minima": 5500, "brivia": 6044},
        "3. Sênior": {"mercado": 8500, "minima": 7000, "brivia": 7245},
        "4. Líder": {"mercado": 10375, "minima": 8500, "brivia": 10411},
        "5. Head": {"mercado": 13375, "minima": 11000, "brivia": 12480},
        "6. Especialista": {"mercado": 12250, "minima": 10000, "brivia": 10411},
    },
    "Analista de Infraestrutura": {
        "1. Junior": {"mercado": 6000, "minima": 4500, "brivia": 4206},
        "2. Pleno": {"mercado": 8125, "minima": 6500, "brivia": 6044},
        "3. Sênior": {"mercado": 10750, "minima": 8500, "brivia": 7245},
        "4. Líder": {"mercado": 12250, "minima": 10000, "brivia": 10411},
        "5. Head": {"mercado": 15375, "minima": 13000, "brivia": 12480},
        "6. Especialista": {"mercado": 13250, "minima": 11000, "brivia": 12480},
    },
    "Analista de Midia": {
        "1. Junior": {"mercado": 5500, "minima": 4000, "brivia": 4206},
        "2. Pleno": {"mercado": 7625, "minima": 6000, "brivia": 6044},
        "3. Sênior": {"mercado": 9625, "minima": 8000, "brivia": 7245},
        "4. Líder": {"mercado": 11750, "minima": 9500, "brivia": 10411},
        "5. Head": {"mercado": 14375, "minima": 12000, "brivia": 12480},
        "6. Especialista": {"mercado": 12250, "minima": 10000, "brivia": 10411},
    },
    "Analista de Mídias Sociais": {
        "1. Junior": {"mercado": 5200, "minima": 4000, "brivia": 4206},
        "2. Pleno": {"mercado": 6700, "minima": 5500, "brivia": 6044},
        "3. Sênior": {"mercado": 8500, "minima": 7000, "brivia": 7245},
        "4. Líder": {"mercado": 10375, "minima": 8500, "brivia": 10411},
        "5. Head": {"mercado": 13375, "minima": 11000, "brivia": 12480},
        "6. Especialista": {"mercado": 12250, "minima": 10000, "brivia": 10411},
    },
    "Analista de Performance": {
        "1. Junior": {"mercado": 4800, "minima": 4500, "brivia": 4206},
        "2. Pleno": {"mercado": 6900, "minima": 6000, "brivia": 6044},
        "3. Sênior": {"mercado": 9275, "minima": 7500, "brivia": 7245},
        "4. Líder": {"mercado": 11600, "minima": 9000, "brivia": 10411},
        "5. Head": {"mercado": 14300, "minima": 11500, "brivia": 12480},
        "6. Especialista": {"mercado": 11325, "minima": 10000, "brivia": 10411},
    },
    "Analista de Plataforma": {
        "1. Junior": {"mercado": 4725, "minima": 4500, "brivia": 4206},
        "2. Pleno": {"mercado": 7050, "minima": 6000, "brivia": 6044},
        "3. Sênior": {"mercado": 9475, "minima": 7800, "brivia": 7245},
        "4. Líder": {"mercado": 11900, "minima": 9200, "brivia": 10411},
        "5. Head": {"mercado": 14425, "minima": 11000, "brivia": 12480},
        "6. Especialista": {"mercado": 11400, "minima": 9800, "brivia": 10411},
    },
    "Analista de Qualidade/ Tester": {
        "1. Junior": {"mercado": 4475, "minima": 4200, "brivia": 4206},
        "2. Pleno": {"mercado": 6600, "minima": 5600, "brivia": 6044},
        "3. Sênior": {"mercado": 8900, "minima": 7000, "brivia": 7245},
        "4. Líder": {"mercado": 11150, "minima": 8500, "brivia": 10411},
        "5. Head": {"mercado": 13550, "minima": 10200, "brivia": 12480},
        "6. Especialista": {"mercado": 10750, "minima": 9400, "brivia": 10411},
    },
    "Analista de SAC": {
        "1. Junior": {"mercado": 4050, "minima": 3800, "brivia": 4206},
        "2. Pleno": {"mercado": 5725, "minima": 4800, "brivia": 6044},
        "3. Sênior": {"mercado": 7700, "minima": 6200, "brivia": 7245},
        "4. Líder": {"mercado": 9725, "minima": 7500, "brivia": 10411},
        "5. Head": {"mercado": 12075, "minima": 9500, "brivia": 12480},
        "6. Especialista": {"mercado": 10000, "minima": 8800, "brivia": 10411},
    },
    "Analista de Sistema": {
        "1. Junior": {"mercado": 4675, "minima": 4200, "brivia": 4206},
        "2. Pleno": {"mercado": 6900, "minima": 5500, "brivia": 6044},
        "3. Sênior": {"mercado": 9225, "minima": 7000, "brivia": 7245},
        "4. Líder": {"mercado": 11550, "minima": 8500, "brivia": 10411},
        "5. Head": {"mercado": 13925, "minima": 10000, "brivia": 12480},
        "6. Especialista": {"mercado": 11100, "minima": 9200, "brivia": 10411},
    },
    "Analista de Suporte": {
        "1. Junior": {"mercado": 4225, "minima": 4000, "brivia": 4206},
        "2. Pleno": {"mercado": 6250, "minima": 5200, "brivia": 6044},
        "3. Sênior": {"mercado": 8375, "minima": 6500, "brivia": 7245},
        "4. Líder": {"mercado": 10550, "minima": 8000, "brivia": 10411},
        "5. Head": {"mercado": 12775, "minima": 9800, "brivia": 12480},
        "6. Especialista": {"mercado": 10600, "minima": 9000, "brivia": 10411},
    },
    "Analista Growth": {
        "1. Junior": {"mercado": 4650, "minima": 3800, "brivia": 4206},
        "2. Pleno": {"mercado": 6725, "minima": 6000, "brivia": 6044},
        "3. Sênior": {"mercado": 8875, "minima": 7500, "brivia": 7245},
        "4. Líder": {"mercado": 11075, "minima": 9000, "brivia": 10411},
        "5. Head": {"mercado": 13550, "minima": 11000, "brivia": 12480},
        "6. Especialista": {"mercado": 10925, "minima": 10200, "brivia": 10411},
    },
    "Analista SEO": {
        "1. Junior": {"mercado": 4600, "minima": 4500, "brivia": 4206},
        "2. Pleno": {"mercado": 6675, "minima": 5800, "brivia": 6044},
        "3. Sênior": {"mercado": 8825, "minima": 7200, "brivia": 7245},
        "4. Líder": {"mercado": 11000, "minima": 8800, "brivia": 10411},
        "5. Head": {"mercado": 13350, "minima": 10500, "brivia": 12480},
        "6. Especialista": {"mercado": 10750, "minima": 9800, "brivia": 10411},
    },
    "Arte Finalista": {
        "1. Junior": {"mercado": 4000, "minima": 3900, "brivia": 4206},
        "2. Pleno": {"mercado": 5725, "minima": 5100, "brivia": 6044},
        "3. Sênior": {"mercado": 7675, "minima": 6400, "brivia": 7245},
        "4. Líder": {"mercado": 9775, "minima": 7900, "brivia": 10411},
        "5. Head": {"mercado": 11950, "minima": 9600, "brivia": 12480},
        "6. Especialista": {"mercado": 9850, "minima": 9100, "brivia": 10411},
    },
    "Atendimento": {
        "1. Junior": {"mercado": 4275, "minima": 3800, "brivia": 4206},
        "2. Pleno": {"mercado": 6100, "minima": 5000, "brivia": 6044},
        "3. Sênior": {"mercado": 8150, "minima": 7000, "brivia": 7245},
        "4. Líder": {"mercado": 10225, "minima": 10000, "brivia": 10411},
        "5. Head": {"mercado": 12600, "minima": 12500, "brivia": 12480},
        "6. Especialista": {"mercado": 12400, "minima": 10000, "brivia": 10411},
    },
    "Cientista de Dados": {
        "1. Junior": {"mercado": 6000, "minima": 5200, "brivia": 6044},
        "2. Pleno": {"mercado": 7700, "minima": 6800, "brivia": 6044},
        "3. Sênior": {"mercado": 10225, "minima": 8600, "brivia": 7245},
        "4. Líder": {"mercado": 12600, "minima": 10200, "brivia": 10411},
        "5. Head": {"mercado": 15025, "minima": 12800, "brivia": 12480},
        "6. Especialista": {"mercado": 12600, "minima": 12000, "brivia": 12480},
    },
    "Desenvolvedor Back-End": {
        "1. Junior": {"mercado": 5000, "minima": 4800, "brivia": 6044},
        "2. Pleno": {"mercado": 7475, "minima": 6500, "brivia": 7245},
        "3. Sênior": {"mercado": 10100, "minima": 8200, "brivia": 10411},
        "4. Líder": {"mercado": 12550, "minima": 9800, "brivia": 12480},
        "5. Head": {"mercado": 15200, "minima": 12000, "brivia": 12480},
        "6. Especialista": {"mercado": 12325, "minima": 11500, "brivia": 12480},
    },
    "Desenvolvedor de Dados": {
        "1. Junior": {"mercado": 5050, "minima": 4900, "brivia": 6044},
        "2. Pleno": {"mercado": 7500, "minima": 6600, "brivia": 7245},
        "3. Sênior": {"mercado": 10150, "minima": 8300, "brivia": 10411},
        "4. Líder": {"mercado": 12600, "minima": 10000, "brivia": 12480},
        "5. Head": {"mercado": 15100, "minima": 12200, "brivia": 12480},
        "6. Especialista": {"mercado": 12400, "minima": 11800, "brivia": 12480},
    },
    "Desenvolver Front-end": {
        "1. Junior": {"mercado": 4800, "minima": 4700, "brivia": 6044},
        "2. Pleno": {"mercado": 7200, "minima": 6400, "brivia": 7245},
        "3. Sênior": {"mercado": 9750, "minima": 8000, "brivia": 10411},
        "4. Líder": {"mercado": 12125, "minima": 9600, "brivia": 12480},
        "5. Head": {"mercado": 14675, "minima": 11800, "brivia": 12480},
        "6. Especialista": {"mercado": 11900, "minima": 11400, "brivia": 12480},
    },
    "Desenvolver Full Stack": {
        "1. Junior": {"mercado": 5100, "minima": 4600, "brivia": 6044},
        "2. Pleno": {"mercado": 7600, "minima": 6300, "brivia": 7245},
        "3. Sênior": {"mercado": 10150, "minima": 7900, "brivia": 10411},
        "4. Líder": {"mercado": 12600, "minima": 9500, "brivia": 12480},
        "5. Head": {"mercado": 15075, "minima": 11600, "brivia": 12480},
        "6. Especialista": {"mercado": 12400, "minima": 11300, "brivia": 12480},
    },
    "Diretor de Arte": {
        "1. Junior": {"mercado": 4700, "minima": 4500, "brivia": 4206},
        "2. Pleno": {"mercado": 6925, "minima": 6400, "brivia": 6044},
        "3. Sênior": {"mercado": 9100, "minima": 8000, "brivia": 7245},
        "4. Líder": {"mercado": 11300, "minima": 9600, "brivia": 10411},
        "5. Head": {"mercado": 13825, "minima": 11800, "brivia": 12480},
        "6. Especialista": {"mercado": 11275, "minima": 9000, "brivia": 12480},
    },
    "Editor de Conteúdo": {
        "1. Junior": {"mercado": 4400, "minima": 4300, "brivia": 4206},
        "2. Pleno": {"mercado": 6375, "minima": 5700, "brivia": 6044},
        "3. Sênior": {"mercado": 8575, "minima": 7100, "brivia": 7245},
        "4. Líder": {"mercado": 10825, "minima": 8800, "brivia": 10411},
        "5. Head": {"mercado": 13425, "minima": 11300, "brivia": 12480},
        "6. Especialista": {"mercado": 10975, "minima": 10100, "brivia": 12480},
    },
    "Engenheiro de Dados": {
        "1. Junior": {"mercado": 5275, "minima": 5200, "brivia": 6044},
        "2. Pleno": {"mercado": 7700, "minima": 6600, "brivia": 7245},
        "3. Sênior": {"mercado": 10175, "minima": 8200, "brivia": 10411},
        "4. Líder": {"mercado": 12600, "minima": 10000, "brivia": 12480},
        "5. Head": {"mercado": 15225, "minima": 12500, "brivia": 19360},
        "6. Especialista": {"mercado": 12400, "minima": 11200, "brivia": 12480},
    },
    "Engenheiro de Sistema": {
        "1. Junior": {"mercado": 5325, "minima": 4500, "brivia": 6044},
        "2. Pleno": {"mercado": 7800, "minima": 6800, "brivia": 7245},
        "3. Sênior": {"mercado": 10300, "minima": 8400, "brivia": 10411},
        "4. Líder": {"mercado": 12750, "minima": 10200, "brivia": 12480},
        "5. Head": {"mercado": 15475, "minima": 12800, "brivia": 19360},
        "6. Especialista": {"mercado": 12400, "minima": 11400, "brivia": 12480},
    },
    "Gerente de Projeto": {
        "1. Junior": {"mercado": 6500, "minima": 5900, "brivia": 7760},
        "2. Pleno": {"mercado": 8525, "minima": 7800, "brivia": 8989},
        "3. Sênior": {"mercado": 11175, "minima": 9500, "brivia": 10411},
        "4. Líder": {"mercado": 13700, "minima": 11200, "brivia": 12480},
        "5. Head": {"mercado": 16500, "minima": 13800, "brivia": 19360},
        "6. Especialista": {"mercado": 13225, "minima": 12400, "brivia": 12480},
    },
    "Product Owner": {
        "1. Junior": {"mercado": 5525, "minima": 5200, "brivia": 6044},
        "2. Pleno": {"mercado": 8000, "minima": 6700, "brivia": 7245},
        "3. Sênior": {"mercado": 10450, "minima": 8100, "brivia": 10411},
        "4. Líder": {"mercado": 13025, "minima": 9800, "brivia": 12480},
        "5. Head": {"mercado": 15850, "minima": 12300, "brivia": 19360},
        "6. Especialista": {"mercado": 12500, "minima": 10900, "brivia": 12480},
    },
    "Produtor": {
        "1. Junior": {"mercado": 4450, "minima": 3800, "brivia": 4206},
        "2. Pleno": {"mercado": 6400, "minima": 6200, "brivia": 6044},
        "3. Sênior": {"mercado": 8475, "minima": 7700, "brivia": 7245},
        "4. Líder": {"mercado": 10550, "minima": 9200, "brivia": 10411},
        "5. Head": {"mercado": 13050, "minima": 11700, "brivia": 12480},
        "6. Especialista": {"mercado": 10650, "minima": 10400, "brivia": 12480},
    },
    "Redator": {
        "1. Junior": {"mercado": 4500, "minima": 3800, "brivia": 4206},
        "2. Pleno": {"mercado": 6450, "minima": 5400, "brivia": 6044},
        "3. Sênior": {"mercado": 8525, "minima": 7900, "brivia": 7245},
        "4. Líder": {"mercado": 10600, "minima": 9400, "brivia": 10411},
        "5. Head": {"mercado": 13125, "minima": 12000, "brivia": 12480},
        "6. Especialista": {"mercado": 10700, "minima": 10600, "brivia": 12480},
    },
    "Scrum Master": {
        "1. Junior": {"mercado": 5425, "minima": 4300, "brivia": 4206},
        "2. Pleno": {"mercado": 8375, "minima": 6700, "brivia": 6044},
        "3. Sênior": {"mercado": 11300, "minima": 9100, "brivia": 7245},
        "4. Líder": {"mercado": 14200, "minima": 11400, "brivia": 10411},
        "5. Head": {"mercado": 17100, "minima": 13700, "brivia": 19360},
        "6. Especialista": {"mercado": 13225, "minima": 10600, "brivia": 12480},
    },
    "UI": {
        "1. Junior": {"mercado": 4450, "minima": 3500, "brivia": 4206},
        "2. Pleno": {"mercado": 6900, "minima": 5400, "brivia": 6044},
        "3. Sênior": {"mercado": 9300, "minima": 7200, "brivia": 7245},
        "4. Líder": {"mercado": 11725, "minima": 9100, "brivia": 10411},
        "5. Head": {"mercado": 14500, "minima": 11400, "brivia": 12480},
        "6. Especialista": {"mercado": 11250, "minima": 8800, "brivia": 10411},
    },
    "UX": {
        "1. Junior": {"mercado": 4450, "minima": 3500, "brivia": 4206},
        "2. Pleno": {"mercado": 6900, "minima": 5400, "brivia": 6044},
        "3. Sênior": {"mercado": 9300, "minima": 7200, "brivia": 7245},
        "4. Líder": {"mercado": 11725, "minima": 9100, "brivia": 10411},
        "5. Head": {"mercado": 14500, "minima": 11400, "brivia": 12480},
        "6. Especialista": {"mercado": 11250, "minima": 8800, "brivia": 10411},
    },
    "Head de Tribo": {
        "1. Junior": {"mercado": 18000, "minima": 15000, "brivia": 19360},
        "2. Pleno": {"mercado": 20000, "minima": 17000, "brivia": 19360},
        "3. Sênior": {"mercado": 23000, "minima": 20000, "brivia": 19360},
        "4. Líder": {"mercado": 26000, "minima": 23000, "brivia": 19360},
        "5. Head": {"mercado": 29250, "minima": 26000, "brivia": 19360},
        "6. Especialista": {"mercado": 27250, "minima": 24000, "brivia": 19360},
    }
}

# --- MAPEAMENTO DE SERVIÇOS PARA OFERTAS ---
MAPEAMENTO_OFERTAS = {
    "Ad Campaign": "Communication & Advertising Management",
    "Always on Communication": "Communication & Advertising Management",
    "Always on Media": "Media Management",
    "Production": "Production Management",
    "Performance Media": "Performance Management",
    "Customer Relationship Strategy": "CRM",
    "Customer Relationship Management": "CRM",
    "Social Media & Community Management": "Social Media",
    "Social Listening": "Social Media",
    "SAC 3.0": "CX Management",
    "Customer Journey Management": "CX Management",
    "Outsourcing Com": "TaaS Com",
    "Digital Channels Design": "Experience Design",
    "Digital Channels Development": "Experience Development",
    "Growth Squad": "Growth Marketing",
    "Growth Sprint": "Growth Marketing",
    "Content Marketing Management": "Content Marketing",
    "Inbound & Outbound Marketing": "Content Marketing",
    "Cloud Computing": "IT Projects & Consulting",
    "DevSecOps": "IT Projects & Consulting",
    "Engineering Consulting": "IT Projects & Consulting",
    "Baseline Services/ ITSM": "IT Projects & Consulting",
    "Discovery Squad": "Digital Factory",
    "Delivery Squad": "Digital Factory",
    "Martech Consulting & Implementation": "Platforms & Partnerships",
    "Outsourcing Tech": "TaaS Tech",
    "Estratégia e Propósito": "Branding",
    "Naming & Identidade": "Branding",
    "Arquitetura de Marca": "Branding",
    "Digital Maturity Assessment": "Digital Transformation",
    "Customer Journey Mapping": "CX Strategy & Consulting",
    "Research": "CX Strategy & Consulting",
    "Discovery & Strategy": "Business Strategy & Consulting",
    "Data Discovery & Roadmap Strategy": "Data Intelligence",
    "Data Architecture": "Data Intelligence",
    "Strategic Data Analytics Process": "Data Intelligence",
    "Data Analytics Process": "Data Factory",
    "Data Visualization": "Data Factory",
    "Listening and Monitoring": "Data Factory",
    "Predicting Analysis & Artificial Intelligence Process": "Data Factory"
}

# --- RECEITA TOTAL POR CENÁRIO (7. GM!B7) ---
RECEITA_TOTAL_CENARIO = {
    "mercado": 37358.00,
    "minima": 26711.00,
    "brivia": 36273.00
}



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
    elif st.session_state.fase_atual == 2:
        renderizar_fase_2()
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
    st.subheader("Receita Adicional")
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
        st.markdown("**TOTAL RECEITA ADICIONAL**")
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
        st.metric("Receita Adicional", formatar_moeda(total_receita_bruta))
    
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

# ==================== FASE 2: EQUIPE CLT ====================

def renderizar_fase_2():
    st.header("FASE 2: Equipe CLT")
    st.markdown('<div class="brivia-alerta">Seleção de profissionais, cálculo de Man-Hours e rateio proporcional de Preço de Venda conforme cenário.</div>', unsafe_allow_html=True)

    if 'lista_equipe' not in st.session_state:
        st.session_state.lista_equipe = []

    # --- SELEÇÃO DE RÉGUA SALARIAL ---
    regua_selecionada = st.radio(
        "Selecione a Régua Salarial para os cálculos:",
        ["Média de mercado", "Faixa Mínima", "Média Brivia (mercer)"],
        horizontal=True
    )

    mapa_regua = {
        "Média de mercado": "mercado",
        "Faixa Mínima": "minima",
        "Média Brivia (mercer)": "brivia"
    }
    regua_id = mapa_regua[regua_selecionada]

    # --- ENTRADA DE DADOS ---
    col1, col2 = st.columns(2)
    with col1:
        perfil = st.selectbox("Perfil", list(BASE_SALARIAL.keys()))
        nivel = st.selectbox("Nível", ["1. Junior", "2. Pleno", "3. Sênior", "4. Líder", "5. Head", "6. Especialista"])
    with col2:
        servico = st.selectbox("Serviço Brivia", list(MAPEAMENTO_OFERTAS.keys()))
        oferta_2025 = MAPEAMENTO_OFERTAS.get(servico, "Não mapeado")
        st.text_input("Oferta Brivia (2025)", value=oferta_2025, disabled=True)

    col3, col4 = st.columns(2)
    with col3:
        qtd_func = st.number_input("Quantidade de Funcionários", min_value=1, value=1, step=1)
    with col4:
        dedicacao = st.slider("Dedicação (%)", 0, 100, 100)

    # --- CÁLCULOS TÉCNICOS DA LINHA ATUAL (PREVIEW) ---
    total_horas_preview = qtd_func * (dedicacao / 100) * 170
    salario_base_preview = BASE_SALARIAL.get(perfil, {}).get(nivel, {}).get(regua_id, 0)
    custo_hora_preview = (((salario_base_preview * 1.6485) + 1190)) / 170 if salario_base_preview > 0 else 0
    custo_total_preview = custo_hora_preview * total_horas_preview

    # Métricas de Resumo Instantâneo (Preview)
    st.markdown("---")
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Salário Base", f"R$ {salario_base_preview:,.2f}")
    m2.metric("Custo Hora", f"R$ {custo_hora_preview:,.2f}")
    m3.metric("Total Horas", f"{total_horas_preview:.1f}h")
    m4.metric("Custo Total (K10)", f"R$ {custo_total_preview:,.2f}")

    if st.button("＋ Adicionar Funcionário à Equipe", use_container_width=True):
        # Guardamos apenas os inputs base para poder recalcular tudo dinamicamente se a régua mudar
        novo_recurso = {
            "Perfil": perfil,
            "Nível": nivel,
            "Serviço": servico,
            "Qtd": qtd_func,
            "Dedicação %": dedicacao
        }
        st.session_state.lista_equipe.append(novo_recurso)
        st.rerun()

    # --- TABELA DE RESUMO E RATEIO DINÂMICO ---
    if st.session_state.lista_equipe:
        st.markdown("---")
        st.subheader(f"Resumo da Equipe CLT - Cenário: {regua_selecionada}")

        # Criamos o DataFrame a partir dos inputs e calculamos os valores financeiros NA HORA
        df = pd.DataFrame(st.session_state.lista_equipe)

        # 1. Calculamos Salário, Custo Hora e Custo Total (K10) para cada linha baseado na régua atual
        def calc_financeiro(row):
            sal = BASE_SALARIAL.get(row['Perfil'], {}).get(row['Nível'], {}).get(regua_id, 0)
            c_hora = (((sal * 1.6485) + 1190)) / 170 if sal > 0 else 0
            t_horas = row['Qtd'] * (row['Dedicação %'] / 100) * 170
            c_total = c_hora * t_horas
            return pd.Series([sal, c_hora, c_total], index=['Salário Base', 'Custo Hora', 'Custo Total'])

        df[['Salário Base', 'Custo Hora', 'Custo Total']] = df.apply(calc_financeiro, axis=1)

        # 2. Etapa 11: Rateio Proporcional (Fórmula: K10 / K42 * B7)
        soma_k42 = df["Custo Total"].sum() # Soma de todos os custos totais (K42)
        receita_b7 = RECEITA_TOTAL_CENARIO[regua_id] # Receita do cenário (B7)

        if soma_k42 > 0:
            # Aplicação exata da sua fórmula: SE($E10=0;0;$K10/K$42*'7. GM'!B$7)
            df["Preço Venda"] = (df["Custo Total"] / soma_k42) * receita_b7
        else:
            df["Preço Venda"] = 0.0

        # Tratamento de erro/vazio (SEERRO)
        df["Preço Venda"] = df["Preço Venda"].fillna(0.0)

        # Exibição da tabela
        edited_df = st.data_editor(
            df,
            use_container_width=True,
            num_rows="dynamic",
            key="editor_fase2_dinamico",
            disabled=["Salário Base", "Custo Hora", "Custo Total", "Preço Venda"] # Apenas inputs são editáveis na lixeira
        )

        # Sincronização da memória ao deletar
        if len(edited_df) != len(st.session_state.lista_equipe):
            # Mantemos apenas as colunas de input na memória original
            st.session_state.lista_equipe = edited_df[['Perfil', 'Nível', 'Serviço', 'Qtd', 'Dedicação %']].to_dict('records')
            st.rerun()

        # Resumo Financeiro Acumulado para conferência
        st.markdown("---")
        c_tot1, c_tot2 = st.columns(2)
        c_tot1.metric("Soma Custos Totais (K42)", f"R$ {soma_k42:,.2f}")
        c_tot2.metric("Soma Preços Venda (B7)", f"R$ {df['Preço Venda'].sum():,.2f}")

if __name__ == "__main__":
    main()