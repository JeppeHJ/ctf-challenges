import { hideLoginModal } from './main.js';

document.addEventListener('DOMContentLoaded', () => {
    const cakeForm = document.getElementById('cakeLoginForm');
    const errMsg = document.getElementById('login-error');
    if (cakeForm) {
        cakeForm.addEventListener('submit', async e => {
            e.preventDefault();
            errMsg.classList.add('hidden');
            const fd = new FormData(cakeForm);
            const res = await fetch('/api/login', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    email: fd.get('email'),
                    password: fd.get('password')
                })
            });
            const data = await res.json();
            if (res.ok) {
                localStorage.setItem('cakenewsAccessToken', data.token);
                localStorage.setItem('cakenewsUserProfile', JSON.stringify({
                    email: fd.get('email'),
                    username: data.username,
                    role: data.role
                }));
                hideLoginModal();
                location.reload();
            } else {
                errMsg.textContent = data.error || 'Login failed';
                errMsg.classList.remove('hidden');
            }
        });
    }
});
