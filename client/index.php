<!DOCTYPE html>
<meta charset="utf-8">
<html>
<head>
  <title>Simple Frontend</title>
  <link rel="stylesheet" href="./style.css">
</head>
<body>
  <h1>Doctor's Portal </h1>
  
  <form>
    <div class="form-field">
      <input type="text" placeholder="Username" required/>
    </div>
    
    <div class="form-field">
      <input type="password" placeholder="Password" required/>                         
    </div>
    
    <div class="form-field">
      <button class="btn" type="submit">Log in</button>
      
    </div>
  </form>
  <?php
if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $data = array(
        'Username' => $_POST['Username'],
        'Email' => $_POST['Email']
    );
    
    // Convert data to JSON format
    $json_data = json_encode($data, JSON_PRETTY_PRINT);

    // Save JSON data to a file
    file_put_contents('data.json', $json_data);

    echo "Form data has been saved as JSON.";
}
?>

</body>
</html>
