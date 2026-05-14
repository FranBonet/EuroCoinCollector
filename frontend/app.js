/* ============================================================
   EuroCoinCollector v4 — Frontend Application
   ============================================================ */

const API = 'http://localhost:8000';
let vistaFaltantes = false;
let cachePaises = [];

/* ── Colores de banderas por código ISO ──────────────────── */

const COLORES_BANDERA = {
    DE: { dir: 'horizontal', colores: ['#000000', '#DD0000', '#FFCC00'] },
    ES: { dir: 'horizontal', colores: ['#AA151B', '#F1BF00', '#F1BF00', '#AA151B'] },
    FR: { dir: 'vertical',   colores: ['#002395', '#FFFFFF', '#ED2939'] },
    IT: { dir: 'vertical',   colores: ['#009246', '#FFFFFF', '#CE2B37'] },
    GR: { dir: 'horizontal', colores: ['#0D5EAF', '#FFFFFF', '#0D5EAF', '#FFFFFF', '#0D5EAF'] },
    PT: { dir: 'vertical',   colores: ['#006600', '#006600', '#FF0000', '#FF0000', '#FF0000'] },
    AT: { dir: 'horizontal', colores: ['#ED2939', '#FFFFFF', '#ED2939'] },
    BE: { dir: 'vertical',   colores: ['#000000', '#FDDA24', '#EF3340'] },
    FI: { dir: 'horizontal', colores: ['#FFFFFF', '#003580', '#FFFFFF'] },
    LU: { dir: 'horizontal', colores: ['#EF3340', '#FFFFFF', '#00A1DE'] },
    NL: { dir: 'horizontal', colores: ['#AE1C28', '#FFFFFF', '#21468B'] },
    SM: { dir: 'horizontal', colores: ['#FFFFFF', '#73C2FB'] },
    VA: { dir: 'vertical',   colores: ['#FFE000', '#FFFFFF'] },
};

/* ── Utilidades DOM ──────────────────────────────────────── */

function $(id) { return document.getElementById(id); }
function setTexto(id, texto) { $(id).textContent = texto; }
function setHTML(id, html) { $(id).innerHTML = html; }
function mostrar(id) { $(id).style.display = ''; }
function ocultar(id) { $(id).style.display = 'none'; }
function valorInput(id) { return $(id).value; }
function setValorInput(id, valor) { $(id).value = valor; }

/* ── Fetch helpers ───────────────────────────────────────── */

function fetchJSON(url) { return fetch(`${API}${url}`).then(r => r.json()); }
function fetchPUT(url, body) { return fetch(`${API}${url}`, { method: 'PUT', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(body) }).then(r => r.json()); }
function fetchPOST(url, body) { return fetch(`${API}${url}`, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(body) }).then(r => r.json()); }
function fetchDELETE(url) { return fetch(`${API}${url}`, { method: 'DELETE' }); }
function fetchPATCH(url) { return fetch(`${API}${url}`, { method: 'PATCH' }).then(r => r.json()); }

/* ── Toast Notifications ─────────────────────────────────── */

function mostrarToast(mensaje, tipo) {
    const t = document.createElement('div');
    t.className = `toast toast-${tipo}`;
    t.textContent = mensaje;
    $('toast-container').appendChild(t);
    setTimeout(() => t.remove(), 3000);
}

/* ── Navegación ──────────────────────────────────────────── */

function inicializarNavegacion() { $('nav-tabs').addEventListener('click', _handleNavClick); }

function _handleNavClick(e) {
    if (e.target.classList.contains('nav-tab')) activarSeccion(e.target.dataset.section);
}

function activarSeccion(nombre) {
    document.querySelectorAll('.nav-tab').forEach(t => t.classList.remove('active'));
    document.querySelectorAll('.section').forEach(s => s.classList.remove('active'));
    document.querySelector(`[data-section="${nombre}"]`).classList.add('active');
    $(`section-${nombre}`).classList.add('active');
    const acciones = { dashboard: cargarDashboard, catalogo: cargarMonedas, coleccion: cargarColeccion, deseos: cargarDeseos, intercambios: cargarIntercambios };
    acciones[nombre]();
}

/* ── Generar bandera con imagen (flagcdn.com) ────────────── */

function crearBanderaCSS(codigo, grande) {
    if (!codigo) return `<span class="flag-fallback">??</span>`;
    const size = grande ? 'flag-lg' : 'flag-sm';
    const code = codigo.toLowerCase();
    const w = grande ? 80 : 40;
    return `<img class="flag-img ${size}" src="https://flagcdn.com/w${w}/${code}.png" alt="${codigo}" loading="lazy" onerror="handleFlagError(this,'${codigo}')">`;
}

function handleFlagError(img, codigo) {
    const span = document.createElement('span');
    span.className = 'flag-fallback';
    span.textContent = codigo;
    img.replaceWith(span);
}

/* ── Generar SVG de moneda (fallback) ────────────────────── */

function crearSVGMoneda(codigo, anyo) {
    const info = COLORES_BANDERA[codigo];
    const color1 = info ? info.colores[0] : '#666';
    return `<svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
        <defs>
            <linearGradient id="g${codigo}${anyo}" x1="0" y1="0" x2="1" y2="1">
                <stop offset="0%" stop-color="#D4A843"/>
                <stop offset="50%" stop-color="#F5CE5B"/>
                <stop offset="100%" stop-color="#C4963A"/>
            </linearGradient>
        </defs>
        <circle cx="50" cy="50" r="48" fill="url(#g${codigo}${anyo})" stroke="#B8860B" stroke-width="2"/>
        <circle cx="50" cy="50" r="38" fill="none" stroke="#B8860B" stroke-width="1.5" opacity="0.5"/>
        <circle cx="50" cy="50" r="35" fill="${color1}" opacity="0.15"/>
        <text x="50" y="42" text-anchor="middle" font-size="22" font-weight="bold" fill="#7A5C1F" font-family="serif">2€</text>
        <text x="50" y="62" text-anchor="middle" font-size="12" font-weight="bold" fill="#8B6F2F" font-family="sans-serif">${codigo || ''}</text>
        <text x="50" y="78" text-anchor="middle" font-size="10" fill="#8B6F2F" font-family="sans-serif">${anyo || ''}</text>
    </svg>`;
}

/* ── Imagen real de moneda (con fallback a SVG) ──────────── */

function crearImagenMoneda(moneda) {
    const imgUrl = moneda?.imagen_url;
    const codigo = moneda?.pais?.codigo_iso || '';
    const anyo = moneda?.anyo || '';
    if (imgUrl) {
        const cacheBuster = "v=1.3";
        return `<img class="coin-img" src="${imgUrl}?${cacheBuster}" alt="${moneda.nombre || ''}" loading="lazy" onerror="handleCoinImgError(this,'${codigo}','${anyo}')">` ;
    }
    return crearSVGMoneda(codigo, anyo);
}

const _imgCache = {};

function handleCoinImgError(img, codigo, anyo) {
    const parts = img.src.split('/');
    let filename = decodeURIComponent(parts.pop());
    // If it's a thumb URL, the original filename is the previous part
    if (img.src.includes('/thumb/') && parts.length > 0) {
        filename = decodeURIComponent(parts.pop());
    }
    
    if (_imgCache[filename] === 'fail') { img.outerHTML = crearSVGMoneda(codigo, anyo); return; }
    if (_imgCache[filename]) { img.onerror = null; img.src = _imgCache[filename]; return; }
    img.onerror = null;
    _resolverImagenWiki(filename).then(url => {
        if (url) { _imgCache[filename] = url; img.src = url; img.onerror = function() { this.outerHTML = crearSVGMoneda(codigo, anyo); }; }
        else { _imgCache[filename] = 'fail'; img.outerHTML = crearSVGMoneda(codigo, anyo); }
    });
}

async function _resolverImagenWiki(filename) {
    try {
        const langs = ['en', 'commons', 'de', 'es', 'fr', 'it', 'nl', 'el', 'pt', 'fi'];
        const apis = langs.map(lang => 
            lang === 'commons' 
            ? `https://commons.wikimedia.org/w/api.php?action=query&titles=File:${encodeURIComponent(filename)}&prop=imageinfo&iiprop=url&iiurlwidth=300&format=json&origin=*`
            : `https://${lang}.wikipedia.org/w/api.php?action=query&titles=File:${encodeURIComponent(filename)}&prop=imageinfo&iiprop=url&iiurlwidth=300&format=json&origin=*`
        );
        for (const apiUrl of apis) {
            const resp = await fetch(apiUrl);
            const data = await resp.json();
            const pages = data?.query?.pages;
            if (!pages) continue;
            const page = Object.values(pages)[0];
            const info = page?.imageinfo?.[0];
            if (info) return info.thumburl || info.url;
        }
    } catch (e) { console.warn('Wiki image resolve failed:', e); }
    return null;
}

/* ── Dashboard ───────────────────────────────────────────── */

function cargarDashboard() { Promise.all([cargarEstadisticas(), cargarMonedasDashboard()]); }

function cargarEstadisticas() {
    fetchJSON('/estadisticas').then(d => {
        setTexto('stat-catalogo', d.total_catalogo);
        setTexto('stat-poseidas', d.total_poseidas);
        setTexto('stat-cantidad', d.total_cantidad);
        setTexto('stat-valor', `${Number(d.valor_estimado).toFixed(2)}€`);
        setTexto('progress-percent', `${d.porcentaje_completado}%`);
        $('progress-fill').style.width = `${d.porcentaje_completado}%`;
    });
}

function cargarMonedasDashboard() {
    fetchJSON('/monedas').then(monedas => renderizarGrid('dashboard-coins', monedas.slice(0, 6), false));
}

/* ── Catálogo ────────────────────────────────────────────── */

function cargarPaises() {
    fetchJSON('/paises').then(paises => {
        cachePaises = paises;
        const opts = '<option value="">Todos los países</option>' +
            paises.map(p => `<option value="${p.id_pais}">${p.nombre}</option>`).join('');
        setHTML('filter-pais', opts);
        setHTML('filter-coleccion-pais', opts);
    });
}

function cargarMonedas() {
    const params = new URLSearchParams();
    const pais = valorInput('filter-pais');
    const tipo = valorInput('filter-tipo');
    const anyo = valorInput('filter-anyo');
    if (pais) params.set('pais', pais);
    if (tipo) params.set('tipo', tipo);
    if (anyo) params.set('anyo', anyo);
    fetchJSON(`/monedas?${params.toString()}`).then(monedas => renderizarGrid('catalogo-coins', monedas, false));
}

function limpiarFiltros() {
    setValorInput('filter-pais', '');
    setValorInput('filter-tipo', '');
    setValorInput('filter-anyo', '');
    cargarMonedas();
}

/* ── Renderizar Grid de Monedas ──────────────────────────── */

function renderizarGrid(containerId, monedas, isMissing) {
    if (!monedas.length) {
        setHTML(containerId, '<div class="empty-state"><div class="empty-state-icon">🏛️</div><div class="empty-state-text">No se encontraron monedas</div></div>');
        return;
    }
    setHTML(containerId, monedas.map(m => renderizarCoinCard(m, isMissing)).join(''));
}

function renderizarCoinCard(moneda, isMissing) {
    const codigo = moneda.pais?.codigo_iso || '';
    const pais = moneda.pais?.nombre || '—';
    const imagenMoneda = crearImagenMoneda(moneda);
    const missingClass = isMissing ? ' missing' : '';
    const missingBadge = isMissing ? '<span class="badge badge-missing">FALTA</span>' : '';

    return `<div class="coin-card${missingClass}">
        <div class="coin-card-header">
            <div class="coin-icon">${imagenMoneda}</div>
            <div class="coin-badges">
                <span class="badge badge-${moneda.tipo}">${moneda.tipo}</span>
                ${missingBadge}
            </div>
        </div>
        <div class="coin-card-body">
            <div class="coin-name">${moneda.nombre}</div>
            <div class="coin-meta">
                <span>${crearBanderaCSS(codigo, false)} ${pais}</span>
                <span>📅 ${moneda.anyo}</span>
            </div>
            <div class="coin-price">${moneda.precio_mercado ? Number(moneda.precio_mercado).toFixed(2) + '€' : '—'}</div>
        </div>
        <div class="coin-card-footer">
            <button class="btn btn-gold btn-sm" onclick="abrirModalColeccion(${moneda.id_moneda})">💰 Colección</button>
            <button class="btn btn-ghost btn-sm" onclick="abrirModalDeseo(${moneda.id_moneda})">⭐ Deseos</button>
        </div>
    </div>`;
}

/* ── Mi Colección ────────────────────────────────────────── */

function cargarColeccion() { vistaFaltantes ? _cargarFaltantes() : _cargarMisMonedas(); }

function _cargarMisMonedas() {
    const pais = valorInput('filter-coleccion-pais');
    fetchJSON(pais ? `/coleccion?pais=${pais}` : '/coleccion').then(renderizarColeccion);
}

function _cargarFaltantes() {
    const pais = valorInput('filter-coleccion-pais');
    fetchJSON(pais ? `/coleccion/faltantes?pais=${pais}` : '/coleccion/faltantes').then(renderizarFaltantes);
}

function renderizarColeccion(entradas) {
    if (!entradas.length) { setHTML('coleccion-coins', ''); mostrar('coleccion-empty'); return; }
    ocultar('coleccion-empty');
    setHTML('coleccion-coins', entradas.map(renderizarColeccionCard).join(''));
}

function renderizarColeccionCard(entrada) {
    const m = entrada.moneda;
    const codigo = m?.pais?.codigo_iso || '';
    const imagenMoneda = crearImagenMoneda(m);
    return `<div class="coin-card">
        <div class="coin-card-header">
            <div class="coin-icon">${imagenMoneda}</div>
            <div class="coin-badges"><span class="badge badge-owned">×${entrada.cantidad}</span></div>
        </div>
        <div class="coin-card-body">
            <div class="coin-name">${m?.nombre || '—'}</div>
            <div class="coin-meta">
                <span>${crearBanderaCSS(codigo, false)} ${m?.pais?.nombre || '—'}</span>
                <span>📅 ${m?.anyo || '—'}</span>
            </div>
            ${entrada.notas ? `<p style="color:var(--text-muted);font-size:0.8rem;margin-top:6px">📝 ${entrada.notas}</p>` : ''}
        </div>
        <div class="coin-card-footer">
            <button class="btn btn-gold btn-sm" onclick="abrirModalColeccion(${entrada.id_moneda})">✏️ Editar</button>
            <button class="btn btn-danger btn-sm" onclick="eliminarDeColeccion(${entrada.id_moneda})">🗑️ Eliminar</button>
        </div>
    </div>`;
}

function renderizarFaltantes(monedas) {
    if (!monedas.length) {
        setHTML('coleccion-coins', '');
        $('coleccion-empty').querySelector('.empty-state-text').textContent = '¡Tienes todas las monedas!';
        $('coleccion-empty').querySelector('.empty-state-icon').textContent = '🎉';
        mostrar('coleccion-empty'); return;
    }
    ocultar('coleccion-empty');
    setHTML('coleccion-coins', monedas.map(m => renderizarCoinCard(m, true)).join(''));
}

function toggleVistaMisMonedas() {
    vistaFaltantes = false;
    $('btn-mis-monedas').classList.add('toggle-active'); $('btn-mis-monedas').classList.remove('btn-ghost');
    $('btn-me-faltan').classList.remove('toggle-active'); $('btn-me-faltan').classList.add('btn-ghost');
    cargarColeccion();
}

function toggleVistaFaltantes() {
    vistaFaltantes = true;
    $('btn-me-faltan').classList.add('toggle-active'); $('btn-me-faltan').classList.remove('btn-ghost');
    $('btn-mis-monedas').classList.remove('toggle-active'); $('btn-mis-monedas').classList.add('btn-ghost');
    cargarColeccion();
}

/* ── Eliminar de Colección ───────────────────────────────── */

function eliminarDeColeccion(idMoneda) {
    if (!confirm('¿Estás seguro de eliminar esta moneda de tu colección?')) return;
    fetchDELETE(`/coleccion/${idMoneda}`).then(() => {
        mostrarToast('Moneda eliminada de la colección', 'success');
        cargarEstadisticas(); cargarMonedasDashboard(); cargarColeccion();
    }).catch(() => mostrarToast('Error al eliminar', 'error'));
}

/* ── Lista de Deseos ─────────────────────────────────────── */

function cargarDeseos() { fetchJSON('/lista_deseos').then(renderizarDeseos); }

function renderizarDeseos(deseos) {
    if (!deseos.length) { ocultar('deseos-table-container'); mostrar('deseos-empty'); return; }
    ocultar('deseos-empty'); mostrar('deseos-table-container');
    setHTML('deseos-tbody', deseos.map(d => {
        const ico = { alta: '🔴', media: '🟡', baja: '🔵' }[d.prioridad] || '⚪';
        return `<tr>
            <td>${crearBanderaCSS(d.moneda?.pais?.codigo_iso, false)} ${d.moneda?.nombre || '—'}</td>
            <td>${d.moneda?.pais?.nombre || '—'}</td>
            <td>${d.moneda?.anyo || '—'}</td>
            <td><span class="priority-${d.prioridad}">${ico} ${d.prioridad}</span></td>
            <td>${d.moneda?.precio_mercado ? Number(d.moneda.precio_mercado).toFixed(2) + '€' : '—'}</td>
            <td style="color:var(--text-muted)">${d.notas || '—'}</td>
            <td><button class="btn btn-danger btn-sm" onclick="eliminarDeseo(${d.id_moneda})">🗑️</button></td>
        </tr>`;
    }).join(''));
}

function eliminarDeseo(idMoneda) {
    fetchDELETE(`/lista_deseos/${idMoneda}`).then(() => { mostrarToast('Eliminada de deseos', 'success'); cargarDeseos(); });
}

/* ── Intercambios ────────────────────────────────────────── */

function cargarIntercambios() { fetchJSON('/intercambios').then(renderizarIntercambios); }

function renderizarIntercambios(intercambios) {
    if (!intercambios.length) { setHTML('intercambios-grid', ''); mostrar('intercambios-empty'); return; }
    ocultar('intercambios-empty');
    setHTML('intercambios-grid', intercambios.map(i => {
        const o = i.moneda_ofrecida; const b = i.moneda_buscada;
        const fecha = new Date(i.fecha_publicacion).toLocaleDateString('es-ES', { day: 'numeric', month: 'short', year: 'numeric' });
        const buscaHTML = b
            ? `<div class="intercambio-moneda"><span class="label">Busca:</span> ${crearBanderaCSS(b.pais?.codigo_iso, false)} ${b.nombre} (${b.anyo})</div>`
            : '<div class="intercambio-moneda"><span class="label">Busca:</span> Cualquier oferta</div>';
        return `<div class="intercambio-card ${i.estado}">
            <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:8px">
                <span class="intercambio-usuario">👤 ${i.nombre_usuario}</span>
                <span class="badge badge-${i.estado}">${i.estado}</span>
            </div>
            <div class="intercambio-detalle">
                <div class="intercambio-moneda"><span class="label">Ofrece:</span> ${crearBanderaCSS(o?.pais?.codigo_iso, false)} ${o?.nombre || '—'} (${o?.anyo || '—'})</div>
                ${buscaHTML}
            </div>
            ${i.descripcion ? `<div class="intercambio-descripcion">"${i.descripcion}"</div>` : ''}
            <div class="intercambio-contacto">📧 ${i.contacto}</div>
            <div class="intercambio-fecha">📅 ${fecha}</div>
            <div class="intercambio-acciones">
                ${i.estado === 'activo' ? `<button class="btn btn-gold btn-sm" onclick="cerrarIntercambio(${i.id_intercambio})">✅ Cerrar</button>` : ''}
                <button class="btn btn-danger btn-sm" onclick="eliminarIntercambio(${i.id_intercambio})">🗑️</button>
            </div>
        </div>`;
    }).join(''));
}

/* ── Modales ──────────────────────────────────────────────── */

function abrirModalColeccion(id) { setValorInput('modal-col-id', id); setValorInput('modal-col-cantidad', 1); setValorInput('modal-col-fecha', ''); setValorInput('modal-col-notas', ''); $('modal-coleccion').classList.add('active'); }
function cerrarModalColeccion() { $('modal-coleccion').classList.remove('active'); }

function guardarColeccion() {
    fetchPUT(`/coleccion/${valorInput('modal-col-id')}`, {
        cantidad: parseInt(valorInput('modal-col-cantidad')) || 1,
        fecha: valorInput('modal-col-fecha') || null,
        notas: valorInput('modal-col-notas') || null,
    }).then(() => { cerrarModalColeccion(); mostrarToast('Moneda añadida a la colección', 'success'); cargarEstadisticas(); cargarMonedasDashboard(); })
      .catch(() => mostrarToast('Error al guardar', 'error'));
}

function abrirModalDeseo(id) { setValorInput('modal-deseo-id', id); setValorInput('modal-deseo-prioridad', 'media'); setValorInput('modal-deseo-notas', ''); $('modal-deseo').classList.add('active'); }
function cerrarModalDeseo() { $('modal-deseo').classList.remove('active'); }

function guardarDeseo() {
    fetchPOST(`/lista_deseos/${valorInput('modal-deseo-id')}`, {
        prioridad: valorInput('modal-deseo-prioridad'),
        notas: valorInput('modal-deseo-notas') || null,
    }).then(r => { if (r.detail) { mostrarToast(r.detail, 'error'); return; } cerrarModalDeseo(); mostrarToast('Añadida a deseos', 'success'); })
      .catch(() => mostrarToast('Error', 'error'));
}

function abrirModalIntercambio() {
    fetchJSON('/monedas').then(monedas => {
        const opts = '<option value="">— Selecciona moneda —</option>' + monedas.map(m => `<option value="${m.id_moneda}">${m.pais?.codigo_iso} | ${m.nombre} (${m.anyo})</option>`).join('');
        setHTML('modal-inter-ofrecida', opts);
        setHTML('modal-inter-buscada', '<option value="">— Cualquiera —</option>' + monedas.map(m => `<option value="${m.id_moneda}">${m.pais?.codigo_iso} | ${m.nombre} (${m.anyo})</option>`).join(''));
    });
    setValorInput('modal-inter-usuario', ''); setValorInput('modal-inter-contacto', '');
    setValorInput('modal-inter-ofrecida', ''); setValorInput('modal-inter-buscada', '');
    setValorInput('modal-inter-descripcion', '');
    $('modal-intercambio').classList.add('active');
}

function cerrarModalIntercambio() { $('modal-intercambio').classList.remove('active'); }

function guardarIntercambio() {
    const datos = {
        nombre_usuario: valorInput('modal-inter-usuario'),
        id_moneda_ofrecida: parseInt(valorInput('modal-inter-ofrecida')) || 0,
        id_moneda_buscada: parseInt(valorInput('modal-inter-buscada')) || null,
        descripcion: valorInput('modal-inter-descripcion') || null,
        contacto: valorInput('modal-inter-contacto'),
    };
    if (!datos.nombre_usuario || !datos.id_moneda_ofrecida || !datos.contacto) { mostrarToast('Rellena los campos obligatorios', 'error'); return; }
    fetchPOST('/intercambios', datos).then(r => {
        if (r.detail) { mostrarToast(r.detail, 'error'); return; }
        cerrarModalIntercambio(); mostrarToast('Intercambio publicado', 'success'); cargarIntercambios();
    }).catch(() => mostrarToast('Error al publicar', 'error'));
}

function cerrarIntercambio(id) { if (!confirm('¿Cerrar este intercambio?')) return; fetchPATCH(`/intercambios/${id}/cerrar`).then(() => { mostrarToast('Cerrado', 'success'); cargarIntercambios(); }); }
function eliminarIntercambio(id) { if (!confirm('¿Eliminar?')) return; fetchDELETE(`/intercambios/${id}`).then(() => { mostrarToast('Eliminado', 'success'); cargarIntercambios(); }); }

/* ── Exportar ────────────────────────────────────────────── */

function exportarCSV() { window.open(`${API}/exportar/csv`, '_blank'); }

/* ── Cerrar Modales con Overlay ──────────────────────────── */

function inicializarModales() {
    ['modal-coleccion', 'modal-deseo', 'modal-intercambio'].forEach(id => {
        $(id).addEventListener('click', e => { if (e.target.id === id) $(id).classList.remove('active'); });
    });
}

/* ── Inicialización ──────────────────────────────────────── */

document.addEventListener('DOMContentLoaded', () => {
    inicializarNavegacion();
    inicializarModales();
    cargarPaises();
    cargarDashboard();
});
