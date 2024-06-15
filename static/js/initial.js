$(document).ready(function(){
    var firstname = $('#firstName').text();
    var lastname = $('#lastName').text();
    var initials = $('#firstName').text().charAt(0) + $('#lastName').text().charAt(0);
    console.log(initials + "hi");
    var profileImage = $('#profileImage').text(initials);
});