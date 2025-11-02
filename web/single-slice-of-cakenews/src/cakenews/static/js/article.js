// Article page logic
(function(){
  const articleId = window.__ARTICLE_ID__;
  if(!articleId) return;

  document.addEventListener('DOMContentLoaded', ()=>{
    loadArticle();
    loadComments();
    renderCommentFormIfLoggedIn();
    renderReportButtons();
  });

  async function loadArticle(){
    try{
      const res = await fetch(`/api/articles/${articleId}`);
      const article = await res.json();
      if(article.error){console.error('Article not found');return;}
      document.title = `${article.title} - CakeNews`;
      document.getElementById('article-image').src = article.image_url;
      document.getElementById('article-title').textContent = article.title;
      document.getElementById('article-author').textContent = `By ${article.author}`;
      document.getElementById('article-date').textContent = new Date(article.created_at).toLocaleDateString('en-US');
      document.getElementById('article-content').textContent = article.content;
      const catEl = document.getElementById('article-category');
      catEl.textContent = article.category;
      if(article.category === 'LIVE') catEl.classList.add('live-tag');
    }catch(err){console.error('Error loading article:', err);}
  }

  function escapeHTML(str) {
    return str.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;').replace(/'/g, '&#039;');
  }

  async function loadComments(){
    try{
      const res = await fetch(`/api/articles/${articleId}/comments`);
      const comments = await res.json();
      const wrap = document.getElementById('comments-section');
      if(comments.length === 0){
        wrap.innerHTML = '<p class="text-gray-500">No comments yet. Be the first!</p>';
        return;
      }

      const renderComment = c => `
        <div class="comment-card">
          <div class="flex items-center justify-between mb-2">
            <span class="font-medium text-gray-900" data-username="${c.username}">
              ${escapeHTML(c.username)}
            </span>
            <span class="text-sm text-gray-500">
              ${new Date(c.created_at).toLocaleDateString('en-US')}
            </span>
          </div>
          <p class="text-gray-700">${c.content}</p>
        </div>`;

      wrap.innerHTML = comments.map(renderComment).join('');
    }catch(err){
      console.error('Error loading comments:', err);
    }
  }

  function renderReportButtons(){
    const prof = JSON.parse(localStorage.getItem('cakenewsUserProfile') || 'null');
    if(!prof) return;
    const wrap = document.getElementById('report-buttons');
    if(!wrap) return;
    let html='';
    if(prof.role==='user'){
      html = `<button id=\"report-journalist\" class=\"btn-warning\">Report article to journalist</button>`;
    }else if(prof.role==='journalist'){
      html = `<button id=\"report-admin\" class=\"btn-danger\">Report article to Brunnernelogin admin</button>`;
    }
    wrap.innerHTML = html;
    if(prof.role==='user'){
      document.getElementById('report-journalist').onclick = async ()=>{
        const token = localStorage.getItem('cakenewsAccessToken');
        const res = await fetch(`/api/articles/${articleId}/report-journalist`, {method:'POST', headers:{'Authorization':`Bearer ${token}`}});
        alert(res.ok? 'Reported to journalist':'Not allowed');
      };
    }else if(prof.role==='journalist'){
      document.getElementById('report-admin').onclick = async ()=>{
        const token = localStorage.getItem('cakenewsAccessToken');
        const res = await fetch(`/api/articles/${articleId}/report-admin`, {method:'POST', headers:{'Authorization':`Bearer ${token}`}});
        alert(res.ok? 'Escalated to admin':'Not allowed');
      };
    }
  }

  function renderCommentFormIfLoggedIn(){
    const prof = JSON.parse(localStorage.getItem('cakenewsUserProfile') || 'null');
    if(!prof) return;
    const wrapper = document.getElementById('comment-form');
    if(!wrapper) return;
    wrapper.innerHTML = `<textarea id="new-comment" rows="4" placeholder="Write your comment here" class="w-full border border-gray-300 rounded p-3 focus:outline-none"></textarea><button id="post-comment" class="mt-3 bg-green-600 hover:bg-green-700 text-white font-semibold py-2 px-4 rounded">Create comment</button>`;
    document.getElementById('post-comment').onclick = async ()=>{
      const content = document.getElementById('new-comment').value.trim();
      if(!content) return;
      const token = localStorage.getItem('cakenewsAccessToken');
      const res = await fetch(`/api/articles/${articleId}/comments`, {method:'POST', headers:{'Content-Type':'application/json','Authorization':`Bearer ${token}`}, body: JSON.stringify({content})});
      if(res.ok){ document.getElementById('new-comment').value=''; loadComments(); } else { alert('Could not post comment'); }
    };
  }
})();
