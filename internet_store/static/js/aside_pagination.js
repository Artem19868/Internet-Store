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

//Prevent the form from being sent
document.getElementById('filters_form').addEventListener('submit', function(e) {
    e.preventDefault();
});

function submitCategories(){
    const form = document.getElementById("filters_form");
    const formData = new FormData(form);

    formData.delete("max_price");
    formData.delete("min_price");

    const params = new URLSearchParams(formData);
    window.location.search = params.toString();
}

function submitPrice(){
    const form = document.getElementById("filters_form");
    const formData = new FormData(form);

    formData.delete("categories_slug");

    const params = new URLSearchParams(formData);
    window.location.search = params.toString();
}

function submitAllFilters(){
    const form = document.getElementById("filters_form");
    const formData = new FormData(form);

    const params = new URLSearchParams(formData);
    window.location.search = params.toString();
}

function clearFilters(){
    const params = new URLSearchParams();

    const currentParams = new URLSearchParams(window.location.search);
    const searchParam = currentParams.get("search");

    if(searchParam){
        params.set("search", searchParam);
    }
    console.log(params)
    window.location.search = params.toString();
}