export function render(users) {
  var items = users.map(function (u) {
    return "<li>" + u.email + "</li>";
  });
  return "<ul>" + items.join("") + "</ul>";
}
