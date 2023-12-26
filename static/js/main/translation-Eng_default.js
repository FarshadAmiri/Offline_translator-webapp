// import { JSEncrypt } from 'jsencrypt';

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

  // var radioButtons = document.querySelectorAll('input[name="btnradio_right"], input[name="btnradio_left"]');
  // radioButtons.forEach(function(radioButton) {
  //   radioButton.addEventListener('change', function() {
  //     if (this.id === 'btnradio1') {
  //       // If the first radio button is selected, select the corresponding disabled radio button
  //       document.getElementById('btnradio1').checked = true;
  //       document.getElementById('btnradio4').checked = true;
  //     } else if (this.id === 'btnradio2') {
  //       // If the second disabled radio button is selected, select the first radio button
  //       document.getElementById('btnradio2').checked = true;
  //       document.getElementById('btnradio3').checked = true;
  //     }
  //   });
  // });


  function disableCorrespondingRadio(element) {
    element.checked = true;
    var radio1 = document.getElementsByName("btnradio_left");
    var radio2 = document.getElementsByName("btnradio_right");
  
    for (var i = 0; i < radio1.length; i++) {
      if (radio1[i].checked) {
        var lang = radio1[i].value;
  
        for (var j = 0; j < radio2.length; j++) {
          if (radio2[j].value === lang) {
            if (radio2[j].checked === true){
              radio2[j].checked = false;
              if (j === 0) {
                radio2[j+1].checked = true;
              } else {
                radio2[j-1].checked = true;
              }
            }
          }
        }
        break;
      }
    }
    element.checked = true;
    for (var k = 0; k < radio2.length; k++) {
      if (radio2[k].checked) {
        var lang = radio2[k].value;
  
        for (var l = 0; l < radio1.length; l++) {
          if (radio1[l].value === lang) {
            if (radio1[l].checked === true) {
              radio1[l].checked = false;
              if (l === 0) {
                radio1[l+1].checked = true;
              } else {
                radio1[l-1].checked = true;
              }
            }
          }
        }
        break;
      }
    }
  }

// Add an event listener for the radio buttons
// var radioButtons = document.querySelectorAll('input[name="btnradio_right"], input[name="btnradio_left"]');
// var textArea1 = document.getElementById('source_text');
// var textArea2 = document.getElementById('translation');

// radioButtons.forEach(function(radioButton) {
//   radioButton.addEventListener('change', function() {
//     if (this.id === 'btnradio1') {
//       // If the first radio button is selected, set the placeholder to "Enter text1"
//       textArea1.placeholder = 'Enter text';
//       textArea1.style.fontFamily = "RobotoSlab";
//       textArea1.style.fontSize = '20px';
//       textArea1.style.fontWeight = 'normal';
//       textArea1.style.textAlign = 'left';
//       textArea1.dir = 'ltr';
//       textArea1.rows = 20 ;

//       textArea2.style.fontFamily = "IranSans";
//       textArea2.style.fontSize = '16px';
//       textArea2.style.fontWeight = 'bold';
//       textArea2.style.textAlign = 'right';
//       textArea2.rows = 25 ;
//       textArea2.dir = 'rtl';
//     } else if (this.id === 'btnradio2') {
//       // If the second radio button is selected, set the placeholder to "Enter text2"
//       textArea2.style.fontFamily = "RobotoSlab";
//       textArea2.style.fontSize = '20px';
//       textArea2.style.fontWeight = 'normal';
//       textArea2.style.textAlign = 'left';
//       textArea2.dir = 'ltr';
//       textArea2.rows = 20 ;

//       textArea1.placeholder = "متن را وارد کنید";
//       textArea1.style.fontFamily = "IranSans";
//       textArea1.style.fontSize = '16px';
//       textArea1.style.fontWeight = 'bold';
//       textArea1.style.textAlign = 'right';
//       textArea1.rows = 25 ;
//       textArea1.dir = 'rtl';
//     }
//   });
// });

// function encodeTextWithRSA(event) {

//   var textInput = document.getElementById("source_text");
//   var encodedText;
//   var chunkSizePersian = 200;
//   var chunkSizeEnglish = 500;

//   // Replace specific characters like ’ with '
//   var modifiedText = textInput.value.replace(/[’]/g, "'");

//   // Check if btnradio1 is checked (indicating Persian text)
//   var encryptedChunks = [];
//   var btnradio1 = document.getElementById("btnradio1");
//   if (btnradio1.checked) {
//     // English input
//     var textChunks = textToChuncks(modifiedText, chunkSizeEnglish);
//     for (var i = 0; i < textChunks.length; i++) {
//       var encryptedText = encrypt(textChunks[i]); // Encrypt each text
//       encryptedChunks.push(encryptedText); // Store encrypted text in encryptedChunks
//     }
//   } else {
//     // Persian input
//     var textChunks = textToChuncks(modifiedText, chunkSizePersian);
//     for (var i = 0; i < textChunks.length; i++) {
//       // encodedText = btoa(unescape(encodeURIComponent(modifiedText)));
//       var encryptedText = unescape(encodeURIComponent(textChunks[i]));
//       encryptedText = btoa(encryptedText);
//       encryptedText = encrypt(encryptedText);
//       encryptedChunks.push(encryptedText); // Store encrypted text in encryptedChunks
//     }
//   }