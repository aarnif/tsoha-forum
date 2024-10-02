const displayErrorMessageBox = () => {
  const displayTime = 3000;
  const errorMessageBox = document.getElementById("error-message-box");
  const errorMessage = document.querySelector(".error-message");
  if (errorMessage.textContent === "") {
    return;
  } else {
    console.log("Error message:", errorMessage.textContent);
    errorMessageBox.style.display = "block";
    setTimeout(() => {
      errorMessageBox.style.display = "none";
    }, displayTime);
  }
};
displayErrorMessageBox();
