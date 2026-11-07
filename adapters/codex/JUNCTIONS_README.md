# Descoberta de Skills no Codex via Windows NTFS Junctions

## Contexto Técnico

No Windows, o Codex procura skills na pasta local do projeto `.agents/skills/<skill-name>/SKILL.md` ou na pasta global `~/.codex/skills/`.

Ao contrário de symlinks (`New-Item -ItemType SymbolicLink`), que exigem elevação administrativa (Developer Mode ou UAC elevado) no Windows, **Directory Junctions** (`mklink /J` no `cmd.exe`) possuem as seguintes vantagens críticas:
1. **Sem Elevação:** Podem ser criadas por usuários sem privilégios de administrador.
2. **Resolução Transparente no Kernel:** O driver do sistema de arquivos NTFS resolve junctions no nível do kernel (`IO_REPARSE_TAG_MOUNT_POINT`), de modo que aplicações rodando dentro de sandboxes ou subprocessos (como o Codex sandbox) enxergam a pasta como um diretório normal.
3. **Sem Duplicação de Arquivos:** As skills permanecem na fonte única de verdade (`refactored_skills/` ou `runtime/refactored_skills/`), eliminando a necessidade de 150 wrappers estáticos.

## Descoberta no Codex: Exigência de Depth 1

O scanner do OpenAI Codex procura skills exclusivamente no primeiro nível de profundidade sob o diretório `.agents/skills/`, na estrutura:
`.agents/skills/<skill-name>/SKILL.md`

Criar uma junction para a pasta de domínio inteira (`.agents/skills/frontend`) aninha as skills no segundo nível (`.agents/skills/frontend/<skill-name>/SKILL.md`), tornando-as invisíveis ao Codex.

Portanto, as **Directory Junctions devem ser criadas por skill individual**.

## Como Criar Junctions Individuais

### Via Skill Hub CLI (Recomendado)
O comando `link-junctions` cria automaticamente as junctions individuais para todas as skills de um domínio (ou para uma skill específica):

```cmd
:: Criar junctions individuais para todas as skills do domínio frontend
python "%USERPROFILE%\.lay-skills\runtime\scripts\skill_hub.py" link-junctions --workspace "CAMINHO_DO_PROJETO" --domain frontend

:: Ou para uma skill específica
python "%USERPROFILE%\.lay-skills\runtime\scripts\skill_hub.py" link-junctions --workspace "CAMINHO_DO_PROJETO" --skill elevating-frontend-taste
```

### Manualmente via `cmd.exe`
```cmd
cmd /c mklink /J ".agents\skills\elevating-frontend-taste" "%USERPROFILE%\.lay-skills\runtime\refactored_skills\frontend\elevating-frontend-taste"
```

## Como Remover Junctions com Segurança

Para remover uma Directory Junction sem apagar os arquivos da fonte:
```cmd
cmd /c rmdir ".agents\skills\elevating-frontend-taste"
```
*Atenção:* Nunca use comandos recursivos com flags de força como `rmdir /s /q` ou `Remove-Item -Recurse` no PowerShell sobre junctions, pois versões legadas podem tentar deletar os arquivos dentro da pasta de destino.
