#!/usr/bin/env python3
"""Generate localized case collections from the public data and locale files."""
import argparse, html, json, pathlib, urllib.parse
ROOT=pathlib.Path(__file__).resolve().parents[1]
LANGS=[('en','English','README.md'),('es','Español','README_es.md'),('pt','Português','README_pt.md'),('ja','日本語','README_ja.md'),('ko','한국어','README_ko.md'),('de','Deutsch','README_de.md'),('fr','Français','README_fr.md'),('tr','Türkçe','README_tr.md'),('zh-TW','繁體中文','README_zh-TW.md'),('zh-CN','简体中文','README_zh-CN.md'),('ru','Русский','README_ru.md')]
CATEGORIES=[('mechanical','⚙️'),('worlds','🏞️'),('svg','🎨'),('games','🎮'),('web','🖥️'),('comparison','🔬')]
COLORS=['111111','ffb703','2a9d8f','52b788','4ea8de','f4a261','e76f51','d62828','8338ec','ef476f','577590']
BADGES='\n'.join(f'[![{name}](https://img.shields.io/badge/{urllib.parse.quote(name)}-{color})]({filename})' for (_,name,filename),color in zip(LANGS,COLORS))
def render(data,locale):
 g=locale['copy'];cases=data['cases'];translations=locale['cases']
 if len(cases)!=len(translations):raise ValueError('Locale/case count mismatch')
 chunks=['<div align="center">\n\n<a href="https://evolink.ai?utm_source=github&amp;utm_medium=banner&amp;utm_campaign=kimi-k3-1-usecases&amp;utm_content=readme_banner"><img src="'+data['banner_url']+'" alt="Awesome Kimi K3.1 Use Cases" width="760"></a>\n\n[![License: CC BY 4.0](https://img.shields.io/badge/License-CC_BY_4.0-lightgrey.svg)](LICENSE)\n\n'+BADGES+'\n\n</div>\n',f'## 🍌 {g["introduction"]}\n\n{g["intro"]}\n\n**{g["purpose"]}**\n',f'<a id="overview"></a>\n## 📊 {g["overview"]}\n\n{g["stats"]}\n\n> [!NOTE]\n> {g["evidence"]}\n',f'<a id="quick-start"></a>\n## ⚡ {g["quick_start"]}\n\n{g["steps"]}\n\n[{g["official"]}](https://www.kimi.com/)\n',f'<a id="menu"></a>\n## 📑 {g["menu"]}\n\n| {g["case"]} | {g["category"]} | {g["type"]} |\n|---|---|---|']
 for c,t in zip(cases,translations):chunks.append(f'| [{c["number"]}. {t[0]}](#case-{c["number"]}) | {g["categories"][c["category"]]} | {c["type"]} |')
 chunks.append(f'| [{g["overview"]}](#overview) | {g["overview"]} | |\n| [{g["quick_start"]}](#quick-start) | {g["quick_start"]} | |\n| [{g["related"]}](#related-repositories) | {g["related"]} | |\n| [{g["acknowledge"]}](#acknowledge) | {g["acknowledge"]} | |\n')
 for category,emoji in CATEGORIES:
  group=[(c,t) for c,t in zip(cases,translations) if c['category']==category]
  if not group:continue
  chunks.append(f'<a id="{category}"></a>\n## {emoji} {g["categories"][category]}\n')
  for c,t in group:
   chunks.append(f'<a id="case-{c["number"]}"></a>\n### {g["case"]} {c["number"]}: [{t[0]}]({c["source_url"]}) ({g["by"]} [@{c["author_handle"]}]({c["author_url"]}))\n\n**{t[1]}**\n\n{t[2]}\n')
   if c.get('related_sources'):
    chunks.append(g['additional']+' '+', '.join(f'[@{s["author_handle"]}]({s["source_url"]})' for s in c['related_sources'])+'\n')
   cells=[]
   for i,m in enumerate(c['media'],1):
    dest=m['playable_url'] if m['type']=='video' else m['image_url'];poster=m['poster_url'] if m['type']=='video' else m['image_url'];label=g['video'] if m['type']=='video' else g['image'];alt=html.escape(f'{t[0]} — {i}',quote=True)
    cells.append(f'<td align="center"><a href="{html.escape(dest,quote=True)}"><img src="{html.escape(poster,quote=True)}" alt="{alt}" width="480"></a><br>{label}'+(f'<br>{html.escape(m["display_label"])}' if m.get('display_label') else '')+'</td>')
   for start in range(0,len(cells),2):chunks.append('<table><tr>'+''.join(cells[start:start+2])+'</tr></table>\n')
   chunks.append(f'{g["type"]}: {c["type"]} | {g["date"]}: {c["date"]}\n\n---\n')
 chunks.append(f'<a id="related-repositories"></a>\n## {g["related"]}\n\n- [{g["open_related"].format(model="Kimi K3")}](https://github.com/Evolink-AI/awesome-kimi-k3-usecases)\n- [{g["open_related"].format(model="Gemini 4 Carbon")}](https://github.com/cheercheung/awesome-gemini-4-carbon-guide-and-use-cases)\n')
 authors=list(dict.fromkeys((c['author_handle'],c['author_url']) for c in cases))
 for c in cases:
  for s in c.get('related_sources',[]):
   pair=(s['author_handle'],f'https://x.com/{s["author_handle"]}')
   if pair not in authors:authors.append(pair)
 chunks.append(f'<a id="acknowledge"></a>\n## 🙏 {g["acknowledge"]}\n\n{g["thanks"]}\n\n'+', '.join(f'[@{handle}]({url})' for handle,url in authors)+f'\n\n{g["corrections"]}\n')
 return '\n'.join(chunks).rstrip()+'\n'
def main():
 p=argparse.ArgumentParser();p.add_argument('--english-only',action='store_true');p.add_argument('--check',action='store_true');a=p.parse_args();data=json.loads((ROOT/'data/kimi-k3-1-usecase-curated.json').read_text());errors=[]
 for code,_,filename in LANGS:
  if a.english_only and code!='en':continue
  locale=json.loads((ROOT/f'data/locales/{code}.json').read_text());out=render(data,locale);path=ROOT/filename
  if a.check:
   if not path.is_file() or path.read_text()!=out:errors.append(filename)
  else:path.write_text(out)
 catalog='# Update Log and Curated Case Register\n\n## 2026-10-23\n\n40 independent works across six categories; 54 retained media assets. Reposts and comparisons remain attached to their underlying work.\n\nThis generated Markdown register mirrors the canonical JSON. Dates use the UTC publication date of each primary source.\n\n| Case | Work | Creator | Category | Type | Date |\n|---|---|---|---|---|---|\n'
 for c in data['cases']:catalog+=f'| {c["number"]} | [{c["title"]}]({c["source_url"]}) | [@{c["author_handle"]}]({c["author_url"]}) | {c["category"]} | {c["type"]} | {c["date"]} |\n'
 catalog_path=ROOT/'docs/update-log.md'
 if a.check:
  if not catalog_path.is_file() or catalog_path.read_text()!=catalog:errors.append('docs/update-log.md')
 else:catalog_path.write_text(catalog)
 if errors:raise SystemExit('Generated README drift: '+', '.join(errors))
 print('README generation check passed' if a.check else 'README files generated')
if __name__=='__main__':main()
