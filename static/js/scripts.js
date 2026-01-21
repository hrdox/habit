document.addEventListener('DOMContentLoaded', () => {
    // Theme Toggle
    const toggleBtn = document.getElementById('theme-toggle');
    const html = document.documentElement;

    // Initialize from storage or system preference
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme === 'dark') {
        html.setAttribute('data-theme', 'dark');
        if (toggleBtn) toggleBtn.textContent = '☀️';
    } else if (!savedTheme && window.matchMedia('(prefers-color-scheme: dark)').matches) {
        // html.setAttribute('data-theme', 'dark'); // Optional auto-dark
    }

    if (toggleBtn) {
        toggleBtn.addEventListener('click', () => {
            if (html.getAttribute('data-theme') === 'dark') {
                html.removeAttribute('data-theme');
                localStorage.setItem('theme', 'light');
                toggleBtn.textContent = '🌙';
            } else {
                html.setAttribute('data-theme', 'dark');
                localStorage.setItem('theme', 'dark');
                toggleBtn.textContent = '☀️';
            }
        });
    }

    // Mobile Menu Toggle
    const mobileBtn = document.getElementById('mobile-menu-toggle');
    const closeBtn = document.getElementById('mobile-sidebar-close'); // New
    const sidebar = document.querySelector('aside');

    if (mobileBtn && sidebar) {
        mobileBtn.addEventListener('click', (e) => {
            e.stopPropagation();
            sidebar.classList.toggle('active');
        });

        // Listener for close button
        if (closeBtn) {
            closeBtn.addEventListener('click', (e) => {
                e.stopPropagation();
                sidebar.classList.remove('active');
            });
        }

        document.addEventListener('click', (e) => {
            if (sidebar.classList.contains('active') && !sidebar.contains(e.target) && e.target !== mobileBtn) {
                sidebar.classList.remove('active');
            }
        });
    }

    // Create Toast Container if missing
    let toastContainer = document.getElementById('toast-container');
    if (!toastContainer) {
        toastContainer = document.createElement('div');
        toastContainer.id = 'toast-container';
        document.body.appendChild(toastContainer);
    }
});

// Toast Function
function showToast(message, type = 'success') {
    const container = document.getElementById('toast-container');
    if (!container) return;

    const toast = document.createElement('div');
    toast.className = `toast ${type}`;
    toast.innerHTML = `<span>${type === 'success' ? '✅' : '⚠️'}</span> ${message}`;

    container.appendChild(toast);

    // Fade out and remove
    setTimeout(() => {
        toast.style.opacity = '0';
        toast.style.transform = 'translateY(10px)';

        // Remove after transition
        let removed = false;
        const removeToast = () => {
            if (!removed) {
                if (toast.parentElement) toast.remove();
                removed = true;
            }
        };

        toast.addEventListener('transitionend', removeToast);

        // Safety fallback if transitionend doesn't fire
        setTimeout(removeToast, 400);
    }, 3000);
}

// Global functions for inline onclick handlers
window.toggleHabit = async function (id, btn) {
    const originalContent = btn.innerHTML;
    const isPrimary = btn.classList.contains('btn-primary');

    // Loading State
    btn.disabled = true;
    btn.innerHTML = `<span style="opacity:0.75">⏳</span>`;

    try {
        const res = await fetch(`/habit/toggle/${id}`, { method: 'POST' });
        const data = await res.json();

        if (data.success) {
            const isMultistep = data.target_value > 1;

            if (isMultistep) {
                // Update counter if it exists
                const counter = btn.parentElement.querySelector('span');
                if (counter) {
                    counter.textContent = `${data.value_done} / ${data.target_value}`;
                }

                if (data.new_status) {
                    btn.classList.remove('btn-primary');
                    btn.style.backgroundColor = 'var(--secondary)';
                    btn.textContent = 'Target Hitted (Reset)';
                    showToast('Goal reached! Amazing work!', 'success');
                } else {
                    btn.classList.add('btn-primary');
                    btn.style.backgroundColor = '';
                    btn.textContent = '+1 Track';
                    if (data.value_done === 0) {
                        showToast('Habit reset.', 'success');
                    } else {
                        showToast(`Progress: ${data.value_done}/${data.target_value}`, 'success');
                    }
                }
            } else {
                // Simple Toggle
                if (data.new_status) {
                    btn.classList.remove('btn-primary');
                    btn.style.backgroundColor = 'var(--secondary)';
                    btn.textContent = 'Undo';
                    showToast('Habit completed!', 'success');
                } else {
                    btn.classList.add('btn-primary');
                    btn.style.backgroundColor = '';
                    btn.textContent = 'Mark Done';
                    showToast('Habit status reset.', 'success');
                }
            }
        } else {
            showToast(data.error || 'Failed to update habit', 'error');
            btn.innerHTML = originalContent;
        }
    } catch (e) {
        console.error(e);
        showToast('Network error occured', 'error');
        btn.innerHTML = originalContent;
    } finally {
        btn.disabled = false;
    }
};

window.toggleRoutine = async function (id, btn) {
    const originalContent = btn.innerHTML;
    btn.disabled = true;
    btn.innerHTML = `⏳`;

    try {
        const res = await fetch(`/schedule/toggle/${id}`, { method: 'POST' });
        const data = await res.json();

        if (data.success) {
            if (data.new_status) {
                // Done
                btn.classList.remove('btn-outline');
                btn.style.backgroundColor = 'var(--secondary)';
                btn.style.color = '#fff';
                btn.textContent = '✅ Done';
                showToast('Routine marked as done.', 'success');
            } else {
                // Not Done
                btn.classList.add('btn-outline');
                btn.style.backgroundColor = '';
                btn.style.color = '';
                btn.textContent = 'Mark Done';
                showToast('Routine status reset.', 'success');
            }
        } else {
            showToast(data.error || 'Error', 'error');
            btn.innerHTML = originalContent;
        }
    } catch (e) {
        console.error(e);
        showToast('Network error', 'error');
        btn.innerHTML = originalContent;
    } finally {
        btn.disabled = false;
    }
};

window.togglePrayer = async function (prayerName, element) {
    const isCompleted = element.classList.contains('completed');
    const newStatus = !isCompleted;

    // Optimistic UI update
    element.classList.toggle('completed');

    try {
        const res = await fetch('/prayers', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ prayer: prayerName, status: newStatus })
        });
        const data = await res.json();

        if (data.success) {
            // Update score
            const scoreEl = document.getElementById('spiritual-score-display');
            if (scoreEl && data.score !== undefined) {
                // Animate score change
                animateValue(scoreEl, parseInt(scoreEl.innerText), data.score, 1000);
            }
            const msg = newStatus ? `${prayerName} recorded.` : `${prayerName} unchecked.`;
            showToast(msg, 'success');
        } else {
            // Revert
            element.classList.toggle('completed');
            showToast('Failed to update prayer', 'error');
        }
    } catch (e) {
        console.error(e);
        // Revert
        element.classList.toggle('completed');
        showToast('Network error', 'error');
    }
};

function animateValue(obj, start, end, duration) {
    let startTimestamp = null;
    const step = (timestamp) => {
        if (!startTimestamp) startTimestamp = timestamp;
        const progress = Math.min((timestamp - startTimestamp) / duration, 1);
        obj.innerHTML = Math.floor(progress * (end - start) + start);
        if (progress < 1) {
            window.requestAnimationFrame(step);
        }
    };
    window.requestAnimationFrame(step);
}

// Day Overview AJAX Update
window.updateDayField = async function (field, value) {
    const statusEl = document.getElementById('save-status');
    if (statusEl) {
        statusEl.textContent = 'Saving...';
        statusEl.style.opacity = '1';
        statusEl.style.color = 'var(--text-muted)';
    }

    try {
        const res = await fetch('/api/day/update', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ [field]: value })
        });
        const data = await res.json();

        if (data.success) {
            if (statusEl) {
                statusEl.textContent = 'Saved';
                statusEl.style.color = 'var(--success)';
                setTimeout(() => {
                    statusEl.style.opacity = '0';
                }, 2000);
            }
        }
    } catch (e) {
        console.error(e);
        if (statusEl) {
            statusEl.textContent = 'Error';
            statusEl.style.color = 'var(--danger)';
        }
    }
};
