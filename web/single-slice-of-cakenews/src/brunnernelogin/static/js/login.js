window.addEventListener('DOMContentLoaded', ()=>{
  const form = document.getElementById('loginForm');
  const err  = document.getElementById('sso-error');
  if(!form) return;
  form.addEventListener('submit', async e=>{
    e.preventDefault(); err.classList.add('hidden');
    const fd = new FormData(form);
    const res = await fetch('/api/login', {
      method:'POST',
      headers:{'Content-Type':'application/json'},
      body: JSON.stringify({email: fd.get('email'), password: fd.get('password')})
    });
    const data = await res.json();
    if(res.ok){
      localStorage.setItem('brunnerneAccessToken', data.token);
      localStorage.setItem('brunnerneUser', JSON.stringify({email: fd.get('email')}));
      window.location.href = '/profile';
    }else{
      err.textContent = data.error || 'Login failed';
      err.classList.remove('hidden');
    }
  });
});
