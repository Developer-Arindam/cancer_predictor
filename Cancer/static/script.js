document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById("prediction-form");
    const resultDisplay = document.getElementById("result");

    form.addEventListener("submit", function (event) {
        event.preventDefault();  // Prevent form from submitting the traditional way

        // Collect form data
        const formData = new FormData(form);

        // Send form data to the Flask backend via POST request
        fetch("/predict", {
            method: "POST",
            body: formData
        })
        .then(response => response.text())
        .then(result => {
            resultDisplay.innerText = `Prediction Result: ${result}`;  // Display result in <p id="result">
        })
        .catch(error => {
            console.error("Error:", error);
            resultDisplay.innerText = "An error occurred. Please try again.";
        });
        
        let output = document.getElementById("result").style;
        output.backgroundColor = "#efff93";
        output.color = "#154216";
        output.textAlign = "center";
        output.fontSize = "25px";
        output.fontWeight = "bold";
        output.marginTop = "20px";
        output.marginBottom = "20px";
        output.border = "2px solid #4CAF50";
        output.padding = "10px 0px 0px 0px";
        output.borderRadius = "5px";
        
    });
});
