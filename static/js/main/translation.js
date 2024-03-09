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


  function disableCorrespondingRadio(mode, element) {
    var sourceTextElement = document.getElementById("source_text");
    var previousSourceLangElement = document.getElementById("current_state");
    console.log("previousSourceLangElement: " + previousSourceLangElement.value)
    if (previousSourceLangElement.value === 'en') {
      sourceText_English = sourceTextElement.value;
    } else if (previousSourceLangElement.value === 'ar') {
      sourceText_Arabic = sourceTextElement.value;
    } else if (previousSourceLangElement.value=== 'fa') {
      sourceText_Persian = sourceTextElement.value;
    }
    element.checked = true;
    // var radioInput = document.getElementsByName("btnRadio_input");
    // var radioOutput = document.getElementsByName("btnRadio_output");
  
    // for (var i = 0; i < radioInput.length; i++) {
    //   if (radioInput[i].checked) {
    //     var lang = radioInput[i].value;
  
    //     for (var j = 0; j < radioOutput.length; j++) {
    //       if (radioOutput[j].value === lang) {
    //         if (radioOutput[j].checked === true){
    //           radioOutput[j].checked = false;
    //           if (j === 0) {
    //             radioOutput[j+2].checked = true;
    //           } else {
    //             radioOutput[j-1].checked = true;
    //           }
    //         }
    //       }
    //     }
    //     break;
    //   }
    // }
    // element.checked = true;
    // for (var k = 0; k < radioOutput.length; k++) {
    //   if (radioOutput[k].checked) {
    //     var lang = radioOutput[k].value;
  
    //     for (var l = 0; l < radioInput.length; l++) {
    //       if (radioInput[l].value === lang) {
    //         if (radioInput[l].checked === true) {
    //           radioInput[l].checked = false;
    //           if (l === 0) {
    //             radioInput[l+2].checked = true;
    //           } else {
    //             radioInput[l-1].checked = true;
    //           }
    //         }
    //       }
    //     }
    //     break;
    //   }
    // }
    var checkedInputElement = document.querySelector('input[name="btnRadio_input"]:checked');
    previousSourceLangElement.value = checkedInputElement.value;
  }

  
  function changeText(element) {
    const checkedInputValue = document.querySelector('input[name="btnRadio_input"]:checked').value;
    const checkedOutputValue = document.querySelector('input[name="btnRadio_output"]:checked').value;
    var sourceTextElement = document.getElementById("source_text");
    var targetTextElement = document.getElementById("translation");

    // if (element.id === "btnInput-en") {
    //   sourceTextElement.value = sourceText_English;
    // } else if (element.id === "btnInput-ar") {
    //   sourceTextElement.value = sourceText_Arabic;
    // } else if (element.id === "btnInput-fa") {
    //   sourceTextElement.value = sourceText_Persian;
    // }
    if (checkedInputValue === "en") {
      sourceTextElement.value = sourceText_English;
    } else if (checkedInputValue === "ar") {
      sourceTextElement.value = sourceText_Arabic;
    } else if (checkedInputValue === "fa") {
      sourceTextElement.value = sourceText_Persian;
    }
    if (checkedOutputValue === "en") {
      targetTextElement.value = transText_English;
    } else if (checkedOutputValue === "ar") {
      targetTextElement.value = transText_Arabic;
    } else if (checkedOutputValue === "fa") {
      targetTextElement.value = transText_Persian;
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
    textArea.rows = 26 ;
    textArea.dir = 'rtl';
  };
  if (lang === "ar") {
    if ( mode === "input") {textArea.placeholder = "أدخل النص العربي"}
    textArea.style.fontFamily = "IranSans";
    textArea.style.fontSize = '16px';
    textArea.style.fontWeight = 'bold';
    textArea.style.textAlign = 'right';
    textArea.rows = 26 ;
    textArea.dir = 'rtl';
  };
  if (lang === "en") {
    if ( mode === "input") {textArea.placeholder = "Enter English text"}
    textArea.style.fontFamily = "RobotoSlab";
    textArea.style.fontSize = '20px';
    textArea.style.fontWeight = 'normal';
    textArea.style.textAlign = 'left';
    textArea.dir = 'ltr';
    textArea.rows = 21 ;
  };
}
