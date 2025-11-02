// BrunnerneLogin profile page logic
async function loadProfile(){
  const token = localStorage.getItem('brunnerneAccessToken');
  if(!token){
    alert('Not logged in');
    window.location.href='/login';
    return;
  }
  try{
    const res = await fetch('/api/profile',{headers:{'Authorization':`Bearer ${token}`}});
    if(!res.ok) throw new Error('Unauthorized');
    const data = await res.json();
    document.getElementById('sso-email').textContent = data.email;
    if(data.flag){
      const p=document.createElement('p');
      p.innerHTML = `<strong>Flag:</strong> <span class="text-red-600">${data.flag}</span>`;
      document.querySelector('main .space-y-4').appendChild(p);
    }
  }catch(err){
    alert('Session expired. Please log in again.');
    localStorage.removeItem('brunnerneAccessToken');
    window.location.href='/login';
  }
}

document.addEventListener('DOMContentLoaded', loadProfile);
