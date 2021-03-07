
function MakeThread(data){
    if (data.privacy == "P"){
        privacy=1
    }
    else{
        privacy=0
    }
    var thread= document.createElement("div")
    thread.dataset.privacy=privacy
    thread.dataset.info=data.id
    thread.dataset.payment=data.payment_method
    thread.id="thread"
    thread.innerHTML=`<i class="fab fa-cc-${data.payment_method}" style="font-size: 50px;position: absolute;right: 80px;"></i>



                        <h3> Created by ${data.admin}</h3>
                        <p id="buyout"><b>Monthly Savings:</b> <span class="byserver">${ data.monthly_charge }</span></p>
                        <p id="participants"><b>Participants:</b> <span class="byserver">${ data.participants.length }</span></p>

                        <button class="btn btn-secondary" id="join" onclick='go_to_thread(event)'>View</button>
                            `
    document.querySelector("#threads").prepend(thread)
}
function create_thread_paypal(event){
    $("#payment-method").val("paypal")
    // $("#thread-creation-form").submit()
    var form = document.querySelector("#thread-creation-form")
    var price= form.children[0].children[1].value
    if (price <= 4000 && price >=100){
    var privacy = form.children[1].children[1].value
    var password= form.children[2].children[1].value
    var payment_method="paypal"
    $.ajax({
        url:"{% url 'create-thread' %}",
        method:"POST",
        data:{
            "csrfmiddlewaretoken":"{{ csrf_token }}",
            "price": price,
            "privacy":privacy,
            "password":password,
            "payment_method":payment_method,
        },
        success:function(e){
            console.log(e,status)
           // CallHome()
        //window.location="/home/"
                setTimeout(function() {
//your code to be executed after 1 second
}, 3000);
                MakeThread(e.thread)
                $('#createModal').modal('hide');
                //location.reload()
            return false;
            }

    })
   //CallHome()
}}
function create_thread_stripe(event){
    $("#payment-method").val("stripe")
    var form = document.querySelector("#thread-creation-form")
    var price= form.children[0].children[1].value
    if (price <= 4000 && price >=100){
    var privacy = form.children[1].children[1].value
    var password= form.children[2].children[1].value
    var payment_method="stripe"
    $.ajax({
        url:"{% url 'create-thread' %}",
        method:"POST",
        data:{
            "csrfmiddlewaretoken":"{{ csrf_token }}",
            "price": price,
            "privacy":privacy,
            "password":password,
            "payment_method":payment_method,
        },
        success:function(e){
            console.log(e,status)
            // alert(e.message)

            if ( e.message.substring(0,5) == "Our o" ){
                alert(e.message)

                CallHome()
                return false
    
            }
            else if (e.message == "CardInput"){
                window.location.href="{% url 'CardInput' %}"
                    return false
            }
            else{

                CallHome()
                    return false
            }

            window.location="{% url 'home' %}"
        },
        error:function(data){
            document.querySelector("#message-modal").innerText=data.message
            $('exampleModalCenter').modal('show');
            CallHome()

        }


    })
}}


function CallHome(){
    window.location.href="{% url 'home' %}"
    window.history.pushState(`home/`,"Home","Home")
}
$("#privacy-div").on('click',()=>{

$("#privacy-div").change(()=>{

    console.log($("#privacy-div").find(":selected").val())
    if ($("#privacy-div").find(":selected").val() == "P"){
        $("#password-div").css("display","block")

    }
    else{
        $("#password-div").css("display","none")
    }
})})
function send_req(e){
    thread_id= event.target.parentNode.parentNode.parentNode.parentNode.dataset.info
    password=$("#password-thread").val()
    console.log(thread_id,password)
    $.ajax({
            url: "{% url 'Join' %}",
            method:"POST",
            data: {
            'thread_id':thread_id,
            "password":password
            },
            dataType: 'json',
            success: function (data) {
            console.log(data)
                $("#thread-password-modal").modal("hide")
                if(data.message == "No Card"){
                    window.location.href='/card/'
                }
                if(data.message == "Incorrect password"){
                    $("#errorModal").modal("show")
                }
                 else if(data.message == "paypal success"){
                    $("#paypalModal").modal("show")
                }
                else if( data.message == "Success" ){
                window.location.href=`${thread_id}`
                }
            },
            error:function(e){
                window.location='/card/'
            }

    });
}
function Show_Creation_form(e){
    // document.querySelector("#thread_form").style.display="block"
    $('#createModal').modal('show');
}
function go_to_thread(e){
    console.log(event.target.parentNode)
    var thread_id=event.target.parentNode.dataset.info
    window.location.href=thread_id
}
function Display_card_form (e){

    var thread_id=event.target.parentNode.dataset.info
    var thread_payment_method=event.target.parentNode.dataset.payment
    if(event.target.parentNode.dataset.privacy == 1){
        document.querySelector("#thread-password-modal").dataset.info=thread_id
        document.querySelector("#thread-password-modal").dataset.payment=thread_payment_method
        $("#thread-password-modal").modal('show')
        if (thread_payment_method == "paypal"){
            $.ajax({
                url:"{% url 'Plan' %}",
                type:"POST",
                data:{"thread_id":thread_id},
                dataType:"json",
                success:function(data){
                    window.plan_id =data.plan_id

                }
            })

        }

    else{
        if (thread_payment_method == "paypal"){
                $.ajax({
                 url:"{% url 'Plan' %}",
                type:"POST",
                data:{"thread_id":thread_id},
                dataType:"json",
                success:function(data){
                        window.plan_id =data.plan_id
                        $("#paypalModal").modal("show")
                        }
                })
                //$("#paypalModal").modal("show")
        }
        else{
                $.ajax({
                url: "{% url 'Join' %}",
                type:"POST",
                data: {
                'thread_id':thread_id,
                "payment_method":thread_payment_method
                },
                dataType: 'json',
                success: function (data) {
                console.log(data)

                window.location=`${thread_id}`

                },
                error:function(e){
                        window.location='/card/'
                    }

                });
                }
            }}}
        paypal.Buttons({

createSubscription: function(data, actions) {

  return actions.subscription.create({

    'plan_id': window.plan_id

  });

},


onApprove: function(data, actions) {
    $.ajax({
        url:"{% url 'CreateSubscription' %}",
        type:"POST",
        data:{
            "plan_id":window.plan_id,
            "subscription_id":data.subscriptionID
        },
        dataType:'json',
        success:function(){
            console.log(data)
            CallHome()
            // alert('You have successfully created subscription ' + data.subscriptionID);
        }
    })


}


}).render('#paypal-button-container');
        function go_to_chat(e){
            var card=document.querySelector("#card_number").value
            var thread_id=document.querySelector(".cardform").dataset.info
            var cvc=document.querySelector("#cvc").value
            var exp_month=document.querySelector("#exp_month").value
            var exp_year=document.querySelector("#exp_year").value
            $.ajax({
                url: {% url 'Join' %},
                type:"POST",
                data: {
                    'thread_id':thread_id,
                    'cvc':cvc,
                    'card':card,
                    'exp_month':exp_month,
                    'exp_year':exp_year
                    },
                    dataType: 'json',
                    success: function (data) {
                    console.log(data)
    
                    window.location.href=`${thread_id}`
    
                    }
            });
            }
        