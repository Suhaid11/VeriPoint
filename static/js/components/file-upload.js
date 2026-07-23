/**
 * VeriPoint — Dynamic Evidence File Upload Component
 */

document.addEventListener('DOMContentLoaded', () => {
  initFileUpload();
});

function initFileUpload() {
  const fileInput = document.getElementById('evidence-file-input');
  const previewContainer = document.getElementById('evidence-preview-container');

  if (!fileInput || !previewContainer) return;

  fileInput.addEventListener('change', (e) => {
    const files = Array.from(e.target.files);
    previewContainer.innerHTML = ''; // Clear previous

    if (files.length === 0) return;

    files.forEach((file, index) => {
      const card = document.createElement('div');
      card.className = 'card p-4 bg-subtle border-primary flex items-start gap-4 mb-3';

      const isImage = file.type.startsWith('image/');
      let mediaPreview = `<div class="w-12 h-12 bg-surface rounded flex items-center justify-center font-bold text-xs uppercase">${file.name.split('.').pop()}</div>`;

      if (isImage) {
        const url = URL.createObjectURL(file);
        mediaPreview = `<img src="${url}" class="w-12 h-12 object-cover rounded">`;
      }

      card.innerHTML = `
        ${mediaPreview}
        <div class="flex-1">
          <div class="font-semibold text-sm truncate max-w-xs">${file.name} (${(file.size / 1024 / 1024).toFixed(2)} MB)</div>
          <div class="grid grid-cols-2 gap-2 mt-2">
            <div>
              <label class="text-xs text-muted block mb-1">Evidence Type</label>
              <select name="evidence_types" class="form-control text-xs p-1">
                <option value="photo" ${file.type.startsWith('image/') ? 'selected' : ''}>Photo</option>
                <option value="invoice" ${file.name.toLowerCase().includes('invoice') ? 'selected' : ''}>Invoice</option>
                <option value="receipt" ${file.name.toLowerCase().includes('receipt') ? 'selected' : ''}>Receipt</option>
                <option value="document" ${file.type === 'application/pdf' ? 'selected' : ''}>Document (PDF)</option>
                <option value="screenshot">Screenshot</option>
              </select>
            </div>
            <div>
              <label class="text-xs text-muted block mb-1">Description / Caption</label>
              <input type="text" name="evidence_captions" placeholder="Describe this proof..." class="form-control text-xs p-1">
            </div>
          </div>
        </div>
      `;
      previewContainer.appendChild(card);
    });
  });
}
