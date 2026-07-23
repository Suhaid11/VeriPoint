/**
 * VeriPoint — Evidence Lightbox Viewer Component
 */

document.addEventListener('DOMContentLoaded', () => {
  initEvidenceViewer();
});

function initEvidenceViewer() {
  document.querySelectorAll('.evidence-preview-trigger').forEach((trigger) => {
    trigger.addEventListener('click', (e) => {
      e.preventDefault();
      const fileUrl = trigger.dataset.fileUrl;
      const fileType = trigger.dataset.fileType;
      const filename = trigger.dataset.filename;
      const caption = trigger.dataset.caption;

      openEvidenceLightbox(fileUrl, fileType, filename, caption);
    });
  });
}

function openEvidenceLightbox(url, type, filename, caption) {
  let backdrop = document.getElementById('evidence-lightbox');

  if (!backdrop) {
    backdrop = document.createElement('div');
    backdrop.id = 'evidence-lightbox';
    backdrop.className = 'modal-backdrop';
    document.body.appendChild(backdrop);
  }

  const isImage = ['photo', 'screenshot'].includes(type) || url.match(/\.(jpg|jpeg|png|gif|webp)$/i);

  let contentHtml = '';
  if (isImage) {
    contentHtml = `<img src="${url}" alt="${caption || filename}" class="max-w-full max-h-[70vh] rounded shadow-lg mx-auto block">`;
  } else {
    contentHtml = `
      <div class="p-8 text-center bg-subtle rounded-lg">
        <i data-lucide="file-text" class="w-16 h-16 text-primary mx-auto mb-4"></i>
        <h4 class="mb-2">${filename}</h4>
        <p class="text-sm text-muted mb-4">This document format (${type}) can be opened in a new tab.</p>
        <a href="${url}" target="_blank" rel="noopener" class="btn btn-primary btn-sm">Open File in New Tab</a>
      </div>
    `;
  }

  backdrop.innerHTML = `
    <div class="modal-dialog max-w-3xl">
      <div class="modal-header">
        <h3 class="text-lg font-bold flex items-center gap-2">
          <i data-lucide="shield-check" class="text-accent"></i> Verified Evidence: ${filename}
        </h3>
        <button class="btn btn-secondary btn-icon" id="close-lightbox-btn">&times;</button>
      </div>
      <div class="modal-body text-center">
        ${contentHtml}
        ${caption ? `<p class="text-sm text-muted mt-4 italic">"${caption}"</p>` : ''}
      </div>
    </div>
  `;

  backdrop.classList.add('show');
  if (window.lucide) window.lucide.createIcons();

  const closeBtn = backdrop.querySelector('#close-lightbox-btn');
  closeBtn.addEventListener('click', () => backdrop.classList.remove('show'));

  backdrop.addEventListener('click', (e) => {
    if (e.target === backdrop) backdrop.classList.remove('show');
  });
}
