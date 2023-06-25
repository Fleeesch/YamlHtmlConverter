

 // Generate the table of contents
var tocList = document.getElementById('toc-list');

var items = document.querySelectorAll('.toc-header');
items.forEach(function (item) {

      var listItemLink = document.createElement('a');
      var listItem = document.createElement('li');

      listItemLink.textContent = item.textContent.replace(":","").trim();
      listItemLink.setAttribute("href", "#header-" + listItemLink.textContent);


      listItem.appendChild(listItemLink);
      tocList.appendChild(listItem)



});

    var previouslyMarkedElement = null;

function copyLine(event){
  var clickedElement = event.currentTarget;
      var textToCopy = clickedElement.textContent.trim().split(":")[0] + ":";
      navigator.clipboard.writeText(textToCopy)

if (previouslyMarkedElement) {
        previouslyMarkedElement.classList.remove('marked');
      }

          clickedElement.classList.add('marked');

      previouslyMarkedElement = clickedElement;

}
