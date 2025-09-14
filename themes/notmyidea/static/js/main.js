// Create search UI
function createSearchUI() {
    console.log("Creating search UI...");
    const searchContainer = document.getElementById('search');

    if (!searchContainer) {
        console.error("Search container not found!");
        return;
    }

    console.log("Search container found, creating UI...");

    searchContainer.innerHTML = `
                                <div class="search-container">
                                    <div class="search-input-wrapper">
                                        <input type="text" id="search-input" placeholder="Search articles..." autocomplete="off">
                                        <div class="search-icon">🔍</div>
                                    </div>
                                    <div id="search-results" class="search-results"></div>
                                </div>
                            `;

    console.log("Search UI created successfully");

    // Add event listeners
    const searchInput = document.getElementById('search-input');
    const searchResults = document.getElementById('search-results');

    if (!searchInput || !searchResults) {
        console.error("Search input or results not found after creation");
        return;
    }

    // Search functionality
    searchInput.addEventListener('input', async (e) => {
        const query = e.target.value.trim();

        if (query.length === 0) {
            searchResults.style.display = 'none';
            return;
        }

        console.log("Searching for:", query);

        if (!pagefind) {
            console.error("Pagefind not initialized");
            return;
        }

        try {
            searchResults.innerHTML = '<div class="search-loading">Searching...</div>';
            searchResults.style.display = 'block';

            const search = await pagefind.search(query);
            console.log("Search results:", search);

            if (search.results.length === 0) {
                searchResults.innerHTML = '<div class="search-no-results">No results found</div>';
                return;
            }

            // Load first 5 results
            const resultsToLoad = search.results.slice(0, 5);
            const resultsData = await Promise.all(
                resultsToLoad.map(result => result.data())
            );

            console.log("Results data:", resultsData);

            const resultsHTML = resultsData.map(result => {
                const title = result.meta?.title || 'Untitled';
                const url = result.url || '#';
                const excerpt = result.excerpt || '';

                return `
                                            <div class="search-result-item">
                                                <a href="${url}" class="search-result-link">
                                                    <h3 class="search-result-title">${title}</h3>
                                                    <div class="search-result-excerpt">${excerpt}</div>
                                                </a>
                                            </div>
                                        `;
            }).join('');

            searchResults.innerHTML = `
                                        <div class="search-results-header">
                                            <span class="search-results-count">${resultsData.length} result${resultsData.length !== 1 ? 's' : ''} found</span>
                                        </div>
                                        <div class="search-results-list">
                                            ${resultsHTML}
                                        </div>
                                    `;

        } catch (error) {
            console.error("Search error:", error);
            searchResults.innerHTML = '<div class="search-error">Search failed. Please try again.</div>';
        }
    });

    // Focus management
    searchInput.addEventListener('focus', () => {
        searchContainer.classList.add('search-focused');
    });

    searchInput.addEventListener('blur', (e) => {
        setTimeout(() => {
            if (!searchContainer.contains(document.activeElement)) {
                searchContainer.classList.remove('search-focused');
                searchResults.style.display = 'none';
            }
        }, 200);
    });

    console.log("Search UI setup complete");
}

// Initialize when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    console.log("DOM Content Loaded - initializing search...");
    createSearchUI();
    initPagefind();
});

// Also try to initialize immediately if DOM is already loaded
if (document.readyState === 'loading') {
    console.log("Document still loading, waiting for DOMContentLoaded...");
} else {
    console.log("Document already loaded, initializing search immediately...");
    createSearchUI();
    initPagefind();
}

console.log("=== INLINE SEARCH SCRIPT COMPLETE ===");
