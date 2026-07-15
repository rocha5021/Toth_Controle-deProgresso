"""
Resolve imagens reais da TibiaWiki Brasil (tibiawiki.com.br) para
criaturas, itens, charms e bosses - por link direto (sem download).

Descoberta: a pagina 'Especial:FilePath/<Arquivo>' redireciona pro
arquivo estatico real (ex: /images/9/9c/Amazon.gif) e esse caminho
/images/ NAO fica atras do desafio Cloudflare que protege o resto do
site. Entao da pra resolver isso com requests simples, sem precisar
de navegador headless, para milhares de nomes rapidamente.
"""
import re
import time
import urllib.parse
import urllib.request

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) EK-Management-System/1.0"
FILEPATH_BASE = "https://www.tibiawiki.com.br/wiki/Especial:FilePath/"

_ROMAN_SUFFIX_RE = re.compile(r"\s+(I{1,3}|IV|V)$")


def _candidates_for(name, kind):
    base = name.strip()
    variants = [base]

    no_roman = _ROMAN_SUFFIX_RE.sub("", base)
    if no_roman != base:
        variants.append(no_roman)

    if kind == "charm":
        # charms usam o icone "<Nome sem numeral romano>_Icon.gif"
        variants = [f"{no_roman} Icon", f"{base} Icon"]

    if "'" in base:
        variants.append(base.replace("'s", "").replace("'", ""))

    seen = set()
    out = []
    for v in variants:
        if v not in seen:
            seen.add(v)
            out.append(v)
    return out


def _try_url(filename, ext):
    enc = urllib.parse.quote(filename.replace(" ", "_") + "." + ext)
    url = FILEPATH_BASE + enc
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    try:
        with urllib.request.urlopen(req, timeout=8) as resp:
            if resp.status == 200:
                return resp.geturl()
    except Exception:
        return None
    return None


def resolve_image(name, kind="creature"):
    """kind: 'creature' | 'boss' | 'charm' | 'item'"""
    for cand in _candidates_for(name, kind):
        for ext in ("gif", "png"):
            url = _try_url(cand, ext)
            if url:
                return url
    return None


def resolve_many(names, kind="creature", pause=0.02, progress=None):
    """names: lista de strings. Retorna dict {nome: url_ou_None}."""
    out = {}
    for i, n in enumerate(names):
        out[n] = resolve_image(n, kind)
        if progress and i % 25 == 0:
            progress(i, len(names))
        time.sleep(pause)
    return out
