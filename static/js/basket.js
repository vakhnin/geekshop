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

    $('.basket_list').on('click', () => {
        let t_href = $(event.target)

        let action = "no-action"
        if (t_href.hasClass("increase-count")) {
            action = "increase-count"
        }
        if (t_href.hasClass("decrease-count")) {
            action = "decrease-count"
        }

        $.ajax(
            {
                url: "/baskets/edit/" + t_href.attr("name") + "/" + action + "/",
                success: (data) => {
                    $('.basket_list').html(data.result);
                    $('.total-quantity-navigation').text($('.total-quantity').text());
                    if (data.no_product) {
                        $('#no-product-modal').modal('show');
                    }
                },
            });
        event.preventDefault()
    });
});
