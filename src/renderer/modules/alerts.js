const showAlert = (message, type = "success") => {
  if (type === "error") {
    Swal.fire({
      icon: "error",
      title: "Erro",
      text: message,
    });
  } else {
    Swal.fire({
      icon: "success",
      title: "Sucesso",
      text: message,
      timer: 1500,
      showConfirmButton: false,
    });
  }
};

export { showAlert };
