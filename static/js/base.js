function name_menu(n1, n2){
var name = "{{ first_name }}";
var lastname = "{{ last_name }}";
var initials = name.charAt(0)+""+lastname.charAt(0);
document.getElementById("name").innerHTML = initials;
}