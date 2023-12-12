// import { JSEncrypt } from 'jsencrypt';

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

  var radioButtons = document.querySelectorAll('input[name="btnradio_right"], input[name="btnradio_left"]');
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
var radioButtons = document.querySelectorAll('input[name="btnradio_right"], input[name="btnradio_left"]');
var textArea1 = document.getElementById('source_text');
var textArea2 = document.getElementById('translation');

radioButtons.forEach(function(radioButton) {
  radioButton.addEventListener('change', function() {
    if (this.id === 'btnradio1') {
      // If the first radio button is selected, set the placeholder to "Enter text1"
      textArea1.placeholder = 'Enter text';
      textArea1.style.fontFamily = "RobotoSlab";
      textArea1.style.fontSize = '20px';
      textArea1.style.fontWeight = 'normal';
      textArea1.style.textAlign = 'left';
      textArea1.dir = 'ltr';
      textArea1.rows = 20 ;

      textArea2.style.fontFamily = "IranSans";
      textArea2.style.fontSize = '16px';
      textArea2.style.fontWeight = 'bold';
      textArea2.style.textAlign = 'right';
      textArea2.rows = 25 ;
      textArea2.dir = 'rtl';
    } else if (this.id === 'btnradio2') {
      // If the second radio button is selected, set the placeholder to "Enter text2"
      textArea2.style.fontFamily = "RobotoSlab";
      textArea2.style.fontSize = '20px';
      textArea2.style.fontWeight = 'normal';
      textArea2.style.textAlign = 'left';
      textArea2.dir = 'ltr';
      textArea2.rows = 20 ;

      textArea1.placeholder = "متن را وارد کنید";
      textArea1.style.fontFamily = "IranSans";
      textArea1.style.fontSize = '16px';
      textArea1.style.fontWeight = 'bold';
      textArea1.style.textAlign = 'right';
      textArea1.rows = 25 ;
      textArea1.dir = 'rtl';
    }
  });
});

function encodeText(event) {

  var textInput = document.getElementById("source_text");
  var encodedText;
  var chunkSizePersian = 200;
  var chunkSizeEnglish = 500;

  // Replace specific characters like ’ with '
  var modifiedText = textInput.value.replace(/[’]/g, "'");

  // Check if btnradio1 is checked (indicating Persian text)
  var encryptedChunks = [];
  var btnradio1 = document.getElementById("btnradio1");
  if (btnradio1.checked) {
    // English input
    var textChunks = textToChuncks(modifiedText, chunkSizeEnglish);
    for (var i = 0; i < textChunks.length; i++) {
      var encryptedText = encrypt(textChunks[i]); // Encrypt each text
      encryptedChunks.push(encryptedText); // Store encrypted text in encryptedChunks
    }
  } else {
    // Persian input
    var textChunks = textToChuncks(modifiedText, chunkSizePersian);
    for (var i = 0; i < textChunks.length; i++) {
      // encodedText = btoa(unescape(encodeURIComponent(modifiedText)));
      var encryptedText = unescape(encodeURIComponent(textChunks[i]));
      encryptedText = btoa(encryptedText);
      encryptedText = encrypt(encryptedText);
      encryptedChunks.push(encryptedText); // Store encrypted text in encryptedChunks
    }
  }
  // alert(encodedText)

  var encryptedText = encryptedChunks.join("%NEW_CHUNCK%");

  textInput.value = "";

  // Create a hidden input element
  var hiddenInput = document.createElement("input");
  hiddenInput.type = "hidden";
  hiddenInput.name = "encodedText";
  hiddenInput.id = "encodedText";
  hiddenInput.value = encryptedText;

  // Append the hidden input to the form
  var form = document.getElementById("translation_form");
  form.appendChild(hiddenInput);
}


function textToChuncks(text, chunkSize) {
  const chunks = [];
  let startIndex = 0;
  let endIndex = Math.min(chunkSize, text.length);

  while (startIndex < text.length) {
    const chunk = text.substring(startIndex, endIndex);
    chunks.push(chunk);

    startIndex = endIndex;
    endIndex = Math.min(startIndex + chunkSize, text.length);
  }
  return chunks;
}


async function encodeTextAndKey(event) {
  event.preventDefault();
  try {
    // Declare RSA public key
    var rsaPublicKey = "-----BEGIN PUBLIC KEY-----\n" +
    "MIICIjANBgkqhkiG9w0BAQEFAAOCAg8AMIICCgKCAgEAvRW2QcbKbzDobMdkLqvY\n" +
    "Fb66Ih41T1+X3spW1WP6UduM1kS+bVh7HwG23pt8e/XJAf9G4IhWTZfkgVBdMsFP\n" +
    "UfCJDiP/9cbQBgNDtT85jlFHjB1dBlJ51Hh8kDkx/1/dgy2b/ZjJ0YwAFLpk2k8W\n" +
    "ZO8wtIOEHMSdLryVh8Jkpk1qSYZPZZuW+QEE/G+TJcF286mLEpTfZ/RQN4mg/nCS\n" +
    "FhW4Rv9wnF8dhgU43kTiLwV8wVgOTKxAseDxMyvbjKiiH+u5YByZNN1hPVFSYQNx\n" +
    "06IK0Ea7wk0UTRhCwLFu2AOPGL3AylFnjlHCd+/vbDrW3WDj3KRTbZFxtysYqn3B\n" +
    "SnNZy6D1xPn79nsgWfKrgQo9KTgP9gpSoebBZwFIRmBD5Q2BpwZvbZj5lJgEYJpe\n" +
    "xH5LW6Rfv2GZjU+S5SEPNXMlSf6kmfbJAEhsyqKj+tWZtri3AfEBhG7hkmmz51zA\n" +
    "32JwSGV/IFqblOHsONsZizOl4OxzSytgfhCyOkAg6zcb5Hcd3Zod0SHscgkYPAeO\n" +
    "9ZZvD6pneRrcB1tgBPz3CSp6UOe9ktK0Lo5ZlapNUmpIR1Av/immdBnfRfB6m+ax\n" +
    "efNjY6Myl8/aepuND/E1MJviOMCm3cyrmOsNj5rwg2AIGO4vw4hdjXqOLez87t/X\n" +
    "OYNP74TrWvLmcNmlKfQNfMsCAwEAAQ==\n" +
    "-----END PUBLIC KEY-----";

    var rsaPublicKeyBase64 = "Ii0tLS0tQkVHSU4gUFVCTElDIEtFWS0tLS0tXG4iICsNC" +
    "iAgICAiTUlJQ0lqQU5CZ2txaGtpRzl3MEJBUUVGQUFPQ0FnOEFNSUlDQ2dLQ0FnRUF2Ulc" + 
    "yUWNiS2J6RG9iTWRrTHF2WVxuIiArDQogICAgIkZiNjZJaDQxVDErWDNzcFcxV1A2VWR1T" +
    "TFrUytiVmg3SHdHMjNwdDhlL1hKQWY5RzRJaFdUWmZrZ1ZCZE1zRlBcbiIgKw0KICAgICJ" + 
    "VZkNKRGlQLzljYlFCZ05EdFQ4NWpsRkhqQjFkQmxKNTFIaDhrRGt4LzEvZGd5MmIvWmpKM" + 
    "Fl3QUZMcGsyazhXXG4iICsNCiAgICAiWk84d3RJT0VITVNkTHJ5Vmg4SmtwazFxU1laUFp" +
    "adVcrUUVFL0crVEpjRjI4Nm1MRXBUZlovUlFONG1nL25DU1xuIiArDQogICAgIkZoVzRSd" +
    "jl3bkY4ZGhnVTQza1RpTHdWOHdWZ09US3hBc2VEeE15dmJqS2lpSCt1NVlCeVpOTjFoUFZ" +
    "GU1lRTnhcbiIgKw0KICAgICIwNklLMEVhN3drMFVUUmhDd0xGdTJBT1BHTDNBeWxGbmpsS" +
    "ENkKy92YkRyVzNXRGozS1JUYlpGeHR5c1lxbjNCXG4iICsNCiAgICAiU25OWnk2RDF4UG4" + 
    "3OW5zZ1dmS3JnUW85S1RnUDlncFNvZWJCWndGSVJtQkQ1UTJCcHdadmJaajVsSmdFWUpwZ" + 
    "VxuIiArDQogICAgInhINUxXNlJmdjJHWmpVK1M1U0VQTlhNbFNmNmttZmJKQUVoc3lxS2o" + 
    "rdFdadHJpM0FmRUJoRzdoa21tejUxekFcbiIgKw0KICAgICIzMkp3U0dWL0lGcWJsT0hzT" + 
    "05zWml6T2w0T3h6U3l0Z2ZoQ3lPa0FnNnpjYjVIY2QzWm9kMFNIc2Nna1lQQWVPXG4iICs" +
    "NCiAgICAiOVpadkQ2cG5lUnJjQjF0Z0JQejNDU3A2VU9lOWt0SzBMbzVabGFwTlVtcElSM" + 
    "UF2L2ltbWRCbmZSZkI2bStheFxuIiArDQogICAgImVmTmpZNk15bDgvYWVwdU5EL0UxTUp" + 
    "2aU9NQ20zY3lybU9zTmo1cndnMkFJR080dnc0aGRqWHFPTGV6ODd0L1hcbiIgKw0KICAgI" + 
    "CJPWU5QNzRUcld2TG1jTm1sS2ZRTmZNc0NBd0VBQVE9PVxuIiArDQogICAgIi0tLS0tRU5" + 
    "EIFBVQkxJQyBLRVktLS0tLSI7Ii0tLS0tQkVHSU4gUFVCTElDIEtFWS0tLS0tXG4iICsNC" + 
    "iAgICAiTUlJQ0lqQU5CZ2txaGtpRzl3MEJBUUVGQUFPQ0FnOEFNSUlDQ2dLQ0FnRUF2Ulc" + 
    "yUWNiS2J6RG9iTWRrTHF2WVxuIiArDQogICAgIkZiNjZJaDQxVDErWDNzcFcxV1A2VWR1T" +
    "TFrUytiVmg3SHdHMjNwdDhlL1hKQWY5RzRJaFdUWmZrZ1ZCZE1zRlBcbiIgKw0KICAgICJ" +
    "VZkNKRGlQLzljYlFCZ05EdFQ4NWpsRkhqQjFkQmxKNTFIaDhrRGt4LzEvZGd5MmIvWmpKM" +
    "Fl3QUZMcGsyazhXXG4iICsNCiAgICAiWk84d3RJT0VITVNkTHJ5Vmg4SmtwazFxU1laUFp" +
    "adVcrUUVFL0crVEpjRjI4Nm1MRXBUZlovUlFONG1nL25DU1xuIiArDQogICAgIkZoVzRSd" +
    "jl3bkY4ZGhnVTQza1RpTHdWOHdWZ09US3hBc2VEeE15dmJqS2lpSCt1NVlCeVpOTjFoUFZ" +
    "GU1lRTnhcbiIgKw0KICAgICIwNklLMEVhN3drMFVUUmhDd0xGdTJBT1BHTDNBeWxGbmpsS" +
    "ENkKy92YkRyVzNXRGozS1JUYlpGeHR5c1lxbjNCXG4iICsNCiAgICAiU25OWnk2RDF4UG4" +
    "3OW5zZ1dmS3JnUW85S1RnUDlncFNvZWJCWndGSVJtQkQ1UTJCcHdadmJaajVsSmdFWUpwZ" +
    "VxuIiArDQogICAgInhINUxXNlJmdjJHWmpVK1M1U0VQTlhNbFNmNmttZmJKQUVoc3lxS2o" +
    "rdFdadHJpM0FmRUJoRzdoa21tejUxekFcbiIgKw0KICAgICIzMkp3U0dWL0lGcWJsT0hzT" +
    "05zWml6T2w0T3h6U3l0Z2ZoQ3lPa0FnNnpjYjVIY2QzWm9kMFNIc2Nna1lQQWVPXG4iICs" +
    "NCiAgICAiOVpadkQ2cG5lUnJjQjF0Z0JQejNDU3A2VU9lOWt0SzBMbzVabGFwTlVtcElSM" +
    "UF2L2ltbWRCbmZSZkI2bStheFxuIiArDQogICAgImVmTmpZNk15bDgvYWVwdU5EL0UxTUp" +
    "2aU9NQ20zY3lybU9zTmo1cndnMkFJR080dnc0aGRqWHFPTGV6ODd0L1hcbiIgKw0KICAgI" +
    "CJPWU5QNzRUcld2TG1jTm1sS2ZRTmZNc0NBd0VBQVE9PVxuIiArDQogICAgIi0tLS0tRU5" + 
    "EIFBVQkxJQyBLRVktLS0tLSI7"
    
    // Get text input
    var textInput = document.getElementById("source_text");
    
    // Generate AES key
    const aesKey = await window.crypto.subtle.generateKey(
      {
        name: 'AES-GCM',
        length: 256,
      },
      true,
      ['encrypt', 'decrypt']
    );

    // Import RSA public key
    const importedRSAPublicKey = await window.crypto.subtle.importKey(
      'spki',
      rsaPublicKey,
      {
        name: 'RSA-OAEP',
        hash: { name: 'SHA-512' },
      },
      false,
      ['encrypt']
    );

    // Export AES key
    const exportedAESKey = await window.crypto.subtle.exportKey('raw', aesKey);

    // Encrypt text with AES key
    const textEncoder = new TextEncoder();
    const encodedText = await window.crypto.subtle.encrypt(
      {
        name: 'AES-GCM',
        iv: window.crypto.getRandomValues(new Uint8Array(12)),
      },
      aesKey,
      textEncoder.encode(textInput)
    );

    // Encrypt AES key with RSA public key
    const encryptedAESKey = await window.crypto.subtle.encrypt(
      {
        name: 'RSA-OAEP',
      },
      importedRSAPublicKey,
      exportedAESKey
    );

    alert('exportedAESKey:', exportedAESKey);
    alert('encodedText:', encodedText);

    // Encoded text and AES key
    const encodedData = {
      encodedText: Array.from(new Uint8Array(encodedText))
        .map(byte => String.fromCharCode(byte))
        .join(''),
      encryptedAESKey: Array.from(new Uint8Array(encryptedAESKey))
        .map(byte => String.fromCharCode(byte))
        .join(''),
    };
    var hiddenEncodedText = document.createElement("input");
    hiddenEncodedText.type = "hidden";
    hiddenEncodedText.name = "encodedText";
    hiddenEncodedText.id = "encodedText";
    hiddenEncodedText.value = encodedText;

    var hiddenEncryptedAESKey = document.createElement("input");
    hiddenEncryptedAESKey.type = "hidden";
    hiddenEncryptedAESKey.name = "encryptedAESKey";
    hiddenEncryptedAESKey.id = "encryptedAESKey";
    hiddenEncryptedAESKey.value = encryptedAESKey;

    // Append the hidden input to the form
    var form = document.getElementById("translation_form");
    form.appendChild(hiddenEncodedText);
    form.appendChild(hiddenEncryptedAESKey);

    return encodedData;
  } catch (error) {
    alert('Error:', error);
    return null;
  }
}

