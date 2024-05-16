let button = document.querySelector("#btn_orders")
console.log("Seems like I'm running")
button.addEventListener("click", () => {

    let inputvalue = document.querySelector("#id_number").value
    if (!inputvalue){
        alert("Please input a number")
    }else{
        window.location.replace(`/orders/${inputvalue}`)
    }
})