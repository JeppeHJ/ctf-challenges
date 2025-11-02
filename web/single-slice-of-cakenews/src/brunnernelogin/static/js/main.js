// BrunnerneLogin shared front-end helpers
function updateNav(){
  const nav=document.getElementById('nav-actions');
  if(!nav) return;
  const user=localStorage.getItem('brunnerneUser');
  if(user){
    nav.innerHTML=`<a href="/profile" class="px-4 py-2 bg-white text-slate-700 rounded shadow">Profile</a><button id="logoutBtn" class="px-4 py-2 bg-cyan-600 text-white rounded">Logout</button>`;
    document.getElementById('logoutBtn').addEventListener('click',()=>{
      localStorage.removeItem('brunnerneUser');
      localStorage.removeItem('brunnerneAccessToken');
      window.location.href='/';
    });
  }
}

document.addEventListener('DOMContentLoaded', updateNav);
