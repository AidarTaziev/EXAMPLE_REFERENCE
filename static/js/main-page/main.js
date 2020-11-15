let custom_selects = [];
$(document).ready(() => {
    let scroll_top = getCookie('reference_scroll_position');
    setTimeout(() => {
        $('.preload-wrap').hide();
        $('header').show().css('display', 'flex');
        if (scroll_top) {
            $('.content-wrap').scrollTop(scroll_top);
            setCookie('reference_scroll_position', 0);
        }
    }, 1000);
    const customs = $('.select-activator');
    for (let i = 0; i < customs.length; i++) {
      custom_selects.push({
        input: customs[i],
        name: $(customs[i]).attr('name'),
        selected_options: 0,
        options: []
      });
    }
    var inputNames = ['shortcode', 'ptr_left', 'ptr_right', 'density_left', 'density_right', 't_vika_left', 't_vika_right'];
    var selectNames = ['application_category', 'application', 'type', 'subtype', 'copolymer', 'color', 'plant', 'obtaining_method', 'procm'];
    var url_string = window.location.href;
    var url = new URL(url_string);
    for (var i = 0; i < inputNames.length; i++) {
      var param = url.searchParams.get(inputNames[i]);
      if (param) $('#' + inputNames[i]).val(param);
    }
    for (var i = 0; i < selectNames.length; i++) {
      var param = url.searchParams.get(selectNames[i]);$('#' + selectNames[i]);        
      if (param) {
        param = param.split(',');
        custom_selects.map(function (item) {
          if (item.name === selectNames[i]) {
            const spans = $('input[name="'+ item.name +'"]').siblings('.hidden-list').children();
            for (let j = 0; j < spans.length; j++) {
              param.map(function (par) {
                if (par === $(spans[j]).attr('data-value')) {
                  $(spans[j]).addClass('active-list-item');
                  item.options.push(par);
                  item.selected_options += 1;
                }
                return true;
              });
            }
          }
          return true;
        });
      }
    }
    for (let i = 0; i < customs.length; i++) {
      const span = $(customs[i]).parent().siblings('.label-title').children('.options-count');
      console.log(custom_selects[i].selected_options);
      if ($(span)[0] !== undefined)
        $(span)[0].innerHTML = custom_selects[i].selected_options;
      custom_selects.map(function (item) {
        if (item.name === 'type') {
          if (item.options.length > 0) {
            $('input[name="subtype"]').siblings('.hidden-list')
              .children().attr('style', 'display: none;');
            item.options.map(function (elem) {
              $('input[name="subtype"]').siblings('.hidden-list')
                .children('span[data-parent="'+elem+'"]').attr('style', 'display: unset;');
            });      
          } else {
            $('input[name="subtype"]').siblings('.hidden-list')
              .children().attr('style', 'display: unset;');      
          }
        }
      });
    }
});

$('.profile-image').click(function () {
    let names = ['sber', 'man', 'menu'];
    let name = $(this).attr('data-id');
    for (let i in names) {
      if (name != names[i]) {
        $('div[data-id="'+names[i]+'"]').siblings('.profile-list').slideUp('slow');
        $('div[data-id="'+names[i]+'"]').parent().addClass('hide-list');
        $('img[data-id="'+names[i]+'"]').siblings('.profile-list').slideUp('slow');
        $('img[data-id="'+names[i]+'"]').parent().addClass('hide-list');
      }
    }
    $(this).siblings('.profile-list').slideToggle('slow').css('display', 'flex');
    $(this).siblings('.mobile-menu-close').toggleClass('active-closer');
});

$('.mobile-menu-close').click(function () {
    $('.profile-list').slideUp('slow');
    $(this).removeClass('active-closer');
    setTimeout(function () {
        $('div[data-id="man"]').parent().removeClass('hide-list');
        $('img[data-id="menu"]').parent().removeClass('hide-list');
        $('div[data-id="sber"]').parent().removeClass('hide-list');
    }, 500);
});

$('.profile-item').click(function () {
    let link = $(this).children('a').attr('href');
    if (link != undefined)
      location.href = link;
});

$('#agreement_close').click(() => {
  closeAgreement();
});

$('.select-activator').on('input', function (){
  const hList = $(this).siblings('.hidden-list');
  if ($(this).val() === '') {
    hList.slideUp();
    $(hList).siblings('.multi-list-open').removeClass('multi-list-close');
  } else {
    $(hList).siblings('.multi-list-open').addClass('multi-list-close');
    hList.slideDown().css('display', 'flex');
  }  
  const list = $(this).siblings('.hidden-list').children();
  const val = $(this).val().toLowerCase();
  for (let i = 0; i < list.length; i++) {
    if (!list[i].innerHTML.toLowerCase().includes(val)) {
      $(list[i]).attr('style', 'display: none;');
    } else {
      $(list[i]).attr('style', 'display: unset;');
    }
  }
});

$('.filter').submit(function (e) {
  e.preventDefault();
  let data = $(this).serialize().split("&");
  let obj = new Object();
  for(var key in data)
  {
      obj[data[key].split("=")[0]] = data[key].split("=")[1];
  }
  const list = $('.select-activator').siblings('.hidden-list').children();
  custom_selects.map(function (item) {
    obj[item.name] = item.options;
  });
  get_form_data = object => Object.keys(object).reduce((formData, key) => {
    console.log(object[key], key);
    if (object[key] !== '' && object[key] !== ' ' && object[key].length !== 0) {
      if (formData !== '')
        formData += '&' + key + '=' + object[key];
      else
        formData += '' + key + '=' + object[key];
    }
    return formData;
  }, '');
  window.location.href = window.location.origin + '/search?' + get_form_data(obj);
});

$('.multi-list-open').click(function () {
  $(this).toggleClass('multi-list-close');
  const list = $(this).siblings('.hidden-list');
  if (list.css('display') === 'flex') {
    list.slideUp();
  } else {
    const input = $(this).siblings('input');
    input.focus();
    list.slideDown().css('display', 'flex');
  }
});

$('.mutli-list-item').click(function () {
  const input = $(this).parent().siblings('input');
  let index = 0;
  $(this).toggleClass('active-list-item');
  for (let i = 0; i < custom_selects.length; i++) {
    if (input[0] === custom_selects[i].input) {
      index = i;
      if (!custom_selects[i].options.includes($(this).attr('data-value'))) {
        custom_selects[i].options.push($(this).attr('data-value'));
        custom_selects[i].selected_options += 1;
      } else {
        custom_selects[i].options = deleteElemFromArr(custom_selects[i].options, $(this).attr('data-value'));
        custom_selects[i].selected_options -= 1;
      }
      $(input).parent().siblings('.label-title').children('.options-count')[0].innerHTML = custom_selects[i].selected_options;
    }
  }
  if ($(input).attr('name') === 'type') {
    if (custom_selects[index].options.length > 0) {
      $('input[name="subtype"]').siblings('.hidden-list')
        .children().attr('style', 'display: none;');
      custom_selects[index].options.map(function (item) {
        $('input[name="subtype"]').siblings('.hidden-list')
          .children('span[data-parent="'+item+'"]').attr('style', 'display: unset;');
      });      
    } else {
      $('input[name="subtype"]').siblings('.hidden-list')
        .children().attr('style', 'display: unset;');      
    }
  }
});

$('.content-wrap').scroll(function (event) {
    setCookie('reference_scroll_position', $(this).scrollTop(), {
        expires: 10
    });
});

$('#open_sber').click((e) => {
  e.preventDefault();
  $('.modal-wrap').addClass('active-wrap');
	$('.mobile-menu-close').click();
});

$('#sberbank').submit(function(e) {
  e.preventDefault();
  let data = getFormData($(this));
  data.csrfmiddlewaretoken = getCookie('csrftoken');
  data.order_url = location.href;
  getSberBankLink(data);
});

$('.before').on('input', function () {
  const after = $(this).siblings('.after');
  if ($(after).val() !== undefined && $(after).val() !== '') {
    if (parseInt($(this).val()) > parseInt($(after).val())) {
      $(this).addClass('input-error');
    } else {
      $(this).removeClass('input-error');
      $(after).removeClass('input-error');
    }
  }
});

$('.after').on('input', function () {
  const before = $(this).siblings('.before');
  if ($(before).val() !== undefined && $(before).val() !== '') {
    if (parseInt($(this).val()) < parseInt($(before).val())) {
      $(this).addClass('input-error');
    } else {
      $(this).removeClass('input-error');
      $(before).removeClass('input-error');
    }
  }
});

$('.close-modal').click(() => {
  $('.modal-wrap').removeClass('active-wrap');
});

$('.modal-wrap .hover').click(() => {
  $('.modal-wrap').removeClass('active-wrap');
});

$('.sberbank-button').click(function (){
	if ($(this).attr('href') != undefined && $(this).attr('href') != null)
		location.href = $(this).attr('href');
});