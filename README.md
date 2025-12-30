# Sistema de Precificação Brivia

Sistema integrado para precificação de contratos e projetos da Brivia.

## Estrutura do Projeto

### Arquivos Principais

- **`app.py`** - Aplicação principal com todas as fases integradas
- **`config_database.py`** - Base de dados centralizada com todas as constantes e configurações

### Arquivos Antigos (para referência)

- `2Dados_v6.py` - Versão antiga da fase 1
- `2Dados_v7.py` - Versão antiga com código misturado (DESCONTINUADO)
- `3Equipe.py` - Versão antiga da fase 2
- `fase2v2.py` - Versão antiga da fase 2

## Como Executar

```bash
streamlit run app.py
```

## Fases do Sistema

### Fase 1: Dados Básicos
- Informações do cliente e contrato
- Tributação e impostos
- Comissões (NB e Parceiros)
- Receita adicional
- Custos extras
- Gross Margin

### Fase 2: Equipe CLT
- Seleção de profissionais
- Cálculo de Man-Hours
- Rateio proporcional de Preço de Venda
- Três cenários: Média de mercado, Faixa Mínima, Média Brivia

### Fase 3: Terceiros
(Em desenvolvimento)

### Fase 4: Ferramentas
(Em desenvolvimento)

## Melhorias Implementadas

1. **Base de Dados Centralizada**: Todas as constantes e configurações em um único arquivo (`config_database.py`)
2. **Código Consolidado**: Todas as fases integradas em um único arquivo principal (`app.py`)
3. **Navegação Melhorada**: Sistema de fases com indicadores visuais
4. **Correção de Erros**: Eliminação de código duplicado e misturado
5. **Estrutura Organizada**: Separação clara entre configurações e lógica de negócio

## Tecnologias Utilizadas

- Python 3.x
- Streamlit
- Pandas
- Plotly

## Dados

### Base Salarial
Base completa com salários de mercado, mínimo e Brivia para todos os perfis profissionais.

### Mapeamento de Ofertas
Relacionamento entre serviços Brivia e ofertas 2025.

### Configurações de Tributação
Empresas e alíquotas de impostos por tipo de serviço.
