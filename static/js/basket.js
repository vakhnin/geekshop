$(document).ready(function () {
    "use strict";

    $('.card_add_basket').on('click', 'button[type="button"]', () => {
        let t_href = event.target.value;
        const user_authenticated = document.getElementById('user-authenticated');

        if (!user_authenticated) {
            $('#authenticated-modal').modal('show');
            return
        }

        $.ajax(
            {
                url: "/baskets/add/" + t_href + "/",
                success: (data) => {
                    $('.total-quantity-navigation').text(data.total_quantity);
                    if (data.no_product) {
                        $('#no-product-modal').modal('show');
                    }
                },
            });
        event.preventDefault()
    });

    function changeCount (event) {
        let eventChangeCount = $(event.target).first()
        let productID = eventChangeCount.attr("data-product-id")

        let action = "no-action"
        if (eventChangeCount.hasClass("increase-count")) {
            action = "increase-count"
        } else if (eventChangeCount.hasClass("decrease-count")) {
            action = "decrease-count"
        } else if (eventChangeCount.hasClass("delete-product")) {
            action = "delete-product"
        }

        $.ajax(
            {
                url: "/baskets/edit/" + productID + "/" + action + "/",
                success: (data) => {
                    if (data.no_product) {
                        $('#no-product-modal').modal('show');
                    } else {
                        $('.basket_list').html(data.result);
                        $('.total-quantity-navigation').text($('.total-quantity').text());

                        $('.change-count').on('click', 'a', (event) => {
                            changeCount(event)
                        })
                    }
                },
            });
        event.preventDefault()
    }

    $('.change-count').on('click', 'a', (event) => {
        changeCount(event)
    })
});
