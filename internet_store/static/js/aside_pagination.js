// Pagination
document.querySelectorAll(".round_pagination_inactive").forEach(div => {
    if (div.classList.contains("round_pagination_active")){
        div.classList.remove("round_pagination_inactive")
    }
});
// Aside
document.querySelectorAll('.aside_link').forEach(link => {
    link.addEventListener('click', function(event) {
        const icon = this.querySelector('.aside_icon')
        if(icon.style.rotate.includes('180deg')){
            icon.style.rotate = '0deg'
        } else{
            icon.style.rotate = '180deg'
        }
    })   
});

document.getElementById("all_products_checkbox").addEventListener('click', function(event) {
    document.querySelectorAll('.category_aside_checkbox').forEach(asideCheckbox => {
        asideCheckbox.disabled = !asideCheckbox.disabled;
    })
});