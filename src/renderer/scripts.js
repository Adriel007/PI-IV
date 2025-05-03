document.addEventListener("DOMContentLoaded", () => {
  setTimeout(() => {
    document.getElementById("loading").classList.add("hidden");
    document.getElementById("container").classList.remove("hidden");
  }, 2_000);
});
