'use strict';

function fetchCart() {
    $.ajax({
        url: '/shop/cart?type=json',
        success: function (response) {
            $('#cart-items-count').text(response.cart_items_count);
            $('#cart-total').text('$' + response.cart_total);
        }
    });
}

function success(message) {
    Toastify({
        text: message,
        close: true,
        style: {
            background: "#7fad39",
        }
    }).showToast();
}

$(document).ready(function () {
    // load cart info
    fetchCart();

    $('.add-to-cart').click(function (e) {        
        $.ajax({
            url: '/shop/cart?action=add',
            method: 'POST',
            headers: {
                "X-CSRFToken": csrfToken
            },
            data: {
                'id': $(this).data('id'),
                'price': $(this).data('price'),
                'quantity': $('#quantity').val() ?? $(this).data('quantity')
            },
            success: function (response) {
                $('#cart-items-count').text(response.cart_items_count);
                $('#cart-total').text('$' + response.cart_total);
                
                success("Item was added successfully !");
            }
        }); 
    });

    $('.update-cart').click(function (e) {        
        let cart_updated_items = [];

        $('.quantity-input').each(function (index) {
            cart_updated_items.push({
                'id': $(this).data('id'),
                'price': $(this).data('price'),
                'quantity': $(this).val()
            });
        });

        $.ajax({
            url: '/shop/cart?action=update',
            method: 'POST',
            headers: {
                "X-CSRFToken": csrfToken
            },
            data: {
                'data': JSON.stringify(cart_updated_items)
            },
            success: function (response) {
                $('#cart-items-count').text(response.cart_items_count);
                $('#cart-total').text('$' + response.cart_total);
                $('#order-total').text('$' + response.cart_total);

                let cart_updated_items = JSON.parse(response.cart_items)['data'];

                cart_updated_items.forEach(function (item) {
                    $('#item-total-' + item['id']).text('$' + item['total']);
                });
                
                success("Cart was updated successfully !");
            }
        }); 
    });

    $('.remove-from-cart').click(function (e) {
        if (!confirm('Are you sure ?')) {
            return;
        }
        
        $('#item-' + $(this).data('id')).remove();

        let cart_updated_items = [];

        $('.quantity-input').each(function (index) {
            cart_updated_items.push({
                'id': $(this).data('id'),
                'price': $(this).data('price'),
                'quantity': $(this).val()
            });
        });

        $.ajax({
            url: '/shop/cart?action=update',
            method: 'POST',
            headers: {
                "X-CSRFToken": csrfToken
            },
            data: {
                'data': JSON.stringify(cart_updated_items)
            },
            success: function (response) {
                $('#cart-items-count').text(response.cart_items_count);
                $('#cart-total').text('$' + response.cart_total);
                $('#order-total').text('$' + response.cart_total);

                let cart_updated_items = JSON.parse(response.cart_items)['data'];

                cart_updated_items.forEach(function (item) {
                    $('#item-total-' + item['id']).text('$' + item['total']);
                });
                
                success("Cart was updated successfully !");
            }
        }); 
    });
});