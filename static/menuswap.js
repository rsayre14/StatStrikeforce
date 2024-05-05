// Get all the menu buttons
var menuButtons = document.querySelectorAll('.menuButton');



// Add click event listener to each menu button
menuButtons.forEach(function(button) {
  button.addEventListener('click', function() {
    swapMenu(this.id);
  });
});



function swapMenu(buttonID) {
  // Remove 'active' class from all menu buttons
  menuButtons.forEach(function(button) {
    button.classList.remove('active');
  });

  // Add 'active' class to the clicked button
  document.getElementById(buttonID).classList.add('active');

  // Get the ContentID that corresponds with the ButtonID
  var contentID = buttonID.replace('Button', 'Content');

  // Get all content divs
  var contentDivs = document.querySelectorAll('.content');

  // Hide all content divs
  contentDivs.forEach(function(content) {
    content.style.display = 'none';
  });

  document.getElementById(contentID).style.display = 'block';

}

