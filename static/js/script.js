// ======================================
// AI Clothing Classification
// main.js / script.js
// ======================================

// Preview Image
const imageInput = document.querySelector('input[type="file"]');
const previewImage = document.getElementById("preview-image");
const fileName = document.getElementById("file-name");
const predictBtn = document.getElementById("predict-btn");
const loading = document.getElementById("loading");

if (imageInput) {

    imageInput.addEventListener("change", function () {

        const file = this.files[0];

        if (!file) return;

        const allowed = ["image/jpeg", "image/png", "image/jpg"];

        if (!allowed.includes(file.type)) {

            alert("File harus berupa JPG, JPEG, atau PNG");

            this.value = "";

            return;
        }

        if (fileName) {
            fileName.innerHTML = file.name;
        }

        const reader = new FileReader();

        reader.onload = function (e) {

            if (previewImage) {

                previewImage.src = e.target.result;

                previewImage.style.display = "block";

            }

        }

        reader.readAsDataURL(file);

    });

}


// ======================================
// Loading Animation
// ======================================

const form = document.querySelector("form");

if (form) {

    form.addEventListener("submit", function () {

        if (loading) {

            loading.style.display = "block";

        }

        if (predictBtn) {

            predictBtn.disabled = true;

            predictBtn.innerHTML =
                '<span class="spinner-border spinner-border-sm"></span> Predicting...';

        }

    });

}


// ======================================
// Smooth Scroll
// ======================================

document.querySelectorAll('a[href^="#"]').forEach(anchor => {

    anchor.addEventListener("click", function (e) {

        e.preventDefault();

        document.querySelector(this.getAttribute("href"))
            .scrollIntoView({

                behavior: "smooth"

            });

    });

});


// ======================================
// Fade Animation
// ======================================

window.addEventListener("load", () => {

    const cards = document.querySelectorAll(".card");

    cards.forEach((card, index) => {

        setTimeout(() => {

            card.classList.add("fade-up");

        }, index * 200);

    });

});