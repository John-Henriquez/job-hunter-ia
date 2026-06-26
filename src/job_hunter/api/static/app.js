const API = '';
let currentPage = 1;
const PER_PAGE = 25;
let totalJobs = 0;
let fetchPolling = null;
let searchDebounce = null;

function escapeHTML(value) {
    return String(value ?? '').replace(/[&<>"']/g, char => ({
    '&': '&amp;',
    '<': '&lt;',
    '>': '&gt;',
    '"': '&quot;',
    "'": '&#39;',
    }[char]));
}

function safeURL(value) {
    try {
        const url = new URL(value, window.location.origin);
        return ['http:', 'https:'].includes(url.protocol) ? url.href : null;
    } catch(e) {
        return null;
    }
}

function mutedDash() {
    return '<span style="color:var(--muted)">—</span>';
}

function showError(message) {
    const el = document.getElementById('bannerError');
    el.textContent = message;
    el.classList.add('show');
}

function clearError() {
    const el = document.getElementById('bannerError');
    el.textContent = '';
    el.classList.remove('show');
}

async function apiFetch(url, options = {}) {
    let response;
    try {
        response = await fetch(url, options);
    } catch (e) {
        throw new Error('No se pudo conectar con el servidor');
    }
    if (!response.ok) {
        let detail = `HTTP ${response.status}`;
        try {
            const body = await response.json();
            if (body?.detail) detail = body.detail;
        } catch (e) { /* respuesta sin JSON, se usa el detail default */ }
        throw new Error(detail);
    }
    return response;
}

async function init() {
    await Promise.all([loadStats(), loadJobs(), loadFacets()]);
}

function facetFiltersExcept(exclude) {
    const params = new URLSearchParams();
    const search = document.getElementById('searchInput').value.trim();
    const source = document.getElementById('filterSource').value;
    const modality = document.getElementById('filterModality').value;
    const workMode = document.getElementById('filterWorkMode').value;
    const seniority = document.getElementById('filterSeniority').value;
    const applicationStatus = document.getElementById('filterApplicationStatus').value;
 
    if (search) params.set('search', search);
    if (source && exclude !== 'source') params.set('source', source);
    if (modality && exclude !== 'modality') params.set('modality', modality);
    if (workMode && exclude !== 'work_mode') params.set('work_mode', workMode);
    if (seniority && exclude !== 'seniority') params.set('seniority', seniority);
    if (applicationStatus && exclude !== 'application_status') params.set('application_status', applicationStatus);
 
    return params;
}
 
async function loadFacets() {
    try {
        const params = facetFiltersExcept(null);
        const r = await apiFetch(`${API}/jobs/facets?${params.toString()}`);
        const data = await r.json();
        populateSelect('filterSource', data.source, SOURCE_LABELS);
        populateSelect('filterModality', data.modality);
        populateSelect('filterWorkMode', data.work_mode, WORK_MODE_LABELS);
        populateSelect('filterSeniority', data.seniority);
    } catch(e) {
    // Los facets son una mejora de UX; si fallan, los selects mantienen
    // sus opciones previas y el resto de la app sigue funcionando.
    console.warn('No se pudieron cargar los facets:', e.message);
    }
}
 
const SOURCE_LABELS = { getonboard: 'GetOnBoard', arbeitnow: 'Arbeitnow' };
const WORK_MODE_LABELS = { remote: 'Remoto', hybrid: 'Híbrido', 'on-site': 'Presencial' };
 
function populateSelect(selectId, counts, labelMap = null) {
    const select = document.getElementById(selectId);
    const currentValue = select.value;
    const placeholder = select.options[0];
 
    const entries = Object.entries(counts || {}).sort((a, b) => b[1] - a[1]);
 
    select.innerHTML = '';
    select.appendChild(placeholder);
 
    for (const [value, count] of entries) {
        const option = document.createElement('option');
        option.value = value;
        const label = labelMap?.[value] || value;
        option.textContent = `${label} (${count.toLocaleString()})`;
        select.appendChild(option);
    }
 
    if (currentValue && entries.some(([v]) => v === currentValue)) {
        select.value = currentValue;
    }
}

async function loadStats() {
    try {
        const r = await apiFetch(`${API}/stats/`);
        const data = await r.json();
        document.getElementById('statTotal').textContent = data.total.toLocaleString();
        document.getElementById('statSources').textContent = Object.keys(data.by_source).length;
        document.getElementById('statRemote').textContent = data.by_source['arbeitnow'] 
            ? (data.by_source['getonboard'] || 0) + (data.by_source['arbeitnow'] || 0)
            : data.total;
        document.getElementById('statCategories').textContent = Object.keys(data.by_category).length;
        document.getElementById('headerTotal').textContent = `${Number(data.total || 0).toLocaleString()} vacantes`;
    } catch(e) {
        document.getElementById('headerTotal').textContent = 'API no disponible';
        showError(`No se pudieron cargar las estadísticas: ${e.message}`);
    }
}

function buildQueryParams() {
    const params = new URLSearchParams();
    const search = document.getElementById('searchInput').value.trim();
    const source = document.getElementById('filterSource').value;
    const modality = document.getElementById('filterModality').value;
    const workMode = document.getElementById('filterWorkMode').value;
    const seniority = document.getElementById('filterSeniority').value;
    const applicationStatus = document.getElementById('filterApplicationStatus').value;
 
    if (search) params.set('search', search);
    if (source) params.set('source', source);
    if (modality) params.set('modality', modality);
    if (workMode) params.set('work_mode', workMode);
    if (seniority) params.set('seniority', seniority);
    if (applicationStatus) params.set('application_status', applicationStatus);
    params.set('page', currentPage);
    params.set('per_page', PER_PAGE);

    return params;
}

async function loadJobs() {
    document.getElementById('jobsBody').innerHTML = 
        '<tr><td colspan="7"><div class="loading"><div class="spinner"></div> Cargando vacantes...</div></td></tr>';
    clearError();

    try {
        const params = buildQueryParams();
        const r = await apiFetch(`${API}/jobs/?${params.toString()}`);
        const data = await r.json();
 
        totalJobs = data.total;
        renderTable(data.data);
        renderPagination();
    } catch(e) {
        document.getElementById('jobsBody').innerHTML = 
            '<tr><td colspan="7"><div class="empty"><div class="empty-icon">⚠</div>Error al cargar vacantes</div></td></tr>';
        showError(`No se pudieron cargar las vacantes: ${e.message}`);
    }
}

function applyFilters() {
    currentPage = 1;
    loadJobs();
    loadFacets();
}

function onSearchInput() {
    clearTimeout(searchDebounce);
    searchDebounce = setTimeout(applyFilters, 350);
}

  function resetFilters() {
    document.getElementById('searchInput').value = '';
    document.getElementById('filterSource').value = '';
    document.getElementById('filterModality').value = '';
    document.getElementById('filterWorkMode').value = '';
    document.getElementById('filterSeniority').value = '';
    document.getElementById('filterApplicationStatus').value = '';
    applyFilters();
}

function renderTable(jobs) {
    document.getElementById('resultsInfo').textContent = `${totalJobs.toLocaleString()} vacantes`;
 
    if (jobs.length === 0) {
        document.getElementById('jobsBody').innerHTML =
            '<tr><td colspan="7"><div class="empty"><div class="empty-icon">🔍</div>Sin resultados para estos filtros</div></td></tr>';
    return;
    }
 
    document.getElementById('jobsBody').innerHTML = jobs.map(j => {
        const jobId = Number(j.id);
        if (!Number.isFinite(jobId)) return '';
 
        return `
        <tr onclick="openJob(${jobId})">
            <td>
            <div class="job-title">${escapeHTML(j.title || '—')}</div>
            <div class="job-company">${escapeHTML(j.company || '—')}</div>
        </td>
        <td>${workModeBadge(j.work_mode)}</td>
        <td>${j.seniority ? `<span class="badge badge-seniority">${escapeHTML(j.seniority)}</span>` : mutedDash()}</td>
        <td style="max-width:160px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;color:var(--muted);font-size:12px">${escapeHTML(j.category || '—')}</td>
        <td><span class="badge badge-source">${escapeHTML(j.source || '—')}</span></td>
        <td>${statusBadge(j.application_status)}</td>
        <td style="color:var(--muted);font-size:12px;font-family:var(--mono)">${formatDate(j.published_at)}</td>
        </tr>
    `;
    }).join('');
}

function workModeBadge(mode) {
    const map = {
        'remote': '<span class="badge badge-remote">Remoto</span>',
        'hybrid': '<span class="badge badge-hybrid">Híbrido</span>',
        'on-site': '<span class="badge badge-onsite">Presencial</span>',
    };
    return map[mode] || mutedDash();
}

function statusLabel(status) {
    return {
        saved: 'Guardada',
        applied: 'Postulada',
        interviewing: 'En proceso',
        discarded: 'Descartada',
    }[status] || 'Guardada';
}

function statusBadge(status) {
    const normalized = ['saved', 'applied', 'interviewing', 'discarded'].includes(status) ? status : 'saved';
    return `<span class="badge badge-status-${normalized}">${statusLabel(normalized)}</span>`;
}

function statusActions(jobId, currentStatus) {
    const statuses = ['saved', 'applied', 'interviewing', 'discarded'];
    return statuses.map(status => `
        <button
            type="button"
            class="status-btn ${status === currentStatus ? 'active' : ''}"
            onclick="updateApplicationStatus(${jobId}, '${status}')"
        >${statusLabel(status)}</button>
    `).join('');
}

function formatDate(iso) {
    if(!iso) return '—';
    const d = new Date(iso);
    return d.toLocaleDateString('es-CL', { day:'2-digit', month:'short', year:'numeric' });
}

function renderPagination() {
    const total = Math.ceil(totalJobs / PER_PAGE);
    if(total <= 1) { document.getElementById('pagination').innerHTML = ''; return; }

    let pages = '';
    const start = Math.max(1, currentPage - 2);
    const end = Math.min(total, currentPage + 2);

    if(start > 1) pages += `<button class="page-btn" onclick="goPage(1)">1</button>`;
    if(start > 2) pages += `<span style="color:var(--muted)">…</span>`;

    for(let i = start; i <= end; i++) {
        pages += `<button class="page-btn ${i === currentPage ? 'active' : ''}" onclick="goPage(${i})">${i}</button>`;
    }

    if(end < total - 1) pages += `<span style="color:var(--muted)">…</span>`;
    if(end < total) pages += `<button class="page-btn" onclick="goPage(${total})">${total}</button>`;

    document.getElementById('pagination').innerHTML = `
        <button class="page-btn" onclick="goPage(${currentPage-1})" ${currentPage===1?'disabled':''}>←</button>
        ${pages}
        <button class="page-btn" onclick="goPage(${currentPage+1})" ${currentPage===total?'disabled':''}>→</button>
        <span class="page-info">${currentPage} / ${total}</span>
    `;
}

function goPage(p) {
    const total = Math.ceil(totalJobs / PER_PAGE);
    if(p < 1 || p > total) return;
    currentPage = p;
    loadJobs();
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

async function openJob(id) {
    document.getElementById('modalBody').innerHTML = '<div class="loading"><div class="spinner"></div> Cargando...</div>';
    document.getElementById('modalOverlay').classList.add('open');
    document.body.style.overflow = 'hidden';

    try {
        const r = await apiFetch(`${API}/jobs/${id}`);
        const j = await r.json();
        const applyURL = safeURL(j.url);
        const jobId = Number(j.id);
        const currentStatus = ['saved', 'applied', 'interviewing', 'discarded'].includes(j.application_status)
            ? j.application_status
            : 'saved';

        document.getElementById('modalBody').innerHTML = `
            <div class="modal-title">${escapeHTML(j.title || '—')}</div>
            <div class="modal-company">${escapeHTML(j.company || 'Empresa no especificada')} · ${escapeHTML(j.location || '—')}</div>
            <div class="modal-badges">
                ${workModeBadge(j.work_mode)}
                ${j.seniority ? `<span class="badge badge-seniority">${escapeHTML(j.seniority)}</span>` : ''}
                ${j.modality ? `<span class="badge badge-source">${escapeHTML(j.modality)}</span>` : ''}
                <span class="badge badge-source">${escapeHTML(j.source || '—')}</span>
                ${j.category ? `<span class="badge badge-source">${escapeHTML(j.category)}</span>` : ''}
                ${statusBadge(currentStatus)}
            </div>

            <div class="modal-section">
                <div class="modal-meta">
                    <div class="meta-item">
                        <div class="meta-label">Salario</div>
                        <div class="meta-value">${escapeHTML(j.salary ? `$${j.salary}` : 'No especificado')}</div>
                    </div>

                    <div class="meta-item">
                        <div class="meta-label">Publicado</div>
                        <div class="meta-value">${formatDate(j.published_at)}</div>
                    </div>
                </div>
            </div>

            ${Number.isFinite(jobId) ? `
            <div class="modal-section">
                <h4>Estado</h4>
                <div class="status-actions">${statusActions(jobId, currentStatus)}</div>
            </div>
        ` : ''}

        ${j.description ? `
            <div class="modal-section">
                <h4>Descripción</h4>
                <div class="modal-description">${escapeHTML(j.description)}</div>
            </div>
        ` : ''}

        ${applyURL ? `<a href="${escapeHTML(applyURL)}" target="_blank" rel="noopener noreferrer" class="btn-apply">Ver oferta completa →</a>` : ''}
    `;
    } catch(e) {
        document.getElementById('modalBody').innerHTML = '<div class="empty">Error al cargar el detalle</div>';
    }
}

async function updateApplicationStatus(jobId, status) {
    const buttons = document.querySelectorAll('.status-btn');
    buttons.forEach(btn => btn.disabled = true);

    try {
        const r = await apiFetch(`${API}/jobs/${jobId}/status`, {
            method: 'PATCH',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ status }),
        });

        const updated = await r.json();
        await loadJobs();
        await openJob(updated.id);
    } catch(e) {
        buttons.forEach(btn => btn.disabled = false);
        showError(`No se pudo actualizar el estado: ${e.message}`);
    }
}

function closeModal(e) {
    if(e.target === document.getElementById('modalOverlay')) closeModalDirect();
}

function closeModalDirect() {
    document.getElementById('modalOverlay').classList.remove('open');
    document.body.style.overflow = '';
}

document.addEventListener('keydown', e => { if(e.key === 'Escape') closeModalDirect(); });

async function triggerFetch(provider) {
    const btns = document.querySelectorAll('.btn-refresh');
    btns.forEach(b => b.disabled = true);
    const statusEl = document.getElementById('fetchStatus');
    statusEl.className = 'fetch-status running';
    statusEl.textContent = `Iniciando fetch de ${provider}...`;

    try {
        const url = provider === 'all' ? `${API}/fetch/` : `${API}/fetch/${provider}`;
        await apiFetch(url, { method: 'POST' });
        statusEl.textContent = 'Descargando vacantes...';
        pollFetchStatus();
    } catch(e) {
        statusEl.className = 'fetch-status';
        statusEl.textContent = 'Error al iniciar fetch';
        btns.forEach(b => b.disabled = false);
    }
}

function pollFetchStatus() {
    if(fetchPolling) clearInterval(fetchPolling);
    fetchPolling = setInterval(async () => {
        try {
            const r = await apiFetch(`${API}/fetch/status`);
            const data = await r.json();
            const statusEl = document.getElementById('fetchStatus');
            const btns = document.querySelectorAll('.btn-refresh');

            if(!data.running) {
                clearInterval(fetchPolling);
                btns.forEach(b => b.disabled = false);
                statusEl.className = 'fetch-status done';
                if(data.last_result) {
                    statusEl.textContent = `✓ ${data.last_result.saved} guardados, ${data.last_result.skipped} duplicados`;
                } else {
                    statusEl.textContent = '✓ Completado';
                }
                await Promise.all([loadStats(), loadJobs()]);
                setTimeout(() => { statusEl.textContent = ''; statusEl.className = 'fetch-status'; }, 5000);
            }
        } catch(e) {
            clearInterval(fetchPolling);
            const statusEl = document.getElementById('fetchStatus');
            statusEl.className = 'fetch-status error';
            statusEl.textContent = `Error consultando estado: ${e.message}`;
            document.querySelectorAll('.btn-refresh').forEach(b => b.disabled = false);
        }
    }, 2000);
}

function toggleSidebar() {
    document.querySelector('aside').classList.toggle('open');
    document.getElementById('sidebarOverlay').classList.toggle('open');
}
 
function closeSidebar() {
    document.querySelector('aside').classList.remove('open');
    document.getElementById('sidebarOverlay').classList.remove('open');
}
 
init();