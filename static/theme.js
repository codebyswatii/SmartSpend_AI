document.addEventListener("DOMContentLoaded", () => {

    const toggle = document.getElementById("theme-toggle");

    let theme = localStorage.getItem("theme") || "light";

    if (theme === "dark") {
        document.body.classList.add("dark-mode");

        if (toggle) {
            toggle.textContent = "☀️";
        }
    }

    if (toggle) {

        toggle.addEventListener("click", () => {

            document.body.classList.toggle("dark-mode");

            if (document.body.classList.contains("dark-mode")) {

                localStorage.setItem("theme", "dark");
                toggle.textContent = "☀️";

            } else {

                localStorage.setItem("theme", "light");
                toggle.textContent = "🌙";
            }

        });

    }

});