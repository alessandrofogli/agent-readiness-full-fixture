import { render } from "./app.js";

var el = document.getElementById("app");
if (el) {
  el.innerHTML = render([{ email: "alice@example.com" }]);
}
