function clearText(textBoxId) {
    const checkedInputValue = document.querySelector('input[name="btnRadio_input"]:checked').value;
    const checkedOutputValue = document.querySelector('input[name="btnRadio_output"]:checked').value;
    document.getElementById(textBoxId).value = "";
  
    if (textBoxId == "source_text") {
      if (checkedInputValue === "en") {
        sourceText_English = "";
      } else if (checkedInputValue === "ar") {
        sourceText_Arabic = "" ;
      } else if (checkedInputValue === "fa") {
        sourceText_Persian = "" ;
      } else if (checkedInputValue === "he") {
        sourceText_Hebrew = "" ;
      }
    } else if (textBoxId == "translation") {
      if (checkedOutputValue === "en") {
        transText_English = "" ;
      } else if (checkedOutputValue === "ar") {
        transText_Arabic = "" ;
      } else if (checkedOutputValue === "fa") {
        transText_Persian = "" ;
      } else if (checkedOutputValue === "he") {
        transText_Hebrew = "" ;
      };
    }
  }
  
  
  function copyTextToClipboard(text) {
    var textarea = document.createElement("textarea");
    textarea.value = text;
    // Make the textarea non-editable to avoid focus and move outside of view
    textarea.setAttribute("readonly", "");
    textarea.style.position = "absolute";
    textarea.style.left = "-9999px";
    // Add the textarea to the HTML document
    document.body.appendChild(textarea);
    // Select and copy the text inside the textarea
    textarea.select();
    document.execCommand("copy");
    // Remove the textarea from the document
    document.body.removeChild(textarea);
  };
  
  
  function copyText(textboxId) {
      var textbox = document.getElementById(textboxId);
      var text = textbox.value;
    
      copyTextToClipboard(text);
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
      } else if (previousSourceLangElement.value=== 'he') {
        sourceText_Hebrew = sourceTextElement.value;
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
  
    
    function changeText() {
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
      } else if (checkedInputValue === "he") {
        sourceTextElement.value = sourceText_Hebrew;
      }
      if (checkedOutputValue === "en") {
        targetTextElement.value = transText_English;
      } else if (checkedOutputValue === "ar") {
        targetTextElement.value = transText_Arabic;
      } else if (checkedOutputValue === "fa") {
        targetTextElement.value = transText_Persian;
      } else if (checkedOutputValue === "he") {
        targetTextElement.value = transText_Hebrew;
      }
    };
  
  
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
      } else if (btnInput.id === "btnInput-he") {
        applyLanguageSettings (textArea1, "he", "input")
      };
      if (btnOutput.id === "btnOutput-en") {
        applyLanguageSettings (textArea2, "en", "output")
      } else if (btnOutput.id === "btnOutput-ar") {
        applyLanguageSettings (textArea2, "ar", "output")
      } else if (btnOutput.id === "btnOutput-fa") {
        applyLanguageSettings (textArea2, "fa", "output")
      } else if (btnOutput.id === "btnOutput-he") {
        applyLanguageSettings (textArea2, "he", "output")
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
      textArea.style.fontFamily = "Tahoma";
      textArea.style.fontSize = '20px';
      textArea.style.fontWeight = 'normal';
      textArea.style.textAlign = 'left';
      textArea.dir = 'ltr';
      textArea.rows = 21 ;
    };
    if (lang === "he") {
      if ( mode === "input") {textArea.placeholder = "הזן טקסט בעברית"}
      textArea.style.fontFamily = "Arial";
      textArea.style.fontSize = '20px';
      textArea.style.fontWeight = 'normal';
      textArea.style.textAlign = 'right';
      textArea.dir = 'rtl';
      textArea.rows = 21 ;
    };
  }
  
  
  function swapTexts() {
    const checkedInputValue = document.querySelector('input[name="btnRadio_input"]:checked').value;
    const checkedOutputValue = document.querySelector('input[name="btnRadio_output"]:checked').value;
    var sourceTextElement = document.getElementById("source_text");
    var targetTextElement = document.getElementById("translation");
  
    var sourceTextTemp = document.getElementById("source_text").value;
    var targetTextTemp = document.getElementById("translation").value;
    
    if (checkedInputValue === "en") {
      document.getElementById('btnOutput-en').click();
    } else if (checkedInputValue === "ar") {
      document.getElementById('btnOutput-ar').click();
    } else if (checkedInputValue === "fa") {
      document.getElementById('btnOutput-fa').click();
    } else if (checkedInputValue === "he") {
      document.getElementById('btnOutput-he').click();
    };
    if (checkedOutputValue === "en") {
      document.getElementById('btnInput-en').click();
    } else if (checkedOutputValue === "ar") {
      document.getElementById('btnInput-ar').click();
    } else if (checkedOutputValue === "fa") {
      document.getElementById('btnInput-fa').click();
    } else if (checkedOutputValue === "he") {
      document.getElementById('btnInput-he').click();
    };
  
    targetTextElement.value = sourceTextTemp;
    sourceTextElement.value = targetTextTemp;
  };