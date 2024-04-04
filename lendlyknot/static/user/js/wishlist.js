
    document.addEventListener('DOMContentLoaded', () => {
        const links = document.querySelectorAll('.wishlist-link');
        links.forEach(link => {
            link.addEventListener('click', function(event) {
                event.preventDefault(); // Prevent default link behavior
                const productId = this.dataset.productId;// Get product ID
                const userId = this.dataset.userId;
                if (userId == "None"){
                    alert("You are not logged in, Please login to add items to wishlist...");
                }else{
                    addToWishlist(productId,userId); // Call function to add to wishlist
                    
                }
                
            });
        });
    });

   
    function addToWishlist(productId,userId) {
        const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');
        fetch('/add_wishlist/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken    // Add the CSRF token if using Django
            },
            body: JSON.stringify(
                { 
                    product: productId,
                    user:userId
                }
            )
    })
    .then(response => response.json())
    .then(data => {
        console.log('Success:', data);
        alert('Product added to wishlist!');
    })
    .catch((error) => {
        console.error('Error:', error);
        alert('Failed to add product to wishlist.');
    });
}
