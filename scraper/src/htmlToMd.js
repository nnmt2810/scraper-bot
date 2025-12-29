const TurndownService = require('turndown');

const turndownService = new TurndownService({
    headingStyle: 'atx',
    codeBlockStyle: 'fenced'
});

function convert(article) {
    // Add front matter
    const header = `---\ntitle: ${article.title}\nurl: ${article.html_url}\n---\n\n`;
    
    // Turndown the HTML body to Markdown
    const markdownBody = turndownService.turndown(article.body);
    
    return header + markdownBody;
}

module.exports = convert;