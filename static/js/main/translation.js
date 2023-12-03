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
var textArea1 = document.getElementById('Textbox-1');
var textArea2 = document.getElementById('Textbox-2');

radioButtons.forEach(function(radioButton) {
  radioButton.addEventListener('change', function() {
    if (this.id === 'btnradio1') {
      // If the first radio button is selected, set the placeholder to "Enter text1"
      textArea1.placeholder = 'Enter text';
      textArea1.style.fontFamily = "RobotoSlab";
      textArea1.style.fontSize = '20px';
      textArea1.style.fontWeight = 'normal';
      textArea1.style.textAlign = 'left';
      textArea1.rows = 20 ;

      textArea2.style.fontFamily = "IranSans";
      textArea2.style.fontSize = '16px';
      textArea2.style.fontWeight = 'bold';
      textArea2.style.textAlign = 'right';
      textArea2.rows = 25 ;
    } else if (this.id === 'btnradio2') {
      // If the second radio button is selected, set the placeholder to "Enter text2"
      textArea2.style.fontFamily = "RobotoSlab";
      textArea2.style.fontSize = '20px';
      textArea2.style.fontWeight = 'normal';
      textArea2.style.textAlign = 'left';
      textArea2.rows = 20 ;
      textArea2.dir = 'rtl';

      textArea1.placeholder = 'متن را وارد کنید';
      textArea1.style.fontFamily = "IranSans";
      textArea1.style.fontSize = '16px';
      textArea1.style.fontWeight = 'bold';
      textArea1.style.textAlign = 'right';
      textArea1.rows = 25 ;
      textArea1.dir = 'rtl';
    }
  });
});