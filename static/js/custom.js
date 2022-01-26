function email_check(email_element) {

  var value = email_element.val()
  $.ajax({
    url: '/users/ajax/check-email/',
    data: {
      'email': value,
    },
    success: function (data) {
      if (data.exists) {
        email_element.addClass("is-invalid").removeClass("is-valid");
        if (email_element.closest(".form-group").children("label.error").length == 0) {
          $('<label class="error">Email already exists. Please choose a different one.</label>').insertAfter(email_element);
        }
        return false
      } else {
        if (value) {
          email_element.removeClass("is-invalid").addClass("is-valid");
        } else {
          email_element.removeClass("is-invalid").removeClass("is-valid");
        }
        email_element.parent().children(".error").remove()
        return true
      }
    },
    error: function (xhr, textStatus, error) {
      console.log(xhr.statusText);
      console.log(textStatus);
      console.log(error);
    }
  });
};
function password_valid() {
  var password1 = $("#password1").val()
  var password2 = $("#password2").val()
  var valid = true

  $.ajax({
    url: '/users/ajax/check-password/',
    data: {
      'password1': password1,
      'password2': password2,
    },
    success: function (data) {

      document.querySelector('.step-experience').disabled = true
      if (password1.length === 0) {
        $("#password1").removeClass("is-invalid").removeClass("is-valid");
      }

      if (password2.length === 0) {
        $("#password2").removeClass("is-invalid").removeClass("is-valid");
      }

      if (data.valid) {
        if (password1 && password2) {
          $("#password1").removeClass("is-invalid").addClass("is-valid");
          $("#password2").removeClass("is-invalid").addClass("is-valid");
          $("#password1").parent().children(".error").remove()
          $("#password2").parent().children(".error").remove()
          document.querySelector('.step-experience').disabled = false
        } else {
          $("#password1").removeClass("is-invalid").removeClass("is-valid");
          $("#password1").parent().children(".error").remove()
        }
      } else {
        if (data.type == 'match' && (password1 && password2)) {
          $("#password1").addClass("is-invalid").removeClass("is-valid");
          $("#password2").addClass("is-invalid").removeClass("is-valid");
          if ($("#password2").closest(".form-group").children("label.error").length == 0) {
            $(`<label class="error">${data.message}</label>`).insertAfter($("#password2"));
          }
        } else {
          $("#password1").addClass("is-invalid").removeClass("is-valid");
          if ($("#password1").closest(".form-group").children("label.error").length == 0) {
            $(`<label class="error">${data.message}</label>`).insertAfter($("#password1"));
          }
        }
        valid = false
      }
    },
    error: function (xhr, textStatus, error) {
      console.log(xhr.statusText);
      console.log(textStatus);
      console.log(error);
    }
  });

  return valid
};

function number_only(element, e) {
  //if the letter is not digit then display error and don't type anything
  if (e.which != 8 && e.which != 0 && (e.which < 48 || e.which > 57)) {
    //display error message
    element.addClass("is-invalid");
    if (element.closest(".form-group").children("label.error").length == 0) {
      if (element.closest(".form-group").children("div.input-group").length) {
        var afterThis = element.closest(".form-group").children("div.input-group")
      } else {
        var afterThis = element.closest(".form-group").children("input")
      }
      $('<label class="error">Numeric Only.</label>').insertAfter(afterThis);
    }
    return false;
  } else {
    element.removeClass("is-invalid");
    element.closest(".form-group").children("label.error").remove();
  }
}

$(document).on('click', '.step-personal', function (e) {
  e.preventDefault()
  if ($(this).hasClass("next")) {
    var valid = $("#registrationForm").valid()
    if (valid == true) {
      $('.nav-item a[href="#tab-personal"]').tab('show')
    }
  } else {
    $('.nav-item a[href="#tab-personal"]').tab('show')
  }
})

$(document).on('click', '.step-login', function (e) {
  e.preventDefault();
  if ($(this).hasClass("next")) {
    var valid = $("#registrationForm").valid()
    if (valid == true) {
      $('.nav-item a[href="#tab-login"]').tab('show')
    }
  } else {
    $('.nav-item a[href="#tab-login"]').tab('show')
  }
})

$(document).on('click', '.step-experience', function (e) {
  e.preventDefault();
  if ($(this).hasClass("next")) {
    var valid = $("#registrationForm").valid()
    if (valid) {
        $('.nav-item a[href="#tab-experience"]').tab('show')
    }
  } else {
    $('.nav-item a[href="#tab-experience"]').tab('show')
  }
})

$(document).on('click', '.step-company-details', function (e) {
  e.preventDefault()
  if ($(this).hasClass("next")) {
    var valid = $("#registrationForm").valid()
    if (valid == true) {
      if (password_valid()) {
        $('.nav-item a[href="#tab-company-details"]').tab('show')
      }
    }
  } else {
    $('.nav-item a[href="#tab-company-details"]').tab('show')
  }
})

$(document).on('submit', "#registrationForm", function (e) {
  if ($('.required:visible').length) {
    var valid = $('.required:visible').valid()
    if (valid) {
      if ($(".submit").is(":visible")) {
        $("#overlay").css('display', 'flex');
      } else {
        e.preventDefault();
        $(".next:visible").trigger("click");
      }
    } else {
      e.preventDefault();
    }
  } else {
    if ($(".submit").is(":visible")) {
      $("#overlay").css('display', 'flex');
    } else {
      e.preventDefault();
      $(".next:visible").trigger("click");
    }
  }
});

$(document).on('keypress', ".number_only", function (e) {
  //if the letter is not digit then display error and don't type anything
  return number_only($(this), e)
});

$(document).on('focusout', ".number_only", function (e) {
  //if the letter is not digit then display error and don't type anything
  return number_only($(this), e)
});

$(document).on('focusout', '#password2', function (e) {
  password_valid()
});

$(document).on('change', ".address-select", function (e) {
  var _id = $(this).val()
  var url = $(this).attr("data-ajax-url")
  var value = $(this).attr("data-value")
  var target_name = $(this).attr("data-target").replace('user_', '')
  var current_name = $(this).attr('name')
  var heirarchy = {
    "region": [
      $(this).closest('.form-group').parent().find("#user_province"),
      $(this).closest('.form-group').parent().find("#user_municipality"),
      $(this).closest('.form-group').parent().find("#user_barangay")
    ],
    "province": [
      $(this).closest('.form-group').parent().find("#user_municipality"),
      $(this).closest('.form-group').parent().find("#user_barangay")
    ],
    "municipality": [
      $(this).closest('.form-group').parent().find("#user_barangay")
    ],
    "barangay": [],
  }

  $.ajax({
    url: url,
    data: {
      '_id': _id,
      'value': value,
      'target_name': target_name,
      'current_name': current_name
    },
    success: function (data) {
      heirarchy = heirarchy[current_name]
      var target = heirarchy.shift();
      target.html(data);
      $.each(heirarchy, function (index, element) {
        element.html('<option value="">Select...</option>');
      });
    },
    error: function (xhr, textStatus, error) {
      console.log(xhr.statusText);
      console.log(textStatus);
      console.log(error);
    }
  });
});

$(document).on('keyup', '.phone_number', function (e) {
  var value = $(this).val()
  if (value.length == 3) {
    $(this).val(value + '-')
  }
})

$(document).on('focusout', '#password1', function (e) {
  password_valid();
});

$(document).on('click', '.see-password', function (e) {
  var input = $(this).parent().find('input')
  event.preventDefault();
  if (input.attr("type") == "text") {
    input.attr('type', 'password');
    $(this).find('i').addClass("fa-eye-slash");
    $(this).find('i').removeClass("fa-eye");
  } else if (input.attr("type") == "password") {
    input.attr('type', 'text');
    $(this).find('i').removeClass("fa-eye-slash");
    $(this).find('i').addClass("fa-eye");
  }
});

$(".alert").delay(20000).slideUp(200, function() {
    $(this).alert('close');
});

$(document).on('keyup', '.two-digit', function() {
    limitText(this, 2)
});

$(document).on('keyup', '.three-digit', function() {
    limitText(this, 3)
});

function limitText(field, maxChar){
    var ref = $(field),
        val = ref.val();
    if ( val.length >= maxChar ){
        ref.val(function() {
            console.log(val.substr(0, maxChar))
            return val.substr(0, maxChar);
        });
    }
}
