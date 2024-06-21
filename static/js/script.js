/*== CSRF DOCUMENTATION ==*/
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
const csrftoken = getCookie('csrftoken');
/*== END OF DOCUMENTATION ==*/






let btns = document.querySelectorAll(".col-4 button")  /*== DIV LOCATION OF THE BUTTON ==*/

btns.forEach(btn =>{
    btn.addEventListener("click", addToCart)  /*== CLICK LISTENER ==*/
})

function addToCart(e){                  /*== TO TARGET THE EXACT BUTTON CLICKED(by value in button field) ==*/
    let product_id = e.target.value
    let url = "/add_to_cart"
    let quantity = "#quantity"

    /*== pass to the id key to data ==*/

    let data = {
        "id":product_id,
        "qty":quantity
    }

    fetch(url, {
        method:"POST",
        headers: {"Content-Type":"application/json", 'X-CSRFToken': csrftoken},
        body: JSON.stringify(data)      
    })
    /*== TYPE OF FILE BEING SENT ==*/
    /*== CSRF ATTACHMENT ==*/
    /*== MESSAGE BODY(WE CONVERT THE DATA TO JSON DATA) ==*/

    .then(res=>res.json())     /*==THE METHOD OF RESPONSE GOING TO THE VIEWS(JSON FORMAT)==*/
    .then(data=>{
        document.getElementById("num_of_items").innerHTML = data        /*== TO ADD TO CART WITHOUT REFRESHING ==*/
        console.log(data)       /*== DATA TO BE PASSED TO VIEWS TO BE DISPLAYED ==*/
    })
    .catch(error=>{
        console.log(error)        /*IF ANY ERROR, LETS BE NOTIFIED */
    })
}


/*---== JAVASCRIPT FOR AVOID PAGE REFRESH AFTER PRODUCT REVIEW AND STAR RATING REVIEW==--*/
console.log("working fine");

$("#commentForm").submit(function(e){
    e.preventDefault();

    $.ajax({
        data: $(this).serialize(),

        method: $(this).attr("method"),

        url: $(this).attr("action"),

        dataType: "json",

        success: function(res){
            console.log("Comment saved to database...");

            if(res.bool == true){
                $("#review-res").html("Review added successfully")
                //$(".hide-comment-form").hide()
                //$(".add-review").hide()

                let _html = '<div class="review-section">'

                    _html += '<div class="review-child">'
                    _html += '<span><b>{{review.user.username}}</b></span>'       
                    _html += '<span class="review-date">{{review.date|date:"d,M, Y"}}</span>'

                    _html += '<div>'
                    for(var i=1; i <=res.context.rating; i++){
                        _html += '★';
                    }
                    _html += '</div>'

                    _html += '<p>'+ res.context.review +'</p>'
                    _html += '</div>'

                    _html += '</div>'
                    
                    $(".comment-list").prepend(_html)
            }
        }    
    })
})





/*==== GETTING TIEM AND YEAR USING JS ====*/
const monthNames = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug","Sep","Oct", "Nov", "Dec"];

$("#commentForm").submit(function(e){
    e.preventDefault();

    let dt = new Date();
    let time = dt.getDay() + " " + monthNames[dt.getUTCMonth()] + ", " + dt.getFullYear()


})




/*--==== FUNCTION TO SELECT CATEGORY OR VENDOR FROM TICKBOX  ====--*/
$(document).ready(function (){
    $(".filter-checkbox").on("click", function(){
        
        console.log("A checkbox has been clicked");

        let filter_object = {}

        $(".filter-checkbox").each(function(){
            let filter_value = $(this).val()
            let filter_key = $(this).data("filter")

            console.log("Filter value is:", filter_value);
            console.log("Filter key is:", filter_key);
        })
    })





    /*--=== ADDING TO WISHLIST ===--*/
    $(document).on("click", ".add-to-wishlist", function(){
        let product_id = $(this).attr("data-product-item")
        let this_val = $(this)

        console.log("Product_ID is:", product_id);

        $.ajax({
            url: "/add-to-wishlist",
            data: {
                "id": product_id
            },
            dataType:"json",
            beforeSend: function(){
                console.log("Adding to wishlist...")
            },
            success: function(response){
                this_val.html("Tick")
                if (response.bool === True){
                    console.log("Added to wishlist...");
                }
            }
        })
    })


    


   

    function makePayment() {

        /*--===TO GET THE TOTAL PRICE AND IDENTIFY THE INDIVIDUAL CART IN CHECKOUT===*/
        let cart_total = "{{cart.total_price}}"
        let cart_id = "{{cart.id}}" 

        FlutterwaveCheckout({                                              
            /*= IMPORTANT NOTICE =*/
            public_key: "FLWSECK_TEST-7c8fd3a982a2f69aa8faecce686c37b9-X",   /*== MY SECRET API KEY FROM FLUTTERWAVE ==*/
            tx_ref: "titanic-48981487343MDI0NzMx",
            amount: cart_total,
            currency: "NGN",
            payment_options: "card, mobilemoneyghana, ussd",                    /*= IMPORTANT NOTICE =*/
            redirect_url: "http://127.0.0.1:8000/cart/confirm_payment/"+ cart_id,  /*= IF ON DEV SERVER, REMOVE THE LAST "/" AND LET IT BE "HTTP" NOT HTTPS =*/
            meta: {
                consumer_id: 23,
                consumer_mac: "92a3-912ba-1192a",
            },
            customer: {
                email: "rose@unsinkableship.com",
                phone_number: "08104848224",
                name: "{{request.user.username}}",
            },
            customizations: {
                title: "Myke Store",
                description: "Tech with Style",
                logo: "{% static 'img/myke.jpg' %}",
            },

        });
    }



    /*----==== JQUERY FOR ALERT SIGNUP MESSAGE ====----*/
    setTimeout(function(){
    $('message').fadeOut('slow')
    }, 3000)






})











