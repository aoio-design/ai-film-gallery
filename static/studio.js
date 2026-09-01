/* ============================================================
   AOIO Studio — shared behavior
   Theme · accordions · focus mode · FAB agent drawer ·
   media strips · uploads · lightbox · toasts
   ============================================================
   FULL DESIGN NOTES for the "Talk to your agent" FAB + drawer
   (loop diagram, backend endpoints, response flow, how to reuse
   on a new page, gotchas): see docs/FAB-DESIGN.md in this repo.
   ============================================================ */

/* ---------- Theme (Apple light default, true dark mode) ---------- */
(function () {
  var t = localStorage.getItem('studio-theme');
  if (t === 'dark') document.documentElement.classList.add('dark');
})();
function toggleTheme() {
  var h = document.documentElement;
  var dark = h.classList.toggle('dark');
  localStorage.setItem('studio-theme', dark ? 'dark' : 'light');
  document.querySelectorAll('.theme-toggle').forEach(function (b) {
    b.textContent = dark ? '☀️' : '🌙';
  });
}

/* ---------- Accordions ---------- */
function toggleAcc(head) {
  head.closest('.acc').classList.toggle('open');
}

/* ---------- Toast ---------- */
var _toastTimer = null;
function toast(msg) {
  var el = document.getElementById('toast');
  if (!el) return;
  el.textContent = msg;
  el.classList.add('on');
  clearTimeout(_toastTimer);
  _toastTimer = setTimeout(function () { el.classList.remove('on'); }, 2600);
}

/* ---------- Lightbox ---------- */
var _lbZoom = 100;
function applyLightboxZoom() {
  var img = document.getElementById('lightbox-img');
  var pct = document.getElementById('zoomPct');
  var rng = document.getElementById('zoomRange');
  if (img) img.style.transform = 'scale(' + (_lbZoom / 100) + ')';
  if (pct) pct.textContent = _lbZoom + '%';
  if (rng) rng.value = _lbZoom;
}
function lightboxZoom(delta) {
  _lbZoom = Math.min(300, Math.max(50, _lbZoom + delta));
  applyLightboxZoom();
}
function lightboxZoomTo(v) {
  _lbZoom = parseInt(v, 10) || 100;
  applyLightboxZoom();
}
function openLightbox(src) {
  var lb = document.getElementById('lightbox');
  if (!lb) return;
  document.getElementById('lightbox-img').src = src;
  _lbZoom = 100;
  applyLightboxZoom();
  lb.classList.add('active');
}
function closeLightbox() {
  var lb = document.getElementById('lightbox');
  if (lb) lb.classList.remove('active');
}

/* ---------- Focus mode: 3 sections, edge bars, + / − ---------- */
function studioFocus(section) {
  document.body.classList.remove('focus-script', 'focus-preview', 'focus-shots');
  if (section) {
    document.body.classList.add('focus-' + section);
    try { localStorage.setItem('studio-focus', section); } catch (e) {}
  } else {
    try { localStorage.removeItem('studio-focus'); } catch (e) {}
  }
  window.dispatchEvent(new Event('studio-focus-change'));
}
function studioResetFocus() { studioFocus(null); }
(function () {
  try {
    var f = localStorage.getItem('studio-focus');
    if (f) document.body.classList.add('focus-' + f);
  } catch (e) {}
})();

/* ---------- "Talk to your agent" drawer ---------- */
var AGENT_CTX = null;   // {target, id, project, section, label}

function studioSetContext(ctx) { AGENT_CTX = ctx || null; renderAgentChip(); }
function agentContextLabel(ctx) {
  if (!ctx) return '';
  var bits = [];
  if (ctx.section) bits.push(ctx.section);
  if (ctx.label) bits.push(ctx.label);
  return bits.join(' · ');
}

/* ---------- Context capture: explicit CLICK only (never hover) ----------
   Hover-based capture was wrong: simply moving the mouse toward the FAB
   re-tagged the feedback with whatever card the cursor happened to cross.
   Context now changes ONLY when the user actually clicks something, and
   clearing it with the chip's ✕ stays cleared until the next click. */
function _accTitleOf(el) {
  var acc = el && el.closest ? el.closest('.acc') : null;
  if (!acc) return '';
  var t = acc.querySelector('.acc-title');
  return t ? t.textContent.trim() : '';
}

/* Episode script: tag the actual line (or selected line range) clicked. */
function studioScriptContext() {
  var ta = document.getElementById('episodeScript');
  if (!ta) { studioSetContext({ target: 'episode', section: 'Episode Script' }); return; }
  var val = ta.value, s = ta.selectionStart, e = ta.selectionEnd;
  var lineOf = function (i) { return val.slice(0, i).split('\n').length; };
  var l1 = lineOf(s), l2 = lineOf(e);
  var label = (e > s)
    ? (l1 === l2 ? 'line ' + l1 : 'lines ' + l1 + '\u2013' + l2)
    : 'line ' + l1;
  studioSetContext({ target: 'episode', project: ta.dataset.project,
                     section: 'Episode Script', label: label });
}

var STUDIO_CTX_OPTS = { project: null };
function studioInitContextCapture(opts) {
  STUDIO_CTX_OPTS = opts || { project: null };
  var proj = STUDIO_CTX_OPTS.project;
  // Expose the project id globally so the drawer's reply poller can filter by it
  if (window.studioProject === undefined) window.studioProject = proj;
  try { if (proj) sessionStorage.setItem('studio-project', proj); } catch (e) {}

  document.addEventListener('click', function (e) {
    var t = e.target;
    if (!t || !t.closest) return;
    // Never let chrome / the drawer itself change the context
    if (t.closest('#agentDrawer') || t.closest('.fab') || t.closest('#resetChip') ||
        t.closest('.edge-bar') || t.closest('.header') || t.closest('nav') ||
        t.closest('.sec-head') || t.closest('.lightbox')) return;

    // 1) Episode Script pane
    if (t.closest('.pane-script')) { studioScriptContext(); return; }

    // 2) Video Preview pane -> the clip currently loaded
    if (t.closest('.pane-player')) {
      var now = document.getElementById('playerNow');
      var id = (now && now.textContent && now.textContent.trim() !== '\u2014')
                 ? now.textContent.trim().split(' ')[0] : null;
      studioSetContext(id
        ? { target: 'shot', id: id, project: proj, section: 'Video Preview', label: id }
        : { target: null, project: proj, section: 'Video Preview' });
      return;
    }

    // 3) A shot card — include which row was clicked (Image Prompt / Video / ...)
    var card = t.closest('.shot');
    if (card) {
      var row = _accTitleOf(t);
      var sid = card.dataset.shot;
      studioSetContext({ target: 'shot', id: sid, project: proj, section: 'Shot List',
                         label: row ? (sid + ' \u00b7 ' + row) : sid });
      return;
    }

    // 4) An asset card (Character Bible) — include which field was clicked
    var asset = t.closest('.asset');
    if (asset) {
      var nameEl = asset.querySelector('.asset-name');
      var base = nameEl ? nameEl.textContent.trim() : asset.dataset.asset;
      var field = (t.dataset && t.dataset.field) ? t.dataset.field.replace(/_/g, ' ') : '';
      studioSetContext({ target: 'asset', id: asset.dataset.asset, project: proj,
                         section: 'Assets', label: field ? (base + ' \u00b7 ' + field) : base });
      return;
    }
  }, true);

  // Keep the script line label in step with the caret / selection
  var ta = document.getElementById('episodeScript');
  if (ta) {
    ['keyup', 'select', 'mouseup'].forEach(function (ev) {
      ta.addEventListener(ev, function () {
        if (AGENT_CTX && AGENT_CTX.target === 'episode') studioScriptContext();
      });
    });
  }
}

function renderAgentChip() {
  var chip = document.getElementById('agentChip');
  if (!chip) return;
  var label = agentContextLabel(AGENT_CTX);
  if (label) {
    chip.style.display = 'inline-flex';
    document.getElementById('agentChipText').textContent = '\u21b3 ' + label;
  } else {
    chip.style.display = 'none';
  }
}
function toggleDrawer(open) {
  var d = document.getElementById('agentDrawer');
  var bd = document.getElementById('drawerBackdrop');
  if (!d) return;
  var willOpen = (typeof open === 'boolean') ? open : !d.classList.contains('open');
  d.classList.toggle('open', willOpen);
  if (bd) bd.classList.toggle('open', willOpen);
  if (willOpen) {
    renderAgentChip();
    setTimeout(function () { var ta = document.getElementById('agentTa'); if (ta) ta.focus(); }, 250);
  }
}
function agentMsg(cls, text) {
  var box = document.getElementById('agentMsgs');
  if (!box) return;
  var el = document.createElement('div');
  el.className = 'msg ' + cls;
  el.textContent = text;
  box.appendChild(el);
  box.scrollTop = box.scrollHeight;
}
function clearAgentContext() { studioSetContext(null); }

function sendAgentFeedback() {
  var ta = document.getElementById('agentTa');
  var btn = document.getElementById('agentSend');
  var text = (ta.value || '').trim();
  if (!text) return;
  var payload = { text: text, context: AGENT_CTX || {} };
  var label = agentContextLabel(AGENT_CTX);
  btn.disabled = true;
  agentMsg('me', text);
  if (label) agentMsg('sys', '↳ ' + label);
  ta.value = '';
  fetch('/agent_feedback', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload)
  })
    .then(function (r) { return r.json(); })
    .then(function (d) {
      if (d.ok) agentMsg('sys', '✓ Sent to your agent');
      else agentMsg('sys', '⚠ ' + (d.error || 'Failed to send'));
    })
    .catch(function () { agentMsg('sys', '⚠ Network error — not sent'); })
    .finally(function () { btn.disabled = false; ta.focus(); });
}

/* Esc closes drawer + lightbox; Enter sends (Shift+Enter = newline) */
document.addEventListener('keydown', function (e) {
  if (e.key === 'Escape') { toggleDrawer(false); closeLightbox(); }
});
document.addEventListener('DOMContentLoaded', function () {
  var ta = document.getElementById('agentTa');
  if (ta) {
    ta.addEventListener('keydown', function (e) {
      if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); sendAgentFeedback(); }
    });
  }
});

/* ---------- Media strips: choose primary image / video ---------- */
function selectShotMedia(project, shot, kind, filename, el) {
  var field = (kind === 'image') ? 'primary_image' : 'primary_video';
  var fd = new FormData();
  fd.append('field', field);
  fd.append('value', filename);
  fetch('/p/' + project + '/' + shot + '/update', { method: 'POST', body: fd }).catch(function () {});
  var fb = new FormData();
  fb.append('text', '[approved ' + kind + '] ' + filename);
  fetch('/p/' + project + '/' + shot + '/feedback', { method: 'POST', body: fb }).catch(function () {});
  var main = document.getElementById('media-' + kind + '-' + shot);
  if (main) {
    var url = '/p/' + project + '/' + shot + '/file/' + encodeURIComponent(filename);
    if (kind === 'image') {
      main.innerHTML = '<img src="' + url + '" onclick="openLightbox(this.src)" alt="' + shot + ' image">';
    } else {
      main.innerHTML = '<video controls playsinline preload="metadata" src="' + url + '"></video>';
      if (window.onShotVideoReplaced) window.onShotVideoReplaced(shot, url);
    }
  }
  var strip = document.getElementById('strip-' + kind + '-' + shot);
  if (strip) {
    strip.querySelectorAll('.thumb').forEach(function (t) { t.classList.remove('sel'); });
    strip.querySelectorAll('.star').forEach(function (s) { s.classList.remove('on'); });
  }
  if (el) {
    el.classList.add('sel');
    var star = el.querySelector('.star');
    if (star) star.classList.add('on');
  }
}

/* ---------- Asset media strips: choose primary reference (single-star) ---------- */
function selectAssetMedia(scope, asset, filename, el) {
  var fd = new FormData();
  fd.append('field', 'primary_image');
  fd.append('value', filename);
  fetch('/a/' + scope + '/' + asset + '/update', { method: 'POST', body: fd }).catch(function () {});
  var fb = new FormData();
  fb.append('text', '[approved] ' + filename);
  fetch('/a/' + scope + '/' + asset + '/feedback', { method: 'POST', body: fb }).catch(function () {});
  var strip = el ? el.parentElement : null;
  if (strip) {
    strip.querySelectorAll('.thumb').forEach(function (t) { t.classList.remove('sel'); });
    strip.querySelectorAll('.star').forEach(function (s) { s.classList.remove('on'); });
  }
  if (el) {
    el.classList.add('sel');
    var star = el.querySelector('.star');
    if (star) star.classList.add('on');
  }
}

/* ---------- Uploads (multi-file, never overwrite) ---------- */
function studioUpload(project, shot, kind) {
  var inp = document.createElement('input');
  inp.type = 'file';
  inp.multiple = true;
  inp.accept = (kind === 'image')
    ? 'image/png,image/jpeg,image/webp,image/gif'
    : 'video/mp4,video/webm,video/quicktime';
  inp.onchange = function () {
    if (!inp.files || !inp.files.length) return;
    var fd = new FormData();
    for (var i = 0; i < inp.files.length; i++) fd.append('files', inp.files[i]);
    toast('Uploading ' + inp.files.length + ' file' + (inp.files.length > 1 ? 's' : '') + '…');
    fetch('/p/' + project + '/' + shot + '/upload', { method: 'POST', body: fd })
      .then(function (r) { return r.json(); })
      .then(function (d) {
        if (d.ok && d.saved.length) {
          toast('✓ Added ' + d.saved.length + ' file' + (d.saved.length > 1 ? 's' : '') + ' — refreshing');
          try { sessionStorage.setItem('studio-scroll', String(document.getElementById('scrollArea') ? document.getElementById('scrollArea').scrollLeft : 0)); } catch (e) {}
          setTimeout(function () { location.reload(); }, 700);
        } else {
          toast(d.skipped && d.skipped.length ? '⚠ Unsupported file type: ' + d.skipped.join(', ') : '⚠ Nothing uploaded');
        }
      })
      .catch(function () { toast('⚠ Upload failed'); });
  };
  inp.click();
}

/* Restore horizontal scroll on the shot strip after upload refresh */
document.addEventListener('DOMContentLoaded', function () {
  var sa = document.getElementById('scrollArea');
  if (!sa) return;
  try {
    var x = sessionStorage.getItem('studio-scroll');
    if (x !== null) { sa.scrollLeft = parseInt(x, 10) || 0; sessionStorage.removeItem('studio-scroll'); }
  } catch (e) {}
});
