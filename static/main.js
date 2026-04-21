// Card number auto-formatter (cosmetic only — real validation is in Python/Flask)
const cardNum = document.getElementById('card-number');
if (cardNum) {
  cardNum.addEventListener('input', function () {
    let v = this.value.replace(/\D/g, '').slice(0, 16);
    this.value = v.replace(/(.{4})/g, '$1 ').trim();
  });
}

// Expiry formatter
const cardExp = document.getElementById('card-expiry');
if (cardExp) {
  cardExp.addEventListener('input', function () {
    let v = this.value.replace(/\D/g, '').slice(0, 4);
    if (v.length > 2) v = v.slice(0, 2) + ' / ' + v.slice(2);
    this.value = v;
  });
}

// CVV — digits only
const cardCvv = document.getElementById('card-cvv');
if (cardCvv) {
  cardCvv.addEventListener('input', function () {
    this.value = this.value.replace(/\D/g, '').slice(0, 3);
  });
}

// Auto-dismiss flash messages after 3 seconds
setTimeout(() => {
  document.querySelectorAll('.flash').forEach(el => {
    el.style.transition = 'opacity 0.5s';
    el.style.opacity = '0';
    setTimeout(() => el.remove(), 500);
  });
}, 3000);
