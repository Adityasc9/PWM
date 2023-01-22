var regex = /^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$/;
function checkValidPasswords() {
    let pass1 = document.getElementById("InputPassword").value;
    let pass2 = document.getElementById("RetypePassword").value;
    let warning = document.getElementById("warning-message");
    let button = document.getElementById("submit-button");
    if(regex.test(pass1)){

        if(pass1 === pass2){
            button.disabled = false;
            warning.innerHTML = "";
        }

        else{
            warning.innerHTML = "PASSWORDS DO NOT MATCH";
            button.disabled = true;
        }


    }

    else{
        button.disabled = true;
        warning.innerHTML = "passwords need to have a min of 8 letters, with at least a symbol, upper and lower case letters and a number";
    }

};
function addValidPassword(){
    let pass = document.getElementById("NewPass").value;
    let button = document.getElementById("add-button");
    let warning = document.getElementById("new-warning-message");
    let website = document.getElementById("newWebsite").value;
    let user = document.getElementById("newUsername").value;

    if(regex.test(pass) && !(website == "") && !(user == "")){
        button.disabled = false;
        warning.innerHTML = "";
    }
    else {
        button.disabled = true;
        warning.innerHTML = "Complete all fields. Passwords need to have a min of 8 letters, with at least a symbol, upper and lower case letters and a number";
    }

    
    

}
function getValue() {
    var length = document.getElementById("PasswordRange").value;
     document.getElementById("RangeValue").innerHTML = length + " characters";
}

function generate(){
    var length = document.getElementById("PasswordRange").value;
    var chars = "0123456789abcdefghijklmnopqrstuvwxyz!@#$%^&*()ABCDEFGHIJKLMNOPQRSTUVWXYZ";
    var charactersLength = chars.length;
    let Genpass = "";
    let NewPass = document.getElementById("NewPass");
    while(regex.test(Genpass) == false){
        Genpass = "";
        for(let step = 0; step < length; step++){
            Genpass += chars.charAt(Math.floor(Math.random() * charactersLength));

        }
    }
    NewPass.value = Genpass;
    addValidPassword();

}
