(function(){
  'use strict';
  var timerEl=document.getElementById('timer');
  var total=600;
  function pad(n){return n<10?'0'+n:String(n)}
  function renderTimer(){if(timerEl) timerEl.textContent=pad(Math.floor(total/60))+' : '+pad(total%60)}
  renderTimer();
  if(timerEl) window.setInterval(function(){total=total>0?total-1:600;renderTimer()},1000);

  function openModal(id){var el=document.getElementById(id);if(el)el.classList.add('show')}
  function closeAll(){document.querySelectorAll('.modal.show').forEach(function(m){m.classList.remove('show')})}
  document.querySelectorAll('[data-close]').forEach(function(b){b.addEventListener('click',function(){var wasWin=b.closest('#mWin');closeAll();if(wasWin){var order=document.getElementById('order');if(order){order.classList.remove('hidden');order.scrollIntoView({behavior:'smooth',block:'center'})}}})});
  document.querySelectorAll('.modal').forEach(function(m){m.addEventListener('click',function(e){if(e.target===m)closeAll()})});
  document.addEventListener('keydown',function(e){if(e.key==='Escape')closeAll()});

  var doors=document.querySelectorAll('.door');
  var played=false;
  doors.forEach(function(d){d.addEventListener('click',function(){if(played)return;played=true;doors.forEach(function(x){x.classList.add('open');x.disabled=true});d.classList.add('win');var pct=d.querySelector('.pct');if(pct)pct.textContent=d.getAttribute('data-v')||pct.textContent;window.setTimeout(function(){openModal('mWin')},450)})});
  var gift=document.getElementById('gift');
  if(gift)gift.addEventListener('click',function(){var t=document.getElementById('doorsTitle');if(t)t.scrollIntoView({behavior:'smooth',block:'start'})});

  var phone=document.getElementById('fPhone');
  var msg=document.getElementById('phoneMsg');
  function formatPhone(raw){var d=raw.replace(/\D/g,'');if(d.indexOf('998')===0)d=d.slice(3);d=d.slice(0,9);var out='+998';if(d.length>0)out+=' '+d.slice(0,2);if(d.length>2)out+=' '+d.slice(2,5);if(d.length>5)out+=' '+d.slice(5,7);if(d.length>7)out+=' '+d.slice(7,9);return out}
  function phoneValid(){return phone&&/^\+998 \d{2} \d{3} \d{2} \d{2}$/.test(phone.value)}
  function showPhoneState(valid){if(!phone||!msg)return;phone.classList.toggle('ok',valid);phone.classList.toggle('bad',!valid);msg.className='msg '+(valid?'ok':'bad');msg.textContent=valid?"✅ Telefon raqami to'g'ri":"⚠️ Telefon raqami noto'g'ri! Format: +998 XX XXX XX XX"}
  if(phone){phone.addEventListener('focus',function(){if(!phone.value)phone.value='+998 '});phone.addEventListener('input',function(){var pos=phone.selectionStart;phone.value=formatPhone(phone.value);if(phone.value.length>5)showPhoneState(phoneValid());else if(msg)msg.className='msg';try{phone.setSelectionRange(phone.value.length,phone.value.length)}catch(e){}});phone.addEventListener('blur',function(){if(phone.value && !phoneValid())showPhoneState(false)})}
  var form=document.getElementById('orderForm');
  if(form)form.addEventListener('submit',function(e){e.preventDefault();var name=document.getElementById('fName');var address=document.getElementById('fAddress');var age=document.getElementById('fAge');if(!name||!name.value.trim()){if(name)name.focus();return}if(!phoneValid()){showPhoneState(false);if(phone)phone.focus();return}if(!address||!address.value.trim()){if(address)address.focus();return}if(!age||!age.value||Number(age.value)<18||Number(age.value)>100){if(age)age.focus();return}openModal('mThanks');form.reset();if(phone)phone.className='field';if(msg)msg.className='msg';total=600;renderTimer()});

  var burger=document.getElementById('burger');var links=document.getElementById('navLinks');
  if(burger&&links){burger.addEventListener('click',function(){var open=links.classList.toggle('open');burger.setAttribute('aria-expanded',String(open))});links.addEventListener('click',function(e){if(e.target.closest('a')){links.classList.remove('open');burger.setAttribute('aria-expanded','false')}})}
})();
