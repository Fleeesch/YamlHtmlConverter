// - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -v
//  Setup
// - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -v

// -------------------------------
//  Globals
// -------------------------------

// CSS selectors
const css_hidden = "hidden";
const css_marked = "marked";
const css_collapsed = "collapsed";
const css_content = "content";
const css_grid_wrapper = "#grid-wrapper";
const css_filter_input = "input-filter";
const css_toc_link = "#table-of-contents a";
const css_section_header_root = '.section.level-0';
const css_linewrapper_root = '.line-wrapper.level-0';
const css_fire_ref = ".file-reference"
const css_attribute = ".entry-attribute";
const css_toc = 'table-of-contents';
const css_toc_list = 'table-of-contents-list';
const css_toc_links = '#table-of-contents-list a';
const css_highlight = 'highlight';

// -------------------------------
//  Creating Table of Contents
// -------------------------------

// get table of contents and children
var toc = document.getElementById(css_toc);
var tocList = document.getElementById(css_toc_list);

// get all root level headers
var items = document.querySelectorAll(css_linewrapper_root + ", " + css_fire_ref);

// go through headers
items.forEach(function (item) {

    // create list entry with hyperlink
    var listItemLink = document.createElement('a');
    var listItem = document.createElement('li');

    // generate name, implement hyperlink-entry
    listItemLink.textContent = item.textContent.replaceAll(":", "").trim();
    listItemLink.setAttribute("href", "#" + item.id);



    // write html
    listItem.appendChild(listItemLink);
    tocList.appendChild(listItem)

    if (listItemLink.textContent.includes(".yml") || listItemLink.textContent.includes(".yaml")) {
        listItem.classList.add("table-of-contents-file-reference");
    }

});

// always filter input on start
filterInput()


// - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -v
//  Function : Toggle Side Panel
// - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -v

function toggleSidePanel() {

    sidepanel = document.querySelector(css_grid_wrapper);

    if (sidepanel) {

        if (sidepanel.classList.contains(css_collapsed)) {
            sidepanel.classList.remove(css_collapsed);
        } else {
            sidepanel.classList.add(css_collapsed);
        }
    }

}


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
        previouslyMarkedElement.classList.remove(css_marked);
    }

    // add marker
    clickedElement.classList.add(css_marked);

    // store marked element
    previouslyMarkedElement = clickedElement;

}


// - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -v
//  Function : Filter Structure Elements
// - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -v

function filterStructureElements(filter) {

    // get root headers
    lines = document.querySelectorAll(css_section_header_root);

    // iterate over root headers
    lines.forEach(function iterate(line) {

        // get child attribute
        children = line.querySelectorAll(css_attribute);

        // get formatted text of attribute
        var text = children[0].textContent.trim();
        
        // skip file references
        if (text.includes(".yaml") || text.includes(".yml")){
            return;
        }        
        
        // hide containers that don't match filters
        if (text.includes(filter)) {
            line.classList.remove(css_hidden);
        } else {
            line.classList.add(css_hidden);
        }

    });


}

// - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -v
//  Function : Filter Table of Contents
// - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -v

function filterTableOfContents(filter) {
    
    // get hyperlinks from table of contents
    lines = document.querySelectorAll(css_toc_link);
    
    // iterate over lines
    lines.forEach(function iterate(link, index) {
        
        // store formatted line
        var text = link.textContent.trim();
        
        // skip file references
        if (text.includes(".yaml") || text.includes(".yml")){
            return;
        }
        
        
        // remove lines that don't match filter
        if (text.includes(filter)) {
            link.classList.remove(css_hidden);
        } else {
            link.classList.add(css_hidden);
        }
    
    });



}

// - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -v
//  Function : Filter Input
// - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -v

function filterInput() {


    // get formatted input text
    input = document.getElementById(css_filter_input).value.trim();

    // filter structure
    filterStructureElements(input);

    // filter table of contents
    filterTableOfContents(input);

}

// - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -v
//  Dynamic Scrolling Highlight
// - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -v


// collect all the element references
const contentContainer = document.getElementById(css_content);
const contentRootSections = document.querySelectorAll(css_linewrapper_root + ", " + css_fire_ref);
const tocLinks = document.querySelectorAll(css_toc_links)



// create eventlistener for content container scroll events
contentContainer.addEventListener("scroll", () => {

    // get scroll position relative to container
    const scrollPosition = window.pageYOffset || document.documentElement.scrollTop || document.body.scrollTop;

    // mark the first active entry
    var activeClassSet = false;

    // go through entries
    for (const [idx, ct] of contentRootSections.entries()) {
        
        // get bounding box of entry
        elementBox = ct.getBoundingClientRect();

        // grab table of contents equivalent
        link = tocLinks[idx]

        // element higher positioned than scroll position or one entry already marked?
        if (elementBox.top <= scrollPosition || activeClassSet) {
            // remove highlight
            link.classList.remove(css_highlight);
        } else {
            // first entry in view!

            // add highlight
            link.classList.add(css_highlight);

            // remember marked entry
            activeClassSet = true;
        }

    }

});
