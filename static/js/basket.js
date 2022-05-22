$(document).ready(function () {
    "use strict";

    $('.card_add_basket').on('click', 'button[type="button"]', () => {
        let t_href = event.target.value
        $.ajax(
            {
                url: "/baskets/add/" + t_href + "/",
                success: (data) => {
                    $('.card_add_basket').html(data.result)
                },
            });
        event.preventDefault()
    });

    $('.basket_list').on('click', 'input[type="number"]', () => {
        let t_href = event.target
        $.ajax(
            {
                url: "/baskets/edit/" + t_href.name + "/" + t_href.value + "/",
                success: (data) => {
                    $('.basket_list').html(data.result)
                },
            });
        event.preventDefault()
    });
});
