
const changeContentButton = document.getElementById('changeContentButton');

// Add event listener for button click
changeContentButton.addEventListener('click', function() {
    // Change the content of the container
    const container = document.querySelector('.container');
    container.innerHTML = '<h1>New Content Here</h1>';
});
