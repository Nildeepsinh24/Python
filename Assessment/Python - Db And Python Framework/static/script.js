// 🌙 DARK MODE TOGGLE LOGIC
const toggleButton = document.getElementById("themeToggle");
const htmlElement = document.documentElement;

// Load theme from localStorage
const currentTheme = localStorage.getItem("theme") || "light";
htmlElement.setAttribute("data-theme", currentTheme);
toggleButton.textContent = currentTheme === "dark" ? "☀️" : "🌙";

// Toggle event
toggleButton.addEventListener("click", () => {
  const newTheme = htmlElement.getAttribute("data-theme") === "light" ? "dark" : "light";
  htmlElement.setAttribute("data-theme", newTheme);
  localStorage.setItem("theme", newTheme);
  toggleButton.textContent = newTheme === "dark" ? "☀️" : "🌙";
});
