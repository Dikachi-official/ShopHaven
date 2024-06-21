/*--==== FUNCTION TO SELECT CATEGORY OR VENDOR FROM TICKBOX  ====--*/
$(document).ready(function (){
    $(".filter-checkbox, #price-filter-btn").on("click", function(){
        
        console.log("A checkbox has been clicked");

        let filter_object = {}

        let min_price = $("#max_price").attr("min") //get the attr (min) from our product temp(input section)
        let max_price = $("#max_price").val()  //get the val of max_price from our product temp(input section)

        filter_object.min_price = min_price; //reassign var to filter-object.min_price
        filter_object.max_price = max_price;

        $(".filter-checkbox").each(function(){
            let filter_value = $(this).val()
            let filter_key = $(this).data("filter")  

            /*=== console.log("Filter value is:", filter_value); ===*/
            /*=== console.log("Filter key is:", filter_key); ===*/

            filter_object[filter_key] = Array.from(document.querySelectorAll('input[data-filter=' + filter_key + ']:checked')).map(function(element){
                return element.value
            })
        })
        console.log("Filter Object is: ", filter_object);
        $.ajax({
            url: '/filter-product',
            data: filter_object,
            dataType: 'json',
            beforeSend: function(){
                console.log("Trying to filter product....");
            },
            success: function(response){
                console.log(response);
                console.log("Data filtered successfully...");
                $("#filtered-product").html(response.data)
            }
        })
    })

    /*--=== FUNCTION TO MAKE SLIDER INTERACTIVE ===--*/
    $("#max_price").on("blur", function(){
        let min_price = $(this).attr("min")
        let max_price = $(this).attr("max")
        let current_price = $(this).val()

        //console.log("The current price is :", current_price);
        //console.log("The maximum price is :", max_price);
        //console.log("The minimum price is :", min_price);

        if(current_price < parseInt(min_price) || current_price > parseInt(max_price)){
            
            //console.log("Price Error Occured");

            alert("Price must be between $" + min_price + "and $" + max_price)
            $(this).val(min_price)
            $("#range").val(min_price)

            $(this).focus()

            return false
        }
    })

    
    /*--=== FUNCTION TO DELETE PRODUCTS IN CART PAGE ===--*/
    $(document).on("click", ".delete-product", function(){

        let id = $(this).attr("data-product")
        let this_val = $(this)

        console.log("Product ID is:",id);

        $.ajax({
            url: "/delete-cart",
            data: {
                "id":id
            },
            dataType: "json",
            beforeSend: function(){
                /*this_val.hide()*/
                console.log("Deleting Product");
            },
            success: function(response){
                this_val.show()
                $("#cart-list").html(response.data)
                console.log("Deleted product from cart");
            }
        })
    })



     /*--=== FUNCTION TO UPDATE PRODUCTS IN CART PAGE ===--*/
     $(".update-product").on("click", function(){

        let product_id = $(this).attr("data-product")
        let product_qty = $(".product-qty-"+product_id).val()
        let this_val = $(this)

        console.log("Product ID:",product_id);
        console.log("product quantity:", product_qty);

        $.ajax({
            url: "/update-cart",
            data: {
                "id":product_id,
                "qty":product_qty,
            },
            dataType: "json",
            beforeSend: function(){
                this_val.hide()
            },
            success: function(response){
                this_val.show()
                $("#cart-list").html(response.data)
            }
        })
    })



    /*--=== FUNCTION IN MAKING DEFAULT ADDRESS ===--*/
    $(document).on("click", ".make-default-address", function(){
        let id = $(this).attr("data-address-id")
        let this_val = $(this)

        console.log("My ID is:", id);
        console.log("Element is:",this_val);

        $.ajax({
            url: "/make-default-address",
            data: {
                "id":id
            },
            dataType: "json",
            success: function(response){
                console.log("Address Made Default...");
                if (response.boolean == true){

                    $(".check").hide()
                    $(".action_btn").show()

                    $(".check"+id).show()
                    $(".button"+id).hide()
                }
            }
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
                this_val.html("✔")
                if (response.bool === True){
                    $(".add-to-wishlist").hide()
                    console.log("Added to wishlist...");
                }
            }
        })
    })


    /*--== DELETE WISHLIST ==*/
    $(document).on("click", ".wish-delete", function(){
        let wishlist_id = $(this).attr("data-wishlist-product")
        let this_val = $(this)

        console.log("Wishlist ID is:",wishlist_id);

        $.ajax({
            url: "/delete-from-wishlist",
            data: {
                "id": wishlist_id
            },
            dataType: "json",
            beforeSend: function(){
                console.log("Deleting product from wishlist");
            },
            success: function(response){
                $("#wishlist-list").html(response.data)
                console.log("Deleted product from wishlist");
            }
        })
    })


    /*=== CONTACT US FORM ===*/
    $(document).on("submit", "#contact-form-ajax", function(e){
        e.preventDefault()
        console.log("Form Submitted......");


        let full_name = $("#firstname").val()
        let email = $("#email").val()
        let phone = $("#phone").val()
        let subject = $("#sender-subject").val()
        let message = $("#sender-msg").val()

        console.log("Name :", full_name);
        console.log("Email :", email);
        console.log("Phone :", phone);
        console.log("Subject :", subject);
        console.log("Message :", message);

        $.ajax({
            url: "/ajax-contact-form",
            data: {
                "full_name": full_name,
                "email":email,
                "phone":phone,
                "subject": subject,
                "message":message,
            },
            dataType:"json",
            beforeSend: function(){
                console.log("Sending Data To Server...");    
            },
            success: function(res){
                console.log("Sent Data to Server!!!!");
            }
        })

    })



})