document.addEventListener('DOMContentLoaded', function () {
    const startCameraButton = document.getElementById('startCamera');
    const cameraContainer = document.getElementById('cameraContainer');
    const video = document.getElementById('video');
    const captureButton = document.getElementById('capture');
    const canvas = document.createElement('canvas');
    const context = canvas.getContext('2d');
    let stream;

    startCameraButton.addEventListener('click', () => {
        // Check for camera support
        if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
            navigator.mediaDevices.getUserMedia({ video: true })
                .then(videoStream => {
                    stream = videoStream;
                    video.srcObject = stream;
                    cameraContainer.style.display = 'block';
                })
                .catch(error => {
                    console.error('Error accessing camera:', error);
                });
        } else {
            console.error('getUserMedia not supported on your browser');
        }
    });

    captureButton.addEventListener('click', () => {
        // Draw the current frame of the video onto the canvas
        context.drawImage(video, 0, 0, canvas.width, canvas.height);

        // Extract the image data from the canvas
        const imageData = canvas.toDataURL('image/jpeg');

        // Stop the video stream
        if (stream) {
            stream.getTracks().forEach(track => track.stop());
            cameraContainer.style.display = 'none';
        }

        // Send the image data to the server using an AJAX request
        fetch('/capture_photo/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrf_token,
            },
            body: JSON.stringify({ photo: imageData }),
        })
            .then(response => response.json())
            .then(data => {
                console.log(data);
                // Handle the server response as needed
            })
            .catch(error => {
                console.error('Error:', error);
            });
    });
});