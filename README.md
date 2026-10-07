# Inferock Articles

This repository stores article sources, working files, metadata, and media. GitHub Pages publishes only files inside article `media/` directories.

## Archive layout

Articles use `articles/YYYY/MM/{id}-{slug}/`. The three digit ID follows the existing article sequence: Article 1 is `001`, and later articles receive the next available ID. Once media is published, keep its article directory path stable.

Each article uses `article.md` as its main text source, `article.docx` when available, `metadata.yaml`, and a `media/` directory for public assets. Supporting material that is not part of the public article belongs in `source/`.

Metadata uses `published` for platform URLs and `publication_status` for reported publishing outcomes. A null URL means no link has been supplied; refer to the status field to see whether the article was published. `publication_status_updated` records when the status was reported, not the publication date.

The Pages workflow copies only `media/` directories into its deployment artifact. Markdown, DOCX, metadata, and source files remain in the repository archive and are not deployed.

## Current article

- `articles/2026/09/001-why-ai-providers-shouldnt-grade-their-own-bills/`
- The month reflects the September 2026 source revision. No publication date or already published media URL was found in the supplied files.
- The Markdown and DOCX contain different text. Both are preserved; compare them before publishing a final version.

## Article 2

- `articles/2026/10/002-the-retry-worked-what-broke-the-first-time/`
- Published on DEV, Medium, Hashnode, Hugging Face, LinkedIn, and X, as confirmed by the user on October 5, 2026. Exact publication dates and URLs have not been supplied.

## Article 3

- `articles/2026/10/003-a-stream-can-start-finishing-is-another-matter/`
- User-supplied final article and its header image, archived in October 2026. Published on DEV, Medium, Hashnode, LinkedIn, and X, as confirmed by the user on October 5, 2026. Hugging Face publication was blocked for an unknown reason. Exact publication dates and URLs have not been supplied.

## Article 4

- `articles/2026/10/004-your-llm-dashboard-says-success-show-us-the-evidence/`
- Draft article following one tool call through Inferock Watch, Calls, and Proof, with a 5:2 header and an in-article evidence illustration. Article text remains in the archive; the images are served through GitHub Pages.
