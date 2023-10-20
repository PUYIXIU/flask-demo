// $(function(){}) = window.onload = function(){}
function bindClick(){
    $('#send-code-button').click(click)
}

function click(e){
   e.preventDefault()
   let email = $('#email').val()
   $.ajax({
       url:`/index/captcha/email?email=${email}`,
       method:'GET',
       success:res=>{
           let {code, message, data} = res
           let count = 60
           if(code===200){
               $('#send-code-button').unbind('click',click)
               $('#send-code-button').css('cursor','not-allowed')
                   $('#counter').text(count)
               $('#counter').css('display','block')
               let counter = setInterval(()=>{
                   $('#counter').text(--count)
                   if(count<=0){
                        $('#counter').css('display','none')
                        $('#send-code-button').css('cursor','pointer')
                        bindClick()
                        clearInterval(counter)
                   }
               },1000)
           }
       },
       error:err=>{
           alert('oh no :( send fail')
       }
   })
}

$(function(){
    bindClick()
})