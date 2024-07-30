function previewAvatar(event) {
    var input = event.target;
    var reader = new FileReader();
    reader.onload = function(){
        var imgElement = document.getElementById('avatar-preview');
        imgElement.src = reader.result;
    };
    reader.readAsDataURL(input.files[0]);
}