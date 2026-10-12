/**
 * Template de configuração do lint-staged para novos projetos.
 * Salve como: lint-staged.config.mjs
 * 
 * NOTA DE ENGENHARIA WINDOWS:
 * Muitos arquivos de uma vez estouram o limite de linha de comando do Windows (cmd.exe buffer de ~8 KB).
 * Acima de 30 arquivos alterados em um único commit, o script roda no projeto inteiro em vez de listar cada caminho.
 */

const MAX = 30;
const quote = (files) => files.map((f) => JSON.stringify(f)).join(" ");

const config = {
  "*.{ts,tsx,mts}": (files) =>
    files.length > MAX
      ? ["eslint --fix --max-warnings=0 .", "prettier --write src e2e"]
      : [`eslint --fix --max-warnings=0 ${quote(files)}`, `prettier --write ${quote(files)}`],
  "*.{css,json,md,mjs}": (files) =>
    files.length > MAX ? "prettier --write ." : `prettier --write ${quote(files)}`,
};

export default config;
