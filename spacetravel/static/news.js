// Wordcloud
// Set up the word cloud layout
var svg = d3.select("#wordcloud");
svg.selectAll("text")
    .data(wordData)
    .enter().append("text")
    .attr("class", "word")
    .attr("font-size", function (d) { return d.size + "px"; })
    .attr("x", function () { return Math.random() * 800; }) // Random x position
    .attr("y", function () { return Math.random() * 400; }) // Random y position
    .text(function (d) { return d.text; })
    .on("click", function (d) {
        // Handle click event, e.g., redirect to article details page
        //window.location.href = "/article/" + d.id + "/";
        console.log("Id: "+ d.id);
    });


// Tiles
var itemsPerPage = 10; // Adjust the number of items per page as needed
var currentPage = 1;

function makeTiles(item) {
    var tileContainer = document.getElementById("tileContainer");

    // Create a new tile div
    var tileDiv = document.createElement("div");
    tileDiv.classList.add("tile");

    let d = new Date(item.published_at);
    let date = d.toDateString();

    // Populate the tile content
    tileDiv.innerHTML += `
        <a href="${item.url}" target="_blank">
            <img src="${item.image_url}" alt=${item.title} class="tile-image">
            <h3 class="tile-title">${item.title}</h3>
            <p class="tile-summary">${item.summary}</p>
            <div class="tile-info">
                <p class="tile-type">${item.type}</p>
                <p class="tile-source">${item.news_site}</p>
                <p class="tile-date">${date}</p>
                <p class="tile-sentiment">${item.id}</p>
            </div>
        </a>
    `;

    tileContainer.appendChild(tileDiv);
}

function renderPage(page) {
    var startIndex = (page - 1) * itemsPerPage;
    var endIndex = startIndex + itemsPerPage;
    var currentItems = newsData.slice(startIndex, endIndex);

    var tileContainer = document.getElementById("tileContainer");
    tileContainer.innerHTML = "";

    currentItems.forEach(makeTiles);
}

function nextPage() {
    currentPage++;
    renderPage(currentPage);
}

function prevPage() {
    if (currentPage > 1) {
        currentPage--;
        renderPage(currentPage);
    }
}

document.addEventListener("DOMContentLoaded", function () {
    renderPage(currentPage);
});