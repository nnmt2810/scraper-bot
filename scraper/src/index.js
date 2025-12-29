const fs = require('fs');
const path = require('path');
const fetchArticles = require('./fetchArticles');
const convert = require('./htmlToMarkdown');

async function main() {
    const articles = await fetchArticles();
    const outputDir = path.join(__dirname, '../data');

    if (!fs.existsSync(outputDir)) 
        fs.mkdirSync(outputDir);

    articles.forEach(article => {
        const content = convert(article);
        // Save file as slug.md
        const fileName = `${article.slug}.md`;
        fs.writeFileSync(path.join(outputDir, fileName), content);
        console.log(`Saved: ${fileName}`);
    });

    console.log(`Success: Already scraped ${articles.length} articles.`);
}

main();