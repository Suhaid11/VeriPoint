/**
 * VeriPoint — Main JavaScript Engine
 */

document.addEventListener('DOMContentLoaded', () => {
  initTheme();
  initThemeToggle();
  initLucideIcons();
  initToasts();
  initVoteHandlers();
  initBookmarkHandlers();
});

/* --- Theme System --- */
function initTheme() {
  const savedTheme = localStorage.getItem('veripoint_theme');
  if (savedTheme) {
    document.documentElement.setAttribute('data-theme', savedTheme);
  } else if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
    document.documentElement.setAttribute('data-theme', 'dark');
  } else {
    document.documentElement.setAttribute('data-theme', 'light');
  }
}

function initThemeToggle() {
  const toggleBtn = document.getElementById('theme-toggle-btn');
  if (!toggleBtn) return;

  toggleBtn.addEventListener('click', () => {
    const currentTheme = document.documentElement.getAttribute('data-theme');
    const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
    document.documentElement.setAttribute('data-theme', newTheme);
    localStorage.setItem('veripoint_theme', newTheme);
  });
}

/* --- Lucide Icons Auto-render --- */
function initLucideIcons() {
  if (window.lucide) {
    window.lucide.createIcons();
  }
}

/* --- Toast Auto-dismiss --- */
function initToasts() {
  const toasts = document.querySelectorAll('.toast');
  toasts.forEach((toast) => {
    setTimeout(() => {
      toast.style.opacity = '0';
      toast.style.transform = 'translateX(100%)';
      setTimeout(() => toast.remove(), 300);
    }, 5000);
  });
}

/* --- AJAX Voting --- */
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
          // Update vote UI
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

/* --- AJAX Bookmarking --- */
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
          if (data.bookmarked) {
            btn.classList.add('bookmarked');
            showToast('Saved to bookmarks', 'success');
          } else {
            btn.classList.remove('bookmarked');
            showToast('Removed from bookmarks', 'info');
          }
        }
      } catch (err) {
        console.error('Bookmark error:', err);
      }
    });
  });
}

/* --- Helpers --- */
function getCsrfToken() {
  const cookie = document.cookie.split('; ').find(row => row.startsWith('csrftoken='));
  return cookie ? cookie.split('=')[1] : '';
}

function showToast(message, type = 'info') {
  let container = document.querySelector('.toast-container');
  if (!container) {
    container = document.createElement('div');
    container.className = 'toast-container';
    document.body.appendChild(container);
  }

  const toast = document.createElement('div');
  toast.className = `toast toast-${type}`;
  toast.innerHTML = `<span>${message}</span>`;
  container.appendChild(toast);

  setTimeout(() => {
    toast.style.opacity = '0';
    setTimeout(() => toast.remove(), 300);
  }, 4000);
}
