const API_URL = "http://localhost:8000";

// --- DOM Elements ---
const feedContainer = document.getElementById('news-feed');
const queryForm = document.getElementById('query-form');
const queryInput = document.getElementById('query-input');
const responseArea = document.getElementById('response-area');
const submitBtn = document.getElementById('submit-btn');

// --- State ---
let seenArticles = new Set();

// --- Live Feed Logic ---
async function fetchRecentNews() {
    try {
        const response = await fetch(`${API_URL}/recents`);
        if (!response.ok) return;

        const articles = await response.json();

        // Reverse to show newest on top usually, but let's assume API returns ordered
        // We want newest at the top

        let hasNew = false;

        articles.forEach(article => {
            const signature = article.text; // Simple dedup key
            if (!seenArticles.has(signature)) {
                hasNew = true;
                seenArticles.add(signature);
                addArticleToFeed(article);
            }
        });

        if (hasNew && feedContainer.querySelector('.loading-state')) {
            feedContainer.querySelector('.loading-state').remove();
        }

    } catch (e) {
        console.error("Feed error:", e);
    }
}

function addArticleToFeed(article) {
    const el = document.createElement('div');
    el.className = 'news-item';

    // Extract topic if possible (simple regex or fallback)
    const topicMatch = article.text.match(/(AI|Crypto|Stock Market|Climate Change|Space Exploration)/);
    const topic = topicMatch ? topicMatch[0] : "Update";
    const time = new Date().toLocaleTimeString(); // Using local time for request receipt

    el.innerHTML = `
        <div class="news-meta">
            <span class="news-topic-tag">${topic}</span>
            <span>${time}</span>
        </div>
        <div class="news-text">${article.text}</div>
    `;

    // Setup animation
    el.style.opacity = '0';

    // Prepend to top
    feedContainer.insertBefore(el, feedContainer.firstChild);

    // Trigger reflow for anim
    setTimeout(() => el.style.opacity = '1', 50);

    // Limit feed size
    if (feedContainer.children.length > 50) {
        feedContainer.lastChild.remove();
    }
}

// --- Query Logic ---
queryForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    const query = queryInput.value.trim();
    if (!query) return;

    // 1. Add User Message
    addMessage(query, 'user');
    queryInput.value = '';

    // 2. Loading State
    const loadingId = addLoadingMessage();

    try {
        // 3. API Call
        const response = await fetch(`${API_URL}/query`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ query: query })
        });

        const data = await response.json();

        // 4. Remove Loading & Add AI Message
        removeMessage(loadingId);
        addMessage(data.answer, 'ai', data.sources);

    } catch (err) {
        removeMessage(loadingId);
        addMessage("Error: Could not retrieve intelligence. System offline?", 'ai');
    }
});

function addMessage(text, type, sources = []) {
    const el = document.createElement('div');
    el.className = `message ${type}`;

    let content = `<p>${text.replace(/\n/g, '<br>')}</p>`;

    if (sources.length > 0) {
        content += `<div style="margin-top: 10px; border-top: 1px solid var(--glass-border); padding-top: 10px;">
            <div class="source-badge">SOURCE INTEL</div>
            <div style="font-size: 0.8rem; color: var(--text-secondary); font-style: italic;">
                "${sources[0].content.substring(0, 100)}..."
            </div>
        </div>`;
    }

    el.innerHTML = content;
    responseArea.appendChild(el);

    // Scroll to bottom
    const container = document.querySelector('.chat-container');
    container.scrollTop = container.scrollHeight;
}

function addLoadingMessage() {
    const id = 'msg-' + Date.now();
    const el = document.createElement('div');
    el.id = id;
    el.className = 'message ai';
    el.innerHTML = '<span class="loading-dots">Analyzing Real-time Vector Stream</span>';
    responseArea.appendChild(el);
    return id;
}

function removeMessage(id) {
    const el = document.getElementById(id);
    if (el) el.remove();
}

// Start Polling
setInterval(fetchRecentNews, 2000);
fetchRecentNews();
