function userAction(data, flag) { // Вход и регистрация
  let url_ajax;
  let alertSpan;
  flag ? url_ajax = '/auth/login' : url_ajax = '/auth/signup';
  flag ? alertSpan = '.alert-span-log' : alertSpan = '.alert-span-sign';
  $.ajax({
    url: url_ajax,
    type: 'POST',
    data: data,
    success: (res) => {
      if (res.error) {
        let parent_class = '.sign-in';
        let num = 550;
        step = 50;
        if ($('.sign-in').attr('style') == 'display:none;') parent_class = '.sign-up';
        if (parent_class == '.sign-in') {
          num = 300;
          step = 25;
        }
        $(parent_class + ' .Salert').detach();
        $(parent_class + ' input').removeAttr('style');
        $('.sign-wrap').css('height', num + 'px');
        for (var key in res.data) {
          checkErrorsKey(res, parent_class, alertSpan, '#fff', key);
          num += step;
          $('.sign-wrap').css('height' , num + 'px');
        }
      } else {
        $(alertSpan).text('Успешно').css('color', '#fff');
        setTimeout(function (){

          link_exist = $('input[name=next]').val();

          link = link_exist ? link_exist : '/';

          location.href = link;
        }, 500);
      }
    },
    error: (res) => {
      $(alertSpan).text('Нет соединения с сервером').css('color', '#fff');
    }
  });
}

function getSberBankLink(data) {
  $.ajax({
    url: '/bank_account/credit_request',
    type: 'POST',
    data: data,
    success: (res) => {
      if (!res.error) {
        if (res.data.redirect_url != undefined)
          location.href = res.data.redirect_url;
        else
          showAgreement('Сбербанк временно недоступен', '#c23616');
      } else {
        showAgreement(res.data, '#c23616');
      }
    },
    error: () => {
      showAgreement('Сервер временно недоступен', '#c23616');
    }
  });
}
