---
name: integrating-creative-web-toolkits
description: >
  Installs, integrates and configures creative web libraries, WebGL shaders, physics engines and canvas animations with hardware-aware fallbacks and performance boundaries. Use this skill when: a creative library is already selected and must be wired into a web application. Do NOT use this skill when: choosing which library to use (use selecting-creative-libraries) or applying Vanta.js specifically (use rendering-vanta-backgrounds).
---

# Integração de Toolkits Criativos Web e Shaders

Instala e integra bibliotecas criativas web (Three.js, Pixi.js, Matter.js, Howler, GSAP, WebGL Shaders) garantindo ciclo de vida de renderização, limpeza de memória em desmontagem e fallbacks performáticos.

## Input/Output Signature
Input:
- toolkitName: string # Nome da biblioteca ou framework (three, pixi.js, matter-js, gsap)
- componentFilePath: string # Arquivo do componente onde o toolkit será integrado
- packageManager: string # Gerenciador de pacotes (npm, pnpm, yarn, bun)
- enableReducedMotionFallback: boolean # Se deve prover alternativa estática ou simplificada (default: true)
Output:
- integrationSuccess: boolean # Status da integração
- installedPackages: array # Lista de pacotes e tipagens instalados
- lifecycleCleaned: boolean # Confirmação de que listeners e canvas contexts são destruídos
- executionLog: string # Registro de comandos e validações executadas

## Router and Selection Matrix
| Toolkit / Biblioteca | Padrão de Integração Recomendado | Grau de Liberdade |
|---|---|---|
| Three.js / WebGL 3D | Encapsula cena em canvas isolado com hook de cleanup para geometrias e texturas | [FRÁGIL] Exige descarte explícito de texturas e buffers para evitar leak |
| Shaders GLSL Customizados | Carrega fragment e vertex shaders com uniform de delta time e resolução | [FRÁGIL] Requer compilação condicional e tratamento de erros de shader |
| Física 2D (Matter.js) | Vincula motor de física a um loop desacoplado do repaint da UI principal | [FLEXÍVEL] Ajusta precisão de iterações de física conforme taxa de frames |
| Animação SVG / Canvas (GSAP) | Registra plugins necessários e sincroniza com o ciclo de vida do componente | [FLEXÍVEL] Utiliza `gsap.context()` para limpeza automática de timelines |

## Imperative Execution Workflow
1. Instalar Pacotes e Tipagens TypeScript [FRÁGIL]:
   - Adicione o toolkit e suas declarações de tipos (ex: `three` e `@types/three`) utilizando o gerenciador de pacotes do projeto.
2. Criar Contêiner de Renderização e Referência de Canvas [FRÁGIL]:
   - Aloque elemento `<canvas>` ou `<div>` com referência imutável (`useRef`) e escopo isolado de estilização.
3. Implementar Inicialização e Loop de Animação [FLEXÍVEL]:
   - Configure renderizador, câmera e cena disparando o loop via `requestAnimationFrame` condicionado à visibilidade da aba.
4. Implementar Tratamento de Desmontagem e Cleanup [FRÁGIL]:
   - No retorno do ciclo de vida do componente, descarte geometries, materials, listeners de resize e cancele o frame loop.
5. Inserir Fallback de Acessibilidade e Baixo Desempenho [FRÁGIL]:
   - Verifique `prefers-reduced-motion` e limite a taxa de quadros ou apresente captura estática em hardware limitado.

## Execution Checklist
- [ ] Instalar pacotes de produção e suas respectivas tipagens
- [ ] Configurar elemento canvas com isolamento de estilos
- [ ] Implementar loop de renderização com controle de FPS
- [ ] Garantir destruição de buffers, materiais e event listeners no cleanup
- [ ] Tratar `prefers-reduced-motion` e queda de framerate

## On Failure
- **Gatilho de Erro**: Vazamento de memória (GPU Context Lost), erro de compilação de shader GLSL ou incompatibilidade de versão do bundler.
- **Ação Imediata**: Pausar a renderização do canvas e exibir fallback estático na interface.
- **Rollback**: Remover imports adicionados e reverter o arquivo de componente ao estado estável.
- **Fallback**: Substituir componente interativo 3D por imagem estática pré-renderizada ou animação CSS leve.
- **Logs**: Registrar log de compilação do WebGL, stack trace do componente e mensagens de aviso do console.

## Reference Documentation
Consulte a documentação técnica completa: [Referência Técnica](reference.md).
