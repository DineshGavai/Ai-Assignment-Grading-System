
document.getElementById("uploadForm").addEventListener("submit", function (event) {
    event.preventDefault();

    let formData = new FormData(this);

    fetch("http://127.0.0.1:8000/models/upload/", {
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

console.log("Fuck you")