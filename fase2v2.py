import streamlit as st
import pandas as pd

# ==================== 1. CONFIGURAÇÃO E IDENTIDADE VISUAL ====================
st.set_page_config(page_title="Brivia - Dimensionamento CLT", layout="wide")

logo_url = "https://cdn.prod.website-files.com/65c2dcb4330facd527e06bdd/6619a7597575e945de440959_brivia_group.svg"

st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;700&display=swap');
    .stApp {{ background-color: #000000 !important; }}
    .header-brivia {{ display: flex; align-items: center; padding-bottom: 30px; margin-bottom: 20px; border-bottom: 1px solid rgba(255,255,255,0.1); }}
    .logo-brivia {{ height: 35px; margin-right: 20px; filter: brightness(0) invert(1) !important; }}
    .brivia-alerta {{ padding: 15px; border-radius: 4px; background-color: rgba(255,255,255,0.05); border-left: 5px solid #90513b; color: #ffffff; font-family: 'Space Grotesk'; font-size: 0.9rem; margin-bottom: 25px; }}
    h1, h2, h3, label, p {{ font-family: 'Space Grotesk', sans-serif !important; color: white !important; }}
    .fase-container {{ padding: 12px; border-radius: 4px; text-align: center; font-family: 'Space Grotesk'; font-size: 0.75rem; text-transform: uppercase; letter-spacing: 1.5px; margin-bottom: 10px; }}
    .fase-atual {{ background: linear-gradient(#000, #000) padding-box, linear-gradient(135deg, #90513b, #ffffff) border-box; border: 2px solid transparent; color: #ffffff !important; font-weight: 700; box-shadow: 0 0 15px rgba(144, 81, 59, 0.4); }}
    .fase-ok {{ border: 1px solid rgba(255,255,255,0.3); color: rgba(255,255,255,0.6); }}
</style>
<div class="header-brivia">
    <img src="{logo_url}" class="logo-brivia">
    <h1 style="margin:0; font-size: 1.8rem; letter-spacing: -1px;">Dimensionamento Equipe CLT</h1>
</div>
""", unsafe_allow_html=True)

# ==================== 2. BASE DE DADOS COMPLETA (MERCER) ====================

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

# ==================== CÁLCULO DINÂMICO DE RECEITA TOTAL ====================

def calcular_receita_total(tipo_contrato, soma_custos, gross_margin_alvo, aliquota_imposto,
                           comissao_nb, comissao_parceiros, outras_receitas):
    """
    Calcula a receita total baseada na fórmula de precificação reversa.

    Fórmula da planilha:
    =SE('2. Dados'!$C$11="Fee";
        (-SOMA(B$26:B$30)) / ((1 - GM_ALVO) - IMPOSTO - ((COM_NB + COM_PARCEIROS) * (1 - GM_ALVO))) - SOMA(B$10:B$15);
        0)

    Para "Projeto" usa a mesma fórmula.

    Args:
        tipo_contrato: "Fee" ou "Projeto"
        soma_custos: Soma total de custos (Pessoal + Terceiros + Materiais + Viagens + Outros + Comissões)
        gross_margin_alvo: Margem bruta alvo em % (ex: 40.0)
        aliquota_imposto: Alíquota de imposto em % (ex: 6.65)
        comissao_nb: Comissão NB em % (ex: 2.0)
        comissao_parceiros: Comissão parceiros em % (ex: 3.0)
        outras_receitas: Soma de outras receitas (1.3 a 1.8)

    Returns:
        Receita total calculada (ou 0 se não for Fee/Projeto)
    """
    if tipo_contrato not in ["Fee", "Projeto"]:
        return 0.0

    # Converter percentuais para decimais
    gm = gross_margin_alvo / 100
    imposto = aliquota_imposto / 100
    com_nb = comissao_nb / 100
    com_parc = comissao_parceiros / 100

    # Cálculo do denominador
    denominador = (1 - gm) - imposto - ((com_nb + com_parc) * (1 - gm))

    # Evitar divisão por zero
    if denominador == 0:
        return 0.0

    # Cálculo da receita
    # soma_custos já vem positivo, então não precisa do sinal negativo
    receita = (soma_custos / denominador) - outras_receitas

    return max(receita, 0.0)  # Garantir que não retorne negativo

# ==================== 3. LÓGICA DA INTERFACE ====================

def renderizar_fase_2():
    st.header("FASE 2: Equipe CLT")
    st.markdown('<div class="brivia-alerta">Seleção de profissionais, cálculo de Man-Hours e rateio proporcional de Preço de Venda conforme cenário.</div>', unsafe_allow_html=True)

    if 'lista_equipe' not in st.session_state:
        st.session_state.lista_equipe = []

    # ==================== BUSCAR DADOS DA FASE 1 ====================
    # Verificar se os dados da Fase 1 existem
    if 'dados_basicos' not in st.session_state:
        st.warning("⚠️ Por favor, complete a Fase 1 (Dados Básicos) primeiro.")
        return

    # Extrair dados necessários da Fase 1
    dados = st.session_state.dados_basicos
    tipo_contrato = dados.get('tipo_contrato', 'Fee')
    quantidade_meses = dados.get('quantidade_meses', 12)

    # Gross Margin = GM Alvo (40%) - Desconto
    GROSS_MARGIN_ALVO = 40.0
    desconto_gm = st.session_state.gross_margin.get('desconto', 0.0) if 'gross_margin' in st.session_state else 0.0
    gross_margin_final = GROSS_MARGIN_ALVO - desconto_gm

    aliquota_imposto = dados.get('aliquota_imposto', 0.0)
    comissao_nb = dados.get('comissao_nb', 0)
    comissao_parceiros = dados.get('comissao_parceiros', 0)

    # Calcular soma de outras receitas (1.3 a 1.8)
    outras_receitas_total = 0.0
    if 'receita_bruta' in st.session_state:
        for linha, valores in st.session_state.receita_bruta.items():
            verba = valores.get('verba_total', 0.0)
            comissao_pct = valores.get('comissao_pct', 0.0)
            outras_receitas_total += verba * (comissao_pct / 100)

    # Calcular custos fixos da Fase 1 (Viagens + Outros Custos)
    custos_fixos_total = 0.0
    if 'custos' in st.session_state:
        for linha, valores in st.session_state.custos.items():
            if linha not in ["Terceiros", "Materiais"]:  # Esses são calculados em outras fases
                valor_mensal = valores.get('valor_mensal', 0.0)
                custos_fixos_total += valor_mensal * quantidade_meses

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
        soma_k42 = df["Custo Total"].sum()  # Soma de todos os custos CLT (K42)

        # Calcular RECEITA TOTAL dinamicamente (B7)
        # Soma de custos = Custos CLT (K42) + Custos Fixos da Fase 1
        # Nota: Terceiros e Materiais serão adicionados nas próximas fases
        soma_custos_total = soma_k42 + custos_fixos_total

        # Calcular receita usando a fórmula de precificação reversa
        receita_b7 = calcular_receita_total(
            tipo_contrato=tipo_contrato,
            soma_custos=soma_custos_total,
            gross_margin_alvo=gross_margin_final,
            aliquota_imposto=aliquota_imposto,
            comissao_nb=comissao_nb,
            comissao_parceiros=comissao_parceiros,
            outras_receitas=outras_receitas_total
        )

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
        st.subheader("Resumo Financeiro")

        col_r1, col_r2, col_r3 = st.columns(3)
        col_r1.metric("Custos CLT (Pessoal)", f"R$ {soma_k42:,.2f}")
        col_r2.metric("Custos Fixos (Fase 1)", f"R$ {custos_fixos_total:,.2f}")
        col_r3.metric("Custo Total", f"R$ {soma_custos_total:,.2f}")

        col_r4, col_r5, col_r6 = st.columns(3)
        col_r4.metric("Outras Receitas", f"R$ {outras_receitas_total:,.2f}")
        col_r5.metric("Receita Total (B7)", f"R$ {receita_b7:,.2f}")
        col_r6.metric("Soma Preços Venda", f"R$ {df['Preço Venda'].sum():,.2f}")

        # Exibir detalhes dos parâmetros usados no cálculo
        with st.expander("📊 Ver Detalhes do Cálculo de Receita"):
            st.markdown(f"""
            **Parâmetros do Cálculo:**
            - Tipo de Contrato: **{tipo_contrato}**
            - Gross Margin Alvo: **{gross_margin_final:.2f}%**
            - Alíquota de Imposto: **{aliquota_imposto:.2f}%**
            - Comissão NB: **{comissao_nb}%**
            - Comissão Parceiros: **{comissao_parceiros}%**
            - Duração: **{quantidade_meses} meses**

            **Fórmula Aplicada:**
            ```
            Receita = (Soma_Custos / Denominador) - Outras_Receitas

            Onde:
            Denominador = (1 - GM) - Imposto - ((Com_NB + Com_Parceiros) * (1 - GM))
            Denominador = (1 - {gross_margin_final/100:.4f}) - {aliquota_imposto/100:.4f} - (({comissao_nb/100:.4f} + {comissao_parceiros/100:.4f}) * (1 - {gross_margin_final/100:.4f}))
            Denominador = {(1 - gross_margin_final/100) - (aliquota_imposto/100) - ((comissao_nb/100 + comissao_parceiros/100) * (1 - gross_margin_final/100)):.6f}
            ```
            """)

# Inicialização e Execução
if 'fase_atual' not in st.session_state:
    st.session_state.fase_atual = 2

renderizar_fase_2()