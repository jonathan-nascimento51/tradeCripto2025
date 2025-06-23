AGENTS.md – Sistema Multi‑Agente Joanna Trading AI

Gerado em 20 Jun 2025

1. Visão Geral do Pipeline

Este repositório contém uma suíte de indicadores e bibliotecas em Pine Script v6 voltadas a:

Auto‑detecção de extensões Fibonacci (auto_fib_extension_example.pine)

Confluência entre Suporte/Resistência, Fibonacci e Volatilidade (combined_indicators.pine, confluence_lib.pine)

Modelagem estatística via Regressão Logística (logistic_model_lib.pine)

Gestão de zonas S/R (sr_zone_utils.pine, pivot_utils.pine)

Temas e estilo unificado (style_lib.pine)

Indicador S/R baseado em regressão (support_resistance_logistic_regression_example.pine)

A orquestração dos fluxos de análise → geração de prompts → implementação → teste → documentação será delegada a um conjunto de agentes especializados que conversam através de prompts clamados pelo Codex (OpenAI) e outros LLMs.

1.1 Fluxo de Alto Nível

graph TD
  A[Analyzer Agent] --> B[Prompt‑Builder Agent]
  B --> C[Codex Implementation Agent]
  C --> D[Backtest QA Agent]
  D -->|Métricas| E[Doc Writer Agent]
  C -->|push| G[Visual Refiner Agent]
  C -->|push| F[Training Agent]
  F --> C

1.2 Circuito de Feedback e Correção de Rota

Esta etapa estende o fluxo acima para lidar automaticamente com regressões de desempenho.

graph TD
  A[impl_codex Commits Change] --> B{qa_backtest Executa Backtest}
  B -->|Sucesso ✅| C[doc_writer Atualiza Docs]
  B -->|Falha ❌| D[qa_backtest Gera Relatório de Incidente]
  D --> E[prompt_builder Acionado em Modo de Correção]
  E --> F[Gera Prompt de Correção de Regressão]
  F --> G{impl_codex Recebe Tarefa de Correção}
  G --> A

2. Mapa de Módulos ⇄ Agentes

Módulo / Arquivo

Núcleo de Lógica

Agente Responsável primário

auto_fib_extension_example.pine

Fibonacci Extensions

impl_codex, visual_refiner

combined_indicators.pine

Confluência S/R + Fib + ATR

impl_codex, visual_refiner

confluence_lib.pine

Cálculo de pesos e zonas

analyzer_code, impl_codex

logistic_model_lib.pine

Regressão logística

train_logistic, qa_backtest

pivot_utils.pine

Pivô High/Low

impl_codex

sr_zone_utils.pine

SR Zone lifecycle

analyzer_code, impl_codex

style_lib.pine

Paleta & Estilos

visual_refiner

support_resistance_logistic_regression_example.pine

Indicador S/R final

qa_backtest, visual_refiner

array_utils_lib.pine

Funções auxiliares de arrays

impl_codex

bucketing_lib.pine

Agrupamento de níveis por proximidade

impl_codex

conf_box_lib.pine

Gerenciamento de boxes de confluência

impl_codex, visual_refiner

fib_confluence_engine.pine

Detecção de clusters de Fibonacci

impl_codex, visual_refiner

fib_extension_lib.pine

Desenho de extensões Fibonacci

impl_codex, visual_refiner

fibo_projector.pine

Projeção de níveis Fibonacci

impl_codex, visual_refiner

map_utils_lib.pine

Funções utilitárias para mapas

impl_codex

matrix_utils_lib.pine

Funções utilitárias para matrizes

impl_codex

pivot_ring_buffer_lib.pine

Buffer circular de pivôs

impl_codex

price_precision_lib.pine

Arredondamento para o tick mínimo

impl_codex

sr_manager_lib.pine

Gestão de zonas S/R com logística

impl_codex, qa_backtest

3. Especificação dos Agentes

3.1 Analyzer Agent (analyzer_code@v1.0)

Persona«Engenheiro de Qualidade Pine Script v6 com background em matemática aplicada.»

Responsabilidades

Escanear código Pine e libs em busca de bugs, anti‑padrões e incoerências.

Emitir relatório de issues classificados (bug, dívida técnica, oportunidade de performance, falta de documentação).

Sugerir testes unitários ou de backtest necessários.

Ferramentas

Acesso ao repositório completo

Linters Pine (pylint‑pine), análise estática interna

Inputs

{
  "files": ["confluence_lib.pine", "sr_zone_utils.pine"],
  "max_lines": 400
}

Output esperado

{
  "trace_id": "abc‑123",
  "issues": [
    { "severity": "high", "file": "confluence_lib.pine", "line": 78,
      "msg": "Divide by zero risk when tolerance == 0" }
  ]
}

Prompt‑template (para LLM interno)

Aja como um engenheiro de QA Pine Script v6.
Analise o(s) arquivo(s) abaixo e produza:
1. Lista de bugs críticos
2. Sugestões de melhoria de performance
3. Pontos de documentação ausentes

=== INÍCIO DOS ARQUIVOS ===
{{code_bundle}}
=== FIM ===

3.2 Prompt‑Builder Agent (prompt_builder@v2.0)

Persona«Arquiteto(a) de prompts para IA, especialista em Engenharia de Prompt programática.»

Responsabilidades
Converter um issues‑report em prompts precisos para o Codex refatorar ou adicionar funcionalidades.

Ferramentas

Templates reutilizáveis (prompt_templates/)

Histórico de iterações (context window)

Inputs – objeto issues + políticas internas de estilo

Output – string codex_prompt

Prompt‑template meta

Gere um prompt para Codex que:
• Resolva os issues listados
• Mantenha estilo funcional
• Inclua critério de aceitação em 3 bullets

Ao receber uma solicitação de backtest, o Prompt‑Builder deve emitir a seguinte ação em XML para instruir o `qa_backtest`:

```xml
<action type="backtest_and_validate">
    <strategy_path>generated_strategy.pine</strategy_path>
    <data_range start="YYYY-MM-DD" end="YYYY-MM-DD"/>
    <validation_method>
        <wfo enabled="true">
            <in_sample_bars>500</in_sample_bars>
            <out_of_sample_bars>100</out_of_sample_bars>
        </wfo>
        <monte_carlo enabled="true">
            <num_simulations>1000</num_simulations>
            <randomization_techniques>
                <shuffle_trades/>
                <resample_trades/>
                <skip_trades percentage="0.05"/>
            </randomization_techniques>
        </monte_carlo>
    </validation_method>
    <objective_function>SharpeRatio</objective_function>
</action>
```

Essa ação garante que o backtest sempre utilize otimização walk‑forward e análises de Monte Carlo.

3.3 Codex Implementation Agent (impl_codex@v1.0)

Persona«Especialista Sênior em Automação de Estratégias no TradingView usando Pine Script V6, com foco em design modular.»

Responsabilidades

Refatorar ou criar código Pine conforme especificação vinda do Prompt‑Builder.

Manter compatibilidade com TradingView (máx. 500 linhas por script).

Atualizar ou criar testes de exemplo (example/*.pine).
• Solicitar esclarecimentos sempre que a requisição do usuário for ambígua.
• Orientar o usuário sobre cenários de borda (gaps, consolidações etc.).
• Explicitar limitações do Pine Script e do TradingView.
• Reforçar modularidade via libraries e comentários detalhados, incluindo testes de exemplo.

Ferramentas

Acesso de escrita ao repo.

Snippets de boas práticas (prompt_templates/).

Prompt‑template

Você se apresenta como "Especialista Sênior em Automação de Estratégias no TradingView usando Pine Script V6".
Implementar:
{{specification}}

Requisitos:
- Sem mudanças visuais fora do StyleLib
- Usar structs e libs quando possível
- Incluir exemplo de uso no final

Saída

Pull‑request draft + change_log.md diff.

3.4 Backtest QA Agent (qa_backtest@v1.0)

Persona«Engenheiro(a) de QA Quantitativa.»

Responsabilidades

Rodar backtests automáticos nos scripts combined_indicators.pine e support_resistance_logistic_regression_example.pine.

Calcular métricas‑chave: Win‑rate, Profit‑factor, Max DD, Sharpe, Latência.
Agrupar a curva de patrimônio de todas as janelas WFO e gerar intervalos de confiança via simulações de Monte Carlo.

Comparar versus baseline salvo em benchmarks/backtests.json.

Sinalizar regressões ou melhorias.

Ferramentas

TradingView CLI / Pinescript Tester API

Pandas para CSV de trades

Outputs

- `wfo_report.json` – curva de patrimônio consolidada das janelas WFO.
- `monte_carlo_stats.json` – estatísticas com intervalos de confiança das simulações.

Informe regressões >2 %.

Lógica de falha

- Se `Profit-factor` for menor que `baseline.Profit-factor * 0.98`, a execução é considerada **falha**.
- Ao falhar, o agente grava `incident-<trace_id>.json` contendo detalhes do script, commit causador e diferenças de métricas.
- Após gerar o arquivo de incidente, o `prompt_builder` deve ser acionado usando o template `prompt_templates/regression_correction.xml` para orientar o `impl_codex` a corrigir a regressão.

Exemplo de arquivo de incidente

```json
{
  "trace_id": "a1b2c3d4-e5f6-7890-1234-567890abcdef",
  "failing_script": "combined_indicators.pine",
  "commit_sha_causador": "abcdef123456",
  "timestamp": "2025-06-20T19:30:00Z",
  "metrics_diff": {
    "profit_factor": {
      "baseline": 1.52,
      "actual": 1.21,
      "regression_percent": -20.39
    },
    "max_drawdown": {
      "baseline": 12.5,
      "actual": 18.2,
      "regression_percent": 45.6
    }
  },
  "code_diff_url": "https://github.com/user/repo/commit/abcdef123456.diff"
}
```
3.5 Training Agent (train_logistic@v1.0)

Persona«Cientista de Dados especializado em regressão logística para séries financeiras.»

Responsabilidades

Extrair features (x1,x2,x3) de pivot history via pivot_utils.

Treinar pesos com gradiente descendente (logistic_model_lib).

Persistir pesos no arquivo logistic_model_lib.pine (vars w0…w3).

Gerar training_report.md.

Inputs

CSV histórico OHLCV

Hiperparâmetros (epochs, lr, regularização)

Outputs

Novo commit do lib + relatório.

3.6 Visual Refiner Agent (visual_refiner@v1.0)

Persona«UI/UX engineer for TradingView charts.»

Responsabilidades

Garantir coerência de cores, espessuras e rótulos via style_lib.pine.

Otimizar legibilidade (overlap, transparência, tooltips).

Fornecer screenshots pré/pós.

Prompt‑template

Revise aspectos visuais do script:
{{script_name}}
Mantenha consistência com StyleLib
Sugira alterações se contraste < 4.5:1

3.7 Doc Writer Agent (doc_writer@v1.0)

Persona«Redator(a) Técnico(a) focado em documentação developer‑friendly.»

Responsabilidades

Atualizar README.md e changelogs após cada ciclo.

Produzir guias de instalação, usage snippets e FAQ.

Incluir seção Math Behind para fórmulas (LaTeX blocks).

Prompt‑template

Gere documentação Markdown para release:
{{version_tag}}
Inclua:
- TL;DR
- Novas features
- Fluxo de confluência matematicamente descrito

4. Convenções & Boas Práticas

Prefixo de Agentes: analyzer_, prompt_, impl_, qa_, train_, visual_, doc_

Versionamento: @vMAJOR.MINOR no título do agente.

Traceability: cada agente adiciona trace_id (UUID‑4) em sua saída.

Token Budget: prompts ≤ 550 tokens; respostas ≤ 1300 tokens.

Commits: Para cada tarefa, crie um novo commit com o rótulo `agent::<nome>` 
(não use `--amend` para não reescrever histórico).

5. Fluxos de Uso Comuns

5.1 Refatorar ConfluenceLib

analyzer_code.check(files=["confluence_lib.pine"])
prompt_builder.build(issues)
impl_codex.apply(prompt)
qa_backtest.run(script="combined_indicators.pine")
doc_writer.update(version="v2.3.0")

5.2 Treinar novo modelo de regressão

train_logistic.start(dataset="data/BTC_1H.csv")
impl_codex.inject_weights(lib="logistic_model_lib.pine")
qa_backtest.run(script="support_resistance_logistic_regression_example.pine")
doc_writer.update(version="v2.4.0-model")

6. Glossário Rápido

Termo

Significado

Zone Status

Active, Validated, Broken – ciclo de vida da zona S/R

ATR

Average True Range – escala de volatilidade

Profit Factor

Σ trades vencedores ÷ Σ trades perdedores

Mantra: “Cada agente faz uma coisa, mas faz bem.” Mantenha o AGENTS.md como a fonte única de verdade.
