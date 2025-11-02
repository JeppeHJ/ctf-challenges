// Shared CakeNews front-end helpers
export function getUserProfile(){return JSON.parse(localStorage.getItem('cakenewsUserProfile')||'null');}
export function getAccessToken(){return localStorage.getItem('cakenewsAccessToken');}

// Modal helpers
export function showLoginModal(){document.getElementById('login-overlay').style.display='flex'}
export function hideLoginModal(){document.getElementById('login-overlay').style.display='none'}
export function showRegisterModal(){document.getElementById('register-overlay').style.display='flex'}
export function hideRegisterModal(){document.getElementById('register-overlay').style.display='none'}
function logoutCakeNews(){
    localStorage.removeItem('cakenewsAccessToken');
    localStorage.removeItem('cakenewsUserProfile');
    location.reload();
}
function updateAuthLinks(){
    const prof = localStorage.getItem('cakenewsUserProfile');
    const profile = document.getElementById('nav-profile');
    const reg = document.getElementById('nav-register');
    const log = document.getElementById('nav-login');
    const out = document.getElementById('nav-logout');
    if(prof){
        profile.style.display='inline';
        reg.style.display='none';
        log.style.display='none';
        out.style.display='inline';
    }else{
        profile.style.display='none';
        reg.style.display='inline';
        log.style.display='inline';
        out.style.display='none';
    }
}

document.addEventListener('DOMContentLoaded', ()=>{
    const lo = document.getElementById('login-overlay');
    const ro = document.getElementById('register-overlay');
    const lc = lo?.querySelector('.login-modal .close');
    const rc = ro?.querySelector('.register-modal .close');
    if(lc) lc.onclick = hideLoginModal;
    if(rc) rc.onclick = hideRegisterModal;
    lo.onclick = e=>{if(e.target===lo) hideLoginModal();};
    ro.onclick = e=>{if(e.target===ro) hideRegisterModal();};

    // Attach event listeners to nav links
    document.getElementById('nav-register').addEventListener('click', (e) => {
        e.preventDefault();
        showRegisterModal();
    });
    document.getElementById('nav-login').addEventListener('click', (e) => {
        e.preventDefault();
        showLoginModal();
    });
    document.getElementById('nav-logout').addEventListener('click', (e) => {
        e.preventDefault();
        logoutCakeNews();
    });

    // Make "Register here" inside login modal open the register modal
    const loginRegisterLink = lo?.querySelector('#login-register-link');
    if(loginRegisterLink){
        loginRegisterLink.addEventListener('click', (e)=>{
            e.preventDefault();
            hideLoginModal();
            showRegisterModal();
        });
    }

    updateAuthLinks();

// -------- Home page dynamic content --------
if(document.getElementById('news-list')){
  loadArticles();
}

async function loadArticles(){
  try{
    const response = await fetch('/api/articles');
    const articles = await response.json();
    if(articles.length===0) return;
    const featured=articles[0];
    document.getElementById('featured-image').src = featured.image_url;
    document.getElementById('featured-title').textContent = featured.title;
    if(articles.length>1){const s1=articles[1];
      document.getElementById('side-image-1').src=s1.image_url;
      document.getElementById('side-title-1').textContent=s1.title;
      document.getElementById('side-category-1').textContent=s1.category;}
    if(articles.length>2){const s2=articles[2];
      document.getElementById('side-image-2').src=s2.image_url;
      document.getElementById('side-title-2').textContent=s2.title;
      document.getElementById('side-category-2').textContent=s2.category;}
    loadNewsList(articles.slice(3));
    loadMostRead(articles.slice(0,5));
  }catch(err){console.error('Error loading articles:',err);}
}
function loadNewsList(articles){const list=document.getElementById('news-list');if(!list) return;list.innerHTML='';articles.forEach(a=>list.appendChild(createNewsItem(a)));}
function loadMostRead(articles){const list=document.getElementById('most-read-list');if(!list) return;list.innerHTML='';articles.forEach(a=>list.appendChild(createMostReadItem(a)));}
function createNewsItem(a){const d=document.createElement('div');d.className='news-item';d.onclick=()=>window.location.href=`/article/${a.id}`;const t=new Date(a.created_at).toLocaleTimeString('en-US',{hour:'2-digit',minute:'2-digit'});d.innerHTML=`<div class="relative w-20 h-20 flex-shrink-0"><img src="${a.image_url}" alt="${a.title}" class="w-full h-full object-cover rounded"><div class="absolute inset-0 bg-black bg-opacity-20 rounded flex items-center justify-center"><i class="fas fa-play text-white text-sm"></i></div></div><div class="flex-1 min-w-0"><div class="flex items-center space-x-2 mb-2"><span class="category-tag">${a.category}</span><span class="text-gray-500 text-sm">${t}</span></div><h3 class="font-bold text-gray-900 mb-1 line-clamp-2">${a.title}</h3><p class="text-gray-600 text-sm line-clamp-2">${a.content}</p></div>`;return d;}
function createMostReadItem(a){const d=document.createElement('div');d.className='most-read-item';d.onclick=()=>window.location.href=`/article/${a.id}`;const t=new Date(a.created_at).toLocaleTimeString('en-US',{hour:'2-digit',minute:'2-digit'});d.innerHTML=`<div class="relative w-16 h-16 flex-shrink-0"><img src="${a.image_url}" alt="${a.title}" class="w-full h-full object-cover rounded"><div class="absolute inset-0 bg-black bg-opacity-20 rounded flex items-center justify-center"><i class="fas fa-play text-white text-xs"></i></div></div><div class="flex-1 min-w-0"><div class="flex items-center space-x-2 mb-1"><span class="category-tag text-xs">${a.category}</span><span class="text-gray-500 text-xs">${t}</span></div><h4 class="font-medium text-gray-900 text-sm line-clamp-2">${a.title}</h4></div>`;return d;}
});
