function clearText(textboxId) {
    document.getElementById(textboxId).value = "";
}

function copyText(textboxId) {
    var textbox = document.getElementById(textboxId);
    var text = textbox.value;
  
    navigator.clipboard.writeText(text)
      .then(function() {
        console.log("Text copied to clipboard");
      })
      .catch(function(error) {
        console.error("Error copying text to clipboard:", error);
      });
  }


  function disableCorrespondingRadio(element) {
    element.checked = true;
    var radioInput = document.getElementsByName("btnRadio_input");
    var radioOutput = document.getElementsByName("btnRadio_output");
  
    for (var i = 0; i < radioInput.length; i++) {
      if (radioInput[i].checked) {
        var lang = radioInput[i].value;
  
        for (var j = 0; j < radioOutput.length; j++) {
          if (radioOutput[j].value === lang) {
            if (radioOutput[j].checked === true){
              radioOutput[j].checked = false;
              if (j === 0) {
                radioOutput[j+2].checked = true;
              } else {
                radioOutput[j-1].checked = true;
              }
            }
          }
        }
        break;
      }
    }
    element.checked = true;
    for (var k = 0; k < radioOutput.length; k++) {
      if (radioOutput[k].checked) {
        var lang = radioOutput[k].value;
  
        for (var l = 0; l < radioInput.length; l++) {
          if (radioInput[l].value === lang) {
            if (radioInput[l].checked === true) {
              radioInput[l].checked = false;
              if (l === 0) {
                radioInput[l+2].checked = true;
              } else {
                radioInput[l-1].checked = true;
              }
            }
          }
        }
        break;
      }
    }
  }


  function getCheckedRadioButtonsId() {
    var radioInput = document.getElementsByName("btnRadio_input");
    var radioOutput = document.getElementsByName("btnRadio_output");
  
    for (var i = 0; i < radioInput.length; i++) {
      if (radioInput[i].checked) {
        var btnInput = radioInput[i];
      }
    }
    
    for (var i = 0; i < radioOutput.length; i++) {
      if (radioOutput[i].checked) {
        var btnOutput = radioOutput[i];
      }
    }
  
    return {
      btnInput: btnInput,
      btnOutput: btnOutput
    };
  }

var sourceLangElement = document.getElementById('source_lang');
var targetLangElement = document.getElementById('target_lang');
var textArea1 = document.getElementById('source_text');
var textArea2 = document.getElementById('translation');

window.onload = function() {
  var radioInput = document.getElementsByName("btnRadio_input");
  var radioOutput = document.getElementsByName("btnRadio_output");

  if (sourceLangElement.value === "en") {
    applyLanguageSettings (textArea1, "en", "input")
    for (var i = 0; i < radioInput.length; i++) {
      if (radioInput[i].id === "btnInput-en") {radioInput[i].checked = true;} else {radioInput[i].checked = false};        
    }
  };
  if (sourceLangElement.value === "ar") {
    applyLanguageSettings (textArea1, "ar", "input")
    for (var i = 0; i < radioInput.length; i++) {
      if (radioInput[i].id === "btnInput-ar") {radioInput[i].checked = true;} else {radioInput[i].checked = false};        
    }
  };
  if (sourceLangElement.value === "fa") {
    applyLanguageSettings (textArea1, "fa", "input")
    for (var i = 0; i < radioInput.length; i++) {
      if (radioInput[i].id === "btnInput-fa") {radioInput[i].checked = true;} else {radioInput[i].checked = false};        
    }
  };
  if (targetLangElement.value === "en") {
    applyLanguageSettings (textArea2, "en", "output")
    for (var i = 0; i < radioOutput.length; i++) {
      if (radioOutput[i].id === "btnOutput-en") {radioOutput[i].checked = true;} else {radioOutput[i].checked = false};        
    }
  };
  if (targetLangElement.value === "ar") {
    applyLanguageSettings (textArea2, "ar", "output")
    for (var i = 0; i < radioOutput.length; i++) {
      if (radioOutput[i].id === "btnOutput-ar") {radioOutput[i].checked = true;} else {radioOutput[i].checked = false};        
    }
  };
  if (targetLangElement.value === "fa") {
    applyLanguageSettings (textArea2, "fa", "output")
    for (var i = 0; i < radioOutput.length; i++) {
      if (radioOutput[i].id === "btnOutput-fa") {radioOutput[i].checked = true;} else {radioOutput[i].checked = false};        
    }
  };
}



var radioButtons = document.querySelectorAll('input[name="btnRadio_output"], input[name="btnRadio_input"]');

radioButtons.forEach(function(radioButton) {
  radioButton.addEventListener('change', function() {
    var res = getCheckedRadioButtonsId()
    var { btnInput: btnInput, btnOutput: btnOutput } = res;
    sourceLangElement.value = btnInput.value
    targetLangElement.value = btnOutput.value
    if (btnInput.id === "btnInput-en") {
      applyLanguageSettings (textArea1, "en", "input")
    } else if (btnInput.id === "btnInput-ar") {
      applyLanguageSettings (textArea1, "ar", "input")
    } else if (btnInput.id === "btnInput-fa") {
      applyLanguageSettings (textArea1, "fa", "input")
    };
    if (btnOutput.id === "btnOutput-en") {
      applyLanguageSettings (textArea2, "en", "output")
    } else if (btnOutput.id === "btnOutput-ar") {
      applyLanguageSettings (textArea2, "ar", "output")
    } else if (btnOutput.id === "btnOutput-fa") {
      applyLanguageSettings (textArea2, "fa", "output")
    };
  });
});


function applyLanguageSettings (textArea, lang, mode) {
  if (lang === "fa") {
    if ( mode === "input") {textArea.placeholder = "متن فارسی را وارد کنید"}
    textArea.style.fontFamily = "IranSans";
    textArea.style.fontSize = '16px';
    textArea.style.fontWeight = 'bold';
    textArea.style.textAlign = 'right';
    textArea.rows = 25 ;
    textArea.dir = 'rtl';
  };
  if (lang === "ar") {
    if ( mode === "input") {textArea.placeholder = "متن عربی را وارد کنید"}
    textArea.style.fontFamily = "IranSans";
    textArea.style.fontSize = '16px';
    textArea.style.fontWeight = 'bold';
    textArea.style.textAlign = 'right';
    textArea.rows = 25 ;
    textArea.dir = 'rtl';
  };
  if (lang === "en") {
    if ( mode === "input") {textArea.placeholder = "Enter text"}
    textArea.style.fontFamily = "RobotoSlab";
    textArea.style.fontSize = '20px';
    textArea.style.fontWeight = 'normal';
    textArea.style.textAlign = 'left';
    textArea.dir = 'ltr';
    textArea.rows = 20 ;
  };
}
