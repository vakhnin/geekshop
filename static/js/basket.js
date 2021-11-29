window.onload = function () {
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
    })
}
