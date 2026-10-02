# Inferock Articles

This repository stores article sources, working files, metadata, and media. GitHub Pages publishes only files inside article `media/` directories.

## Archive layout

Articles use `articles/YYYY/MM/{id}-{slug}/`. The three digit ID follows the existing article sequence: Article 1 is `001`, and later articles receive the next available ID. Once media is published, keep its article directory path stable.

Each article uses `article.md` as its main text source, `article.docx` when available, `metadata.yaml`, and a `media/` directory for public assets. Supporting material that is not part of the public article belongs in `source/`.

The Pages workflow copies only `media/` directories into its deployment artifact. Markdown, DOCX, metadata, and source files remain in the repository archive and are not deployed.

## Current article

- `articles/2026/09/001-why-ai-providers-shouldnt-grade-their-own-bills/`
- The month reflects the September 2026 source revision. No publication date or already published media URL was found in the supplied files.
- The Markdown and DOCX contain different text. Both are preserved; compare them before publishing a final version.

## Article 2

- `articles/2026/10/002-the-retry-worked-what-broke-the-first-time/`
- The archive month reflects its October 2026 draft and visual assets; no publication date or external publication URL has been provided.
