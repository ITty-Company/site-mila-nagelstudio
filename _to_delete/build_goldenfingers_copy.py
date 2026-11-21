#!/usr/bin/env python3
"""Generates the static HTML pages of golden-fingers (shared header/footer/finale/transition)."""
import json, html
from pathlib import Path
OUT = Path('/home/claude/site/golden-fingers')

TEL = 'tel:+31687862666'; TELT = '06 87 86 26 66'
IG = 'https://www.instagram.com/golden_fingers_waalwijk/'
WA = 'https://wa.me/31687862666'
ROUTE = 'https://www.google.com/maps/search/?api=1&amp;query=Grotestraat+223+5141+Waalwijk'
BOEK = 'afspraak.html'

I = {
 'tel': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 4h3.5l1.6 4.2-2.2 1.4a11 11 0 0 0 6.5 6.5l1.4-2.2L20 15.5V19a1.5 1.5 0 0 1-1.6 1.5C10.6 20 4 13.4 3.5 5.6A1.5 1.5 0 0 1 5 4z"/></svg>',
 'pin': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" aria-hidden="true"><path d="M12 21s-7-6.2-7-11.5A7 7 0 0 1 19 9.5C19 14.8 12 21 12 21z"/><circle cx="12" cy="9.5" r="2.5"/></svg>',
 'ig': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" aria-hidden="true"><rect x="3.5" y="3.5" width="17" height="17" rx="5"/><circle cx="12" cy="12" r="3.8"/><circle cx="17.2" cy="6.8" r=".9" fill="currentColor" stroke="none"/></svg>',
 'cal': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" aria-hidden="true"><rect x="3.5" y="5" width="17" height="15.5" rx="3"/><path d="M3.5 10h17M8 3v4M16 3v4"/></svg>',
 'wa': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linejoin="round" aria-hidden="true"><path d="M4 19.5l1.3-3.8A8 8 0 1 1 8.6 19z"/></svg>',
 'scissors': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" aria-hidden="true"><circle cx="6" cy="7" r="2.6"/><circle cx="6" cy="17" r="2.6"/><path d="M8.2 8.4 20 17M8.2 15.6 20 7"/></svg>',
 'clock': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" aria-hidden="true"><circle cx="12" cy="12" r="8.5"/><path d="M12 7.5V12l3 2"/></svg>',
}

def btn(href, label, kind='', icon=None, ext=False):
    cls = 'btn' + (' ' + kind if kind else '')
    ic = I[icon] if icon else ''
    t = ' target="_blank" rel="noopener"' if ext else ''
    return f'<a class="{cls}" href="{href}"{t}>{ic}{label}</a>'

B_BOEK = lambda label='Plan je afspraak', kind='': btn(BOEK, label, kind, 'cal')
B_TEL = lambda kind='ghost': btn(TEL, f'Bel {TELT}', kind, 'tel')
B_ROUTE = lambda kind='ghost': btn(ROUTE, 'Route plannen', kind, 'pin', True)
B_IG = lambda label='Instagram', kind='ghost': btn(IG, label, kind, 'ig', True)
B_WA = lambda: f'<span class="wa-wrap">{btn(WA, "WhatsApp", "ghost", "wa", True)}<span class="wa-note">nog te bevestigen</span></span>'

PRE = ("<script>document.documentElement.classList.add('js');try{var d=JSON.parse(sessionStorage.getItem('paal')||'null');"
       "if(d){sessionStorage.removeItem('paal');var c=document.documentElement.classList;c.add('pl-closed','pl-noanim');if(d.b)c.add('pl-back');"
       "window.__pl=d.l;setTimeout(function(){c.remove('pl-closed')},2200)}}catch(e){}</script>")

FAV = ("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E%3Crect width='32' height='32' rx='9' fill='%235E1224'/%3E"
       "%3Ccircle cx='10' cy='11' r='3.4' fill='none' stroke='%23C49A3C' stroke-width='2'/%3E%3Ccircle cx='10' cy='21' r='3.4' fill='none' stroke='%23C49A3C' stroke-width='2'/%3E"
       "%3Cpath d='M13 12.6 25 21M13 19.4 25 11' stroke='%23F8F3E8' stroke-width='2' stroke-linecap='round'/%3E%3C/svg%3E")

def head(title, desc, og='assets/img/k8.webp'):
    return f'''<!DOCTYPE html>
<html lang="nl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="theme-color" content="#F8F3E8">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:image" content="{og}">
<meta name="robots" content="noindex">
<link rel="icon" href="{FAV}">
{PRE}
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Bodoni+Moda:ital,opsz,wght@0,6..96,500;1,6..96,500&amp;family=DM+Sans:wght@400;500&amp;family=JetBrains+Mono:wght@500&amp;display=swap" rel="stylesheet">
<link rel="stylesheet" href="assets/style.css">
</head>
<body>
<a class="skip" href="#inhoud">Naar inhoud</a>
'''

def header(cur):
    links = [('diensten.html', 'Diensten'), ('afspraak.html', 'Afspraak'), ('over-ons.html', 'Over ons'), ('contact.html', 'Contact')]
    nav = ''.join(f'<a href="{h}"' + (' aria-current="page"' if h == cur else '') + f'>{t}</a>' for h, t in links)
    return f'''<header class="hd">
  <a class="logo" href="index.html" aria-label="Barbershop Golden Fingers — home"><span><em>Golden</em> Fingers</span><small>Barbershop · Waalwijk</small></a>
  <nav class="nav" id="menu" aria-label="Hoofdmenu">{nav}
    <div class="mnav">{B_BOEK('Afspraak maken')}{B_TEL()}{B_IG()}<p>Grotestraat 223, Waalwijk</p></div>
  </nav>
  <a class="btn pill" href="afspraak.html">Afspraak maken</a>
  <button class="burger" type="button" aria-label="Menu" aria-expanded="false" aria-controls="menu"><span></span><span></span><span></span></button>
</header>
<main id="inhoud">
'''

def finale(frm='var(--foam)', still=None):
    """still: None = shared C1 loop; else (img, img_m, caption, extra class)"""
    if still:
        d, m, cap, cls = still
        bg = f'<div class="bg"><div class="kbw" data-kb><picture><source media="(max-width:760px)" srcset="{m}"><img src="{d}" alt="" loading="lazy"></picture></div></div>'
    else:
        cap, cls = 'Sfeerbeeld', ''
        bg = '<div class="bg"><div class="kbw" data-kb><img src="assets/img/loop-contact-0.webp" alt="" loading="lazy"><video data-auto data-src="assets/loop-contact.mp4" poster="assets/img/loop-contact-0.webp" muted playsinline loop preload="none" aria-hidden="true"></video></div></div>'
    return f'''<section class="finale {cls}" style="--from:{frm}" aria-label="Tot zo">
  {bg}
  <canvas class="dust" data-k="warm" aria-hidden="true"></canvas>
  <span class="cap mono">{cap}</span>
  <div class="wrap"><div class="box glow-follow">
    <span class="eyebrow">Grotestraat 223 · Waalwijk</span>
    <h2 class="words">tot zo in de stoel.</h2>
    <p class="lead rv">Plan je afspraak online in een minuut, of bel even als je liever iemand spreekt. Je vindt Golden Fingers aan de Grotestraat 223 in Waalwijk.</p>
    <div class="row rv" style="--d:1">{B_BOEK()}{B_TEL()}{B_ROUTE()}{B_IG()}</div>
  </div></div>
</section>
'''

def footer(extra_js=''):
    return f'''</main>
<footer>
  <div class="wrap">
    <div><b>Barbershop <em>Golden</em> Fingers</b>Grotestraat 223, 5141 Waalwijk<a class="tel" href="{TEL}">{TELT}</a><a href="{IG}" target="_blank" rel="noopener">@golden_fingers_waalwijk</a><a href="{ROUTE}" target="_blank" rel="noopener">Route plannen</a></div>
    <div><b>Openingstijden</b>Openingstijden volgen — bel even of kijk op Instagram.</div>
    <div><b>Pagina's</b><a href="index.html">Home</a><a href="diensten.html">Diensten</a><a href="afspraak.html">Afspraak</a><a href="over-ons.html">Over ons</a><a href="contact.html">Contact</a></div>
    <p class="demo"><strong>Ontwerpvoorstel — ITty Company.</strong> Alle beelden zijn sfeerbeelden en worden vervangen door eigen foto's van Golden Fingers. De diensten op deze site zijn voorbeelden; de echte lijst en prijzen volgen van de zaak.</p>
  </div>
</footer>
<div class="ctabar">{B_BOEK('Afspraak')}{btn(TEL, 'Bel', 'ghost', 'tel')}</div>
<div class="grain" aria-hidden="true"></div>
<div class="demo-pill">Ontwerpvoorstel — ITty Company</div>
<div id="paal" aria-hidden="true"><div class="strips">{''.join(f'<i style="--k:{k}"></i>' for k in range(12))}</div><div class="lbl"></div></div>
<script src="assets/vendor/lenis.min.js"></script>
<script src="assets/site.js"></script>
{extra_js}</body>
</html>
'''

def fstills(items):
    """items: (img, img_m, inner_html, cap)"""
    lis = ''.join(f'<li><picture><source media="(max-width:760px)" srcset="{m}"><img src="{d}" alt="" loading="lazy"></picture><div class="box">{inner}</div><span class="cap mono">{cap}</span></li>' for d, m, inner, cap in items)
    return f'<ol class="fstills">{lis}</ol>'

# ======================================================================= INDEX
CH = [
 dict(t='eerst het licht.', s='Een lege zaak, een stoel, een nieuwe dag.', fx='dust', cool=1, at=0.35, w='licht', pos='tc', o=[.41, .60, .40, .97], b=[.5, .55], cx=.5, om=[.3, .8, .4, .93]),
 dict(t='alles op zijn plek.', s='Schaar, mes, kam, tondeuse. Klaar voor gebruik.', fx='glint', at=5.0, w='gereedschap', pos='tl', o=[.02, .47, .42, .95], b=[.42, .6], g=[.22, .785, .43, .775], cx=.45, gm=[.35, .83, .85, .815]),
 dict(t='warm voor je begint.', s='Een hete handdoek maakt huid en baard zacht.', fx='steam', at=10.0, w='stoom', pos='tl', o=[.05, .26, .24, .44], b=[.3, .36], src=[.15, .28], cx=.3, srcm=[.35, .38]),
 dict(t='zacht als schuim.', s='Wat glad moet worden, begint zacht.', fx='foam', at=15.0, w='schuim', pos='tc', o=[.33, .58, .42, .76], b=[.46, .5], cx=.5, om=[.15, .9, .5, .72]),
 dict(t='dan de schaar.', s='Millimeter voor millimeter, tot het klopt.', fx='hair', at=19.9, w='knip', pos='tl', o=[.38, .97, .66, .88], b=[.66, .7], cx=.66, floorm=.8),
 dict(t='en dan: <em>scherp.</em>', s='Een strakke lijn zegt meer dan veel woorden.', fx='blade', at=22.4, w='lijn', pos='tl', o=[.22, .94, .55, .86], b=[.56, .62], g=[.30, .73, .58, .62], cx=.5, gm=[.05, .63, .55, .575]),
 dict(t='de laatste glans.', s='Een beetje pomade, een blik — klaar.', fx='caustic', at=27.95, w='glans', pos='tl', o=[.2, .58, .6, .98], b=[.42, .62], cz=[.62, .86, .8, .97], warm=1, cx=.5, czm=[.3, .95, .64, .8]),
]
CARDS = [
 ('De rust voor de eerste knip', 'Een barbershop in de ochtend is een stille plek. Licht door het raam, een schone vloer, een stoel die wacht. Zo hoort een dag in een barbershop te beginnen: eerst alles klaar, dan pas de eerste klant.', ''),
 ('Gereedschap dat je kunt vertrouwen', 'Een goede knipbeurt begint bij scherp, schoon gereedschap op een vaste plek. Schaar, scheermes, kam en tondeuse liggen klaar, zodat er tijdens jouw beurt niets gezocht hoeft te worden.', ''),
 ('Warmte opent alles', 'Een warme handdoek is meer dan luxe. De warmte maakt de huid soepel en de baardharen zachter, zodat scheren en trimmen rustiger en gladder gaan. En eerlijk: het is ook gewoon een fijn moment.', ''),
 ('Schuim met geduld', 'Goed scheerschuim is luchtig en romig. Het legt een laagje tussen huid en mes, houdt het vocht vast en laat het mes glijden in plaats van trekken. Zacht beginnen, strak eindigen.', ''),
 ('Het echte werk', 'Met schaar en kam wordt de vorm gebouwd: bovenop wat lengte, opzij korter, alles in verhouding tot jouw gezicht en jouw haar. Niet snel-snel, maar precies. Wat valt, valt op de juiste plek.', 'bl'),
 ('De lijn die alles afmaakt', 'Een nek die strak is uitgeschoren, een baardlijn die klopt, een scherpe overgang bij de slapen. Het zijn de kleine lijnen waardoor een knipbeurt er nog dagen later verzorgd uitziet.', 'tr'),
 ('Afwerken zoals jij het draagt', 'Tot slot wat styling: een beetje pomade of wax, in model gebracht zoals jij je haar morgen zelf draagt. Even kijken, even bijwerken — en je loopt naar buiten zoals je naar binnen wilde: strak.', 'tr'),
]

def index():
    cards = ''.join(f'<article class="fcard glow-follow {pos}"><span class="no">Ritueel · {i+1:02d} / 08</span><b>{h}</b><p>{p}</p><button class="more" type="button" aria-expanded="false">lees verder +</button></article>' for i, (h, p, pos) in enumerate(CARDS))
    still_items = []
    for i, (c, (h, p, _)) in enumerate(zip(CH, CARDS)):
        inner = ''
        if i == 0:
            inner += f'<span class="chip">Barbershop · Grotestraat 223</span><h1 style="margin-top:14px">strak geknipt aan de grotestraat.</h1><p class="lead">Golden Fingers is een barbershop aan de Grotestraat in Waalwijk. Knippen, fade, baard of een klassieke scheerbeurt — plan je afspraak online, of bel even.</p><div class="row">{B_BOEK()}{B_TEL()}</div><hr style="border:0;height:1px;background:var(--line);margin:22px 0">'
        inner += f'<h2>{c["t"]}</h2><p class="note">{c["s"]}</p><p>{p}</p>'
        still_items.append((f'assets/img/k{i+1}.webp', f'assets/img/k{i+1}-m.webp', inner, 'Sfeerbeeld'))
    chj = json.dumps(CH, ensure_ascii=False)
    hotspots = [
     ('Schaar &amp; kam', 'Voor de vorm bovenop en voor alles wat lengte houdt. Knipt precies en laat haar natuurlijk vallen.', 'diensten.html#knippen', 'Bekijk: knippen', .37, .83),
     ('Tondeuse', 'Voor korte zijkanten en een vloeiende overgang van kort naar lang: de fade.', 'diensten.html#fade', 'Bekijk: fade', .52, .505),
     ('Scheermes', 'Voor strakke lijnen in de nek, bij de slapen en langs de baard, en voor een gladde klassieke scheerbeurt.', 'diensten.html#scheren', 'Bekijk: scheren', .47, .715),
     ('Kam', 'Om te scheiden, te meten en de vorm te controleren. Klein ding, groot verschil.', 'diensten.html#knippen', 'Bekijk: knippen', .30, .615),
    ]
    hots = ''.join(f'<button class="hot" type="button" style="--x:{x*100:.1f}%;--y:{y*100:.1f}%" aria-pressed="{"true" if k==0 else "false"}" aria-label="{html.unescape(n)}" data-n="{html.unescape(n)}" data-t="{t}" data-h="{h}" data-l="{l}"></button>' for k, (n, t, h, l, x, y) in enumerate(hotspots))
    lijst = ''.join(f'<li><b>{n}</b> — {t} <a href="{h}" style="color:var(--gold)">{l}</a></li>' for n, t, h, l, x, y in hotspots)
    n0, t0, h0, l0 = hotspots[0][:4]
    PANO = [('knippen', 'Knippen', 'Een frisse coupe met schaar en tondeuse, afgestemd op jouw haar.', .16),
            ('fade', 'Fade', 'Een vloeiende overgang van huid of heel kort naar langer.', .27),
            ('baard', 'Baard', 'Trimmen, in model brengen en strakke lijnen.', .455),
            ('scheren', 'Klassiek scheren', 'Warme handdoek, schuim en scheermes.', .65),
            ('combi', 'Knippen + baard', 'Alles in één keer netjes.', .36),
            ('kids', 'Kinderen', 'Rustig en zonder gedoe in de stoel.', .84)]
    panels = ''.join(f'<a class="panel" href="diensten.html#{i}" style="text-decoration:none"><div class="crop"><img src="assets/img/d1.webp" alt="" loading="lazy" style="--c:{c}"><span class="cap mono">Sfeerbeeld · voorbeeld</span></div><h3>{n}</h3><p>{t}</p><span class="mono">prijs op aanvraag</span></a>' for i, n, t, c in PANO)
    WIJ = [('fade', 'kort en fris', 'Fade', 'Kort aan de zijkanten, vloeiend naar boven. Fris voor weken.', .27),
           ('knippen', 'gewoon bijwerken', 'Knippen', 'Je vertrouwde model, weer in vorm.', .16),
           ('baard', 'mijn baard', 'Baard', 'Trimmen, lijnen zetten, in model brengen.', .455),
           ('scheren', 'helemaal glad', 'Klassiek scheren', 'Warme handdoek, schuim, scheermes.', .65),
           ('combi', 'alles tegelijk', 'Knippen + baard', 'In één afspraak helemaal klaar.', .36)]
    chips = ''.join(f'<button class="schip" type="button" aria-pressed="{"true" if k==0 else "false"}" data-id="{i}" data-n="{n}" data-t="{t}" data-c="{c}">{ch}</button>' for k, (i, ch, n, t, c) in enumerate(WIJ))
    w0 = WIJ[0]
    return head('Barbershop Golden Fingers — barbier aan de Grotestraat in Waalwijk',
                'Barbershop Golden Fingers, Grotestraat 223 in Waalwijk. Knippen, fade, baard en klassiek scheren. Plan je afspraak online of bel 06 87 86 26 66.') + header('index.html') + f'''<section class="film" data-src="assets/film-main.mp4" data-src-m="assets/film-main-m.mp4" data-poster-m="assets/img/film-main-m-0.webp" data-hud="Ritueel" data-total="8" data-dur="28.2" data-wipe="20.2,21.8" data-portal style="--m:8" aria-label="Golden Fingers — een barbershop maakt zich klaar, van ochtendlicht tot gouden uur">
  <div class="stage">
    <video poster="assets/img/film-main-0.webp" muted playsinline preload="none" aria-hidden="true"></video>
    <div class="vignette"></div>
    <div class="bigword" aria-hidden="true"><span></span></div>
    <canvas class="fx" aria-hidden="true"></canvas>
    <div class="scheer" aria-hidden="true"></div>
    <div class="fhero">
      <div class="top"><span class="chip">Barbershop · Grotestraat 223</span><h1>strak geknipt aan de grotestraat.</h1></div>
      <div class="low glow-follow">
        <p class="lead">Golden Fingers is een barbershop aan de Grotestraat in Waalwijk. Knippen, fade, baard of een klassieke scheerbeurt — plan je afspraak online, of bel even.</p>
        <button class="more" type="button" aria-expanded="false">lees verder +</button>
        <div class="row">{B_BOEK()}{B_TEL()}</div>
        <div class="plates"><a class="plate glow-follow" href="{ROUTE}" target="_blank" rel="noopener">{I['pin']}<span>Grotestraat 223<small>5141 Waalwijk</small></span></a><a class="plate glow-follow" href="{TEL}">{I['tel']}<span>{TELT}<small>bellen</small></span></a><a class="plate glow-follow" href="{IG}" target="_blank" rel="noopener">{I['ig']}<span>@golden_fingers_waalwijk<small>op Instagram</small></span></a></div>
      </div>
    </div>
    <div class="ftitle tc" aria-live="polite"><h2></h2><p></p></div>
    {cards}
    <div class="hud mono" aria-hidden="true"><span class="hl">Ritueel · 01 / 08</span><span class="sf">Sfeerbeeld</span><span class="tc">00:00 / 00:28</span><span class="load"><s></s></span></div>
    <div class="pole" aria-hidden="true"><i></i></div>
    <span class="ftag mono">Sfeerbeeld</span>
    <div class="fhint">scroll — zo wordt de zaak klaargemaakt</div>
  </div>
  {fstills(still_items)}
  <script type="application/json">{chj}</script>
</section>
<section class="portal" data-a="assets/img/film-main-end.webp" data-a-m="assets/img/film-main-m-end.webp" data-b="assets/img/k8.webp" data-b-m="assets/img/k8-m.webp" data-g="[0.73,0.6]" data-g-m="[0.72,0.7]" aria-label="Jouw stoel staat klaar">
  <div class="pstage">
    <img class="pfb a" alt="">
    <img class="pfb b" src="assets/img/k8.webp" alt="Lege bordeauxrode kappersstoel in het gouden avondlicht">
    <canvas class="gl" aria-hidden="true"></canvas>
    <canvas class="dust" data-k="warm" aria-hidden="true"></canvas>
    <div class="ptext glow-follow">
      <span class="eyebrow">Golden Fingers · Waalwijk</span>
      <h2>jouw stoel staat klaar.</h2>
      <p class="p1">Aan het eind van het verhaal staat er maar één ding: een lege stoel in het gouden licht. Die is voor jou. Of je nu elke paar weken je fade laat bijwerken, je baard wilt laten modelleren of gewoon weer eens netjes geknipt wilt worden — bij Golden Fingers aan de Grotestraat in Waalwijk zit je goed.</p>
      <p class="p2">Een afspraak maken hoeft niet ingewikkeld te zijn. Kies wat je wilt laten doen, kies een dag en een tijd, laat je naam en nummer achter. Liever even bellen? Dat kan natuurlijk ook: 06 87 86 26 66.</p>
      <button class="more" type="button" aria-expanded="false">lees verder +</button>
      <div class="row">{B_BOEK()}{B_TEL()}</div>
    </div>
    <span class="phud mono">Ritueel · 08 / 08<span class="sf">Sfeerbeeld</span></span>
    <span class="ptag mono">Sfeerbeeld</span>
    <div class="pdark"></div>
  </div>
</section>

<section class="dark-band seam-bot" id="ambacht" style="--to:var(--foam)">
  <canvas class="dust" data-k="gold" aria-hidden="true"></canvas>
  <div class="wrap j1">
    <div>
      <span class="eyebrow">Het ambacht</span>
      <h2 class="words">knippen is kijken.</h2>
      <div class="prose rv">
        <p>Een barbier begint niet met de schaar, maar met kijken. Hoe groeit je haar, waar zit een kruin, hoe valt het opzij, hoe ziet je gezicht eruit van de zijkant? Pas als dat duidelijk is, weet je wat er weg moet en wat er juist moet blijven. Daarom begint een goede beurt altijd met een korte vraag: wat wil je, en hoe draag je het normaal?</p>
        <p>Daarna is het handwerk. De tondeuse voor de korte zijkanten en een vloeiende fade, de schaar en kam voor de vorm bovenop, het scheermes voor de strakke lijnen in de nek en langs de baard. Elk stuk gereedschap heeft zijn eigen taak, en het verschil zit in hoe ze samenkomen: geen harde randen waar het zacht moet verlopen, geen rommelige lijnen waar het strak moet zijn.</p>
        <p>En dan is er de rust. Een barbershop is een van de weinige plekken waar je een halfuurtje niets hoeft. Je telefoon kan even weg, je zit, er wordt voor je gezorgd. Dat hoort net zo goed bij het vak als een scherpe schaar.</p>
      </div>
    </div>
    <div class="lade rv" style="--d:1">
      <span class="eyebrow">Gereedschapslade — tik op een punt</span>
      <figure class="fig breathe"><img src="assets/img/k2.webp" alt="Schaar, scheermes, kam en tondeuse op een marmeren werkblad" loading="lazy">{hots}<figcaption class="cap mono">Sfeerbeeld</figcaption></figure>
      <div class="tagcard" aria-live="polite"><b>{html.unescape(n0)}</b><p>{t0}</p><a href="{h0}">{l0}</a></div>
      <ul class="ladelist">{lijst}</ul>
      <p class="note">Sfeerbeeld. Welk gereedschap Golden Fingers precies gebruikt, zie je in de zaak.</p>
    </div>
  </div>
</section>

<section class="pano" id="diensten" aria-label="Wat je hier kunt laten doen">
  <div class="pin">
    <div class="head">
      <div><span class="eyebrow">Diensten</span><h2 class="words">van kort opzij tot glad geschoren.</h2></div>
      <p class="rv">Een barbershop draait om een paar dingen, en die moeten goed. Hieronder zie je wat je bij een barbier kunt laten doen — de precieze lijst en prijzen van Golden Fingers volgen nog.</p>
    </div>
    <div class="track">{panels}<div class="panel end"><span class="mono">Voorbeelddiensten — de echte lijst volgt van Golden Fingers</span><ul>{''.join(f'<li><a href="diensten.html#{i}">{n}</a></li>' for i, n, t, c in PANO)}</ul>{btn('diensten.html', 'Alle diensten', '', 'scissors')}</div></div>
    <div class="pbar"><i></i></div>
  </div>
</section>

<section class="bg-marble seam-top seam-bot" id="stijlwijzer" style="--from:var(--foam);--to:var(--foam)">
  <div class="wrap wijzer">
    <div>
      <span class="eyebrow">Stijlwijzer</span>
      <h2 class="words">wat heb je vandaag nodig?</h2>
      <p class="lead rv" style="margin-top:18px">Twijfel je wat je moet kiezen? Tik aan wat je zoekt, dan zie je welke beurt erbij past.</p>
      <div class="chips rv" role="group" aria-label="Wat zoek je?">{chips}</div>
      <p class="note rv">Een suggestie, geen advies — in de stoel kijkt de barbier altijd even met je mee.</p>
    </div>
    <div class="wout rv" style="--d:1" aria-live="polite">
      <div class="crop"><img src="assets/img/d1.webp" alt="" loading="lazy" style="--c:{w0[4]}"><span class="cap mono">Sfeerbeeld · voorbeeld</span></div>
      <div class="body"><small>Voorbeelddienst</small><b>{w0[2]}</b><p>{w0[3]}</p><div class="row">{btn('afspraak.html?dienst=' + w0[0], 'Plan dit', '', 'cal')}</div></div>
    </div>
  </div>
</section>

<section class="bg-foam" id="online">
  <div class="wrap">
    <span class="eyebrow">Online afspraak</span>
    <h2 class="words">in vier tikken geregeld.</h2>
    <p class="lead rv" style="margin-top:18px">Geen wachtrij aan de telefoon, geen gedoe. Je kiest zelf wanneer het jou uitkomt, ook 's avonds op de bank of in je pauze.</p>
    <div class="path">
      <svg viewBox="0 0 1200 90" aria-hidden="true"><path d="M20 60 C 200 10, 330 85, 480 45 S 760 10, 880 50 S 1100 80, 1180 30" fill="none" stroke="rgba(94,18,36,.12)" stroke-width="2"/><path class="draw" d="M20 60 C 200 10, 330 85, 480 45 S 760 10, 880 50 S 1100 80, 1180 30" fill="none" stroke="#C49A3C" stroke-width="2.5" stroke-linecap="round"/><circle class="dot" cx="20" cy="60" r="9" fill="#C49A3C" stroke="#F8F3E8" stroke-width="3"/></svg>
      <ol class="steps"><li><span class="n">01</span><b>Dienst</b>Wat wil je laten doen?</li><li><span class="n">02</span><b>Dag &amp; tijd</b>Kies een moment dat jou past.</li><li><span class="n">03</span><b>Je gegevens</b>Naam en telefoonnummer, meer niet.</li><li><span class="n">04</span><b>Bevestigd</b>Je ziet meteen je afspraak terug.</li></ol>
    </div>
    <div class="row rv">{B_BOEK()}</div>
    <p class="note rv">Golden Fingers staat al op Fresha — in de echte site koppelen we deze agenda daaraan.</p>
  </div>
</section>

<section class="bg-marble seam-top" id="adres" style="--from:var(--foam)">
  <div class="wrap waar">
    <div class="paalorn rv" aria-hidden="true"></div>
    <div>
      <span class="eyebrow">Adres</span>
      <h2 class="words">aan de grotestraat.</h2>
      <div class="prose rv">
        <p>Je vindt Barbershop Golden Fingers aan de Grotestraat 223 in Waalwijk. Kom je met de fiets of loop je even binnen tijdens het boodschappen doen? Plan dan vooraf je afspraak, dan staat de stoel klaar als je er bent.</p>
        <p>De openingstijden zetten we hier zodra Golden Fingers ze heeft doorgegeven. Tot die tijd: bel even naar 06 87 86 26 66 of kijk op Instagram, daar zie je ook het werk van de afgelopen tijd.</p>
      </div>
      <div class="row rv">{B_ROUTE('')}{B_IG('Volg op Instagram')}</div>
    </div>
    <div class="gplates rv" style="--d:1">
      <a class="plate glow-follow" href="{ROUTE}" target="_blank" rel="noopener">{I['pin']}<span>Grotestraat 223<small>5141 Waalwijk</small></span></a>
      <a class="plate glow-follow" href="{TEL}">{I['tel']}<span>{TELT}<small>bellen</small></span></a>
      <a class="plate glow-follow" href="{IG}" target="_blank" rel="noopener">{I['ig']}<span>Instagram<small>@golden_fingers_waalwijk</small></span></a>
      <span class="plate glow-follow">{I['clock']}<span>Openingstijden<small>volgen</small></span></span>
    </div>
  </div>
</section>
''' + finale('var(--marble)') + footer()

# ======================================================================= DIENSTEN
SVC = [
 ('knippen', 'knippen.', .16, ['Een goede knipbeurt begint met een gesprek van een minuut: hoe draag je je haar, wat zit je nu dwars, hoe lang mag het blijven? Daarna wordt de vorm gebouwd met schaar en tondeuse, afgestemd op hoe je haar groeit en hoe je gezicht eruitziet. Het doel is niet alleen dat het vandaag goed zit, maar dat het ook over twee weken nog netjes uitgroeit.', 'Klassiek kort, wat langer bovenop, met scheiding of juist zonder: alles kan. Weet je het zelf niet precies? Neem een foto mee of zeg gewoon wat je níet wilt — dat zegt vaak al genoeg.'], '± 30 min · voorbeeld · prijs op aanvraag', True),
 ('fade', 'fade.', .27, ['Bij een fade loopt het haar vloeiend van heel kort — soms tot op de huid — naar langer. Geen harde rand, maar een zachte overgang waar je geen streep in ziet. Of hij hoog, midden of laag begint, bepaal je samen met de barbier. Het is precisiewerk met de tondeuse, opzetstukken en veel controleren vanuit verschillende hoeken.', 'Een fade ziet er het strakst uit in de eerste weken. Wie hem altijd fris wil houden, plant de volgende afspraak vaak meteen in. Dat kan straks ook gewoon online.'], '± 30 min · voorbeeld · prijs op aanvraag', True),
 ('baard', 'baard.', .455, ['Een baard die goed verzorgd is, maakt een gezicht af. Bij het trimmen wordt de lengte gelijk gemaakt, de vorm in balans gebracht met je kapsel en worden de lijnen gezet: op de wangen, onder de kaak en in de nek. Met het scheermes worden de randen echt strak.', 'Of je nu een korte stoppelbaard draagt of een volle baard laat staan: het verschil zit in de details. Vraag gerust hoe je hem thuis het beste bijhoudt tot de volgende keer.'], '± 30 min · voorbeeld · prijs op aanvraag', True),
 ('scheren', 'klassiek scheren.', .65, ['De oudste dienst van de barbier, en voor veel mensen nog steeds de fijnste. Eerst een warme handdoek, die de huid opent en de haren zacht maakt. Dan een laag romig schuim, en daarna het scheermes, rustig en met de haargroei mee. Tot slot iets verkoelends voor de huid.', 'Het resultaat is gladder dan je thuis ooit krijgt, en het moment zelf is minstens zo belangrijk: even achterover, ogen dicht, niets hoeven.'], '± 30 min · voorbeeld · prijs op aanvraag', True),
 ('combi', 'knippen + baard.', .36, ['Haar en baard horen bij elkaar. Als ze in één afspraak worden gedaan, kan de barbier ze op elkaar afstemmen: de fade die vloeiend overgaat in je baard, de lengte bovenop in verhouding tot je kaaklijn. Dat geeft een rustiger, completer resultaat dan twee losse beurten.', 'Handig ook: één afspraak, één keer in de stoel, en je bent voor de komende weken helemaal bij.'], 'voorbeeld · prijs op aanvraag', True),
 ('kids', 'kinderen.', .79, ['Ook jongens willen er strak uitzien. Een kinderknipbeurt vraagt vooral rust en een beetje geduld: even laten wennen aan de stoel en het geluid van de tondeuse, en dan in een rustig tempo knippen. Kom gerust samen; dan kun je meteen meekijken en meepraten over het model.', 'Of Golden Fingers kinderen knipt en vanaf welke leeftijd, hoor je bij de zaak. Bel even of vraag het op Instagram.'], 'voorbeeld · prijs op aanvraag', False),
]
PANCH = [dict(t='knippen.', s='', c=.09, z=1.6, zm=1.25), dict(t='fade.', s='', c=.27, z=1.6, zm=1.25), dict(t='baard.', s='', c=.455, z=1.6, zm=1.25),
         dict(t='scheren.', s='', c=.65, z=1.6, zm=1.25), dict(t='afwerking.', s='', c=.87, z=1.6, zm=1.25)]
for i, c in enumerate(PANCH): c.update(fx='dust', pos='tl', at=0)

def diensten():
    svc = ''
    for k, (i, h, c, ps, mono, plan) in enumerate(SVC):
        b = btn('afspraak.html?dienst=' + i, 'Plan deze dienst', '', 'cal') if plan else B_TEL('')
        svc += f'''<article class="svc{' rev' if k % 2 else ''}" id="{i}">
      <figure class="fig breathe rv"><img src="assets/img/d1.webp" alt="" loading="lazy" style="--c:{c}"><figcaption class="cap mono">Sfeerbeeld · voorbeeld</figcaption></figure>
      <div><h2 class="words">{h}</h2><div class="prose rv">{''.join(f'<p>{p}</p>' for p in ps)}</div><span class="mono rv">{mono}</span><div class="row rv">{b}</div></div>
    </article>
'''
    marq_items = '<span>knippen</span><i></i><span>fade</span><i></i><span>baard</span><i></i><span>klassiek scheren</span><i></i><span>warme handdoek</span><i></i><span>styling</span><i></i><span>kinderen</span><i></i><em>voorbeeld</em><i></i>'
    stills = [('assets/img/d1.webp', 'assets/img/d1-m.webp', f'<span class="chip">Voorbeelddiensten</span><h1 style="margin-top:14px">wat er in de stoel gebeurt.</h1><p class="lead">Van een frisse fade tot een klassieke scheerbeurt met warme handdoek. Hieronder lees je wat je bij een barbershop kunt laten doen — en hoe je het meteen plant.</p><div class="row">{B_BOEK()}{B_TEL()}</div>', 'Sfeerbeeld')]
    return head('Diensten — Barbershop Golden Fingers, Waalwijk', 'Knippen, fade, baard, klassiek scheren, knippen + baard en kinderen — voorbeelddiensten van Barbershop Golden Fingers, Grotestraat 223 Waalwijk. Prijs op aanvraag.', 'assets/img/d1.webp') + header('diensten.html') + f'''<section class="pan" data-hud="Diensten" style="--m:6" aria-label="Diensten — de camera glijdt over het gereedschap">
  <div class="stage">
    <img class="flat" src="assets/img/d1.webp" width="1344" height="752" alt="Gereedschap van een barbier op wit marmer: schaar en kam, tondeuse, baardborstel en flesje, scheermes en schuim, handdoek en pomade">
    <div class="vignette"></div>
    <canvas class="fx" aria-hidden="true"></canvas>
    <div class="phead">
      <div class="top"><span class="chip">Voorbeelddiensten</span><h1>wat er in de stoel gebeurt.</h1></div>
      <div class="bot glow-follow"><p class="lead">Van een frisse fade tot een klassieke scheerbeurt met warme handdoek. Hieronder lees je wat je bij een barbershop kunt laten doen — en hoe je het meteen plant.</p><div class="row">{B_BOEK()}{B_TEL()}</div></div>
    </div>
    <div class="ftitle" aria-live="polite"><h2></h2><p></p></div>
    <div class="hud mono" aria-hidden="true"><span class="hl">Diensten · 01 / 05</span><span class="sf">Sfeerbeeld</span></div>
    <div class="pole" aria-hidden="true"><i></i></div>
    <span class="ftag mono">Sfeerbeeld</span>
    <div class="fade"></div>
  </div>
  {fstills(stills)}
  <script type="application/json">{json.dumps(PANCH, ensure_ascii=False)}</script>
</section>
<section class="bg-foam" style="padding-bottom:0">
  <div class="wrap">
    <p class="honest rv">Voorbeelddiensten — de echte lijst en prijzen volgen van Golden Fingers. Prijs op aanvraag.</p>
    {svc}
  </div>
</section>
<div class="marq" aria-label="Voorbeelddiensten"><div>{marq_items * 4}</div></div>
<section class="bg-foam">
  <div class="wrap prijs rv">
    <div><h3 style="font-size:clamp(2rem,3.4vw,3rem)">wat kost het?</h3><p class="lead" style="margin-top:12px">De prijzen van Golden Fingers zetten we hier zodra de zaak ze heeft doorgegeven. Tot die tijd: vraag het gerust even via telefoon of Instagram.</p></div>
    <div class="row" style="margin-top:0">{B_TEL('')}{B_IG()}</div>
  </div>
</section>
''' + finale() + footer()

# ======================================================================= AFSPRAAK
OPTS = [('knippen', 'Knippen', 'Schaar en tondeuse, afgestemd op jouw haar.', True), ('fade', 'Fade', 'Vloeiend van kort naar langer.', True),
        ('baard', 'Baard', 'Trimmen, lijnen en model.', True), ('scheren', 'Klassiek scheren', 'Warme handdoek, schuim, scheermes.', True),
        ('combi', 'Knippen + baard', 'Alles in één afspraak.', False), ('kids', 'Kinderen', 'Rustig in de stoel.', False)]

def afspraak():
    opts = ''.join(f'<label class="opt"><input type="radio" name="dienst" value="{i}" data-n="{n}"><b>{n}</b><span>{t}</span><small>{"<em style=\'font-style:normal\'>± 30 min · voorbeeld</em>" if d else "<em style=\'font-style:normal\'>voorbeeld</em>"}<em style="font-style:normal">prijs op aanvraag</em></small></label>' for i, n, t, d in OPTS)
    faq = [('Moet ik een afspraak maken?', 'Met een afspraak weet je zeker dat de stoel klaarstaat. Of je ook zonder afspraak kunt binnenlopen, hoor je bij de zaak.'),
           ('Kan ik mijn afspraak verzetten?', 'Bel even naar 06 87 86 26 66, dan zoek je samen een nieuw moment.'),
           ('Wat als ik te laat ben?', 'Laat het even weten via de telefoon, dan wordt er gekeken wat er nog past.'),
           ('Wat kost het?', 'De prijzen volgen van Golden Fingers. Vraag het gerust even.')]
    faqh = ''.join(f'<details><summary>{q}</summary><p>{a}</p></details>' for q, a in faq)
    return head('Afspraak maken — Barbershop Golden Fingers, Waalwijk', 'Plan je afspraak bij Barbershop Golden Fingers, Grotestraat 223 Waalwijk: kies een dienst, een dag en een tijd. Of bel 06 87 86 26 66.', 'assets/img/a1.webp') + header('afspraak.html') + f'''<section class="phero split" style="--to:var(--foam)" aria-label="Online afspraak">
  <div class="bg"><div class="kbw" data-kb><picture><source media="(max-width:760px)" srcset="assets/img/a1-m.webp"><img src="assets/img/loop-afspraak-0.webp" alt="Bordeauxrode kappersstoel met een opgevouwen cape en een dampende handdoek" fetchpriority="high"></picture><video data-auto data-src="assets/loop-afspraak.mp4" poster="assets/img/loop-afspraak-0.webp" muted playsinline loop preload="none" aria-hidden="true" class="dv"></video></div></div>
  <canvas class="dust" data-k="cool" aria-hidden="true"></canvas>
  <span class="cap mono">Sfeerbeeld</span>
  <div class="wrap"><div class="box">
    <span class="chip">Online afspraak</span>
    <h1 class="words" style="margin-top:16px">plan je stoel.</h1>
    <p class="lead rv">Kies wat je wilt laten doen, kies een dag en tijd die jou uitkomt en laat je gegevens achter. Klaar in een minuut.</p>
    <span class="demo-plate rv">Demo — er wordt niets geboekt</span>
  </div></div>
</section>

<section class="bg-foam" id="boeken" style="padding-top:clamp(40px,8vh,80px)">
  <div class="wrap book" id="wizard">
    <div>
      <ol class="wbar" aria-label="Stappen">
        <li class="cur"><button type="button" disabled>1 Dienst</button></li><li><button type="button" disabled>2 Dag &amp; tijd</button></li><li><button type="button" disabled>3 Je gegevens</button></li><li><button type="button" disabled>4 Bevestigd</button></li>
      </ol>
      <noscript><p class="honest">Zonder JavaScript werkt de demo-afspraak niet. Bel {TELT} of kijk op Instagram.</p></noscript>
      <div class="wstep" data-s="1">
        <h2>wat wil je laten doen?</h2>
        <fieldset style="border:0"><legend class="sr">Kies een dienst</legend><div class="opts">{opts}</div></fieldset>
        <p class="note">Voorbeelddiensten — de echte lijst en prijzen volgen van Golden Fingers.</p>
        <span class="err" id="e1" role="alert"></span>
        <div class="wnav"><button class="btn" type="button" id="n1">Volgende</button></div>
      </div>
      <div class="wstep" data-s="2" hidden>
        <h2>wanneer komt het je uit?</h2>
        <span class="lbl" id="l-dag">Kies een dag</span>
        <div class="days" id="days" role="group" aria-labelledby="l-dag"></div>
        <span class="lbl" id="l-tijd">Kies een tijd</span>
        <div class="slots" id="slots" role="group" aria-labelledby="l-tijd"></div>
        <p class="note">Voorbeeldtijden. De echte agenda en openingstijden volgen van Golden Fingers.</p>
        <span class="err" id="e2" role="alert"></span>
        <div class="wnav"><button class="btn ghost" type="button" id="b2">Terug</button><button class="btn" type="button" id="n2">Volgende</button></div>
      </div>
      <div class="wstep" data-s="3" hidden>
        <h2>op welke naam?</h2>
        <form id="gegevens" novalidate>
          <div class="fields">
            <label class="fld">Naam*<input name="naam" autocomplete="name" placeholder="Voor- en achternaam" required><span class="ferr" aria-live="polite"></span></label>
            <label class="fld">Telefoon*<input name="tel" type="tel" autocomplete="tel" inputmode="tel" placeholder="06 12 34 56 78" required><span class="ferr" aria-live="polite"></span></label>
            <label class="fld full">E-mail (optioneel)<input name="mail" type="email" autocomplete="email" placeholder="naam@voorbeeld.nl"></label>
            <label class="fld full">Opmerking (optioneel)<textarea name="opm" placeholder="bijv. fade opzij, bovenop lang laten"></textarea></label>
            <label class="check full"><input type="checkbox" name="rem"> Stuur me een herinnering (demo)</label>
          </div>
          <p class="priv">We gebruiken je gegevens alleen voor je afspraak. (In deze demo wordt niets verstuurd of opgeslagen.)</p>
          <div class="wnav"><button class="btn ghost" type="button" id="b3">Terug</button><button class="btn" type="submit">Afspraak bevestigen</button></div>
        </form>
      </div>
      <div class="wstep" data-s="4" hidden>
        <h2>tot dan.</h2>
        <div class="receipt">
          <dl><dt>Dienst</dt><dd id="r-dienst"></dd><dt>Dag</dt><dd id="r-dag"></dd><dt>Tijd</dt><dd id="r-tijd"></dd><dt>Naam</dt><dd id="r-naam"></dd><dt>Waar</dt><dd>Grotestraat 223, Waalwijk</dd></dl>
                  </div>
        <p class="honestbox"><strong>Ontwerpvoorstel.</strong> Er is niets geboekt en niets verstuurd. Zo gaat het straks werken als Golden Fingers online afspraken aanneemt. Wil je nu echt een afspraak? Bel 06 87 86 26 66.</p>
        <p class="note">Golden Fingers staat al op Fresha — in de echte site koppelen we deze agenda daaraan.</p>
        <div class="row"><button class="btn" type="button" id="ics">{I['cal']}Zet in agenda (.ics)</button>{B_TEL()}{B_WA()}<button class="btn ghost" type="button" id="nieuw">Nieuwe afspraak</button></div>
      </div>
    </div>
    <aside class="aside" id="aside" aria-live="polite">
      <h3>Jouw afspraak</h3>
      <p class="empty">Nog niets gekozen.</p>
      <dl hidden><dt>Dienst</dt><dd id="s-dienst"></dd><dt>Dag</dt><dd id="s-dag"></dd><dt>Tijd</dt><dd id="s-tijd"></dd></dl>
      <p class="note">Demo — er wordt niets geboekt</p>
    </aside>
  </div>
</section>

<section class="bg-marble seam-top" style="--from:var(--foam)">
  <div class="wrap two">
    <div>
      <h2 class="words">liever even bellen?</h2>
      <p class="lead rv" style="margin-top:16px">Geen probleem. Bel 06 87 86 26 66, of stuur een bericht via Instagram. Je vindt de zaak aan de Grotestraat 223 in Waalwijk.</p>
      <div class="row rv">{B_TEL('')}{B_IG()}</div>
    </div>
    <div class="rv" style="--d:1"><span class="eyebrow">Kort &amp; handig</span>{faqh}</div>
  </div>
</section>
''' + finale('var(--marble)', ('assets/img/k8.webp', 'assets/img/k8-m.webp', 'Sfeerbeeld', 'left k8')) + footer('<script src="assets/booking.js"></script>\n')

# ======================================================================= OVER ONS
OCH = [dict(t='een gewone straat.', s='Een ochtend in Waalwijk.', fx='dust', cool=1, at=1.1, pos='tc', cx=.62),
       dict(t='en daar draait de paal.', s='Een barbershop herken je van ver.', fx='dust', at=4.95, pos='tr', cx=.45)]

def over():
    stills = [('assets/img/o1.webp', 'assets/img/o1-m.webp', f'<span class="chip">Barbershop in Waalwijk</span><h1 style="margin-top:14px">een barbershop om de hoek.</h1><p class="lead">Golden Fingers is een barbershop aan de Grotestraat in Waalwijk. Een plek om even te zitten, goed geknipt te worden en weer strak naar buiten te lopen.</p><div class="row">{B_BOEK()}{btn("diensten.html", "Bekijk diensten", "ghost")}</div><h2 style="margin-top:22px">een gewone straat.</h2><p class="note">Een ochtend in Waalwijk.</p>', 'Sfeerbeeld — niet de echte gevel'),
              ('assets/img/o2.webp', 'assets/img/o2-m.webp', '<h2>en daar draait de paal.</h2><p class="note">Een barbershop herken je van ver.</p>', 'Sfeerbeeld — niet de echte gevel')]
    plaques = ''.join(f'<div class="plaque rv" style="--d:{k}"><i></i><i></i><i></i><i></i><span>Vraag {k+1:02d}</span><b>{q}</b></div>' for k, q in enumerate(['Sinds wanneer?', 'Wie staat er achter de stoel?', 'Waar zijn jullie trots op?']))
    return head('Over ons — Barbershop Golden Fingers, Waalwijk', 'Barbershop Golden Fingers aan de Grotestraat 223 in Waalwijk: een plek om even te zitten, goed geknipt te worden en weer strak naar buiten te lopen.', 'assets/img/o2.webp') + header('over-ons.html') + f'''<section class="film" data-src="assets/film-over.mp4" data-src-m="assets/film-over-m.mp4" data-poster-m="assets/img/film-over-m-0.webp" data-hud="Straat" data-dur="5" style="--m:3" aria-label="Een straat in Waalwijk, en daar draait de barbierspaal">
  <div class="stage">
    <video poster="assets/img/film-over-0.webp" muted playsinline preload="none" aria-hidden="true"></video>
    <div class="vignette"></div>
    <canvas class="fx" aria-hidden="true"></canvas>
    <div class="fhero">
      <div class="top sky"><span class="chip">Barbershop in Waalwijk</span><h1>een barbershop om de hoek.</h1></div>
      <div class="low left glow-follow"><p class="lead">Golden Fingers is een barbershop aan de Grotestraat in Waalwijk. Een plek om even te zitten, goed geknipt te worden en weer strak naar buiten te lopen.</p><div class="row">{B_BOEK()}{btn("diensten.html", "Bekijk diensten", "ghost")}</div></div>
    </div>
    <div class="ftitle tc" aria-live="polite"><h2></h2><p></p></div>
    <div class="hud mono" aria-hidden="true"><span class="hl">Straat · 01 / 02</span><span class="sf">Sfeerbeeld — niet de echte gevel</span><span class="tc">00:00 / 00:05</span><span class="load"><s></s></span></div>
    <div class="pole" aria-hidden="true"><i></i></div>
    <span class="ftag mono">Sfeerbeeld — niet de echte gevel</span>
    <div class="fhint c">scroll — naar de grotestraat</div>
    <div class="fade"></div>
  </div>
  {fstills(stills)}
  <script type="application/json">{json.dumps(OCH, ensure_ascii=False)}</script>
</section>

<section class="bg-foam">
  <div class="wrap split">
    <div>
      <span class="eyebrow">Een barbershop aan de Grotestraat</span>
      <h2 class="words">meer dan een knipbeurt.</h2>
      <div class="prose rv">
        <p>Een barbershop is een bijzonder soort plek. Je komt voor je haar of je baard, maar je blijft even voor de rust. Je gaat zitten, de cape gaat om, en een halfuur lang hoef je niets anders dan stilzitten en af en toe knikken. Voor veel mannen is dat het enige moment in de week waarop iemand anders voor hen zorgt.</p>
        <p>Het vak zelf is eeuwenoud. De gestreepte barbierspaal stamt nog uit de tijd dat barbiers meer deden dan knippen en scheren. Wat bleef, is het handwerk: een scherpe schaar, een vast scheermes, een warme handdoek en iemand die weet wat hij doet.</p>
        <p>Golden Fingers zit aan de Grotestraat 223 in Waalwijk. Wil je weten hoe het eruitziet en wat er de laatste tijd in de stoel is gebeurd? Op Instagram laat de zaak zelf het werk zien.</p>
      </div>
    </div>
    <figure class="fig rv" style="aspect-ratio:4/5;--d:1"><img data-par="60" src="assets/img/k1.webp" alt="Lege barbershop in het ochtendlicht met een bordeauxrode stoel" loading="lazy" style="object-position:50% 50%"><figcaption class="cap mono">Sfeerbeeld</figcaption></figure>
  </div>
</section>

<section class="bg-foam seam-bot" style="--to:var(--bordeaux);padding-top:0">
  <div class="wrap">
    <span class="eyebrow">Waarom een barbershop?</span>
    <div class="fill"><p>Omdat details het verschil maken.</p><p>Omdat een strakke lijn langer meegaat.</p><p>Omdat even zitten ook goed is.</p></div>
  </div>
</section>

<section class="dark-band seam-bot" style="--to:var(--foam)">
  <canvas class="dust" data-k="gold" aria-hidden="true"></canvas>
  <div class="wrap split">
    <div>
      <span class="eyebrow">Het verhaal van Golden Fingers</span>
      <h2 class="words">dit verhaal vertellen ze zelf.</h2>
      <div class="plaques">{plaques}</div>
      <p class="note rv">Dit vertelt Golden Fingers zelf — wordt ingevuld na overleg.</p>
    </div>
    <figure class="fig breathe rv" style="aspect-ratio:4/5;--d:1"><picture><source media="(max-width:760px)" srcset="assets/img/o2-m.webp"><img src="assets/img/o2.webp" alt="Etalage van een barbershop met een gestreepte barbierspaal" loading="lazy" style="object-position:62% 50%"></picture><figcaption class="cap mono">Sfeerbeeld — niet de echte gevel</figcaption></figure>
  </div>
</section>

<section class="bg-foam">
  <div class="wrap">
    <div class="igblock">
      <div class="igring rv" aria-hidden="true"><span>{I['ig']}</span></div>
      <div>
        <h3 class="words" style="font-size:clamp(2rem,3.6vw,3.2rem)">het werk van vandaag.</h3>
        <p class="lead rv" style="margin-top:14px">De nieuwste fades, baarden en coupes staan op Instagram. Daar zie je meteen wat er in de stoel aan de Grotestraat gebeurt.</p>
        <div class="row rv">{B_IG('@golden_fingers_waalwijk', '')}</div>
      </div>
    </div>
    <p class="placeholder rv">Hier komen foto's van de zaak, de stoelen en het team van Golden Fingers.</p>
  </div>
</section>
''' + finale() + footer()

# ======================================================================= CONTACT
def contact():
    faq = [('Hoe maak ik een afspraak?', 'Online via de afspraakpagina, of bel 06 87 86 26 66.'),
           ('Wanneer zijn jullie open?', 'De openingstijden volgen. Bel tot die tijd even of kijk op Instagram.'),
           ('Waar kan ik parkeren of mijn fiets kwijt?', 'Dat hoor je het snelst als je even belt.'),
           ('Kan ik via WhatsApp een bericht sturen?', 'Dat bevestigen we nog met de zaak. Bellen of Instagram werkt in elk geval.')]
    faqh = ''.join(f'<details><summary>{q}</summary><p>{a}</p></details>' for q, a in faq)
    # schematic map: abstract block grid only, no real neighbouring streets
    blocks = ''
    import random
    rnd = random.Random(7)
    for gx in range(0, 8):
        for gy in range(0, 6):
            x, y = 20 + gx * 100, 20 + gy * 100
            if gy == 3: continue
            w, h = 76 + rnd.randint(-6, 4), 76 + rnd.randint(-6, 4)
            blocks += f'<rect x="{x}" y="{y if gy < 3 else y - 0}" width="{w}" height="{h}" rx="10" fill="#EDE6DA"/>'
    mapsvg = f'''<svg viewBox="0 0 800 600" role="img" aria-label="Schematische kaart: Grotestraat 223, Waalwijk">
      <rect width="800" height="600" fill="#F8F3E8"/>{blocks}
      <rect x="0" y="312" width="800" height="62" fill="#fff"/><path d="M0 343H800" stroke="#C49A3C" stroke-width="1.5" stroke-dasharray="2 10" opacity=".6"/>
      <path class="route" d="M40 343 H 420" stroke="#5E1224" stroke-width="3" fill="none" opacity=".5"/>
      <text x="60" y="334" font-family="JetBrains Mono, monospace" font-size="13" letter-spacing="2.5" fill="#6E5A55">GROTESTRAAT</text>
      <circle class="ring" cx="440" cy="343" r="22" fill="none" stroke="#C49A3C" stroke-width="2"/>
      <g class="pin"><path d="M440 343c-16-20-26-33-26-46a26 26 0 0 1 52 0c0 13-10 26-26 46z" fill="#5E1224"/><g transform="translate(428 284)" stroke="#C49A3C" stroke-width="2.2" fill="none" stroke-linecap="round"><circle cx="5" cy="6" r="3.4"/><circle cx="5" cy="18" r="3.4"/><path d="M8 7.6 22 17M8 16.4 22 7"/></g></g>
      <g transform="translate(470 226)"><rect width="196" height="58" rx="14" fill="#F8F3E8" stroke="rgba(94,18,36,.2)"/><text x="16" y="25" font-family="Bodoni Moda, Georgia, serif" font-size="19" fill="#5E1224">Golden Fingers</text><text x="16" y="44" font-family="JetBrains Mono, monospace" font-size="11" letter-spacing="1.5" fill="#6E5A55">GROTESTRAAT 223</text></g>
      <g transform="translate(730 60)" fill="none" stroke="#6E5A55" stroke-width="1.5"><circle r="20"/><path d="M0 -14 5 4 0 0 -5 4z" fill="#6E5A55"/></g>
    </svg>'''
    return head('Contact &amp; route — Barbershop Golden Fingers, Grotestraat 223 Waalwijk', 'Barbershop Golden Fingers, Grotestraat 223, 5141 Waalwijk. Bel 06 87 86 26 66, plan online of volg @golden_fingers_waalwijk op Instagram.', 'assets/img/c1.webp') + header('contact.html') + f'''<section class="phero" style="--to:var(--foam)" aria-label="Contact">
  <div class="bg"><div class="kbw" data-kb><picture><source media="(max-width:760px)" srcset="assets/img/c1-m.webp"><img src="assets/img/loop-contact-0.webp" alt="Uitzicht vanuit de barbershop door het raam op een zonnige straat, met de barbierspaal" fetchpriority="high"></picture><video data-auto data-src="assets/loop-contact.mp4" poster="assets/img/loop-contact-0.webp" muted playsinline loop preload="none" aria-hidden="true" class="dv"></video></div></div>
  <canvas class="dust" data-k="warm" aria-hidden="true"></canvas>
  <span class="cap mono">Sfeerbeeld</span>
  <div class="wrap"><div class="box" style="margin-left:auto">
    <span class="chip">Grotestraat 223 · Waalwijk</span>
    <h1 class="words" style="margin-top:16px">kom even langs.</h1>
    <p class="lead rv">Plan je afspraak online, bel even of stuur een bericht via Instagram. Je vindt Golden Fingers aan de Grotestraat in Waalwijk.</p>
    <div class="row rv">{B_BOEK()}{B_TEL()}</div>
  </div></div>
</section>

<section class="bg-foam" style="padding-top:clamp(40px,8vh,80px)">
  <div class="wrap">
    <div class="cards">
      <div class="gcard glow-follow rv"><span class="eyebrow">Adres</span><b>Grotestraat 223, 5141 Waalwijk</b>{B_ROUTE('sm')}</div>
      <div class="gcard glow-follow rv" style="--d:1"><span class="eyebrow">Telefoon</span><b>{TELT}</b>{btn(TEL, 'Bel nu', 'sm', 'tel')}</div>
      <div class="gcard glow-follow rv" style="--d:2"><span class="eyebrow">WhatsApp</span><b>nog te bevestigen</b><span class="wa-wrap">{btn(WA, 'WhatsApp', 'ghost sm', 'wa', True)}<span class="wa-note">nog te bevestigen</span></span></div>
      <div class="gcard glow-follow rv"><span class="eyebrow">Instagram</span><b>@golden_fingers_waalwijk</b>{btn(IG, 'Volg op Instagram', 'ghost sm', 'ig', True)}</div>
      <div class="gcard glow-follow rv" style="--d:1"><span class="eyebrow">Online afspraak</span><b>Plan hier in een minuut</b><p>ook te vinden op Fresha</p>{btn(BOEK, 'Afspraak maken', 'sm', 'cal')}</div>
      <div class="gcard glow-follow rv" style="--d:2"><span class="eyebrow">Openingstijden</span><b>volgen</b><p>bel even of kijk op Instagram</p></div>
    </div>
  </div>
</section>

<section class="bg-foam" style="padding-top:0">
  <div class="wrap two" style="align-items:center">
    <div>
      <h2 class="words">je vindt ons aan de grotestraat.</h2>
      <p class="lead rv" style="margin-top:16px">Grotestraat 223, 5141 Waalwijk (Noord-Brabant).</p>
      <div class="row rv">{btn(ROUTE, 'Open in Google Maps', '', 'pin', True)}</div>
    </div>
    <figure class="map rv" style="--d:1">{mapsvg}<figcaption class="mono">Golden Fingers · schematisch</figcaption></figure>
  </div>
</section>

<section class="bg-marble seam-top" style="--from:var(--foam)">
  <div class="wrap two">
    <div><span class="eyebrow">Kort &amp; handig</span><h2 class="words">goed om te weten.</h2></div>
    <div class="rv">{faqh}</div>
  </div>
</section>
''' + finale('var(--marble)', ('assets/img/o2.webp', 'assets/img/o2-m.webp', 'Sfeerbeeld — niet de echte gevel', 'left o2')) + footer()

# ======================================================================= 404
def p404():
    return head('Pagina niet gevonden — Barbershop Golden Fingers', 'Deze pagina is weggeschoren. Ga terug naar het begin of plan je afspraak bij Barbershop Golden Fingers.', 'assets/img/k4.webp') + header('') + f'''<section class="p404">
  <picture><source media="(max-width:760px)" srcset="assets/img/k4-m.webp"><img class="pimg" src="assets/img/k4.webp" alt="Schaal met romig scheerschuim op een marmeren werkblad"></picture>
  <canvas class="glints" aria-hidden="true"></canvas>
  <span class="cap mono">Sfeerbeeld</span>
  <div class="wrap"><div class="box glow-follow">
    <span class="eyebrow">404</span>
    <h1 class="words">deze pagina is weggeschoren.</h1>
    <p class="lead rv" style="margin-top:16px">Hier staat niets (meer). Ga terug naar het begin, of plan meteen je afspraak.</p>
    <div class="row rv">{btn('index.html', 'Naar home', 'ghost')}{B_BOEK()}</div>
  </div></div>
</section>
''' + footer()

pages = {'index.html': index(), 'diensten.html': diensten(), 'afspraak.html': afspraak(), 'over-ons.html': over(), 'contact.html': contact(), '404.html': p404()}
for n, s in pages.items():
    (OUT / n).write_text(s, encoding='utf-8')
    print(n, len(s))
