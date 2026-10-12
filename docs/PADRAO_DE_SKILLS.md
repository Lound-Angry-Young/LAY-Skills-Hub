# Padrão Estrito de Engenharia de Agent Skills (Anthropic / LAY)

Toda nova skill criada, adicionada ou refatorada no ecossistema DEVE seguir obrigatoriamente as diretrizes abaixo.

---

## 1. Metadados e Gatilhos (YAML Frontmatter)
Toda skill deve iniciar com frontmatter YAML estrito:
```yaml
---
name: [gerund-name]
description: >
  [Ação em 3ª pessoa]. Use this skill when: [condições exatas]. Do NOT use this skill when: [falsos positivos].
---
```
- **`name`**: Máximo de 64 caracteres. Apenas minúsculas e hifens (`^[a-z0-9-]+$`). Use formato de ação/gerúndio em inglês (ex: `processing-pdfs`, `auditing-code-security`). Proibido usar palavras vagas ou nomes reservados.
- **`description`**: Máximo de 1024 caracteres. Sempre redigida em 3ª pessoa ("Executa X...", "Orquestra Y...", "Audita Z...").
- **Limites Obrigatórios**: Deve encerrar expressamente com:
  - `Use this skill when: [condições exatas de acionamento]`
  - `Do NOT use this skill when: [cenários que pertencem a outras skills ou edição trivial]`

---

## 2. Princípio da Responsabilidade Única (SRP)
- Cada skill deve executar apenas uma competência primária.
- Se a intenção original envolver ações duplas (ex: "Testar e Fazer Deploy", "Criar Backup e Restaurar", "Depreciar e Migrar"), **divida imediatamente em duas skills distintas** e independentes.

---

## 3. Assinatura de Entradas e Saídas (I/O Signature)
Para skills que executam ações (comandos, chamadas de API, alterações de arquivos) — ver seção 8 — declare, logo após o bloco YAML, a assinatura tipada e documentada:
```markdown
## Input/Output Signature
Input:
- targetPath: string # Caminho do arquivo ou recurso alvo
- parameters: object # Parâmetros operacionais
- dryRun: boolean # Execução consultiva sem efeitos colaterais
Output:
- success: boolean # Status da execução
- status: string # Estado final (completed, failed, skipped)
- artifacts: array # Lista de artefatos gerados
- executionLog: string # Mensagem de saída ou diagnóstico
```

---

## 4. Estrutura do Arquivo Principal (SKILL.md)
O arquivo `SKILL.md` atua como **roteador e motor de execução**:
- **Matriz de Roteamento**: Tabela mapeando cenários para ações e graus de liberdade.
- **Passos Imperativos**: Lista numerada (`1.`, `2.`, `3.`), estritamente acionável, sem teoria ou divagação.
- **Graus de Liberdade**:
  - `[FRÁGIL]`: Tarefas sensíveis exigem comandos exatos, flags precisas e validação de pré-condições.
  - `[FLEXÍVEL]`: Tarefas adaptativas recebem heurísticas de decisão.

---

## 5. Workflows e Estratégia de Falha
- **Checklist Copiável**: Todo fluxo deve conter um bloco copiável com caixas de seleção (`- [ ] Passo X`).
- **Seção `## On Failure`** (obrigatória para skills que executam ações; ver seção 8):
  - **Gatilho de Erro**: Condição que dispara a falha.
  - **Ação Imediata**: Interrupção do processo para proteger o estado.
  - **Rollback**: Reversão transacional do que foi modificado.
  - **Fallback**: Notificação e rota alternativa.
  - **Logs**: Captura do stack trace completo e parâmetros.

---

## 6. Progressive Disclosure (Referências Técnicas)
- Se a skill contiver manuais detalhados, schemas extensos ou blocos de código/scripts que somem mais de 100 linhas:
  - Extraia esse conteúdo para um arquivo auxiliar `reference.md` na mesma pasta da skill (ou do domínio).
  - O arquivo `reference.md` DEVE iniciar com `## Table of Contents`.
  - O `SKILL.md` deve manter apenas um link de 1 nível de profundidade: `[Consulte a Referência Completa de Implementação](reference.md)`.

---

## 7. Estrutura de Diretórios
```
refactored_skills/
└── [dominio]/
    ├── SKILL.md                 # Roteador mestre do domínio
    ├── reference.md             # Referência arquitetural do domínio
    └── [gerund-skill-name]/
        ├── SKILL.md             # Habilidade atômica padronizada
        └── reference.md         # Código/templates > 100 linhas (quando aplicável)
```

---

## 8. Seções opcionais e skills de orientação
- Para skills que executam ações (comandos, chamadas de API, alterações de arquivos), recomenda-se declarar `Input/Output Signature`, `Imperative Execution Workflow` e `## On Failure`, com conteúdo derivado da própria skill.
- Skills de orientação (guias de estilo, checklists, referências de design, comunicação) mantêm o conteúdo real da fonte. Não devem receber essas seções genéricas: seção sem conteúdo específico reproduz o boilerplate da Fase 1.
- Requisitos que não se aplicam a uma skill não são exigidos dela. A checagem de conformidade é `scripts/validate_skills.py`, que reporta a contagem de skills sem essas seções como informação, não como erro.
- Corpos com mais de 100 linhas ficam em `reference.md` (seção 6). O `reference.md` começa com `## Table of Contents`, e o `SKILL.md` aponta para ele.
