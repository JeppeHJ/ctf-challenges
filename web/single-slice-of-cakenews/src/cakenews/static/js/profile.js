import { getAccessToken, getUserProfile } from './main.js';

document.addEventListener('DOMContentLoaded', async () => {
    const token = getAccessToken();
    if (!token) {
        alert('You are not logged in');
        window.location.href = '/';
        return;
    }

    try {
        const res = await fetch('/api/profile', { headers: { 'Authorization': `Bearer ${token}` }});
        if (!res.ok) throw new Error('Unauthorized');
        const prof = await res.json();

        document.getElementById('p-username').textContent = prof.username;
        document.getElementById('p-email').textContent = prof.email;
        document.getElementById('p-role').textContent = prof.role;

        // sync cache
        localStorage.setItem('cakenewsUserProfile', JSON.stringify(prof));
    } catch (err) {
        const prof = getUserProfile();
        if (prof) {
            document.getElementById('p-username').textContent = prof.username;
            document.getElementById('p-email').textContent = prof.email;
            document.getElementById('p-role').textContent = prof.role;
        } else {
            alert('Session expired. Please log in again.');
            window.location.href = '/login';
        }
    }
});
