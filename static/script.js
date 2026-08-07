document.addEventListener("DOMContentLoaded", function () {

    const fileInput = document.getElementById("fileInput");
    const dropArea = document.getElementById("dropArea");
    const selectedFile = document.getElementById("selectedFile");

    // -----------------------------
    // File Selection
    // -----------------------------

    if (fileInput) {

        fileInput.addEventListener("change", function () {

            if (fileInput.files.length > 0) {

                selectedFile.innerHTML =
                    "📄 " + fileInput.files[0].name;

            } else {

                selectedFile.innerHTML =
                    "No file selected";

            }

        });

    }

    // -----------------------------
    // Drag & Drop
    // -----------------------------

    if (dropArea) {

        ["dragenter", "dragover"].forEach(function (eventName) {

            dropArea.addEventListener(eventName, function (e) {

                e.preventDefault();

                dropArea.classList.add("dragover");

            });

        });

        ["dragleave", "drop"].forEach(function (eventName) {

            dropArea.addEventListener(eventName, function (e) {

                e.preventDefault();

                dropArea.classList.remove("dragover");

            });

        });

        dropArea.addEventListener("drop", function (e) {

            fileInput.files = e.dataTransfer.files;

            if (fileInput.files.length > 0) {

                selectedFile.innerHTML =
                    "📄 " + fileInput.files[0].name;

            }

        });

    }

    // -----------------------------
    // Auto Fade Alerts
    // -----------------------------

    setTimeout(function () {

        document.querySelectorAll(".alert").forEach(function (alert) {

            alert.style.transition = "0.5s";

            alert.style.opacity = "0";

            setTimeout(function () {

                alert.remove();

            }, 500);

        });

    }, 3000);

    // -----------------------------
    // Search Filter
    // -----------------------------

    const searchInput = document.querySelector(
        'input[name="q"]'
    );

    if (searchInput) {

        searchInput.addEventListener("keyup", function () {

            const value =
                this.value.toLowerCase();

            document.querySelectorAll("tbody tr")
                .forEach(function (row) {

                    row.style.display =
                        row.innerText.toLowerCase().includes(value)
                        ? ""
                        : "none";

                });

        });

    }

});

// -----------------------------
// Copy Share Link
// -----------------------------

function copyLink(link) {

    navigator.clipboard.writeText(link);

    alert("✅ Share link copied successfully!");

}