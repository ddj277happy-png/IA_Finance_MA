# How to Maintain the Annotated Dossier

The site now works as a two-mode bilingual dossier:

- Default mode: `EN / FR`
- Switch mode: `AR / 中文`

The data still stores four languages so that the interface can switch pairs without losing information.

## Main Files

- `index.html`: layout, styling, bilingual rendering, search, and mode switching.
- `data/finance-knowledge.js`: all source, glossary, map, and context data.
- `references/sources.csv`: source inventory.
- `references/attachments/`: local archived PDFs or attachments.

## Add a New Source

1. Add the source metadata to `references/sources.csv`.
2. If the source should be archived locally, place the PDF in `references/attachments/`.
3. Add a matching object under `window.financeKnowledge.sources`.

Example:

```js
{
  meta: ["2026", "Institution", "Report"],
  title: "Report title",
  body: {
    en: "Why this source matters.",
    fr: "Pourquoi cette source compte.",
    ar: "لماذا يهم هذا المصدر.",
    zh: "这份资料为什么重要。"
  },
  url: "references/attachments/report.pdf",
  linkLabel: {
    en: "Open local PDF",
    fr: "Ouvrir le PDF local",
    ar: "فتح PDF المحلي",
    zh: "打开本地 PDF"
  }
}
```

## Add a New Concept

Add an object under `window.financeKnowledge.concepts`.

Valid categories:

- `banking`
- `risk`
- `capital`
- `new-finance`

Example:

```js
{
  id: "Credit guarantee",
  category: "banking",
  terms: {
    en: "Credit guarantee",
    fr: "Garantie de crédit",
    ar: "ضمان ائتماني",
    zh: "信用担保"
  },
  notes: {
    en: {
      plain: "A guarantor absorbs part of the loss if the borrower defaults.",
      use: "Useful for SME finance, development finance, and risk sharing."
    },
    fr: {
      plain: "Un garant absorbe une partie des pertes si l'emprunteur fait défaut.",
      use: "Utile pour le financement des PME, la finance de développement et le partage des risques."
    },
    ar: {
      plain: "يتحمل الضامن جزءا من الخسارة إذا تعثر المقترض.",
      use: "مفيد لفهم تمويل المقاولات الصغرى والمتوسطة وتمويل التنمية وتقاسم المخاطر."
    },
    zh: {
      plain: "担保方在借款人违约时承担部分损失。",
      use: "用于解释中小企业融资、发展金融和风险分担。"
    }
  }
}
```

## Add Context Cards

Use `mapCards` for high-level research map changes.

Use `primers` for contextual notes that help interpret sources.

Use `flowSteps` when the risk-transmission diagram needs a new step.

Each new item should provide `en`, `fr`, `ar`, and `zh` fields.
