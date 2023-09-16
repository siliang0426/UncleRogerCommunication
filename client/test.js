const form = document.getElementById("myForm");

form.addEventListener("submit", function (e) {
  e.preventDefault(); // Prevent the form from submitting

  const formData = new FormData(form);
  const inputValue = formData.get("myInput");

  if (inputValue === "hello") {
    console.log("Input value is the same");
    

    const data = {
      value: inputValue,
      result: true,
    };

    const jsonData = JSON.stringify(data);

    fetch("test.json", {
      method: "POST",
      body: jsonData,
    })
      .then((response) => response.text())
      .then((data) => console.log(data))
      .catch((error) => console.error(error));
  } else {
    console.log("Input value is different");

    const data = {
      value: inputValue,
      result: false,
    };

    const jsonData = JSON.stringify(data);

    fetch("test.json", {
      method: "POST",
      body: jsonData,
    })
      .then((response) => response.text())
      .then((data) => console.log(data))
      .catch((error) => console.error(error));
  }
});