# Platform publishing copies

These are publishing exports of the updated article, not confirmation that it has been posted. The full article uses the compliance-updated supplied content without prose changes. That exact draft is preserved in `../source/compliance-updated-article-supplied.md`. The prior revision remains in `../source/updated-article-supplied.md` for history.

## Shared formats

| Platform | Body copy | Title and cover |
| --- | --- | --- |
| Hashnode | `hashnode.md`, Markdown body with fenced code, inline links, and the evidence image | Enter `title.txt` separately; use `../media/hero.png` as the cover |
| Medium | Open `medium-linkedin-x.html`, select the body, and copy rendered text | Enter `title.txt` separately; upload the header near the top and choose it as the featured image |
| LinkedIn article | Same rendered body as Medium | Enter `title.txt` separately; upload `../media/hero.png` as the cover |
| X Article | Same rendered body, if the account has access to Articles | Enter `title.txt` separately; use `../media/hero.png` as the header |
| X thread | `x-thread.md`, one block per post | Attach the header to post 1 and the evidence illustration to post 5 |

`medium-linkedin-x.txt` is a plain-text fallback for all three rich-text editors. It retains full code examples and explicit source URLs, with an image insertion marker. It does not carry rich formatting.

## Copying and image placement

1. Open the HTML export in a browser. It is a readable publishing preview, not an exact replica of any platform.
2. Select the title with its button and paste it into the title field.
3. Select the article body with its button, then copy and paste normally to preserve available formatting. Do not paste the HTML source into the editor.
4. Upload the header separately as indicated above. It is outside the HTML body selection so it does not accidentally become a duplicate cover.
5. If the evidence image does not transfer, upload it immediately before the paragraph beginning “Illustration only:”. Keep that caption.
6. Review headings, links, images, code indentation, and placeholder angle brackets in the destination editor before publishing. Clipboard transfer has not been tested against signed-in editors. Use native code or quote formatting if needed; the plain-text fallback keeps the code intact.

The body-only Markdown has no duplicate article title or cover. The main `../article.md` remains the complete archive version with both images.

## Public media URLs

- Header: https://opiusai.github.io/articles/2026/10/004-your-llm-dashboard-says-success-show-us-the-evidence/media/hero.png
- Original 16:9 header: https://opiusai.github.io/articles/2026/10/004-your-llm-dashboard-says-success-show-us-the-evidence/media/hero-full-size.png
- Evidence image: https://opiusai.github.io/articles/2026/10/004-your-llm-dashboard-says-success-show-us-the-evidence/media/evidence-trail.png

## Format references

- [Medium story editor](https://help.medium.com/hc/en-us/articles/215194537-Using-the-story-editor)
- [LinkedIn article publishing](https://www.linkedin.com/help/linkedin/answer/a522427/publishing-articles-on-linkedin?lang=en)
- [Hashnode editor overview](https://docs.hashnode.com/blogs/editor/overview)
- [X Articles](https://help.x.com/en/using-x/articles), which require an eligible subscription or account

## Regenerate the full-article exports

Run `source/build-platform-versions.mjs` with Node.js and the `marked` package available. Alternatively set `INFEROCK_MARKED_MODULE` to an installed `marked` ESM module path. The script derives the full-article formats from `article.md`; it does not rewrite the prose or regenerate the separately condensed X thread.
