$(document).ready(() => {
    // if (getCookie('cookie') != 'visited') {
    //   $('.cookies-wrap').fadeIn('slow');
    //  }
    if ((new URL(document.location)).searchParams.get('lang') !== 'ru') {
        $('.ruLang').show();
    }
});

$('.cookies-closer').click(function () {
    $('.cookies-wrap').fadeOut('slow');
    document.cookie = 'cookie=visited; path=/; Domain=.kartli.ch';
});

// Показание и скытие дополнительных элементов меню
$('.nav-bar').on('mouseenter', '.nav-li', function () {
    let elem = $(this).children('.slide-bar');
    elem.addClass('active-bar');
    $(this).children('a').addClass('active-link');
    $(this).mouseleave(() => {
        elem.removeClass('active-bar');
        $(this).children('a').removeClass('active-link');
    });
});

$('.clear').click(function () {
    location.href = location.origin + '/';
});

// $('body').click(function(e){
//   let className = e.target.classList[0];
//   if (className != 'profile-hidden-image' && className != 'profile-item' && className != 'profile-wrap' && $('.profile-list').attr('style') == 'display: block;') {
//     $('.profile-list').slideUp('slow');
//     $('#profile-image').toggleClass('profile-hidden-image');
//     $('#black-profile-image').toggleClass('profile-hidden-image');
//   }
// });

$('#profile-image').click(function () {
    $('.profile-list').slideToggle('slow');
    $('#profile-image').toggleClass('profile-hidden-image');
    $('#black-profile-image').toggleClass('profile-hidden-image');
});

$('.profile-item').click(function () {
    let link = $(this).children('a').attr('href');
    if (link != undefined)
      location.href = link;
});

// $('body').click(function (e) {
//     let className = e.target.classList[0];
//     if (className != 'profile-hidden-image' && className != 'profile-item' && className != 'profile-wrap' && $('.profile-list').attr('style') == 'display: block;') {
//         $('.profile-list').slideUp('slow');
//         $('#profile-image').toggleClass('profile-hidden-image');
//         $('#black-profile-image').toggleClass('profile-hidden-image');
//     }
// });


$('.nav-bar').on('click', '.menu-btn', function () {
    $(this).children('span').eq(0).toggleClass('rotated-first');
    $(this).children('span').eq(1).toggleClass('rotated-sec');
    $('#navigation').toggleClass('nav-opened');
    if ($('body').css('overflow') == 'hidden') {
        $('body').css('overflow', 'scroll');
    } else {
        $('body').css('overflow', 'hidden');
    }
});

// Кнопка Показать/скрыть аналоги
var hideAnalog = 'СКРЫТЬ АНАЛОГИ';
var target;

$('.analog-btn').click(function (e) {
    if ($(this).text() == 'ПОКАЗАТЬ АНАЛОГИ') {
        let id_pol = {
            polymerId: $(this).parent().parent().attr('id')
        };
        $.ajax({
            url: '/get_analogs_for_polymerId',
            type: 'GET',
            data: id_pol,
            success: (res) => {
                if (res.length == undefined) {
                    console.log('res length undefinedd');
                    $(this).parent().children('.analog-block').empty().append(`
              <h2>Аналогов нет</h2>
            `);
                }
                else {
                    if (res[0].viscosity_Mooney || res[0].diene_content || res[0].ethylene_content) {
                        $(this).parent().children('.analog-block').children('table').append(`
                            <tr>
                             <td>Марка</td>
                             <td>Подтип</td> 
                             <td>Производитель</td> 
                             <td>Вязкость по Муни</td> 
                             <td>Массовая доля этилена</td>
                             <td>Массовая доля этилиденнорборнена</td>
                            </tr>  `);
                        for (var i = 0; i < res.length; i++) {
                            $(this).parent().children('.analog-block').children('table').append(`
                                <tr data-href="/polymer/` + res[i].id + `">
                                 <td><a href="/polymer/` + res[i].id + `">` + res[i].shortcode + `</a></td>
                                 <td>` + res[i].subtype__name + `</td>
                                 <td>` + res[i].plants__name + `</td>
                                 <td>` + res[i].viscosity_Mooney + `</td>
                                 <td>` + res[i].ethylene_content + `</td>
                                 <td>` + res[i].diene_content + `</td>
                                </tr>`);
                        }
                    } else {
                        $(this).parent().children('.analog-block').children('table').append(`
                            <tr>
                             <td>Марка</td>
                             <td>Подтип</td> 
                             <td>Производитель</td> 
                             <td>ПТР</td> 
                             <td>Плотность</td>
                            </tr> `);

                        for (var i = 0; i < res.length; i++) {
                            $(this).parent().children('.analog-block').children('table').append(`
                                <tr data-href="/polymer/` + res[i].id + `">
                                 <td><a href="/polymer/` + res[i].id + `">` + res[i].shortcode + `</a></td>
                                 <td>` + res[i].subtype__name + `</td>
                                 <td>` + res[i].plants__name + `</td>
                                 <td>` + res[i].ptr + `</td>
                                 <td>` + res[i].density + `</td>
                                </tr>`);
                        }

                    }

                    if (res[0].viscosity_Mooney) console.log(res[0]);
                }
            },
            error: () => {
                $(this).parent().children('.analog-block').empty().append(`
          <h2>Аналогов нет</h2>
        `);
            }
        });
        $(this).text(hideAnalog);
    } else if ($(this).text() == 'СКРЫТЬ АНАЛОГИ') {
        $(this).parent().children('.analog-block').children('table').children('tr').detach();
        $(this).text('ПОКАЗАТЬ АНАЛОГИ');
    }

    $(this).parent().children('.analog-block').toggleClass('active-analog');
    target = e.target;
});


// TODO: ДОДЕЛАТЬ - классы норм расставить вызов норм. сделать
$('table').click(function (e) {


        // ссылку вытаскиваю из тега data-href ел. tr
        rowLink = e.target.parentElement.getAttribute('data-href');

        // проверка для того чтобы thead не попался
        if (rowLink !== null && rowLink !== undefined) document.location.href = rowLink;
        // e.preventDefault();
        e.stopPropagation();
    }
);
$('.block-row').click(function (e) {
    if (target == e.target) return false;
    else {
        location.href = $(this).children().eq(0).children('h3').children('a').attr('href');
    }
});


var filtersNames = ['shortcode', 'ptr', 'density', 't_vika', 'application_category', 'application', 'type', 'subtype',
    'copolymer', 'color', 'plant', 'obtaining_method', 'processing_method'];

$('body').on('submit', '.filter', function () {
    for (i = 0; i < filtersNames.length; i++) {
        if (($('#' + filtersNames[i]).val() === 'Любой') || (($('#' + filtersNames[i]).val() === ''))
            || ($('#' + filtersNames[i]).val() === 'disabled')) $('#' + filtersNames[i]).prop('disabled', true);
    }
    $('#button').prop('disabled', true);
});

$('select').change(function () {
    if ($(this).val() != 'Любой') {
        $(this).css('background-color', '#fff');
        $(this).css('color', '#000');
    } else {
        $(this).removeAttr('style');
    }
});

function setCookie(name, value, props) {

    props = props || {};

    var exp = props.expires;

    if (typeof exp == "number" && exp) {

        var d = new Date();

        d.setTime(d.getTime() + exp * 1000);

        exp = props.expires = d;

    }

    if (exp && exp.toUTCString) {
        props.expires = exp.toUTCString();
    }

    value = encodeURIComponent(value);

    var updatedCookie = name + "=" + value;

    for (var propName in props) {

        updatedCookie += "; " + propName;

        var propValue = props[propName];

        if (propValue !== true) {
            updatedCookie += "=" + propValue;
        }
    }

    document.cookie = updatedCookie;

}

// удаляет cookie
function deleteCookie(name) {

    setCookie(name, null, {expires: -1})

}

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);

            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
