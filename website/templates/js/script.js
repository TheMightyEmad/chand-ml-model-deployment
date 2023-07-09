const modelInput = $('#model');
const modelResults = $('#model-results');


  modelInput.on('input keydown keyup', (event) => {
    const query = event.target.value;
    if (query.length >= 2) {
    $.ajax({
        url: `/search?query=${query}`,
        success: (results) => {
            modelResults.empty();
            for (const result of results) {
                const li = $('<li class="list-group-item search_items">').text(result);
                li.on('click', () => {
                    modelInput.val(result);
                    modelResults.empty();
                    let selectedModel;
                    console.log(result)
                    selectedModel=result;
                    $.post('/get_years', { selectedModel: selectedModel }, function(response) {
                        $('#year').empty();
                        for (const year of response) {
                            const persianYear = persianNumber(year);
                            $('#year').append($('<option>', {
                                value: year,
                                text: persianYear
                            }));
                        }
                    });
                });
                modelResults.append(li);
            }
        }
    });
}});

function persianNumber(number) {
    const persianNumbers = ["۰","۱","۲","۳","۴","۵","۶","۷","۸","۹"];
    const englishNumbers = ["0","1","2","3","4","5","6","7","8","9"];
    for (let i = 0; i < englishNumbers.length; i++) {
        number = number.toString().replace(new RegExp(englishNumbers[i], "g"), persianNumbers[i]);
    }
    return number;
}

$('input[name="mileage"]').on('input', function() {
  $(this).val(persianNumber($(this).val()));
});


$('#model').on('change', function() {
    console.log('1')
    $(this).addClass('disabled-field');
  });
  $('#model').on('click', function() {
    if ($(this).hasClass('form-control') && $(this).hasClass('disabled-field')) {
      $(this).removeClass('disabled-field');
      $(this).val('');
    }
  });

$(document).ready(function() {
    $('#predict_button').click(function() {
      var variable1 = $('#model').val();
      var variable2 = $('#year').val();
      var variable3 = $('#mileage').val();
      var variable4 = $('#location').val();
      console.log('feshar1')
      $.ajax({

        url: '/predict',
        type: 'POST',
        data: {
          variable1: variable1,
          variable2: variable2,
          variable3: variable3,
          variable4: variable4,
        },
        success: function(response) {
            var jsonResponse = JSON.parse(response);
            price=jsonResponse.variable
            let price_h = price * 105/100
            let price_l = price * 95/100
            let formattedNumber = price.toLocaleString();
            let formattedNumber_h = price_h.toLocaleString();
            let formattedNumber_l = price_l.toLocaleString();
            var outputValue = persianNumber(formattedNumber);
            var outputValue_l = persianNumber(formattedNumber_l);
            var outputValue_h = persianNumber(formattedNumber_h);
            $('#variable-container').text(outputValue);
            $('#variable-container-l').text(outputValue_l);
            $('#variable-container-h').text(outputValue_h);
            $('#grad').addClass('ans grad');
            $('#low-price').removeClass('invsibile');
            $('#suggested-price').removeClass('invsibile');
            $('#high-price').removeClass('invsibile');
        },
        error: function(error) {
          console.log(error);
        }
      });
    });
  });

$(document).ready(function() {
  $('#predict_button').click(function(event) {
    var form = $('form')[0];
    if (form.checkValidity() === false) {
      event.preventDefault();
      event.stopPropagation();
    }
    form.classList.add('was-validated');
  });
});

$(document).ready(function() {
  $(".faq-box").click(function() {
    $(this).find(".hidden-answer").slideToggle();
  });
});