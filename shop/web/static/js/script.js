let locationList = document.querySelector('.location-list');

document.querySelector('#location-btn').onclick = () => {
    locationList.classList.toggle('active');
    navbar.classList.remove('active');
    searchForm.classList.remove('active');
    shoppingCart.classList.remove('active');
    loginForm.classList.remove('active');
}

let searchForm = document.querySelector('.search-form');

document.querySelector('#search-btn').onclick = () => {
    searchForm.classList.toggle('active');
    locationList.classList.remove('active');
    shoppingCart.classList.remove('active');
    loginForm.classList.remove('active');
    navbar.classList.remove('active');
}

let shoppingCart = document.querySelector('.shopping-cart');

document.querySelector('#cart-btn').onclick = () => {
    shoppingCart.classList.toggle('active');
    locationList.classList.remove('active');
    searchForm.classList.remove('active');
    loginForm.classList.remove('active');
    navbar.classList.remove('active');
}

let loginForm = document.querySelector('.login-form');

document.querySelector('#login-btn').onclick = () => {
    loginForm.classList.toggle('active');
    locationList.classList.remove('active');
    searchForm.classList.remove('active');
    shoppingCart.classList.remove('active');
    navbar.classList.remove('active');
}

let navbar = document.querySelector('.navbar');

document.querySelector('#menu-btn').onclick = () => {
    navbar.classList.toggle('active');
    locationList.classList.remove('active');
    searchForm.classList.remove('active');
    shoppingCart.classList.remove('active');
    loginForm.classList.remove('active');
}

window.onscroll = () => {
    searchForm.classList.remove('active');
    shoppingCart.classList.remove('active');
    loginForm.classList.remove('active');
    navbar.classList.remove('active');
    // locationList.classList.remove('active');
}

var user_city= Cookies.get('user_city');
check_cookie(user_city);

function check_cookie(user_city) {
    console.log(user_city);
    if (user_city == undefined) {
        // выпадающий div городов, при первом посещении
        document.querySelector('#location-btn').click();
        locationList.classList.toggle('active');   
    }
}

// обработка событий выбора города
const wrapper = document.querySelector('.location-list');
let city = '';

function handleClick(e) {
    var target_city = e.target.innerHTML
    city = target_city
    console.log('choose city: ', city);
    document.getElementById('city').value = e.target.innerHTML;
}

wrapper.addEventListener('click', handleClick);

$(document).on('submit','#login-form', function(e){
    e.preventDefault();
    $.ajax({
        type: "post",
        url: "/login/",
        data: {
            username: $('#username').val(),
            password: $('#password').val(),
            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
        },
        success: function(data){
            // console.log(response)
            if (data.includes("Error!")){
                alert(data)
            }
            else{
                // refresh page
                location.reload();
            }
        },
        error: (error) => {
            console.log(JSON.stringify(error));
        },
    });
});