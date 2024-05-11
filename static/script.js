
const stripe = Stripe(STRIPE_PUBLIC_KEY);

var createCheckoutSession = function (priceId) {
    return fetch("/v1/create-checkout-session", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ priceId: priceId }),
    }).then(function (response) {
        return response.json();
    });
};

document.addEventListener("DOMContentLoaded", function (event) {
    document
    .getElementById("checkout-premium")
    .addEventListener("click", function (evt) {
        createCheckoutSession(STRIPE_PREMIUM_PRICE_ID).then(function (data) {
            stripe
                .redirectToCheckout({
                    sessionId: data.sessionId,
                });
        });
    });

    document
    .getElementById("checkout-basic")
    .addEventListener("click", function (evt) {
        createCheckoutSession(STRIPE_BASIC_PRICE_ID).then(function (data) {
            stripe
                .redirectToCheckout({
                    sessionId: data.sessionId,
                });
        });
    });

});