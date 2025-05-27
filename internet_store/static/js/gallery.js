const mainImg = document.getElementById('main-photo');

document.querySelectorAll('.gallery-photo').forEach(img => {
    img.addEventListener('click', (event) => {
        const imgUrl = event.currentTarget.src;
        mainImg.src = imgUrl;
    })
})