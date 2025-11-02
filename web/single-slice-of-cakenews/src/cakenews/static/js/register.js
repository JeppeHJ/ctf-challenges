import { hideRegisterModal } from './main.js';

document.addEventListener('DOMContentLoaded', () => {
    const regForm = document.getElementById('registerForm');
    if (!regForm) return;
    let msg;
    regForm.addEventListener('submit', async e => {
        e.preventDefault();
        msg = document.getElementById('register-msg');
        msg.textContent = '';
        const fd = new FormData(regForm);
        const payload = {
            email: fd.get('email'),
            username: fd.get('username'),
            password: fd.get('password'),
            password_confirmation: fd.get('password_confirmation')
        };
        const res = await fetch('/api/register', {
            method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify(payload)
        });
        const data = await res.json();
        if (res.ok) {
            msg.className = 'text-green-600 text-sm';
            msg.textContent = 'Account created!';
            regForm.reset();
            setTimeout(() => hideRegisterModal(), 800);
        } else {
            msg.className = 'text-red-600 text-sm';
            msg.textContent = (data.error === 'email_taken' ? 'E-mail already registered' : data.error === 'username_taken_or_db_error' ? 'Username already taken' : data.error || 'Registration error');
        }
    });
});
