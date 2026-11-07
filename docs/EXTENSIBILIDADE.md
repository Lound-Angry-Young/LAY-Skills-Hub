# Guia Operacional de Extensibilidade: Skills e Agentes

Este documento estabelece o protocolo operacional obrigatório para qualquer LLM ou mantenedor que adicione, atualize, refatore ou desative skills e agentes no **LAY Skills Hub 2.0**.

---

## 1. Princípios Arquiteturais e Fonte Única da Verdade (SSOT)

O ecossistema LAY Skills Hub é centrado em portabilidade, neutralidade e extensibilidade contínua:

- **SSOT de Perfis e Agentes:** `core/perfis.json` define autoritativamente os 11 domínios canônicos, descrições, ferramentas aprovadas e salvaguardas. O arquivo `agents/perfis.json` é um espelho sincronizado para ferramentas legadas.
- **SSOT de Skills Públicas:** `refactored_skills/<dominio>/<nome-da-skill>/SKILL.md`. Versionado no Git, distribuído publicamente.
- **SSOT de Skills Privadas:** `skills-privadas-lay/refactored/<dominio>/<nome-da-skill>/SKILL.md`. Cofre local seguro, ignorado pelo Git (`.gitignore`).
- **Templates Canônicos de Adaptadores:** `adapters/` armazena os templates para cada cliente suportado:
  - `adapters/claude/`: agentes especialistas (`agents/*.md`), árbitro Opus e regras globais (`CLAUDE.md`).
  - `adapters/codex/`: regras globais (`AGENTS.md`) e perfis de execução Sol, Terra e Luna (`*.config.toml`).
  - `adapters/antigravity/`: manifestos de skills (`manifests/*.json`), template de subagentes nativos (`agents/subagents-definition-template.json`) e regras globais (`GEMINI.md`).

---

## 2. Fluxo Operacional em 10 Etapas

Ao receber uma nova skill, repositório externo, pasta ou funcionalidade, siga rigorosamente este fluxo:

```
[1. Inspecionar] ──> [2. Mapear Domínio] ──> [3. Desduplicar] ──> [4. Validar Padrão]
                                                                        │
[8. Regenerar] <── [7. Mapear SSOT] <── [6. Integrar] <── [5. Classificar Escopo]
      │
      └──> [9. Testar Suíte] ──> [10. Dry-Run / Instalar]
```

### Etapa 1: Inspecionar Fonte e Conteúdo
- Examine a licença, autor, dependências externas e propósito técnico da skill proposta.
- Rejeite ou adapte dependências de modelos ou provedores externos proprietários não autorizados.

### Etapa 2: Mapear Domínio e Agente Consumidor
- Identifique a qual dos 11 domínios canônicos a skill pertence:
  - `routing-and-proxy` (`lay-omniroute`): roteamento, gateway local, logs de uso.
  - `frontend` (`lay-frontend`): React, Next.js, motion, anti-slop, UI.
  - `engineering` (`lay-engenharia`): arquitetura, APIs, refatoração, observabilidade.
  - `context` (`lay-contexto`): grafos Graphify, compressão, quebra de tarefas.
  - `devops` (`lay-devops`): git, commits semânticos, CI/CD, releases.
  - `qa` (`lay-qa`): testes, TDD, Playwright, conformidade de componentes.
  - `security` (`lay-seguranca`): análise estática, hardening, auditoria CVE/Semgrep.
  - `creative-3d` (`lay-3d`): Blender MCP, WebGL, shaders, renderização local.
  - `documentation` (`lay-documentacao`): escrita técnica, ADRs, estilo sem marcas de IA.
  - `design` (`lay-design`): identidade visual, brandkit, moodboards, mockups.
  - `database` (`lay-banco-de-dados`): esquemas de banco, integridade, planos de migração.
- Consulte a distribuição atual executando:
  ```powershell
  python scripts/nova_skill.py dominios
  ```

### Etapa 3: Desduplicar e Verificar Conflitos
- Busque no catálogo existente por palavras-chave para evitar duplicar capacidades:
  ```powershell
  python scripts/skill_hub.py search "<termo>"
  ```
- Se já existir skill equivalente ou superior, refatore a existente em vez de duplicar.

### Etapa 4: Validar Padrão Estrito de Skill
Toda skill deve atender aos requisitos de `docs/PADRAO_DE_SKILLS.md`:
- **Nome:** em gerúndio (`action-verb-ing`, máx. 64 caracteres), letras minúsculas e hífens.
- **Descrição:** máx. 1024 caracteres, em 3ª pessoa, com fronteiras explícitas:
  - `Use this skill when:`
  - `Do NOT use this skill when:`
- **Estrutura:** `SKILL.md` obrigatório com título `# <nome>`, objetivo, `## Imperative Execution Workflow` (com marcadores `[FRÁGIL]` ou `[FLEXÍVEL]`), checklist copiável `- [ ]` e seção `## On Failure`.

### Etapa 5: Classificar Escopo (Público vs. Privado)
- **Público:** código genérico, bibliotecas abertas, padrões reutilizáveis (`refactored_skills/`).
- **Privado:** regras de marca LAY, configurações de hardware específicas da máquina local, dados sensíveis (`skills-privadas-lay/refactored/`). Utilize o argumento `--privada`.

### Etapa 6: Integrar Skill e Roteadores
Adicione a nova skill utilizando o script canônico `scripts/nova_skill.py`:
- Para uma skill individual:
  ```powershell
  python scripts/nova_skill.py nova <nome-gerundio> --dominio <dominio> --descricao "<texto com gatilhos>" [--corpo <arquivo.md>] [--privada]
  ```
- Para um lote de skills organizadas em `<pasta>/<dominio>/<nome>/SKILL.md`:
  ```powershell
  python scripts/nova_skill.py lote <pasta> [--privada]
  ```
*Nota: `nova_skill.py` atualiza automaticamente as tabelas de roteamento (`SKILL.md` e `reference.md` da pasta do domínio).*

### Etapa 7: Mapear no SSOT (`core/perfis.json`)
- Se a skill demandar ferramentas adicionais ou pertencer a um novo perfil, atualize `core/perfis.json` (respeitando salvaguardas e perfis somente-leitura como `lay-contexto`, `lay-seguranca` e `lay-banco-de-dados`).
- Sincronize `agents/perfis.json` caso necessário.

### Etapa 8: Regenerar Catálogo e Adaptadores Multicliente
Execute a regeneração canônica:
```powershell
python scripts/build_agents.py
```
Isso recalcula e sincroniza de forma determinística:
1. `.claude/agents/*.md` e documentação de subagentes em `agents/`.
2. `adapters/claude/agents/<nome>.md`: atualiza o bloco `## Skills do domínio` sem alterar frontmatter, modelo (`sonnet`, `opus`), ferramentas ou salvaguardas de RESULT.
3. `adapters/antigravity/manifests/*.json`: sincroniza `skills-frontend.json`, `skills-engineering.json` e `skills-full.json`.
4. `adapters/antigravity/agents/subagents-definition-template.json`: sincroniza o `SystemPrompt` dos subagentes nativos.
5. Catálogo público e documentação (`catalog/skills.json` e `docs/CATALOGO.md`) via `python scripts/skill_hub.py catalog`.

### Etapa 9: Executar Testes Automatizados
Valide a integridade funcional do repositório:
```powershell
python -m unittest tests/test_portable_installer.py
python -m unittest tests/test_extensibility_e2e.py
```
Todos os testes devem passar com `OK`.

### Etapa 10: Dry-Run e Instalação nos Ambientes Alvo
- Simule a instalação sem alterar o sistema:
  ```powershell
  python scripts/skill_hub.py install --agents all --mode public --dry-run
  ```
- Quando aprovado, instale no ambiente local:
  ```powershell
  python scripts/skill_hub.py install --agents all
  ```

---

## 3. Descoberta de Skills por Cliente

| Cliente | Mecanismo de Descoberta | Como uma nova skill é descoberta |
|---|---|---|
| **Claude Code** | `~/.claude/agents/<nome>.md` | O subagente do domínio contém o caminho do `SKILL.md` no bloco `## Skills do domínio`. Atualizado via `build_agents.py` e `skill_hub.py install`. |
| **OpenAI Codex** | `.agents/skills/<skill>/SKILL.md` (depth=1) | Descoberta dinâmica via junctions NTFS no workspace. O comando `python scripts/skill_hub.py link-junctions --workspace <dir> --domain <dominio>` cria junctions para todas as skills do domínio automaticamente. |
| **Google Antigravity** | `.gemini/config/skills.json` e subagentes | Manifestos de inclusão apontam para os diretórios de runtime. Subagentes nativos consultam a lista conceitual em seu `SystemPrompt`. |

---

## 4. Atualização, Refatoração e Deprecação

### Atualizar uma Skill Existente
1. Edite diretamente o arquivo `refactored_skills/<dominio>/<nome>/SKILL.md`.
2. Execute a validação estrita:
   ```powershell
   python scripts/validate_skills.py
   ```
3. Se a descrição foi alterada, execute `python scripts/build_agents.py` para sincronizar os adaptadores.

### Deprecar ou Remover uma Skill
1. Remova a pasta `refactored_skills/<dominio>/<nome>/`.
2. Remova a linha correspondente das tabelas de roteamento em `refactored_skills/<dominio>/SKILL.md` e `reference.md`.
3. Execute `python scripts/build_agents.py` e `python scripts/skill_hub.py catalog`.
4. Execute os testes automatizados para certificar a consistência do ecossistema.
