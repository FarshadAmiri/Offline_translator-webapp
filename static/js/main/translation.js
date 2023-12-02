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