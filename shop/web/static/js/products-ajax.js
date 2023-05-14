var purchase = [];
var temp_deleting = []

$(document).ready(function (){
// main or products page 

    // increment
    $('.products').find('.fa-plus').click(function (e){
        e.preventDefault();
        var inc_value = $(this).closest('.box').find('.qty-input').val();
        var value = parseInt(inc_value, 10);
        var product_amount = $(this).closest('.box').find('.product-amount').val();
        var value_amount = parseInt(product_amount, 10);
        value = isNaN(value) ? 0 : value;
        if (value < value_amount)
        {
            value++;
            $(this).closest('.box').find('.qty-input').val(value);
        }
    });

    // decrement
    $('.products').find('.fa-minus').click(function (e){
        e.preventDefault();
        var dec_value = $(this).closest('.box').find('.qty-input').val();
        var value = parseInt(dec_value, 10);
        // console.log(product_amount);
        value = isNaN(value) ? 0 : value;
        if (value > 1)
        {
            value--;
            $(this).closest('.box').find('.qty-input').val(value);
        }
    })
    // add to cart 
    $('.addToCartBtn').click(function (e){
        e.preventDefault();
        var product_id = $(this).closest('.data-to-cart').find('#product-id').val();
        var product_title = $(this).closest('.data-to-cart').find('#product-title').val();
        var product_qty = $(this).closest('.data-to-cart').find('.qty-input').val();
        var product_price = $(this).closest('.box').find('.product-price').val();
        var product_img = $(this).closest('.box').find('img').attr("src");
        console.log('id: ', product_id, 'qty: ', 
        product_qty, 'price:', product_price, '$', ' img:', product_img);
        var token = $('input[name=csrfmiddlewaretoken]').val();
        $.ajax({
            type: "POST",
            url: "/add-to-cart/",
            data: {
                'id': product_id,
                'title': product_title,
                'qty': product_qty,
                'price': product_price,
                'image': product_img,
                csrfmiddlewaretoken: token,
            },
            dataType: "json",
            success: function (data) {
                // нжатие на кнопку корзины, если неактивна
                var cart_active = $('.shopping-cart').hasClass('active'); 
                if (!cart_active) {
                    $('#cart-btn').click();
                }
                var is_cart_has_item = cart_has_item(product_id)
                var product_data = []
                var dataItem = {}
                if (is_cart_has_item){
                    purchase = purchase.filter((item) => item.id !== product_id);
                    $('.cart-box').each(function(index, value) {
                        var input = $(value).find('input').val()
                        if (input == product_id){
                            console.log('Product id: ',input)
                            $(this).remove()
                        }
                    });
                }
                dataItem["id"] = product_id
                dataItem["title"] = product_title
                dataItem["qty"] = product_qty
                dataItem["price"] = product_price
                purchase.push(dataItem)
                dataItem["image"] = product_img
                product_data.push(dataItem)
                // шаблон из main.html
                var template = $.templates("#hidden-template-cart");
                var htmlOutput = template.render(product_data);
                $(document).find(".shopping-cart-container").append(htmlOutput);
                calc_purchase()
            }
        });
    });

    // delete from cart
    $("body").delegate(".fa-trash", "click", function() {
        var product_id = $(this).parent().find('input').val()
        $.ajax({
            type: "get",
            url: "/delete-from-cart/",
            data: {
                'id': product_id,
            },
            dataType: "json",
            success: function (response) {
                console.log('Sucsess Deleting id:', product_id)
                value = $('.shopping-cart-container').find('input').val()
                $('.shopping-cart-container').find('.cart-box').each(function( index ) {
                    value_id = $(this).find('input').val()
                    if(value_id === product_id){
                        $(this).remove()
                    }
                });
                purchase = purchase.filter((item) => item.id !== product_id);
                calc_purchase()
            },
            error: (error) => {
                console.log(JSON.stringify(error));
            },
        });
    });

    // подсчёт суммы товаров из сессии при загрузке страницы
    $('.shopping-cart-container').find('.cart-box').each(function( index ) {
        dataItem = {}
        dataItem["id"] = $(this).find('input').val()
        dataItem["title"] = $(this).find('#title').val()
        dataItem["qty"] = $(this).find('#quantity').val()
        dataItem["price"] = $(this).find('#price').val()
        purchase.push(dataItem)
        calc_purchase()
    });

    // CART PAGE
    // increment cart
    $('.cart-products').find('.fa-plus').click(function (e){
        e.preventDefault();
        var product_qty = $(this).closest('.box').find('.qty-input').val();
        var product_id = $(this).closest('.box').find('#product-id').val();
        var value = parseInt(product_qty, 10);
        var token = $('input[name=csrfmiddlewaretoken]').val();
        var product_amount = $(this).closest('.box').find('.product-amount').val();
        var value_amount = parseInt(product_amount, 10);
        value = isNaN(value) ? 0 : value;
        if (value < value_amount)
        {
            value++;
            $(this).closest('.box').find('.qty-input').val(value);
        }

        $.ajax({
            type: "post",
            url: "/change-session/",
            data: {
                'id': product_id,
                'qty': value,
                csrfmiddlewaretoken: token,
            },
            dataType: "json",
            success: function (response) { 
                change_item_cart(product_id, value)
                calc_purchase()
            }
        });
        
    });

    // decrement cart
    $('.cart-products').find('.fa-minus').click(function (e){
        e.preventDefault();
        var dec_value = $(this).closest('.box').find('.qty-input').val();
        var product_id = $(this).closest('.box').find('#product-id').val();
        var token = $('input[name=csrfmiddlewaretoken]').val();
        var value = parseInt(dec_value, 10);
        value = isNaN(value) ? 0 : value;
        if (value > 1)
        {
            value--;
            $(this).closest('.box').find('.qty-input').val(value);
        }
        $.ajax({
            type: "post",
            url: "/change-session/",
            data: {
                'id': product_id,
                'qty': value,
                csrfmiddlewaretoken: token,
            },
            dataType: "json",
            success: function (response) {
                change_item_cart(product_id, value)
                calc_purchase()
            }
        });
    })

    // delete from cart
    $('.cart-products').find('.deleteFromCartBtn').click(function (e){
        e.preventDefault();
        var product_id = $(this).closest('.box').find('#product-id').val();
        $.ajax({
            type: "get",
            url: "/delete-from-cart/",
            data: {
                'id': product_id,
            },
            dataType: "json",
            success: function (response) {
                const index = purchase.findIndex(n => n.id === product_id);
                if (index !== -1) {
                    purchase.splice(index, 1);
                }
                $('.cart-products').find('.box').each(function( index ) {
                    value_id = $(this).find('#product-id').val()
                    if(value_id === product_id){
                        console.log('delete this product:', $(this).find('input').val())
                        $(this).remove()
                    }
                });
                calc_purchase()
            }
        });
    });

    // cart-order
    $('.cart-products').find('.orderBtn').click(function (e){
        e.preventDefault();
        var order_price = $(this).closest('.cart-order').find('.total-price').val();
        $.ajax({
            type: "get",
            url: "checkout/",
            data: {
                'order_price': order_price,
            },
            dataType: "json",
            success: function (response) {
                console.log(order_price)
                alert('Order was successful!')
                location.reload()
            }
        });
    });
});

// изменение кол-ва товаров на странице cart
function change_item_cart(product_id, qty){
    purchase = purchase.map((post) => ({
    ...post,
        qty: post.id === product_id ? qty : post.qty
    }));
}

// Проверка содержит ли корзина выбранный товар
function cart_has_item(product_id){
    var search_id = parseInt(product_id, 10)
    var has_item = false;
    $.each(purchase, function() {
        var id = Object.keys(this)[0];
        var value_id = parseInt(this[id], 10);
        if (value_id == search_id){
            has_item = true;
            return true;
        }
    });
    return has_item;
}

// подсчет итоговой суммы покупки
function calc_purchase() {
    var sum_purchase = 0;
    $.each(purchase, function() {
        var id = Object.keys(this)[0];
        var title = Object.keys(this)[1];
        var qty = Object.keys(this)[2];
        var price = Object.keys(this)[3];
        var value_qty = parseInt(this[qty], 10);
        var value_price = parseFloat(this[price]);
        sum_purchase = sum_purchase + (value_qty * value_price)
      });
    // console.log(sum_purchase);
    $('.total-price').val(sum_purchase);
}