// - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -v
//  Setup
// - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -v

// -------------------------------
//  Creating Table of Contents
// -------------------------------

// get table of contents and children
var toc = document.getElementById('table-of-contents');
var tocList = document.getElementById('table-of-contents-list');


// get all root level headers
var items = document.querySelectorAll('.line-wrapper.level-0');

// go through headers
items.forEach(function (item) {

    // create list entry with hyperlink
    var listItemLink = document.createElement('a');
    var listItem = document.createElement('li');

    // generate name, implement hyperlink-entry
    listItemLink.textContent = item.textContent.replaceAll(":", "").trim();
    listItemLink.setAttribute("href", "#" + listItemLink.textContent.replaceAll(" ", ""));

    // write html
    listItem.appendChild(listItemLink);
    tocList.appendChild(listItem)

});




// - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -v
//  Function : Line to Clipboard
// - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -v

// element marked for being copied
var previouslyMarkedElement = null;

function copyLine(event) {

    // get clicked element
    var clickedElement = event.currentTarget;

    // filter text to copy
    var textToCopy = clickedElement.textContent.trim().split(":")[0] + ":";

    // copy to clipboard
    navigator.clipboard.writeText(textToCopy)

    // remove previous marker (if available)
    if (previouslyMarkedElement) {
        previouslyMarkedElement.classList.remove('marked');
    }

    // add marker
    clickedElement.classList.add('marked');

    // store marked element
    previouslyMarkedElement = clickedElement;

}


// - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -v
//  Function : Filter Structure Elements
// - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -v

function filterStructureElements(filter) {

    // get root headers
    lines = document.querySelectorAll('.section.level-0');

    // iterate over root headers
    lines.forEach(function iterate(line, index) {

        // get child attribute
        children = line.querySelectorAll('.attribute');

        // get formatted text of attribute
        var text = children[0].textContent.trim();

        // hide containers that don't match filters
        if (text.includes(input)) {
            line.classList.remove("hidden");
        } else {
            line.classList.add("hidden");
        }

    });


}

// - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -v
//  Function : Filter Table of Contents
// - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -v

function filterTableOfContents(filter) {

   // get hyperlinks from table of contents
    lines = document.querySelectorAll('#table-of-contents a');

    // iterate over lines
    lines.forEach(function iterate(link, index) {

        // store formatted line
        var text = link.textContent.trim();

        // remove lines that don't match filter
        if (text.includes(input)) {
            link.classList.remove("hidden");
        } else {
            link.classList.add("hidden");
        }

    });



}

// - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -v
//  Function : Filter Input
// - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -v

function filterInput() {

    // get formatted input text
    input = document.getElementById('input-filter').value.trim();

    // filter structure
    filterStructureElements(input);

    // filter table of contents
    filterTableOfContents(input);

}