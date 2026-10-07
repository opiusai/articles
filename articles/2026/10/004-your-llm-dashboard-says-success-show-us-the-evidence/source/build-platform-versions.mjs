import { readFile, writeFile, mkdir } from 'node:fs/promises';
import { dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

// Install marked locally or set INFEROCK_MARKED_MODULE to an available module path.
const { marked } = await import(process.env.INFEROCK_MARKED_MODULE || 'marked');
const articleDir = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const outDir = resolve(articleDir, 'platforms');
await mkdir(outDir, { recursive: true });
const source = await readFile(resolve(articleDir, 'article.md'), 'utf8');
const title = source.match(/^# (.+)$/m)[1];
const hero = source.match(/!\[Inferock article header[^\]]*\]\(([^)]+)\)/)[1];
const body = source.replace(/^# .+\n\n/, '').replace(/!\[Inferock article header[^\]]*\]\([^)]+\)\n\n/, '');
const escapeHtml = value => value.replaceAll('&', '&amp;').replaceAll('<', '&lt;').replaceAll('>', '&gt;').replaceAll('"', '&quot;');

function inline(tokens) {
  return tokens.map(token => {
    switch (token.type) {
      case 'text': return token.tokens ? inline(token.tokens) : token.text;
      case 'codespan': return token.text;
      case 'strong': case 'em': case 'del': return inline(token.tokens);
      case 'link': return `${inline(token.tokens)} (${token.href})`;
      case 'image': return `[Insert image: ${token.text}]\n${token.href}`;
      case 'br': return '\n';
      case 'escape': return token.text;
      default: throw new Error(`Unexpected inline token: ${token.type}`);
    }
  }).join('');
}

function plain(tokens) {
  return tokens.map(token => {
    switch (token.type) {
      case 'space': return '';
      case 'heading': case 'paragraph': case 'text': return inline(token.tokens || [{ type: 'text', text: token.text }]);
      case 'code': return token.text;
      case 'list': return token.items.map((item, index) => `${token.ordered ? `${Number(token.start) + index}.` : '•'} ${plain(item.tokens).trim()}`).join('\n\n');
      case 'blockquote': return plain(token.tokens);
      case 'hr': return '----------';
      default: throw new Error(`Unexpected block token: ${token.type}`);
    }
  }).filter(Boolean).join('\n\n');
}

const html = `<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>${escapeHtml(title)} | Publishing copy</title>
<style>
:root { color-scheme: light; }
* { box-sizing: border-box; }
body { margin: 0; background: #fff; color: #10162c; font: 18px/1.7 Georgia, serif; }
.tools { padding: 18px 24px; background: #f3f7ff; border-bottom: 1px solid #dbe5f7; font: 14px/1.5 system-ui, sans-serif; }
.tools p { max-width: 880px; margin: 0 auto 10px; }
.tools button { cursor: pointer; border: 1px solid #087bff; border-radius: 6px; padding: 9px 14px; background: #fff; color: #075aca; font: inherit; }
.tools .actions { max-width: 880px; margin: auto; }
main { max-width: 880px; margin: 48px auto; padding: 0 24px 60px; }
h1, h2 { font-family: system-ui, sans-serif; line-height: 1.2; letter-spacing: -.025em; }
h1 { font-size: 40px; margin: 0 0 30px; }
h2 { font-size: 28px; margin-top: 42px; }
p { margin: 0 0 22px; }
a { color: #096cd1; text-underline-offset: 3px; }
img { display: block; width: 100%; height: auto; margin: 28px 0; }
pre { padding: 18px 20px; background: #f6f8fc; border: 1px solid #e1e7f0; border-radius: 7px; overflow-x: auto; font: 14px/1.6 ui-monospace, monospace; }
code { font: .87em ui-monospace, monospace; }
li { margin: 10px 0; }
@media (max-width: 600px) { h1 { font-size: 30px; } h2 { font-size: 24px; } main { margin-top: 28px; } }
@media print { .tools { display: none; } main { max-width: none; } }
</style>
</head>
<body>
<aside class="tools">
<p>Shared full-article copy for Medium, LinkedIn, and X Articles. Enter the title separately and upload the header as the cover. Select the body below, then copy and paste as formatted text. This is a publishing preview, not an exact platform simulation.</p>
<p>Check pasted headings, links, and code examples in the destination editor. Upload the in-article image at its caption if it does not transfer. For plain-text paste, use the companion .txt file.</p>
<div class="actions"><button id="select-body">Select article body</button> <button id="select-title">Select title</button></div>
</aside>
<main>
<h1 id="article-title">${escapeHtml(title)}</h1>
<img src="${hero}" alt="Article cover image">
<article id="article-body">${marked.parse(body)}</article>
</main>
<script>
function selectElement(id) { const range = document.createRange(); range.selectNodeContents(document.getElementById(id)); const selection = window.getSelection(); selection.removeAllRanges(); selection.addRange(range); }
document.getElementById('select-body').addEventListener('click', () => selectElement('article-body'));
document.getElementById('select-title').addEventListener('click', () => selectElement('article-title'));
</script>
</body>
</html>
`;

await writeFile(resolve(outDir, 'medium-linkedin-x.html'), html);
await writeFile(resolve(outDir, 'medium-linkedin-x.txt'), `${title}\n\n${plain(marked.lexer(body))}\n`);
await writeFile(resolve(outDir, 'hashnode.md'), body);
await writeFile(resolve(outDir, 'title.txt'), `${title}\n`);
console.log('Generated shared rich-text preview, plain-text fallback, Hashnode Markdown body, and title.');
