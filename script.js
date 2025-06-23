// Future JavaScript will go here 

document.addEventListener('DOMContentLoaded', function() {
    const articlesGrid = document.querySelector('.articles-grid');
    const paginationContainer = document.querySelector('.pagination');
    const pageNumbersContainer = document.querySelector('.page-numbers');
    const prevButton = document.querySelector('.page-prev');
    const nextButton = document.querySelector('.page-next');
    const pageInfo = document.querySelector('.page-info');

    let currentPage = 1;
    let totalPages = 1; // Default value
    const articlesPerPage = 12;
    let allArticles = []; // To store all articles from JSON

    function runTest() {
        articlesGrid.innerHTML = '';
        const testArticle = {
            href: "#",
            imgSrc: "imgs/1-24-300x200.jpg", // Make sure this image exists
            title: "这是一个测试文章，如果能看到，说明布局是好的，问题出在数据加载上。",
            time: "刚刚",
            views: "1"
        };
        const articleHTML = `
            <article class="article-card post post-grid">
                <div class="entry-media">
                     <div class="placeholder">
                         <a href="${testArticle.href}" title="${testArticle.title}">
                            <img src="${testArticle.imgSrc}" alt="${testArticle.title}" class="lazyload">
                        </a>
                    </div>
                </div>
                <div class="entry-wrapper">
                    <header class="entry-header">
                        <h2 class="entry-title">
                            <a href="${testArticle.href}" title="${testArticle.title}">${testArticle.title}</a>
                        </h2>
                    </header>
                    <div class="entry-footer">
                       <div class="entry-meta">
                           <span class="meta-date"><i class="far fa-clock"></i> ${testArticle.time}</span>
                            <span class="meta-views"><i class="far fa-eye"></i> ${testArticle.views}</span>
                       </div>
                    </div>
                </div>
            </article>
        `;
        articlesGrid.insertAdjacentHTML('beforeend', articleHTML);
        // Hide pagination for this test
        if(paginationContainer) paginationContainer.style.display = 'none';
    }

    async function loadArticles() {
        try {
            const response = await fetch('articles.json?v=1.4');
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            allArticles = await response.json();
            totalPages = Math.ceil(allArticles.length / articlesPerPage);
            changePage(1);
        } catch (error) {
            console.error("Could not load articles:", error);
            articlesGrid.innerHTML = `<div style="background-color: #ffdddd; border: 1px solid #ff0000; padding: 15px; border-radius: 8px;">
                <h3 style="color: #ff0000;">加载文章时出错！</h3>
                <p><strong>错误详情:</strong> ${error.toString()}</p>
                <p><strong>堆栈跟踪:</strong></p>
                <pre style="white-space: pre-wrap;">${error.stack}</pre>
            </div>`;
        }
    }

    function renderArticles(page) {
        articlesGrid.innerHTML = '';
        
        const startIndex = (page - 1) * articlesPerPage;
        const endIndex = startIndex + articlesPerPage;
        const articlesToRender = allArticles.slice(startIndex, endIndex);

        articlesToRender.forEach(article => {
            const pageId = article.href.split('/').pop().replace('.html', '');
            const newHref = `show_content.html?page=${pageId}`;

            const articleHTML = `
                <article class="article-card post post-grid">
                    <div class="entry-media">
                         <div class="placeholder">
                             <a href="${newHref}" title="${article.title}">
                                <img src="${article.imgSrc}" alt="${article.title}" class="lazyload">
                            </a>
                        </div>
                    </div>
                    <div class="entry-wrapper">
                        <header class="entry-header">
                            <h2 class="entry-title">
                                <a href="${newHref}" title="${article.title}">${article.title}</a>
                            </h2>
                        </header>
                        <div class="entry-footer">
                           <div class="entry-meta">
                               <span class="meta-date"><i class="far fa-clock"></i> ${article.time}</span>
                                <span class="meta-views"><i class="far fa-eye"></i> ${article.views}</span>
                           </div>
                        </div>
                    </div>
                </article>
            `;
            articlesGrid.insertAdjacentHTML('beforeend', articleHTML);
        });
    }

    function renderPagination() {
        pageNumbersContainer.innerHTML = '';
        const pagesToShow = [];
        const maxPages = 5; 
        if (totalPages <= maxPages + 2) {
            for (let i = 1; i <= totalPages; i++) pagesToShow.push(i);
        } else {
            pagesToShow.push(1);
            if (currentPage > 3) pagesToShow.push('...');

            let start = Math.max(2, currentPage - 1);
            let end = Math.min(totalPages - 1, currentPage + 1);
            
            if (currentPage <= 3) {
                start = 2;
                end = 4;
            }
            if (currentPage >= totalPages - 2) {
                start = totalPages - 3;
                end = totalPages - 1;
            }

            for (let i = start; i <= end; i++) {
                pagesToShow.push(i);
            }

            if (currentPage < totalPages - 2) pagesToShow.push('...');
            pagesToShow.push(totalPages);
        }
        
        pagesToShow.forEach(num => {
            if (num === '...') {
                const span = document.createElement('span');
                span.className = 'page-ellipsis';
                span.textContent = '...';
                pageNumbersContainer.appendChild(span);
            } else {
                const a = document.createElement('a');
                a.href = '#';
                a.className = 'page-number';
                a.textContent = num;
                a.dataset.page = num;
                if (num === currentPage) {
                    a.classList.add('active');
                }
                pageNumbersContainer.appendChild(a);
            }
        });

        pageInfo.textContent = `${currentPage} / ${totalPages}`;
        prevButton.classList.toggle('disabled', currentPage === 1);
        nextButton.classList.toggle('disabled', currentPage === totalPages);
    }
    
    function changePage(newPage) {
        if (newPage < 1 || newPage > totalPages) return;
        currentPage = newPage;
        renderArticles(currentPage);
        renderPagination();
        window.scrollTo({ top: 0, behavior: 'smooth' });
    }

    paginationContainer.addEventListener('click', function(e) {
        e.preventDefault();
        if (e.target.matches('.page-next:not(.disabled)')) {
            changePage(currentPage + 1);
        } else if (e.target.matches('.page-prev:not(.disabled)')) {
            changePage(currentPage - 1);
        } else if (e.target.matches('.page-number')) {
            const page = parseInt(e.target.dataset.page, 10);
            changePage(page);
        }
    });

    // Run the test function directly instead of loading from JSON
    // runTest();
    loadArticles(); // We disable the original function for now

    const topButton = document.querySelector('.mobile-nav a:last-child');
    if (topButton) {
        topButton.addEventListener('click', function(e) {
            e.preventDefault();
            window.scrollTo({
                top: 0,
                behavior: 'smooth'
            });
        });
    }
}); 