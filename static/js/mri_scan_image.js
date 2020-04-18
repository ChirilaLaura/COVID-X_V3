//.text-success {
//  color: #28a745 !important; }

//.text-danger {
//color: #dc3545 !important; }
$(document).ready(function () {
  var onCompletion = (res) => {
    consolog.log('Gata1')
    res = JSON.parse(res);
    prediction = res.prediction;
    console.log("Predictie" + prediction + "tip_date=" + (typeof prediction) + "rezultat" + (prediction==1))
    res1 = res.image
    $("#image-box").attr("src", "data:image/jpeg;charset=utf-8;base64," + res1);
    if(prediction == 1) {
      let rezultat_text = '<p>In urma scanarii plamaniilor, rezulta ca pacientul este infectat</p>';
      $('#result').removeClass('text-success').addClass('text-danger').html(rezultat_text);
    } else {
      let rezultat_text = '</p> In urma scanarii plamaniilor, rezulta ca pacientul este sanatos</p>';
      $('#result').removeClass('text-danger').addClass('text-success').html(rezultat_text);
    }
    $('#result-heading').show();
    $('#result-row').show();
  }
  $('#result-heading').hide();
  $('#result-row').hide();
  $('#progress-bar').hide();
});
