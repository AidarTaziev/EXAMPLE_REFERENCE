let patternObj = [
  {
    name: 'consignee',
    pattern: /^.+?/,
    valid: false
  },
  {
    name: 'address',
    pattern: /^.+?/,
    valid: false
  },
  {
    name: 'contact_name',
    pattern: /^[а-яА-ЯёЁa-zA-Z]{1,32}$/,
    valid: false
  },
  {
    name: 'contact_phone',
    pattern: /^((8|\+7)[\- ]?)?(\(?\d{3}\)?[\- ]?)?[\d\- ]{7,10}$/,
    valid: false
  },
  {
    name: 'contact_email',
    pattern: /^[-\w.]+@([A-z0-9][-A-z0-9]+\.)+[A-z]{2,4}$/,
    valid: false
  }
];

$(document).ready(() => {
  let date = new Date();
  let day = date.getDate();
  let month = date.getMonth()+1;
  let sec_month;
  let year = date.getFullYear();
  if (month < 10)
    month = '0' + month;
  if (day < 10)
    day = '0' + day;
  $('input[name="shipment_from"]').val(year + '-' + month + '-' + day);
  if (month == 12) {
    sec_month = '01';
    year += 1;
  }
  $('input[name="shipment_to"]').val(year + '-' + sec_month + '-' + day);
});

$('input[type="text"]').on('input' , function (){
  let i = 0;
  $.each(patternObj, (index) => {
    if (patternObj[index].name == $(this).attr('name')) {
      i = index;
    }
  });
  validate(this, i);
});

function validate(elem, index) {
	if (patternObj[index].pattern.test($(elem).val())) {
		$(elem).css('border' , '1px solid #4cd137');
    patternObj[index].valid = true;
	}
	else {
		$(elem).css('border' , '1px solid #c23616');
    patternObj[index].valid = false;
	}

  let j = 0;
  $.each(patternObj, (i) => {
    if (patternObj[i].valid) {j++;}
    if (j == patternObj.length) {
      $('input[type="submit"]').removeAttr('disabled');
      $('input[type="submit"]').removeClass('disabled-btn');
    } else {
      $('input[type="submit"]').attr('disabled', 'disable');
      $('input[type="submit"]').addClass('disabled-btn');
    }
  });
}

$('.request').submit(function(e) {
  var data = $(this).serialize();
  $.ajax({
    url: 'post_polymer_order',
    type: 'POST',
    data: data,
    success: (res) => {
      if (res) toggleAlert('Заявка отправлена', true);
      else toggleAlert('Возникла ошибка попробуйте еще раз', false);
    },
    error: (res) => {
      if (res) toggleAlert('Возникла ошибка попробуйте еще раз', false);
    }
  });

  e.preventDefault();
});

function toggleAlert(res, flag) {
  if (!flag) $('.alert').css('background-color' , '#c23616');
  else $('.alert').removeAttr('style');
  $('.alert').show();
  $('.alert').children('span').text(res);
  setTimeout(() => {
    $('.alert').hide();
  }, 5000);
}
