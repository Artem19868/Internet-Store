const purchaseButton = document.getElementById("product_purchase_button");
//Timer
let timer = 20;
const intervalId = setInterval(() => {
    purchaseButton.textContent = `Please wait ${timer} seconds`
    if (timer <= 0){
        clearInterval(intervalId);
        purchaseButton.removeAttribute('disabled');
        purchaseButton.textContent = "Buy";
        return;
    }
    timer--;
}, 1000)
//Click event
purchaseButton.addEventListener('click', (event) =>{
    return alert("This feature is currently unavailable")
})