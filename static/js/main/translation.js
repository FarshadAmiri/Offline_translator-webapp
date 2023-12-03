function clearText(textboxId) {
    document.getElementById(textboxId).value = "";
}

function copyText2(textboxId) {
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

  var radioButtons = document.querySelectorAll('input[name="btnradio"]');
  radioButtons.forEach(function(radioButton) {
    radioButton.addEventListener('change', function() {
      if (this.id === 'btnradio1') {
        // If the first radio button is selected, select the corresponding disabled radio button
        document.getElementById('btnradio1').checked = true;
        document.getElementById('btnradio4').checked = true;
      } else if (this.id === 'btnradio2') {
        // If the second disabled radio button is selected, select the first radio button
        document.getElementById('btnradio2').checked = true;
        document.getElementById('btnradio3').checked = true;
      }
    });
  });


// Add an event listener for the radio buttons
var radioButtons = document.querySelectorAll('input[name="btnradio"]');
var textArea = document.getElementById('Textbox-1');

radioButtons.forEach(function(radioButton) {
  radioButton.addEventListener('change', function() {
    if (this.id === 'btnradio1') {
      // If the first radio button is selected, set the placeholder to "Enter text1"
      textArea.placeholder = 'Enter text';
      textArea.style.textAlign = 'left';
    } else if (this.id === 'btnradio2') {
      // If the second radio button is selected, set the placeholder to "Enter text2"
      textArea.placeholder = 'متن را وارد کنید';
      textArea.style.textAlign = 'right';
      textArea.style.fontFamily = "IranSans";
      // textArea.style.fontSize = '16px';
      // textArea.style.fontWeight = 'bold';
    }
  });
});