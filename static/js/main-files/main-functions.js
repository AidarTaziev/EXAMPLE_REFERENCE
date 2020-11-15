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

function deleteElemFromArr(arr, elem) {
  for (let i = 0; i < arr.length; i++) {
    if (arr[i] === elem) {
      arr.splice(i, 1);
    }
  }
  return arr;
}

function showAlert(message, color) {
  closeAlert();
  $('#alert-wrap .alert-frame').children('h2').text(message).css('color', color);
  $('#alert-wrap').addClass('alert-active');
  $('#alert-wrap .alert-frame').addClass('active');
  $('#alert-wrap .hover').show();

  setTimeout(function (){
    closeAlert();
  }, 1250);
}

function showAgreement(message, color) {
  closeAlert();
  $('#agreement-wrap .alert-frame').children('h2').text(message).css('color', color);
  $('#agreement-wrap').addClass('alert-active');
  $('#agreement-wrap .alert-frame').addClass('active');
  $('#agreement-wrap .hover').show();
}

function closeAgreement() {
  $('#agreement-wrap .hover').hide();
  $('#agreement-wrap').removeClass('alert-active');
  $('#agreement-wrap .alert-frame').removeClass('active');
}

function closeAlert() {
  $('#alert-wrap .hover').hide();
  $('#alert-wrap').removeClass('alert-active');
  $('#alert-wrap .alert-frame').removeClass('active');
}

function isChecked(checkbox) {
  if (checkbox.prop('checked')) return true;
  else return false;
}

function checkErrorsKey(res, parent_class, alertSpan, color, key) {
  if (key == '__all__') $(alertSpan).text(res.data[key]).css('color', color);
  let item = $(parent_class + ' input[name="'+key+'"]');
  item.css('border', '2px solid red');
  item.parent().append(`
    <span style="font-size: .8em;" class="Salert"> ` +res.data[key]+  ` </span>
  `);
}

function downloadFile(blob, file_name, content_type) {
  // if (content_type != 'aplication/pdf') {
  //   var newBlob = new Blob([s2ab(btoa(blob))], {type: content_type});
  // } else {
  //   var newBlob = new Blob([blob], {type: content_type});
  // }
  var newBlob = new Blob([blob], {type: content_type});
  if (window.navigator && window.navigator.msSaveOrOpenBlob) {
    window.navigator.msSaveOrOpenBlob(newBlob);
    return;
  }
  const data = window.URL.createObjectURL(newBlob);
  var link = document.createElement('a');
  link.href = data;
  link.download=file_name;
  link.click();
  setTimeout(function(){
    window.URL.revokeObjectURL(data);
    $(link).detach();
  }, 100);
}

function getFormData(form){
  var ser_object = form.serializeArray();
  var res_object = {};

  $.map(ser_object, function(n, i){
      res_object[n['name']] = n['value'];
  });

  return res_object;
}

function setCookie(name, value, props) {

    props = props || {};

    var exp = props.expires;

    if (typeof exp == "number" && exp) {

        var d = new Date();

        d.setTime(d.getTime() + exp*1000);

        exp = props.expires = d;

    }

    if(exp && exp.toUTCString) { props.expires = exp.toUTCString(); }

    value = encodeURIComponent(value);

    var updatedCookie = name + "=" + value;

    for(var propName in props){

        updatedCookie += "; " + propName;

        var propValue = props[propName];

        if(propValue !== true){ updatedCookie += "=" + propValue; }
    }

    document.cookie = updatedCookie;

}

// удаляет cookie
function deleteCookie(name) {

    setCookie(name, null, { expires: -1 })

}

function s2ab(s) {
  var buf = new ArrayBuffer(s.length);
  var view = new Uint8Array(buf);
  for (var i=0; i!=s.length; ++i) view[i] = s.charCodeAt(i) & 0xFF;
  return buf;
}

function drawBalanceRow(row, type, table) {
  console.log(row);
  if (type == "balance") {
    $('#' + table).append(`
      <tr>
        <td class="org-name">`+row.Organization+`</td>
      </tr>
    `);
    for (var i = 0; i < row.Warehouses.length; i++) {
      $('#balance_table').append(`
        <tr>
          <td>`+row.Warehouses[i].Warehouse+`</td>
          <td>`+row.Warehouses[i].Start_balance+` руб.</td>
          <td>`+row.Warehouses[i].Inflow_count+` руб.</td>
          <td>`+row.Warehouses[i].Outflow_count+` руб.</td>
          <td>`+row.Warehouses[i].Final_balance+` руб.</td>
        </tr>
      `);
    };
  } else if (type == 'warehouse') {
    $('#' + table).append(`
      <tr>
        <td class="org-name">`+row.Organization+`</td>
        <td>`+row.Count_on_date+`</td>
        <td>`+row.Total_cost_pt+`</td>
        <td>`+row.Purchase_price+`</td>
        <td>`+row.Additional_costs_pt+`</td>
        <td>`+row.Delivery_cost_pt+`</td>
        <td>`+row.Storage_cost_pt+`</td>
        <td>`+row.PRR_cost_pt+`</td>
        <td>`+row.Credit_cost_pt+`</td>
        <td>`+row.Total_cost+`</td>
      </tr>
    `);
    for (var i = 0; i < row.Warehouses.length; i++) {
      $('#' + table).append(`
        <tr>
          <td>`+row.Warehouses[i].Warehouse+`</td>
          <td>`+row.Warehouses[i].Count_on_date+`</td>
          <td>`+row.Warehouses[i].Total_cost_pt+`</td>
          <td>`+row.Warehouses[i].Purchase_price+`</td>
          <td>`+row.Warehouses[i].Additional_costs_pt+`</td>
          <td>`+row.Warehouses[i].Delivery_cost_pt+`</td>
          <td>`+row.Warehouses[i].Storage_cost_pt+`</td>
          <td>`+row.Warehouses[i].PRR_cost_pt+`</td>
          <td>`+row.Warehouses[i].Credit_cost_pt+`</td>
          <td>`+row.Warehouses[i].Total_cost+`</td>
        </tr>
      `);
    };
  }

}
