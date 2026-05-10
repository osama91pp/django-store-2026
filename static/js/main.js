async function cartUpdate(event, el) {
    event.preventDefault()
    const target = el || event.currentTarget
    const {data} = await axios.get(target.dataset.url)
    const {message, items_count} = data

    if (typeof notyf !== 'undefined') {
        notyf.success({
            message,
            dismissable: true,
            icon: false,
        })
    }

    const cartCount = document.getElementById('cart-count')
    if (cartCount) {
        cartCount.textContent = items_count ?? 0
    }
}

async function cartRemove(event, el) {
    event.preventDefault()
    const target = el || event.currentTarget
    await axios(target.dataset.url)
    location.reload()
}
