function toggleAnswer(button) {
    const answer = button.nextElementSibling;
    answer.classList.toggle("show");
    const icon = button.querySelector("span");
    icon.textContent = answer.classList.contains("show") ? "−" : "+";
}