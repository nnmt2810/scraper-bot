const axios = require('axios');

async function fetchArticles() {
    const url = 'https://support.optisigns.com/api/v2/help_center/en-us/articles.json?per_page=100';
    try {
        const response = await axios.get(url);
        // Return only the first 30 articles
        return response.data.articles.slice(0, 30);
    } catch (error) {
        console.error('Failed to fetch API:', error.message);
        return [];
    }
}

module.exports = fetchArticles;