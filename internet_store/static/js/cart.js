document.querySelectorAll('.add-to-cart').forEach(btn => {
    btn.addEventListener("click", async (event) => {
        const button = event.currentTarget;
        const productId = button.dataset.productId;
        try {
            const response = await fetch(`/cart/add_to_cart/${productId}/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': getCookie('csrftoken'),
                    'Content-Type': 'application/json'
                }
            });
            const data = await response.json();
            if (data.success){
                location.reload()
            }

        } catch (error) {
            console.error('Ошибка:', error);
        }

    })
})

async function handleCartAction(event, action) {
    const button = event.currentTarget;
    const productId = button.dataset.productId;
    const quantitySelector = button.closest('.quantity-selector');
    const quantitySpan = quantitySelector.querySelector('.quantity');
    const minusButton = quantitySelector.querySelector('.cart-minus-button');
    
    try {
        const response = await fetch(`/cart/${action}/${productId}/`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': getCookie('csrftoken'),
                'Content-Type': 'application/json',
                'X-Requested-With': 'XMLHttpRequest'
            },
            credentials: 'same-origin'
        });
        
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        
        const data = await response.json();
        
        if(data.success) {
            if(action === 'minus' && data.product_amount <= 0) {
                location.reload();
            } else {
                quantitySpan.textContent = `Amount: ${data.product_amount}`;
                if (minusButton) {
                    minusButton.disabled = data.product_amount === 1;
                }
            }
        }
    } catch (error) {
        console.error('Error:', error);
        alert('Error updating cart. Please try again.');
    }
}

document.querySelectorAll('.minus-button').forEach(btn => {
    btn.addEventListener('click', (e) => handleCartAction(e, 'minus'));
});

document.querySelectorAll('.plus-button').forEach(btn => {
    btn.addEventListener('click', (e) => handleCartAction(e, 'plus'));
});

document.querySelectorAll('.cart-minus-button').forEach(btn => {
    btn.addEventListener('click', async (event) => {
        const response = await fetch   
    })
})


function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

