const selectImage = document.querySelector('.select-image');
const inputFile = document.querySelector('#file');
const imgArea = document.querySelector('.img-area');
const predictButton = document.querySelector('.predict-button');
const predictionOutput = document.querySelector('.prediction-output');
const predictedClassOutput = document.getElementById('predicted-class');
const predictedConfidenceOutput = document.getElementById('predicted-confidence');

selectImage.addEventListener('click', function () {
    inputFile.click();
});

inputFile.addEventListener('change', function () {
    const formData = new FormData();
    formData.append('file', this.files[0]);

    $.ajax({
        type: 'POST',
        url: 'http://localhost:8000/predict',
        data: formData,
        processData: false,
        contentType: false,
        success: function(response) {
            displayPrediction(response);
        },
        error: function(xhr, status, error) {
            alert('Error uploading image.');
            console.error(error);
        }
    });
});

predictButton.addEventListener('click', function() {
    // Perform prediction when the predict button is clicked
    const formData = new FormData();
    formData.append('file', inputFile.files[0]);

    $.ajax({
        type: 'POST',
        url: 'http://localhost:8000/predict',
        data: formData,
        processData: false,
        contentType: false,
        success: function(response) {
            displayPrediction(response);
        },
        error: function(xhr, status, error) {
            alert('Error uploading image.');
            console.error(error);
        }
    });
});

function displayPrediction(data) {

    // Show the selected image in the image area
    const selectedImage = URL.createObjectURL(inputFile.files[0]);
    imgArea.innerHTML = `
        <img src="${selectedImage}" alt="Uploaded Image">
        <div>
            <p>Predicted Class: ${data.class}</p>
            <p>Confidence: ${data.confidence}</p>
        </div>
    `;

    // Show the prediction output area
    predictionOutput.style.display = 'block';
    // Display the predicted class and confidence
    predictedClassOutput.textContent = `Predicted Class: ${data.class}`;
    predictedConfidenceOutput.textContent = `Confidence: ${data.confidence}`;
}
