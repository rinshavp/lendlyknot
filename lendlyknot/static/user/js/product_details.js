
//Declare flatpickrInstance in a broader scope
        var flatpickrInstance;
        var formattedFromDate, formattedToDate;
        document.getElementById('productSize').addEventListener('change', function () {
            var selectedSize = this.value;
            if (selectedSize) {
                // Make an AJAX request to fetch start and end dates based on the selected size
                var product_id = "{{ product.id }}"
                fetch(`/get_dates/${product_id}/${selectedSize}/`)
                    .then(response => response.json())
                    .then(data => {
                            const bookedDates = data.fully_booked_dates; // Use the Django template tag to insert the JSON
                            console.log(bookedDates); 
                            flatpickr(".flatpickr", {
                                mode: "range",
                                minDate: "today",
                                dateFormat: "Y-m-d",
                                conjunction: " :: ",
                                disable: bookedDates, // Map to required format
                                wrap: true,
                                onClose: function (selectedDates, dateStr, instance) {
                                    var fromDate = selectedDates[0];
                                    var toDate = selectedDates[1];

                                    formattedFromDate = fromDate.getFullYear() + '-' + ('0' + (fromDate.getMonth() + 1)).slice(-2) + '-' + ('0' + fromDate.getDate()).slice(-2);
                                    formattedToDate = toDate.getFullYear() + '-' + ('0' + (toDate.getMonth() + 1)).slice(-2) + '-' + ('0' + toDate.getDate()).slice(-2);
                                    console.log(selectedDates);
                                     // Do something with the selected dates
                                } 
                            });
    
                    });
            } else {
    
                alert('no item');
            }
        });

        function bookingForm() {
            
            var selectedSize = document.getElementById('productSize').value;
            var fromDate = formattedFromDate
            var toDate = formattedToDate
            var quantity = document.getElementById('quantity').value;
            var product_id = "{{ product.id }}"
            var user_id = "{{ request.session.user_id }}"
            
            var formData = {
                'user': user_id,
                'product': product_id,
                'start_date': fromDate,
                'end_date': toDate,
                'quantity_rented': quantity,
                'booked_size': selectedSize
            };

            const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');

            // Make an AJAX request to the server
            fetch('/product_booking/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrfToken    // Add the CSRF token if using Django
                },
                body: JSON.stringify(formData)
            })
            .then(response => response.json())
            .then(data => {
                // Handle the response from the server as needed
                console.log(data);
            })
            .catch(error => {
                console.error('Error:', error);
            });
        }
        
   