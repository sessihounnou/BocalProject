const btn=document.querySelector('.btn')
const rts=document.querySelector('.rate-section')
const items = document.querySelectorAll('.emojis .item');
const submit=document.querySelector('.submit')
const successPopup=document.querySelector('.success-popup')


btn.addEventListener('click', ()=>{
    if(rts.className==="rate-section"){
    rts.classList.add('rate-section-slide')
    }
    else{
        rts.classList.remove('rate-section-slide')
    }
})

items.forEach(item=>{
    item.addEventListener('click', ()=>{
        items.forEach(item=>[
            item.classList.remove('active')
        ])
        item.classList.add('active')
    })
})

submit.addEventListener('click', ()=>{
    successPopup.classList.add('success-popup-slide')
})