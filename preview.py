"""
preview.py — Standalone visual prototype for the RPG system.
Runs independently. Does NOT import or connect to any game backend files.
All data is mock/placeholder only.
"""
from flask import Flask, render_template_string

app = Flask(__name__)

# ─────────────────────────────────────────────────────────────────
#  TEMPLATE  (all HTML / CSS / JS embedded here)
# ─────────────────────────────────────────────────────────────────
TEMPLATE = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Dark Realm — Visual Preview</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@400;600;700&family=Inter:wght@300;400;500;600&family=Crimson+Pro:ital,wght@0,400;0,600;1,400&display=swap" rel="stylesheet">
<style>
/* ══════════════════════════════════════════════════════════
   DESIGN TOKENS
══════════════════════════════════════════════════════════ */
:root {
  --void:       #04030a;
  --bg:         #080610;
  --bg2:        #0d0a16;
  --panel:      #110e1a;
  --surface:    #18142a;
  --raised:     #1e1930;
  --border:     #261e38;
  --border2:    #332850;
  --gold:       #c8a040;
  --gold-b:     #e8c060;
  --gold-d:     #6a520a;
  --crimson:    #cc3030;
  --crimson-d:  #7a1818;
  --amber:      #d06030;
  --blue:       #4080d8;
  --teal:       #30a080;
  --purple:     #9050d0;
  --green:      #38b060;
  --text:       #ddd5cc;
  --text2:      #907868;
  --text3:      #4a3c48;
  --r:          6px;
  --r-sm:       4px;
}

/* ══════════════════════════════════════════════════════════
   RESET & BASE
══════════════════════════════════════════════════════════ */
*,*::before,*::after { box-sizing:border-box; margin:0; padding:0; }
html,body { height:100%; overflow:hidden; }
body {
  background:var(--void);
  color:var(--text);
  font-family:'Inter',sans-serif;
  font-size:13px;
  display:flex; flex-direction:column;
}
::-webkit-scrollbar { width:4px; }
::-webkit-scrollbar-track { background:var(--bg); }
::-webkit-scrollbar-thumb { background:var(--border2); border-radius:2px; }

/* ══════════════════════════════════════════════════════════
   HEADER
══════════════════════════════════════════════════════════ */
#hdr {
  height:48px; flex-shrink:0;
  background:var(--bg2);
  border-bottom:1px solid var(--border2);
  display:flex; align-items:center; padding:0 16px; gap:12px;
  box-shadow:0 2px 12px rgba(0,0,0,.5);
}
.hdr-brand {
  font-family:'Cinzel',serif; font-size:.85rem;
  color:var(--gold); letter-spacing:2px;
  text-shadow:0 0 10px rgba(200,160,64,.4);
  flex-shrink:0;
}
.hdr-divider { width:1px; height:20px; background:var(--border2); }
.hdr-tag {
  font-size:.6rem; letter-spacing:1.5px;
  background:var(--surface); color:var(--text2);
  border:1px solid var(--border); border-radius:20px;
  padding:2px 8px; text-transform:uppercase;
}
.hdr-center {
  flex:1; display:flex; align-items:center; justify-content:center; gap:12px;
}
.turn-display {
  font-family:'Cinzel',serif; font-size:.72rem; letter-spacing:1px;
  color:var(--text2);
}
.turn-num {
  font-size:1rem; color:var(--gold); font-weight:700;
  text-shadow:0 0 8px rgba(200,160,64,.4);
}
.your-turn-badge {
  background:rgba(200,160,64,.1); border:1px solid var(--gold-d);
  color:var(--gold); font-family:'Cinzel',serif; font-size:.6rem;
  letter-spacing:1.5px; padding:3px 10px; border-radius:20px;
  animation:pulse-gold 2s ease-in-out infinite;
}
@keyframes pulse-gold {
  0%,100%{ box-shadow:0 0 6px rgba(200,160,64,.2); }
  50%    { box-shadow:0 0 14px rgba(200,160,64,.5); }
}
.hdr-right { display:flex; gap:6px; align-items:center; }
.sys-chip {
  font-size:.58rem; padding:2px 8px; border-radius:20px; letter-spacing:.8px;
}
.chip-running { background:#081808; color:#60e080; border:1px solid #206040; }
.chip-phase   { background:#1e0808; color:#e06060; border:1px solid #601818; }
.chip-preview { background:#100818; color:#a070e0; border:1px solid #401860; }

/* ══════════════════════════════════════════════════════════
   MAIN GRID
══════════════════════════════════════════════════════════ */
#arena {
  flex:1; display:grid;
  grid-template-columns:270px 1fr 270px;
  gap:8px; padding:8px;
  overflow:hidden;
  min-height:0;
}

/* ══════════════════════════════════════════════════════════
   SHARED PANEL STYLES
══════════════════════════════════════════════════════════ */
.panel {
  background:var(--panel);
  border:1px solid var(--border);
  border-radius:var(--r);
  overflow:hidden;
  display:flex; flex-direction:column;
}
.panel-head {
  padding:8px 12px;
  background:var(--bg2);
  border-bottom:1px solid var(--border);
  display:flex; align-items:center; gap:6px;
  flex-shrink:0;
}
.panel-title {
  font-family:'Cinzel',serif; font-size:.62rem;
  letter-spacing:2px; color:var(--gold-d); text-transform:uppercase;
}
.panel-body { flex:1; overflow-y:auto; padding:10px 12px; display:flex; flex-direction:column; gap:10px; }

/* ══════════════════════════════════════════════════════════
   SHARED COMPONENTS
══════════════════════════════════════════════════════════ */

/* Bar */
.bar-wrap { display:flex; flex-direction:column; gap:2px; }
.bar-row  { display:flex; align-items:center; gap:5px; }
.bar-lbl  { font-size:.58rem; color:var(--text2); width:18px; }
.bar-track {
  flex:1; height:6px; background:var(--bg); border-radius:3px;
  overflow:hidden; border:1px solid var(--border);
}
.bar-fill  { height:100%; border-radius:3px; transition:width .5s ease; }
.bar-nums  { font-size:.58rem; color:var(--text2); white-space:nowrap; }
.hp-hi  { background:linear-gradient(90deg,#1a6030,#38b060); }
.hp-mid { background:linear-gradient(90deg,#704010,#c07020); }
.hp-lo  { background:linear-gradient(90deg,#6a1010,#cc3030); animation:blink-bar .8s ease-in-out infinite; }
.mp-bar { background:linear-gradient(90deg,#203070,#4080d8); }
@keyframes blink-bar { 0%,100%{opacity:1} 50%{opacity:.6} }

/* Status badges */
.statuses { display:flex; flex-wrap:wrap; gap:3px; }
.sbadge {
  font-size:.58rem; padding:2px 6px; border-radius:20px; font-weight:600;
  display:flex; align-items:center; gap:2px;
}
.s-burn   { background:#240608; color:#ff8040; border:1px solid #8a2010; }
.s-bleed  { background:#1a0606; color:#ff5050; border:1px solid #661010; }
.s-poison { background:#061a08; color:#50e050; border:1px solid #165818; }
.s-stun   { background:#1c1600; color:#f0d040; border:1px solid #786010; }
.s-defend { background:#06101c; color:#70a8f0; border:1px solid #183060; }
.s-rage   { background:#1e0614; color:#e050c0; border:1px solid #701848; }
.s-weak   { background:#1a1406; color:#c09040; border:1px solid #605018; }
.s-silence{ background:#100620; color:#9060e0; border:1px solid #401870; }
.s-regen  { background:#061a10; color:#40e090; border:1px solid #186040; }

/* Stat chip grid */
.stat-chips { display:grid; grid-template-columns:1fr 1fr; gap:4px; }
.stat-chip {
  background:var(--surface); border:1px solid var(--border);
  border-radius:var(--r-sm); padding:5px 8px;
  display:flex; flex-direction:column; gap:1px;
}
.stat-chip-lbl { font-size:.52rem; color:var(--text2); text-transform:uppercase; letter-spacing:.8px; }
.stat-chip-val { font-size:.85rem; font-weight:600; color:var(--text); }

/* Section separator */
.sep {
  font-family:'Cinzel',serif; font-size:.55rem; letter-spacing:2px;
  color:var(--text3); text-transform:uppercase;
  display:flex; align-items:center; gap:6px; margin:2px 0;
}
.sep::before,.sep::after {
  content:''; flex:1; height:1px;
  background:linear-gradient(90deg,transparent,var(--border2),transparent);
}

/* ══════════════════════════════════════════════════════════
   LEFT PANEL
══════════════════════════════════════════════════════════ */
#left { overflow:hidden; }

/* Player card */
.player-card {
  background:var(--surface);
  border:1px solid var(--border2);
  border-radius:var(--r);
  padding:12px;
  position:relative;
  overflow:hidden;
}
.player-card::before {
  content:'';
  position:absolute; top:0; left:0; right:0; height:2px;
  background:linear-gradient(90deg,transparent,var(--gold),transparent);
}
.player-top { display:flex; align-items:center; gap:8px; margin-bottom:10px; }
.player-portrait {
  width:40px; height:40px; border-radius:50%;
  background:radial-gradient(circle,#1e1230,#0c0818);
  border:2px solid var(--gold-d);
  display:flex; align-items:center; justify-content:center;
  font-size:1.1rem;
  box-shadow:0 0 10px rgba(200,160,64,.2);
  flex-shrink:0;
}
.player-name { font-family:'Cinzel',serif; font-size:.85rem; color:var(--gold); margin-bottom:1px; }
.player-meta { font-size:.6rem; color:var(--text2); }
.player-level {
  position:absolute; top:10px; right:10px;
  font-family:'Cinzel',serif; font-size:.62rem;
  background:var(--raised); color:var(--gold-d);
  border:1px solid var(--border2); border-radius:20px;
  padding:2px 8px;
}
.gold-display {
  display:flex; align-items:center; gap:4px;
  font-size:.68rem; color:var(--gold);
  background:var(--raised); border:1px solid var(--border);
  border-radius:var(--r-sm); padding:4px 8px; margin-top:6px;
}

/* Companion card */
.companion-card {
  background:var(--surface);
  border:1px solid var(--border);
  border-radius:var(--r);
  padding:8px 10px;
  transition:border-color .2s;
}
.companion-card.inactive { opacity:.45; }
.companion-card.active   { border-color:var(--border2); }
.companion-card:hover:not(.inactive) { border-color:var(--blue); }
.comp-top { display:flex; align-items:center; gap:7px; margin-bottom:7px; }
.comp-portrait {
  width:30px; height:30px; border-radius:50%;
  display:flex; align-items:center; justify-content:center;
  font-size:.9rem; flex-shrink:0; border:2px solid;
}
.cp-cleric  { background:#0a0c18; border-color:#3060a0; }
.cp-warrior { background:#180a0a; border-color:#803020; }
.cp-arcane  { background:#100818; border-color:#601890; }
.comp-info { flex:1; min-width:0; }
.comp-name { font-family:'Cinzel',serif; font-size:.7rem; color:var(--text); }
.comp-role { font-size:.58rem; color:var(--text2); }
.comp-status { font-size:.58rem; }
.comp-status.alive { color:var(--green); }
.comp-status.incap { color:var(--crimson); }
.comp-ability-btn {
  width:100%; margin-top:5px;
  background:var(--raised); border:1px solid var(--border2);
  border-radius:var(--r-sm); padding:5px 8px;
  color:var(--text2); font-size:.62rem; cursor:pointer;
  transition:all .15s; text-align:left; font-family:'Inter',sans-serif;
  display:flex; justify-content:space-between; align-items:center;
}
.comp-ability-btn:hover:not(:disabled) {
  background:var(--panel); border-color:var(--blue); color:var(--text);
}
.comp-ability-btn:disabled { opacity:.3; cursor:not-allowed; }
.ability-cost { color:var(--blue); font-size:.58rem; }

/* Faction bars */
.faction-row { display:flex; flex-direction:column; gap:3px; }
.fac-top { display:flex; justify-content:space-between; align-items:center; }
.fac-name { font-size:.68rem; font-weight:500; }
.fac-rep  { font-size:.6rem; color:var(--text2); }
.fac-bar-track {
  height:5px; background:var(--bg);
  border-radius:3px; overflow:hidden;
  border:1px solid var(--border);
  position:relative;
}
.fac-bar-center {
  position:absolute; top:0; bottom:0;
  width:1px; background:var(--border2);
}
.fac-bar-fill {
  position:absolute; top:0; bottom:0;
  border-radius:3px;
  transition:all .5s ease;
}
.fac-positive { left:50%; }
.fac-negative { right:50%; }
.fac-desc { font-size:.57rem; color:var(--text3); }

/* ══════════════════════════════════════════════════════════
   CENTER PANEL
══════════════════════════════════════════════════════════ */
#center {
  display:flex; flex-direction:column; gap:8px; overflow:hidden;
}

/* Boss panel */
#boss-panel {
  flex-shrink:0;
  background:var(--panel);
  border:1px solid var(--border);
  border-radius:var(--r);
  overflow:hidden;
  position:relative;
  transition:border-color .6s, box-shadow .6s;
}
#boss-panel.phase1 { border-color:#362050; box-shadow:0 0 20px rgba(90,40,160,.15); }
#boss-panel.phase2 { border-color:#5a2808; box-shadow:0 0 20px rgba(180,80,20,.2); }
#boss-panel.phase3 { border-color:var(--crimson-d); box-shadow:0 0 28px rgba(180,30,30,.3); animation:phase3-pulse 2s ease-in-out infinite; }
@keyframes phase3-pulse {
  0%,100%{ box-shadow:0 0 28px rgba(180,30,30,.3); }
  50%    { box-shadow:0 0 40px rgba(220,40,40,.5); }
}
.boss-bg {
  position:absolute; inset:0; pointer-events:none;
  transition:background .8s ease;
}
.boss-bg.phase1 { background:radial-gradient(ellipse 80% 100% at 50% 100%,rgba(80,30,150,.2),transparent 70%); }
.boss-bg.phase2 { background:radial-gradient(ellipse 80% 100% at 50% 100%,rgba(160,60,10,.2),transparent 70%); }
.boss-bg.phase3 { background:radial-gradient(ellipse 80% 100% at 50% 100%,rgba(180,20,20,.3),transparent 70%); }

.boss-inner {
  position:relative; z-index:1;
  display:flex; align-items:center; gap:14px;
  padding:14px 16px;
}
.boss-portrait-wrap { flex-shrink:0; text-align:center; }
.boss-emoji {
  font-size:4.2rem; line-height:1;
  filter:drop-shadow(0 0 16px rgba(200,60,20,.5)) drop-shadow(0 4px 8px rgba(0,0,0,.8));
  animation:boss-breathe 3s ease-in-out infinite;
  display:block;
}
@keyframes boss-breathe {
  0%,100%{ transform:scale(1)   translateY(0); }
  50%    { transform:scale(1.04) translateY(-4px); }
}
.phase-pips { display:flex; gap:4px; justify-content:center; margin-top:5px; }
.phase-pip  { width:10px; height:10px; border-radius:50%; border:1px solid; }
.pip-done   { background:#cc3030; border-color:#ff4040; box-shadow:0 0 5px rgba(200,40,40,.6); }
.pip-active { border-color:var(--gold); background:var(--gold-d); box-shadow:0 0 5px rgba(200,160,64,.5); animation:pulse-gold 1.5s ease-in-out infinite; }
.pip-future { background:transparent; border-color:var(--border2); }

.boss-details { flex:1; min-width:0; }
.boss-name-row { display:flex; align-items:center; gap:8px; margin-bottom:2px; }
.boss-name {
  font-family:'Cinzel',serif; font-size:1.05rem;
  color:var(--crimson); text-shadow:0 0 12px rgba(180,40,40,.5);
}
.phase-badge {
  font-family:'Cinzel',serif; font-size:.58rem; letter-spacing:1px;
  padding:2px 8px; border-radius:20px;
}
.pb-p1 { background:#1a0e2a; color:#a070e0; border:1px solid #502880; }
.pb-p2 { background:#2a1006; color:#e08040; border:1px solid #803010; }
.pb-p3 { background:#1a0606; color:#ff6060; border:1px solid #801010; }
.boss-title { font-size:.65rem; color:var(--text2); font-style:italic; margin-bottom:10px; }

/* Boss HP bar with phase markers */
.boss-hp-outer { margin-bottom:8px; }
.boss-hp-header { display:flex; justify-content:space-between; font-size:.6rem; color:var(--text2); margin-bottom:3px; }
.boss-hp-track {
  height:14px; background:#180808;
  border-radius:5px; overflow:visible;
  border:1px solid #3a1010;
  position:relative;
}
.boss-hp-fill {
  height:100%; border-radius:5px;
  background:linear-gradient(90deg,#5a1010,#cc3030,#e85050);
  transition:width .6s ease;
  position:relative;
}
.boss-hp-fill::after {
  content:''; position:absolute; inset:0; border-radius:5px;
  background:linear-gradient(180deg,rgba(255,255,255,.12),transparent 50%);
}
.boss-hp-shimmer {
  position:absolute; top:0; bottom:0; width:30px;
  background:linear-gradient(90deg,transparent,rgba(255,255,255,.07),transparent);
  animation:shimmer 2.5s linear infinite;
  border-radius:5px;
}
@keyframes shimmer { from{left:-30px} to{left:100%} }
/* Phase boundary markers */
.phase-marker {
  position:absolute; top:-3px; bottom:-3px; width:2px;
  background:rgba(10,6,20,.9); z-index:2;
}
.phase-marker::before {
  content:attr(data-label); position:absolute; top:-14px; left:50%; transform:translateX(-50%);
  font-size:.52rem; color:var(--text3); white-space:nowrap;
}

/* ── Narrative box ── */
#narrative {
  background:var(--panel);
  border:1px solid var(--border);
  border-left:2px solid var(--gold-d);
  border-radius:var(--r);
  padding:12px 14px;
  flex-shrink:0;
}
.narr-label {
  font-family:'Cinzel',serif; font-size:.58rem; letter-spacing:2px;
  color:var(--gold-d); text-transform:uppercase; margin-bottom:8px;
  display:flex; align-items:center; gap:6px;
}
.narr-label::after { content:''; flex:1; height:1px; background:linear-gradient(90deg,var(--gold-d),transparent); }
#narr-text {
  font-family:'Crimson Pro',Georgia,serif;
  font-size:.95rem; line-height:1.7; color:#c8bfb8;
}
#narr-text .hl-enemy   { color:#e06060; font-style:normal; }
#narr-text .hl-player  { color:var(--gold); }
#narr-text .hl-comp    { color:#70a8f0; }
#narr-text .hl-event   { color:#c080f0; font-style:italic; }
#narr-text .hl-item    { color:var(--green); }

/* ── Action buttons ── */
#action-bar {
  display:grid; grid-template-columns:repeat(6,1fr); gap:6px; flex-shrink:0;
}
.act {
  display:flex; flex-direction:column; align-items:center; gap:4px;
  padding:10px 6px; border-radius:var(--r); cursor:pointer;
  font-family:'Inter',sans-serif; transition:all .15s;
  border:1px solid; position:relative; overflow:hidden;
  user-select:none;
}
.act::before {
  content:''; position:absolute; inset:0;
  background:linear-gradient(180deg,rgba(255,255,255,.05),transparent 60%);
  pointer-events:none;
}
.act:active:not(:disabled) { transform:scale(.96); }
.act:disabled { opacity:.35; cursor:not-allowed; }
.act-icon  { font-size:1.2rem; }
.act-label { font-size:.58rem; letter-spacing:1.2px; font-weight:600; text-transform:uppercase; }
.act-sub   { font-size:.52rem; opacity:.7; }

.act-strike {
  background:linear-gradient(135deg,#280808,#481010);
  border-color:#8a2020; color:#ff8080;
  box-shadow:0 0 10px rgba(200,40,40,.3);
  animation:glow-r 2.5s ease-in-out infinite;
}
.act-spell {
  background:linear-gradient(135deg,#160828,#281048);
  border-color:#602898; color:#c090ff;
  box-shadow:0 0 10px rgba(140,60,220,.25);
  animation:glow-p 2.5s ease-in-out infinite;
}
.act-comp {
  background:linear-gradient(135deg,#081020,#102040);
  border-color:#204080; color:#70b0f0;
  box-shadow:0 0 10px rgba(50,100,220,.25);
  animation:glow-b 2.5s ease-in-out infinite;
}
.act-defend {
  background:linear-gradient(135deg,#081820,#103040);
  border-color:#206080; color:#70d0c0;
  box-shadow:0 0 10px rgba(30,140,160,.2);
  animation:glow-t 2.5s ease-in-out infinite;
}
.act-item {
  background:linear-gradient(135deg,#181006,#302010);
  border-color:#705010; color:var(--gold);
  box-shadow:0 0 10px rgba(180,140,40,.2);
  animation:glow-g 2.5s ease-in-out infinite;
}
.act-flee {
  background:linear-gradient(135deg,#101010,#1c1c1c);
  border-color:#383838; color:#808080;
}
.act-flee:hover:not(:disabled) { border-color:#585858; color:#a0a0a0; }

@keyframes glow-r { 0%,100%{box-shadow:0 0 10px rgba(200,40,40,.3)} 50%{box-shadow:0 0 20px rgba(200,40,40,.6)} }
@keyframes glow-p { 0%,100%{box-shadow:0 0 10px rgba(140,60,220,.25)} 50%{box-shadow:0 0 20px rgba(140,60,220,.5)} }
@keyframes glow-b { 0%,100%{box-shadow:0 0 10px rgba(50,100,220,.25)} 50%{box-shadow:0 0 20px rgba(50,100,220,.5)} }
@keyframes glow-t { 0%,100%{box-shadow:0 0 10px rgba(30,140,160,.2)} 50%{box-shadow:0 0 20px rgba(30,140,160,.4)} }
@keyframes glow-g { 0%,100%{box-shadow:0 0 10px rgba(180,140,40,.2)} 50%{box-shadow:0 0 20px rgba(180,140,40,.45)} }

/* ── Spell overlay ── */
#spell-overlay {
  position:absolute; bottom:60px; left:0; right:0; z-index:50;
  background:var(--panel); border:1px solid #502898;
  border-radius:var(--r); padding:12px;
  box-shadow:0 0 24px rgba(120,60,220,.35);
  animation:fadeUp .2s ease;
}
#spell-overlay.hidden { display:none; }
@keyframes fadeUp { from{opacity:0;transform:translateY(10px)} to{opacity:1;transform:none} }
.spell-head { display:flex; justify-content:space-between; margin-bottom:10px; }
.spell-title { font-family:'Cinzel',serif; font-size:.68rem; color:#a080f0; letter-spacing:1px; }
.spell-close { background:none; border:1px solid #402060; color:#a080f0; font-size:.6rem; padding:2px 7px; border-radius:3px; cursor:pointer; }
.spell-grid  { display:grid; grid-template-columns:1fr 1fr; gap:6px; }
.spell-card  {
  background:var(--surface); border:1px solid var(--border2);
  border-radius:var(--r-sm); padding:8px; cursor:pointer;
  transition:all .15s; text-align:left;
}
.spell-card:hover { border-color:#7040c0; background:var(--raised); }
.spell-card-top { display:flex; align-items:center; gap:5px; margin-bottom:3px; }
.spell-icon   { font-size:.9rem; }
.spell-name   { font-size:.65rem; font-weight:600; color:#c090ff; }
.spell-cost   { font-size:.58rem; color:var(--blue); margin-left:auto; }
.spell-desc   { font-size:.58rem; color:var(--text2); line-height:1.3; }

/* ── Combat log ── */
#combat-log {
  flex:1; overflow-y:auto;
  background:var(--panel);
  border:1px solid var(--border);
  border-radius:var(--r);
  padding:8px 12px;
  min-height:80px;
  display:flex; flex-direction:column; gap:1px;
}
.log-line {
  font-size:.78rem; padding:3px 0; line-height:1.5;
  border-bottom:1px solid rgba(38,30,56,.6);
  animation:fadeIn .25s ease;
}
.log-line:last-child { border-bottom:none; }
.ll-attack  { color:#ff8060; }
.ll-enemy   { color:#e06060; }
.ll-spell   { color:#c090ff; }
.ll-comp    { color:#70b8f0; }
.ll-defend  { color:#70d0c0; }
.ll-item    { color:var(--green); }
.ll-event   { color:var(--gold); font-style:italic; }
.ll-system  { color:var(--text2); font-size:.7rem; }
.ll-phase   { color:var(--crimson); font-weight:600; font-family:'Cinzel',serif; font-size:.68rem; letter-spacing:.5px; }
@keyframes fadeIn { from{opacity:0;transform:translateY(3px)} to{opacity:1;transform:none} }

/* ── Floating damage ── */
.float-dmg {
  position:fixed; pointer-events:none; z-index:200;
  font-family:'Cinzel',serif; font-weight:700; font-size:1.2rem;
  animation:float-up 1.1s ease-out forwards;
}
.fd-enemy  { color:#ff6040; text-shadow:0 0 8px rgba(255,80,40,.6); }
.fd-player { color:#e03030; text-shadow:0 0 8px rgba(200,30,30,.5); }
.fd-heal   { color:#40e880; text-shadow:0 0 8px rgba(40,220,100,.5); }
.fd-miss   { color:#707090; }
@keyframes float-up { 0%{opacity:1;transform:translateY(0)} 70%{opacity:1} 100%{opacity:0;transform:translateY(-60px) scale(.7)} }

/* ── Screen flash ── */
#flash { position:fixed; inset:0; z-index:150; pointer-events:none; opacity:0; }
@keyframes do-flash { 0%{opacity:1} 100%{opacity:0} }

/* ══════════════════════════════════════════════════════════
   RIGHT PANEL
══════════════════════════════════════════════════════════ */

/* Story memory */
.memory-item {
  display:flex; align-items:flex-start; gap:6px;
  padding:5px 0; border-bottom:1px solid var(--border);
}
.memory-item:last-child { border-bottom:none; }
.mem-icon  { font-size:.8rem; flex-shrink:0; margin-top:1px; }
.mem-text  { font-size:.65rem; color:var(--text2); line-height:1.4; }
.mem-done  .mem-text { color:var(--text); }
.mem-done  .mem-icon { color:var(--green); }
.mem-pend  .mem-icon { color:var(--text3); }

/* Inventory */
#inv-grid {
  display:grid; grid-template-columns:1fr 1fr; gap:5px;
}
.inv-slot {
  background:var(--surface); border:1px solid var(--border);
  border-radius:var(--r-sm); padding:7px;
  cursor:pointer; transition:all .15s;
  position:relative; min-height:68px;
  display:flex; flex-direction:column; gap:2px;
}
.inv-slot.empty { opacity:.25; cursor:default; }
.inv-slot.equipped { border-color:var(--gold-d); }
.inv-slot:hover:not(.empty) { border-color:var(--border2); background:var(--raised); }
.inv-icon  { font-size:1.1rem; }
.inv-name  { font-size:.6rem; color:var(--text); line-height:1.2; font-weight:500; }
.inv-stat  { font-size:.57rem; color:var(--teal); }
.inv-cnt   { position:absolute; top:4px; right:5px; font-size:.58rem; color:var(--gold); font-weight:700; }
.inv-type  { font-size:.52rem; padding:1px 5px; border-radius:10px; margin-top:auto; width:fit-content; }
.t-weapon  { background:#1c0608; color:#e06060; border:1px solid #601018; }
.t-armor   { background:#060820; color:#6090e0; border:1px solid #102060; }
.t-consum  { background:#061606; color:#60d070; border:1px solid #165818; }
.t-gem     { background:#140618; color:#d080f0; border:1px solid #502060; }
.t-scroll  { background:#181006; color:var(--gold); border:1px solid #604010; }
.t-access  { background:#100c02; color:#c0a030; border:1px solid #504010; }

/* tooltip */
.inv-tip {
  display:none; position:absolute; bottom:calc(100% + 5px); left:0; right:0;
  background:#0e0918; border:1px solid var(--border2);
  border-radius:var(--r-sm); padding:7px 9px; z-index:100;
  box-shadow:0 4px 16px rgba(0,0,0,.7);
}
.inv-slot:hover .inv-tip { display:block; }
.tip-name { font-family:'Cinzel',serif; font-size:.62rem; color:var(--gold); margin-bottom:3px; }
.tip-desc { font-size:.6rem; color:var(--text2); line-height:1.4; }

/* Quest tracker */
.quest-item {
  background:var(--surface); border:1px solid var(--border);
  border-left:2px solid; border-radius:var(--r-sm);
  padding:7px 9px; cursor:default;
}
.quest-name { font-size:.65rem; font-weight:600; margin-bottom:2px; }
.quest-desc { font-size:.58rem; color:var(--text2); line-height:1.3; }
.quest-prog { font-size:.55rem; margin-top:4px; }
.q-main  { border-left-color:var(--gold); }
.q-main .quest-name { color:var(--gold); }
.q-side  { border-left-color:var(--blue); }
.q-side .quest-name { color:var(--blue); }
.q-fac   { border-left-color:var(--purple); }
.q-fac .quest-name { color:var(--purple); }

/* ══════════════════════════════════════════════════════════
   CENTER LAYOUT
══════════════════════════════════════════════════════════ */
#center-wrap {
  position:relative;
  display:flex; flex-direction:column; gap:8px;
  overflow:hidden;
}

/* ══════════════════════════════════════════════════════════
   RESPONSIVE
══════════════════════════════════════════════════════════ */
@media (max-width:900px) {
  #arena { grid-template-columns:1fr; overflow-y:auto; }
  html,body { overflow:auto; }
}
</style>
</head>
<body>

<!-- ═══════════════ HEADER ═══════════════════════════════ -->
<div id="hdr">
  <div class="hdr-brand">⚔ DARK REALM</div>
  <div class="hdr-divider"></div>
  <span class="hdr-tag">Visual Prototype</span>
  <div class="hdr-center">
    <div class="turn-display">Turn <span class="turn-num" id="turn-num">1</span></div>
    <div class="your-turn-badge" id="ytb">⚡ YOUR TURN</div>
  </div>
  <div class="hdr-right">
    <span class="sys-chip chip-running">● RUNNING</span>
    <span class="sys-chip chip-phase" id="phase-chip">PHASE 2</span>
    <span class="sys-chip chip-preview">PREVIEW MODE</span>
  </div>
</div>

<!-- ═══════════════ MAIN GRID ════════════════════════════ -->
<div id="arena">

  <!-- ────── LEFT PANEL ────── -->
  <div class="panel" id="left">
    <div class="panel-head"><span class="panel-title">Party Status</span></div>
    <div class="panel-body">

      <!-- Player card -->
      <div class="player-card">
        <div class="player-level" id="plvl">Lv. 12</div>
        <div class="player-top">
          <div class="player-portrait">🧙</div>
          <div>
            <div class="player-name" id="pname">Ash Valdenmere</div>
            <div class="player-meta" id="pmeta">Void Sorcerer · Chapter III</div>
          </div>
        </div>
        <div class="bar-wrap">
          <div class="bar-row">
            <span class="bar-lbl">HP</span>
            <div class="bar-track"><div class="bar-fill" id="php-fill" style="width:80%"></div></div>
            <span class="bar-nums" id="php-nums">72 / 90</span>
          </div>
          <div class="bar-row">
            <span class="bar-lbl">MP</span>
            <div class="bar-track"><div class="bar-fill mp-bar" id="pmp-fill" style="width:69%"></div></div>
            <span class="bar-nums" id="pmp-nums">55 / 80</span>
          </div>
        </div>
        <div class="stat-chips" style="margin-top:8px">
          <div class="stat-chip"><span class="stat-chip-lbl">ATK</span><span class="stat-chip-val" id="p-atk">28</span></div>
          <div class="stat-chip"><span class="stat-chip-lbl">DEF</span><span class="stat-chip-val" id="p-def">14</span></div>
          <div class="stat-chip"><span class="stat-chip-lbl">SPD</span><span class="stat-chip-val" id="p-spd">16</span></div>
          <div class="stat-chip"><span class="stat-chip-lbl">ARMOR</span><span class="stat-chip-val" id="p-arm">22</span></div>
        </div>
        <div class="statuses" style="margin-top:6px" id="player-statuses"></div>
        <div class="gold-display" style="margin-top:8px">
          💰 <span id="gold-val">1,847</span> gold
        </div>
      </div>

      <!-- XP bar -->
      <div style="display:flex;flex-direction:column;gap:3px">
        <div style="display:flex;justify-content:space-between;font-size:.58rem;color:var(--text2)">
          <span>Experience</span><span id="xp-txt">8,420 / 10,000</span>
        </div>
        <div class="bar-track" style="height:5px">
          <div class="bar-fill" style="background:linear-gradient(90deg,#402080,#9050d0);width:84%"></div>
        </div>
      </div>

      <div class="sep">Companions</div>

      <!-- Companions (rendered by JS) -->
      <div id="companions-list" style="display:flex;flex-direction:column;gap:6px"></div>

      <div class="sep">Faction Standing</div>

      <!-- Factions (rendered by JS) -->
      <div id="factions-list" style="display:flex;flex-direction:column;gap:8px"></div>

    </div>
  </div>

  <!-- ────── CENTER ────── -->
  <div id="center-wrap">

    <!-- Boss panel -->
    <div id="boss-panel" class="phase2">
      <div class="boss-bg phase2" id="boss-bg"></div>
      <div class="boss-inner">
        <div class="boss-portrait-wrap">
          <span class="boss-emoji" id="boss-emoji">💀</span>
          <div class="phase-pips" id="boss-pips"></div>
        </div>
        <div class="boss-details">
          <div class="boss-name-row">
            <div class="boss-name" id="boss-name">Valdris the Undying</div>
            <div class="phase-badge pb-p2" id="phase-badge">PHASE 2 — AWAKENED WRATH</div>
          </div>
          <div class="boss-title" id="boss-title">Herald of the Void Flame • Elder Lich of the Shattered Keep</div>
          <div class="boss-hp-outer">
            <div class="boss-hp-header">
              <span>❤ Vitality</span>
              <span id="boss-hp-nums">480 / 720</span>
            </div>
            <div class="boss-hp-track" id="boss-hp-track">
              <div class="boss-hp-fill" id="boss-hp-fill" style="width:66.7%">
                <div class="boss-hp-shimmer"></div>
              </div>
              <div class="phase-marker" style="left:66.7%" data-label="P2"></div>
              <div class="phase-marker" style="left:33.3%" data-label="P3"></div>
            </div>
          </div>
          <div class="statuses" id="boss-statuses"></div>
        </div>
      </div>
    </div>

    <!-- Narrative -->
    <div id="narrative">
      <div class="narr-label">📜 Narrative</div>
      <div id="narr-text"></div>
    </div>

    <!-- Action buttons -->
    <div id="action-bar">
      <button class="act act-strike" onclick="doStrike()" id="btn-strike">
        <span class="act-icon">⚔</span>
        <span class="act-label">Strike</span>
        <span class="act-sub">Melee</span>
      </button>
      <button class="act act-spell" onclick="toggleSpells()" id="btn-spell">
        <span class="act-icon">✦</span>
        <span class="act-label">Spell</span>
        <span class="act-sub" id="mp-cost-hint">MP</span>
      </button>
      <button class="act act-comp" onclick="doCompanion()" id="btn-comp">
        <span class="act-icon">👥</span>
        <span class="act-label">Ally</span>
        <span class="act-sub">Ability</span>
      </button>
      <button class="act act-defend" onclick="doDefend()" id="btn-defend">
        <span class="act-icon">🛡</span>
        <span class="act-label">Defend</span>
        <span class="act-sub">Stance</span>
      </button>
      <button class="act act-item" onclick="doItem()" id="btn-item">
        <span class="act-icon">🧪</span>
        <span class="act-label">Item</span>
        <span class="act-sub" id="potion-count">×3</span>
      </button>
      <button class="act act-flee" onclick="doFlee()" id="btn-flee">
        <span class="act-icon">💨</span>
        <span class="act-label">Flee</span>
        <span class="act-sub">50%</span>
      </button>
    </div>

    <!-- Spell overlay -->
    <div id="spell-overlay" class="hidden">
      <div class="spell-head">
        <div class="spell-title">✦ Spellbook — Ash Valdenmere</div>
        <button class="spell-close" onclick="toggleSpells()">✕</button>
      </div>
      <div class="spell-grid" id="spell-grid"></div>
    </div>

    <!-- Combat log -->
    <div id="combat-log"></div>

  </div>

  <!-- ────── RIGHT PANEL ────── -->
  <div class="panel" id="right">
    <div class="panel-head"><span class="panel-title">Chronicles & Arsenal</span></div>
    <div class="panel-body">

      <div class="sep">Story Memory</div>
      <div id="memory-list" style="display:flex;flex-direction:column;gap:0"></div>

      <div class="sep">Active Quests</div>
      <div id="quest-list" style="display:flex;flex-direction:column;gap:5px"></div>

      <div class="sep">Inventory</div>
      <div id="inv-grid"></div>

    </div>
  </div>

</div>

<!-- Flash overlay -->
<div id="flash"></div>

<!-- ═══════════════════════════════════════════════════════
     JAVASCRIPT — ALL MOCK DATA & INTERACTIONS
════════════════════════════════════════════════════════ -->
<script>
/* ────────────────────────────────────────────
   MOCK STATE  (no connection to game backend)
──────────────────────────────────────────── */
const G = {
  turn: 1,
  busy: false,
  defending: false,

  player: {
    name:'Ash Valdenmere', cls:'Void Sorcerer', level:12,
    hp:72, maxHp:90, mp:55, maxMp:80,
    atk:28, def:14, spd:16, armor:22, gold:1847,
    xp:8420, xpNext:10000,
    statuses:[]
  },

  boss: {
    name:'Valdris the Undying',
    title:'Herald of the Void Flame • Elder Lich of the Shattered Keep',
    emoji:'💀',
    hp:480, maxHp:720,
    phase:2, maxPhase:3,
    phaseNames:['Dormant Shell','Awakened Wrath','Primordial Rage'],
    statuses:['burn','weak'],
    phaseEmoji:['💀','🔥','☠️'],
  },

  companions: [
    { name:'Seraphina', role:'Divine Cleric', icon:'⛪', portraitCls:'cp-cleric',
      hp:58, maxHp:75, mp:40, maxMp:60,
      ability:'Holy Mend', cost:'20 MP', desc:'Restores 35 HP across the party.',
      statuses:['regen'], active:true },
    { name:'Dregan', role:'Iron Warrior', icon:'⚔', portraitCls:'cp-warrior',
      hp:95, maxHp:120, mp:0, maxMp:0,
      ability:'Shield Wall', cost:'—', desc:'Blocks next 2 incoming attacks.',
      statuses:['defend'], active:true },
    { name:'Zyx the Woven', role:'Arcane Sage', icon:'🔮', portraitCls:'cp-arcane',
      hp:18, maxHp:50, mp:70, maxMp:80,
      ability:'Void Rift', cost:'35 MP', desc:'Tears reality. 60+ AoE damage.',
      statuses:['silence'], active:false },
  ],

  factions: [
    { name:'Iron Covenant',    rep:65,  max:100, color:'#c09040', icon:'⚔', desc:'Military order — your oldest ally' },
    { name:'Circle of Embers', rep:30,  max:100, color:'#e06040', icon:'🔥', desc:'Fire mages — cautiously trusted' },
    { name:'Shadow Court',     rep:-25, max:100, color:'#9050d0', icon:'🌑', desc:'Rogues — hostile after Harwick' },
    { name:'The Old Faith',    rep:80,  max:100, color:'#38b060', icon:'⛪', desc:'Divine order — deeply loyal' },
  ],

  memory: [
    { done:true,  text:'Defeated the Cult of Ash in Thornwall' },
    { done:true,  text:'Freed the prisoners in Underhall' },
    { done:true,  text:'Claimed the First Throne Shard' },
    { done:true,  text:'Betrayed Merchant Harwick (Shadow Court −)' },
    { done:true,  text:'Discovered Valdris\'s true name' },
    { done:false, text:'Spared the Necromancer\'s Apprentice' },
    { done:false, text:'Restored the Old Faith Shrine' },
    { done:false, text:'Saved the village of Coldmere' },
  ],

  quests: [
    { name:'Shatter the Lich',      type:'q-main', desc:'Destroy Valdris before he opens the Void Gate.', prog:'Boss at Phase 2/3' },
    { name:'The Third Shard',       type:'q-side', desc:'Find the Throne Shard hidden in the Ashen Vault.', prog:'0 / 1 found' },
    { name:'Iron Covenant Mission', type:'q-fac',  desc:'Report Valdris\'s location to Commander Varek.', prog:'Pending' },
  ],

  inventory: [
    { name:'Voidfire Blade',   icon:'🗡️', type:'weapon', stat:'+32 ATK',  equipped:true,  desc:'Forged from void iron. Hums with dark energy.',      count:null },
    { name:'Obsidian Plate',   icon:'🛡️', type:'armor',  stat:'+18 DEF',  equipped:true,  desc:'Impossibly black. Fire cannot harm the wearer.',       count:null },
    { name:'Elixir of Mending',icon:'🧪', type:'consum', stat:'Heal 60 HP',equipped:false, desc:'Bottled moonlight. Heals wounds instantly.',            count:3   },
    { name:'Mana Prism',       icon:'💎', type:'gem',    stat:'+30 MP',    equipped:false, desc:'Crystallised arcane energy. Restores MP.',              count:2   },
    { name:'Amulet of Ages',   icon:'📿', type:'access', stat:'+12 All',   equipped:true,  desc:'Worn by the First Sorcerer. Ancient power.',            count:null },
    { name:'Binding Scroll',   icon:'📜', type:'scroll', stat:'Stun foe',  equipped:false, desc:'Chains the target in holy light for 2 turns.',          count:1   },
    { name:'Shadow Cloak',     icon:'🧥', type:'armor',  stat:'+15% EVA',  equipped:false, desc:'Woven from literal shadows. Grants evasion.',           count:null },
    { name:'Phoenix Ash',      icon:'🔥', type:'consum', stat:'Revive ally',equipped:false,'desc':'Rare. Returns a fallen companion at 30% HP.',          count:1   },
    null, null,
  ],

  spells: [
    { name:'Void Lance',    icon:'⚡', cost:'18 MP', desc:'Piercing bolt of void energy. Ignores armor.', dmg:[40,60] },
    { name:'Frost Prison',  icon:'❄️', cost:'25 MP', desc:'Encases target in ice. Stuns for 1 turn.',    dmg:[25,40] },
    { name:'Drain Soul',    icon:'💀', cost:'22 MP', desc:'Steals 30 HP from target. Heals caster.',     dmg:[28,38] },
    { name:'Meteor Strike', icon:'☄️', cost:'50 MP', desc:'Catastrophic AoE. Devastates all enemies.',    dmg:[70,100] },
  ],

  narratives: [
    `<span class="hl-enemy">Valdris the Undying</span> tears away his first form. Pale fire pours from the wound — not blood, but <em>memory</em>. The chamber shudders. Phase Two has begun.<br><br>He turns those hollow eye sockets toward you. Not with rage. With <em>recognition</em>. <span class="hl-event">"You carry the Shard,"</span> his voice reverberates through your ribs. <span class="hl-event">"Give it to me. I will make your end swift."</span>`,
    `<span class="hl-comp">Seraphina</span> grabs your arm. "Do not listen. The Shard is the only thing holding the Veil." <span class="hl-comp">Dregan</span> plants his shield in the fractured stone. "On your word, Ash."<br><br>The air tastes of ozone and ancient grief. The <span class="hl-enemy">Lich</span> raises one clawed hand. The torches die.`,
    `The ground cracks beneath <span class="hl-enemy">Valdris</span>. His form flickers — you glimpse something <em>behind</em> him, vast and formless, pressing against the veil of the world like a hand against wet paper.<br><br><span class="hl-event">"You cannot kill what is already dead,"</span> he says. <span class="hl-event">"You can only delay."</span> <span class="hl-comp">Zyx</span> whispers something broken in Arcane. "He's right. Unless we destroy the anchor."`,
  ],

  combatAttacks: [
    d=>`⚔ Ash channels void energy — <strong>Voidfire Strike</strong> lands for <strong>${d} damage!</strong>`,
    d=>`⚔ Ash lunges forward with the <span class="hl-item">Voidfire Blade</span> — <strong>${d} damage</strong> slips past Valdris's defenses!`,
    d=>`⚔ A burst of raw Sorcerer fury erupts from Ash's hands! <strong>${d} damage!</strong>`,
  ],
  enemyAttacks: [
    d=>`💀 <span class="hl-enemy">Valdris</span> unleashes a <strong>Void Scream</strong> — <strong>${d} damage</strong> to Ash!`,
    d=>`🔥 The Lich fires a bolt of pale fire — <strong>${d} damage!</strong> Ash's HP drops.`,
    d=>`💀 <span class="hl-enemy">Valdris</span> drains life force — Ash takes <strong>${d} damage</strong> and loses 8 MP!`,
  ],

  narIdx: 0,
  atkIdx: 0,
  potions: 3,
};

/* ────────────────────────────────────────────
   STATUS LABEL MAP
──────────────────────────────────────────── */
const STATUSES = {
  burn:   ['🔥 Burning',   's-burn'],
  bleed:  ['🩸 Bleeding',  's-bleed'],
  poison: ['☠ Poisoned',   's-poison'],
  stun:   ['💫 Stunned',   's-stun'],
  defend: ['🛡 Defending', 's-defend'],
  rage:   ['⚡ Enraged',   's-rage'],
  weak:   ['💔 Weakened',  's-weak'],
  silence:['🔇 Silenced',  's-silence'],
  regen:  ['💚 Regen',     's-regen'],
};

function badgeHTML(statuses) {
  return statuses.map(s => {
    const [lbl,cls] = STATUSES[s] || [s,'s-burn'];
    return `<span class="sbadge ${cls}">${lbl}</span>`;
  }).join('');
}

/* ────────────────────────────────────────────
   HP COLOR CLASS
──────────────────────────────────────────── */
function hpCls(pct) {
  return pct > 55 ? 'hp-hi' : pct > 28 ? 'hp-mid' : 'hp-lo';
}

/* ────────────────────────────────────────────
   FLOATING DAMAGE
──────────────────────────────────────────── */
function floatDmg(x, y, text, cls) {
  const el = document.createElement('div');
  el.className = `float-dmg ${cls}`;
  el.textContent = text;
  el.style.left = (x - 24) + 'px';
  el.style.top  = (y - 24) + 'px';
  document.body.appendChild(el);
  setTimeout(() => el.remove(), 1200);
}

/* ────────────────────────────────────────────
   SCREEN FLASH
──────────────────────────────────────────── */
function flash(color) {
  const el = document.getElementById('flash');
  el.style.background = color;
  el.style.animation = 'none';
  void el.offsetWidth;
  el.style.animation = 'do-flash .45s ease forwards';
}

/* ────────────────────────────────────────────
   COMBAT LOG
──────────────────────────────────────────── */
function clog(msg, cls='') {
  const box = document.getElementById('combat-log');
  const div = document.createElement('div');
  div.className = `log-line ${cls}`;
  div.innerHTML = msg;
  box.appendChild(div);
  box.scrollTop = box.scrollHeight;
  while (box.children.length > 40) box.removeChild(box.firstChild);
}

/* ────────────────────────────────────────────
   RENDER: PLAYER STATS
──────────────────────────────────────────── */
function renderPlayer() {
  const p = G.player;
  const hpPct = Math.max(0, Math.round(p.hp/p.maxHp*100));
  const mpPct = Math.max(0, Math.round(p.mp/p.maxMp*100));
  const fill = document.getElementById('php-fill');
  fill.className = `bar-fill ${hpCls(hpPct)}`;
  fill.style.width = hpPct + '%';
  document.getElementById('pmp-fill').style.width = mpPct + '%';
  document.getElementById('php-nums').textContent = `${p.hp} / ${p.maxHp}`;
  document.getElementById('pmp-nums').textContent = `${p.mp} / ${p.maxMp}`;
  document.getElementById('gold-val').textContent = p.gold.toLocaleString();
  document.getElementById('player-statuses').innerHTML = badgeHTML(p.statuses);
}

/* ────────────────────────────────────────────
   RENDER: BOSS
──────────────────────────────────────────── */
function renderBoss() {
  const b = G.boss;
  const pct = Math.max(0, Math.round(b.hp/b.maxHp*100));
  document.getElementById('boss-hp-fill').style.width = pct + '%';
  document.getElementById('boss-hp-nums').textContent = `${b.hp} / ${b.maxHp}`;
  document.getElementById('boss-statuses').innerHTML = badgeHTML(b.statuses);
  document.getElementById('boss-emoji').textContent = b.phaseEmoji[b.phase-1] || b.emoji;

  // Phase pips
  const pips = Array.from({length:b.maxPhase},(_,i)=>{
    const cls = i < b.phase-1 ? 'pip-done' : i === b.phase-1 ? 'pip-active' : 'pip-future';
    return `<div class="phase-pip ${cls}"></div>`;
  }).join('');
  document.getElementById('boss-pips').innerHTML = pips;

  // Phase visual classes
  const pCls = `phase${b.phase}`;
  document.getElementById('boss-panel').className = pCls;
  document.getElementById('boss-bg').className = `boss-bg ${pCls}`;

  const badgeCls = `phase-badge pb-p${b.phase}`;
  const badge = document.getElementById('phase-badge');
  badge.className = badgeCls;
  badge.textContent = `PHASE ${b.phase} — ${b.phaseNames[b.phase-1].toUpperCase()}`;
  document.getElementById('phase-chip').textContent = `PHASE ${b.phase}`;
}

/* ────────────────────────────────────────────
   RENDER: COMPANIONS
──────────────────────────────────────────── */
function renderCompanions() {
  const el = document.getElementById('companions-list');
  el.innerHTML = G.companions.map((c,i) => {
    const hpPct = Math.max(0, Math.round(c.hp/c.maxHp*100));
    const mpPct = c.maxMp ? Math.max(0, Math.round(c.mp/c.maxMp*100)) : 0;
    const inact = !c.active;
    return `
      <div class="companion-card ${inact?'inactive':'active'}">
        <div class="comp-top">
          <div class="comp-portrait ${c.portraitCls}">${c.icon}</div>
          <div class="comp-info">
            <div class="comp-name">${c.name}</div>
            <div class="comp-role">${c.role}</div>
          </div>
          <div class="comp-status ${inact?'incap':'alive'}">${inact?'⚠ Incap.':'● Active'}</div>
        </div>
        <div class="bar-wrap">
          <div class="bar-row">
            <span class="bar-lbl">HP</span>
            <div class="bar-track"><div class="bar-fill ${hpCls(hpPct)}" style="width:${hpPct}%"></div></div>
            <span class="bar-nums">${c.hp}/${c.maxHp}</span>
          </div>
          ${c.maxMp ? `<div class="bar-row">
            <span class="bar-lbl">MP</span>
            <div class="bar-track"><div class="bar-fill mp-bar" style="width:${mpPct}%"></div></div>
            <span class="bar-nums">${c.mp}/${c.maxMp}</span>
          </div>` : ''}
        </div>
        <div class="statuses" style="margin:4px 0">${badgeHTML(c.statuses)}</div>
        <button class="comp-ability-btn" onclick="useCompAbility(${i})" ${inact?'disabled':''}>
          <span>${c.ability} — <em style="color:var(--text2)">${c.desc}</em></span>
          <span class="ability-cost">${c.cost}</span>
        </button>
      </div>`;
  }).join('');
}

/* ────────────────────────────────────────────
   RENDER: FACTIONS
──────────────────────────────────────────── */
function renderFactions() {
  const el = document.getElementById('factions-list');
  el.innerHTML = G.factions.map(f => {
    const pct = Math.abs(f.rep) / f.max * 50;
    const positive = f.rep >= 0;
    return `
      <div class="faction-row">
        <div class="fac-top">
          <span class="fac-name" style="color:${f.color}">${f.icon} ${f.name}</span>
          <span class="fac-rep" style="color:${positive?'#60d080':'#e06060'}">${positive?'+':''}${f.rep}</span>
        </div>
        <div class="fac-bar-track">
          <div class="fac-bar-center" style="left:50%"></div>
          <div class="fac-bar-fill ${positive?'fac-positive':'fac-negative'}"
               style="background:${f.color};opacity:.75;width:${pct}%"></div>
        </div>
        <div class="fac-desc">${f.desc}</div>
      </div>`;
  }).join('');
}

/* ────────────────────────────────────────────
   RENDER: MEMORY + QUESTS
──────────────────────────────────────────── */
function renderMemory() {
  document.getElementById('memory-list').innerHTML = G.memory.map(m => `
    <div class="memory-item ${m.done?'mem-done':'mem-pend'}">
      <span class="mem-icon">${m.done?'✓':'○'}</span>
      <span class="mem-text">${m.text}</span>
    </div>`).join('');
}

function renderQuests() {
  document.getElementById('quest-list').innerHTML = G.quests.map(q => `
    <div class="quest-item ${q.type}">
      <div class="quest-name">${q.name}</div>
      <div class="quest-desc">${q.desc}</div>
      <div class="quest-prog" style="color:var(--text2)">◎ ${q.prog}</div>
    </div>`).join('');
}

/* ────────────────────────────────────────────
   RENDER: INVENTORY
──────────────────────────────────────────── */
function renderInventory() {
  const typeMap = {weapon:'t-weapon',armor:'t-armor',consum:'t-consum',gem:'t-gem',scroll:'t-scroll',access:'t-access'};
  document.getElementById('inv-grid').innerHTML = G.inventory.map(item => {
    if (!item) return `<div class="inv-slot empty"><div class="inv-icon">·</div></div>`;
    return `
      <div class="inv-slot ${item.equipped?'equipped':''}">
        ${item.count ? `<div class="inv-cnt">×${item.count}</div>` : ''}
        <div class="inv-icon">${item.icon}</div>
        <div class="inv-name">${item.name}</div>
        <div class="inv-stat">${item.stat}</div>
        <div class="inv-type ${typeMap[item.type]||'t-scroll'}">${item.type}</div>
        <div class="inv-tip">
          <div class="tip-name">${item.name}</div>
          <div class="tip-desc">${item.desc}</div>
        </div>
      </div>`;
  }).join('');
}

/* ────────────────────────────────────────────
   RENDER: NARRATIVE
──────────────────────────────────────────── */
function renderNarrative(idx) {
  document.getElementById('narr-text').innerHTML = G.narratives[idx % G.narratives.length];
}

/* ────────────────────────────────────────────
   RENDER: SPELLS
──────────────────────────────────────────── */
function renderSpells() {
  document.getElementById('spell-grid').innerHTML = G.spells.map(s => `
    <div class="spell-card" onclick="castSpell('${s.name}')">
      <div class="spell-card-top">
        <span class="spell-icon">${s.icon}</span>
        <span class="spell-name">${s.name}</span>
        <span class="spell-cost">${s.cost}</span>
      </div>
      <div class="spell-desc">${s.desc}</div>
    </div>`).join('');
}

/* ────────────────────────────────────────────
   BOSS PHASE CHECK
──────────────────────────────────────────── */
function checkBossPhase() {
  const b = G.boss;
  const pct = b.hp / b.maxHp;
  let newPhase = 1;
  if (pct <= 0.333) newPhase = 3;
  else if (pct <= 0.667) newPhase = 2;

  if (newPhase !== b.phase) {
    b.phase = newPhase;
    const names = ['', 'Dormant Shell', 'Awakened Wrath', 'PRIMORDIAL RAGE'];
    clog(`⚡ PHASE ${newPhase} — ${names[newPhase].toUpperCase()} ⚡`, 'll-phase');
    clog(`The Lich transforms. The air splits open. Something ancient enters the room.`, 'll-event');
    flash('rgba(180,30,30,.3)');
    G.narIdx = Math.min(newPhase - 1, G.narratives.length - 1);
    renderNarrative(G.narIdx);

    if (newPhase === 2) { b.statuses = ['burn','rage']; }
    if (newPhase === 3) { b.statuses = ['rage','regen']; b.emoji = '☠️'; }
  }
}

/* ────────────────────────────────────────────
   ENEMY TURN
──────────────────────────────────────────── */
function enemyTurn() {
  const b = G.boss;
  const p = G.player;

  let dmg = Math.floor(Math.random() * 20) + 12 + (b.phase * 5);
  if (G.defending) { dmg = Math.floor(dmg * 0.35); }

  p.hp = Math.max(0, p.hp - dmg);
  if (!G.defending) { flash('rgba(180,30,30,.25)'); }

  const msg = G.enemyAttacks[Math.floor(Math.random() * G.enemyAttacks.length)](dmg);
  clog(msg, 'll-enemy');

  // MP drain on phase 3
  if (b.phase === 3 && Math.random() < .4) {
    const mpDrain = Math.floor(Math.random() * 10) + 5;
    p.mp = Math.max(0, p.mp - mpDrain);
    clog(`💀 Valdris siphons ${mpDrain} MP from Ash!`, 'll-enemy');
  }

  // Burn DoT
  if (p.statuses.includes('burn')) {
    const dot = Math.floor(Math.random() * 6) + 3;
    p.hp = Math.max(0, p.hp - dot);
    clog(`🔥 Burning! Ash takes ${dot} fire damage.`, 'll-enemy');
  }

  G.defending = false;
  p.statuses = p.statuses.filter(s => s !== 'defend');

  // Gain small MP regen
  p.mp = Math.min(p.maxMp, p.mp + 4);

  renderPlayer();
  renderBoss();
}

/* ────────────────────────────────────────────
   TURN WRAPPER
──────────────────────────────────────────── */
function doTurn(playerFn) {
  if (G.busy || G.boss.hp <= 0) return;
  G.busy = true;
  setBtnsDisabled(true);
  G.turn++;
  document.getElementById('turn-num').textContent = G.turn;
  document.getElementById('ytb').style.opacity = '0.3';

  playerFn();
  checkBossPhase();
  renderPlayer();
  renderBoss();

  setTimeout(() => {
    if (G.boss.hp > 0 && G.player.hp > 0) {
      enemyTurn();
    }
    document.getElementById('ytb').style.opacity = '1';
    G.busy = false;
    setBtnsDisabled(false);
    updatePotionCount();
  }, 900);
}

function setBtnsDisabled(v) {
  ['strike','spell','comp','defend','item','flee'].forEach(id =>
    document.getElementById('btn-'+id).disabled = v);
}

/* ────────────────────────────────────────────
   ACTIONS
──────────────────────────────────────────── */
function doStrike() {
  doTurn(() => {
    const base = G.player.atk;
    const dmg = Math.floor(Math.random() * 20) + base - 10;
    G.boss.hp = Math.max(0, G.boss.hp - dmg);

    const msg = G.combatAttacks[G.atkIdx % G.combatAttacks.length](dmg);
    G.atkIdx++;
    clog(msg, 'll-attack');

    G.player.xp += Math.floor(dmg * .3);
    G.player.gold += Math.floor(Math.random() * 4);

    const bz = document.getElementById('boss-panel').getBoundingClientRect();
    floatDmg(bz.left + bz.width * .5 + (Math.random()-0.5)*40,
             bz.top  + bz.height * .4, '-' + dmg, 'fd-enemy');
  });
}

function toggleSpells() {
  document.getElementById('spell-overlay').classList.toggle('hidden');
}

function castSpell(name) {
  const sp = G.spells.find(s => s.name === name);
  if (!sp) return;
  const cost = parseInt(sp.cost);
  if (G.player.mp < cost) { clog(`✦ Not enough MP to cast ${name}!`, 'll-system'); return; }

  doTurn(() => {
    G.player.mp -= cost;
    const dmg = Math.floor(Math.random() * (sp.dmg[1]-sp.dmg[0])) + sp.dmg[0];
    G.boss.hp = Math.max(0, G.boss.hp - dmg);
    clog(`✦ Ash casts <strong>${name}</strong> — <strong>${dmg} damage!</strong>`, 'll-spell');
    flash('rgba(120,60,220,.2)');

    const bz = document.getElementById('boss-panel').getBoundingClientRect();
    floatDmg(bz.left + bz.width*.5, bz.top + bz.height*.3, '-'+dmg+'!', 'fd-enemy');

    // Special effects per spell
    if (name === 'Frost Prison') {
      if (!G.boss.statuses.includes('stun')) G.boss.statuses.push('stun');
      clog('❄ Valdris is frozen in place for 1 turn!', 'll-spell');
    }
    if (name === 'Drain Soul') {
      const heal = Math.floor(dmg * .6);
      G.player.hp = Math.min(G.player.maxHp, G.player.hp + heal);
      clog(`💀 Ash drains ${heal} HP back from the Lich.`, 'll-spell');
    }
  });
  toggleSpells();
}

function useCompAbility(idx) {
  const c = G.companions[idx];
  if (!c || !c.active) return;
  doTurn(() => {
    if (c.ability === 'Holy Mend') {
      const heal = 35;
      G.player.hp = Math.min(G.player.maxHp, G.player.hp + heal);
      clog(`⛪ <strong>${c.name}</strong> calls upon divine light — party healed for <strong>${heal} HP!</strong>`, 'll-comp');
      flash('rgba(40,180,100,.15)');
    } else if (c.ability === 'Shield Wall') {
      G.defending = true;
      if (!G.player.statuses.includes('defend')) G.player.statuses.push('defend');
      clog(`🛡 <strong>${c.name}</strong> raises the Shield Wall! Incoming damage reduced by 65%.`, 'll-comp');
    } else if (c.ability === 'Void Rift') {
      if (c.mp < 35) { clog(`🔮 ${c.name} lacks the MP to cast Void Rift!`, 'll-system'); return; }
      c.mp -= 35;
      const dmg = Math.floor(Math.random() * 40) + 60;
      G.boss.hp = Math.max(0, G.boss.hp - dmg);
      clog(`🔮 <strong>${c.name}</strong> tears open reality — VOID RIFT! <strong>${dmg} AoE damage!</strong>`, 'll-comp');
      flash('rgba(120,60,220,.3)');
    }
    renderCompanions();
  });
}

function doCompanion() {
  // Scroll to companions panel as visual cue
  const first = G.companions.find(c => c.active);
  if (!first) { clog('No active companions available.', 'll-system'); return; }
  document.getElementById('companions-list').scrollIntoView({behavior:'smooth',block:'nearest'});
  clog('👥 Choose a companion ability in the left panel.', 'll-system');
}

function doDefend() {
  doTurn(() => {
    G.defending = true;
    if (!G.player.statuses.includes('defend')) G.player.statuses.push('defend');
    clog('🛡 Ash takes a defensive stance. Incoming damage reduced by 65% this turn.', 'll-defend');
    flash('rgba(50,100,200,.15)');
  });
}

function doItem() {
  const potion = G.inventory.find(i => i && i.type === 'consum' && i.count > 0);
  if (!potion) { clog('No consumable items remaining.', 'll-system'); return; }
  doTurn(() => {
    if (potion.stat.includes('Heal')) {
      const heal = 60;
      G.player.hp = Math.min(G.player.maxHp, G.player.hp + heal);
      potion.count--;
      if (potion.count <= 0) G.inventory[G.inventory.indexOf(potion)] = null;
      clog(`🧪 Ash drinks the <strong>${potion.name}</strong> — restored <strong>${heal} HP!</strong>`, 'll-item');
      flash('rgba(40,220,100,.15)');
      const pc = document.querySelectorAll('.party-card')[0];
      if (pc) { const r = pc.getBoundingClientRect(); floatDmg(r.left + r.width*.5, r.top+30, '+'+heal+' HP', 'fd-heal'); }
    } else if (potion.stat.includes('MP')) {
      G.player.mp = Math.min(G.player.maxMp, G.player.mp + 30);
      potion.count--;
      if (potion.count <= 0) G.inventory[G.inventory.indexOf(potion)] = null;
      clog(`💎 Ash absorbs the <strong>${potion.name}</strong> — restored <strong>30 MP!</strong>`, 'll-item');
    }
    renderInventory();
    updatePotionCount();
  });
}

function doFlee() {
  if (G.busy) return;
  const success = Math.random() < .5;
  if (success) {
    clog('💨 Ash makes a desperate sprint toward the chamber exit...', 'll-system');
    setTimeout(() => clog('💨 Escape successful! The encounter ends. (Prototype: refresh to restart)', 'll-event'), 700);
    setBtnsDisabled(true);
  } else {
    clog('💨 Ash stumbles — the Lich''s aura holds you in place! Escape failed.', 'll-enemy');
    const dmg = Math.floor(Math.random() * 15) + 8;
    G.player.hp = Math.max(0, G.player.hp - dmg);
    clog(`💀 Valdris punishes the attempt — ${dmg} damage!`, 'll-enemy');
    flash('rgba(180,30,30,.25)');
    renderPlayer();
  }
}

/* ────────────────────────────────────────────
   HELPERS
──────────────────────────────────────────── */
function updatePotionCount() {
  const p = G.inventory.find(i => i && i.type === 'consum' && i.count > 0);
  document.getElementById('potion-count').textContent = p ? `×${p.count}` : '—';
  document.getElementById('mp-cost-hint').textContent = `${G.player.mp} MP`;
}

/* ────────────────────────────────────────────
   FULL RENDER
──────────────────────────────────────────── */
function renderAll() {
  renderPlayer();
  renderBoss();
  renderCompanions();
  renderFactions();
  renderMemory();
  renderQuests();
  renderInventory();
  renderSpells();
  renderNarrative(0);
  updatePotionCount();
}

/* ────────────────────────────────────────────
   INIT
──────────────────────────────────────────── */
renderAll();

// Opening log entries
setTimeout(()=>clog('📜 The battle for the Shattered Keep begins. Valdris has entered Phase 2.','ll-event'),200);
setTimeout(()=>clog('⚡ Turn 1 — Choose your action carefully.','ll-system'),500);
setTimeout(()=>clog(`💔 Seraphina tends to Zyx's wounds — Regen active.`,'ll-comp'),800);
</script>
</body>
</html>"""


# ─────────────────────────────────────────────────────────────────
#  ROUTES
# ─────────────────────────────────────────────────────────────────
@app.route("/")
def preview():
    return render_template_string(TEMPLATE)


# ─────────────────────────────────────────────────────────────────
#  ENTRY POINT
# ─────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
