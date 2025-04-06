
document.getElementById("uploadForm").addEventListener("submit", function (event) {
    event.preventDefault();

    let formData = new FormData(this);

    fetch("upload/", {
        method: "POST",
        body: formData
    })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                alert(data.error);
            } else {
                document.getElementById("output").classList.remove("hidden");
                document.getElementById("resultContainer").innerText = data.result;
            }
        })
        .catch(error => console.error("Error:", error));
});

