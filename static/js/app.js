/**
 * VeriPoint — Main Application JavaScript
 * Single light theme. No dark mode.
 */

document.addEventListener('DOMContentLoaded', () => {
  initLucideIcons();
  initToasts();
  initVoteHandlers();
  initBookmarkHandlers();
});

/* ==========================================================================
   LUCIDE ICONS
   ========================================================================== */
function initLucideIcons() {
  if (window.lucide) {
    window.lucide.createIcons();
  }
}

/* ==========================================================================
   TOAST AUTO-DISMISS
   ========================================================================== */
function initToasts() {
  document.querySelectorAll('.toast').forEach((toast) => {
    setTimeout(() => {
      toast.style.opacity = '0';
      toast.style.transform = 'translateX(100%)';
      setTimeout(() => toast.remove(), 350);
    }, 5000);
  });
}

/* ==========================================================================
   AJAX VOTING
   ========================================================================== */
function initVoteHandlers() {
  document.querySelectorAll('.btn-vote').forEach((btn) => {
    btn.addEventListener('click', async (e) => {
      e.preventDefault();
      const reviewId = btn.dataset.reviewId;
      const value = btn.dataset.value;
      const csrfToken = getCsrfToken();

      if (!csrfToken) {
        window.location.href = '/accounts/login/';
        return;
      }

      try {
        const response = await fetch(`/community/vote/${reviewId}/`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-CSRFToken': csrfToken,
          },
          body: `value=${value}`,
        });

        if (response.ok) {
          const data = await response.json();
          const voteContainer = btn.closest('.vote-container');
          if (voteContainer) {
            const scoreEl = voteContainer.querySelector('.vote-score');
            if (scoreEl) scoreEl.textContent = data.vote_score;
          }
        } else if (response.status === 403) {
          showToast('You cannot vote on your own review.', 'warning');
        }
      } catch (err) {
        console.error('Vote error:', err);
      }
    });
  });
}

/* ==========================================================================
   AJAX BOOKMARKING
   ========================================================================== */
function initBookmarkHandlers() {
  document.querySelectorAll('.btn-bookmark').forEach((btn) => {
    btn.addEventListener('click', async (e) => {
      e.preventDefault();
      const type = btn.dataset.type;
      const id = btn.dataset.id;
      const csrfToken = getCsrfToken();

      if (!csrfToken) {
        window.location.href = '/accounts/login/';
        return;
      }

      try {
        const response = await fetch('/community/bookmark/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-CSRFToken': csrfToken,
          },
          body: `type=${type}&id=${id}`,
        });

        if (response.ok) {
          const data = await response.json();
          const spanEl = btn.querySelector('span');
          if (data.bookmarked) {
            btn.classList.add('bookmarked');
            if (spanEl) spanEl.textContent = 'Saved';
            showToast('Saved to bookmarks', 'success');
          } else {
            btn.classList.remove('bookmarked');
            if (spanEl) spanEl.textContent = 'Save Bookmark';
            showToast('Removed from bookmarks', 'info');
          }
        }
      } catch (err) {
        console.error('Bookmark error:', err);
      }
    });
  });
}

/* ==========================================================================
   HELPERS
   ========================================================================== */
function getCsrfToken() {
  const cookie = document.cookie.split('; ').find(row => row.startsWith('csrftoken='));
  return cookie ? cookie.split('=')[1] : '';
}

function showToast(message, type = 'info') {
  let container = document.querySelector('.toast-container');
  if (!container) {
    container = document.createElement('div');
    container.className = 'toast-container';
    container.setAttribute('role', 'alert');
    container.setAttribute('aria-live', 'polite');
    document.body.appendChild(container);
  }

  const toast = document.createElement('div');
  toast.className = `toast toast-${type}`;
  toast.setAttribute('role', 'status');
  toast.innerHTML = `<span>${message}</span>`;
  container.appendChild(toast);

  setTimeout(() => {
    toast.style.opacity = '0';
    toast.style.transform = 'translateX(100%)';
    setTimeout(() => toast.remove(), 350);
  }, 4500);
}
