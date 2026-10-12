---
name: animating-react-view-transitions
description: >
  Implements native-feeling animations with React's View Transition API (ViewTransition component, addTransitionType and CSS view-transition pseudo-elements), covering page and route transitions, shared elements, enter and exit animations, list reorder and directional navigation in Next.js. Use this skill when: adding page transitions, route change animations or shared element animations in React without third-party animation libraries. Do NOT use this skill when: animating decorative components (use animating-react-bits-components) or scroll-driven motion (use engineering-gsap-motion-uis).
---

# React View Transitions

Animate between UI states using the browser's native `document.startViewTransition`. Declare *what* with `<ViewTransition>`, trigger *when* with `startTransition` / `useDeferredValue` / `Suspense`, control *how* with CSS classes. Unsupported browsers skip animations gracefully.

## Sections
- When to Animate
- Availability
- Implementation Workflow
- Core Concepts
- Styling with View Transition Classes
- Transition Types
- Shared Element Transitions
- Common Patterns
- How Multiple VTs Interact
- Next.js Integration
- Accessibility
- Reference Files
- Full Compiled Document

## Reference Documentation
Consulte a documentação técnica completa: [Referência Técnica](reference.md).
