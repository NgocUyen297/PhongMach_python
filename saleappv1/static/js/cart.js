function pay(id){
    if(confirm("ban co chac thanh toan khong") == true)
    {
        fetch('/api/pay',
            { method: 'post',
             body: JSON.stringify({
            'id': id,
        }),
        headers: {
            'Content-Type': 'application/json'
        }
           }).then(function(res){
            return res.json()
           }).then(function(data){
            if(data.code == 200){
                location.reload()
            }
           }).catch(function(err){
            console.error(err)
           })
    }
}

function addToCart(i){
    var x = document.getElementsByClassName("medicine");
    var unit = document.getElementsByClassName("unit");
    var how_to_use = document.getElementsByClassName("how_to_use");

    id = x[i].value
    if(id != 0)
    {
        fetch('/api/add_medicine_to_cart',{
        method: 'post',
        body: JSON.stringify({
            'id': id
        }),
        headers: {
            'Content-Type': 'application/json'
        }
       }).then(function(res){
        console.info(res)
        return res.json()
       }).then(function(data){
        console.info(data)
         if(data.unit == 'vien'){
              unit[i].innerHTML =  `<span>viên</span>`
         }
         else
         {
              unit[i].innerHTML =  `<span>chai</span>`
         }
         how_to_use[i].innerHTML = data.how_to_use


       }).catch(function(err){
           console.error(err)
       })
   }
   else
   {
    console.log('id = 0')
   }
}

function saveMedicalBill(){
    if(confirm("ban co chac luu phieu") == true)
    {
        fetch('/api/add_phieu_kham',
            { method: 'post'
           }).then(function(res){
            return res.json()
           }).then(function(data){
            if(data.code == 200){
            }
           }).catch(function(err){
            console.error(err)
           })
    }
}

function updateQuantity(line, obj){
      var x = document.getElementsByClassName("medicine");
      id = x[line].value
      console.log(id)
      console.log(obj.value)
   if(id){
    fetch('/api/update_quantity',
            { method: 'put',
             body: JSON.stringify({
                'id': id,
                'quantity': parseInt(obj.value)
               }),
            headers: {
                    'Content-Type': 'application/json'
              }
           }).then(function(res){
            return res.json()
           }).then(function(data){
            if(data.code == 200){
                console.log("thanh cong")
            }
           }).catch(function(err){
                console.error(err)
           })
    }
    else
    {
      console.log("ko lấy được id")
    }
}