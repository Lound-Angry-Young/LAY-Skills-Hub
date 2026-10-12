# Internacionalização Leve (i18n) e Arquitetura de Design Tokens

> **Objetivo:** Estabelecer uma arquitetura de internacionalização (i18n) com tipagem estrita e reatividade garantida no DOM sem bibliotecas pesadas de terceiros, aliada a um sistema de Design Tokens nativos via CSS Modules.

---

## 1. Internacionalização Reativa Zero-Dependência

Muitas bibliotecas de i18n adicionam sobrecarga de hidratação e wrappers complexos que quebram o React 19 Server Components. Uma abordagem limpa e direta garante 100% de controle:

### Estrutura de Arquivos

```
src/
├── locales/
│   ├── pt-BR.json      # Dicionário primário de strings
│   └── en.json         # Dicionário traduzido par
└── lib/
    ├── i18n.ts         # Tipos estritos baseados na estrutura do JSON e função t()
    └── store.ts        # Estado reativo do idioma atual (ex: 'pt-BR' | 'en')
```

### Exemplo de Implementação (`src/lib/i18n.ts`)

```typescript
import ptBR from "@/locales/pt-BR.json";
import en from "@/locales/en.json";

export type Locale = "pt-BR" | "en";
export type TranslationSchema = typeof ptBR;

const dictionaries: Record<Locale, TranslationSchema> = {
  "pt-BR": ptBR,
  "en": en,
};

/**
 * Recupera uma string de tradução navegando pela árvore com segurança de chave.
 */
export function getTranslation(locale: Locale): TranslationSchema {
  return dictionaries[locale] ?? dictionaries["pt-BR"];
}
```

### A Regra Crítica de Reatividade de i18n

Ao utilizar animações de separação de caracteres (como GSAP `SplitText` ou `ScrambleText`), elementos mutados no DOM podem não reagir à troca de idioma no React.
- **Solução:** Adicione a propriedade `key={locale}` no elemento container que abriga textos traduzidos:
  ```tsx
  <div key={locale} className={styles.heroText}>
    <h1>{t.hero.title}</h1>
  </div>
  ```
  Isso força o React a remontar limpo o nó de texto com a nova linguagem, destruindo mutações residuais da biblioteca de animação.

---

## 2. Sistema de Design Tokens CSS Nativos

Para evitar dependência de frameworks utilitários volumosos que padronizam a estética de forma genérica (como Tailwind), adote **Design Tokens em CSS puro**:

### Arquivo `src/styles/tokens.css`

```css
:root {
  /* 1. Base Tipográfica Decimal: 1rem = 10px */
  font-size: 62.5%;

  /* 2. Escala de Espaçamento Base-8 */
  --space-05: 4px;
  --space-1: 8px;
  --space-2: 16px;
  --space-3: 24px;
  --space-4: 32px;
  --space-6: 48px;
  --space-8: 64px;
  --space-12: 96px;

  /* 3. Paleta de Cores e Superfícies */
  --color-bg: #faf5e9;
  --color-surface: #242424;
  --color-primary: #fff201;
  --color-accent: #ff3eb5;
  --color-danger: #c21818;
  --color-text: #000000;
  --color-text-muted: #666666;

  /* 4. Curvas de Easing (Mecânica e Tensão) */
  --ease-snap: cubic-bezier(0.2, 0, 0, 1);
  --ease-punch: cubic-bezier(0.34, 1.56, 0.64, 1);
  --ease-drift: cubic-bezier(0.16, 1, 0.3, 1);

  /* 5. Sombras Sólidas */
  --shadow-solid-sm: 2px 2px 0 #000000;
  --shadow-solid-md: 4px 4px 0 #000000;
  --shadow-solid-lg: 6px 8px 0 var(--color-accent);
}
```

### Encapsulamento com CSS Modules

Todo componente React deve ser acompanhado de seu respectivo arquivo `.module.css`:

```typescript
// Button.tsx
import styles from "./Button.module.css";

export function Button({ children, onClick }: ButtonProps) {
  return (
    <button className={styles.btn} onClick={onClick}>
      {children}
    </button>
  );
}
```

```css
/* Button.module.css */
.btn {
  padding: var(--space-1) var(--space-3);
  font-size: 1.4rem;
  font-weight: 700;
  background: var(--color-primary);
  border: 2px solid #000;
  box-shadow: var(--shadow-solid-md);
  cursor: pointer;
  transition: transform 0.1s var(--ease-snap), box-shadow 0.1s var(--ease-snap);
}

.btn:hover {
  transform: translate(-2px, -2px);
  box-shadow: 6px 6px 0 #000;
}

.btn:active {
  transform: translate(2px, 2px);
  box-shadow: 2px 2px 0 #000;
}
```
