let modoLogin = true;

function alternar() {
    modoLogin = !modoLogin;

    document.getElementById("formLogin").style.display = modoLogin ? "block" : "none";
    document.getElementById("formCadastro").style.display = modoLogin ? "none" : "block";

    document.getElementById("titulo").innerText = modoLogin ? "Login" : "Cadastro";
    document.getElementById("textoAlternar").innerText =
        modoLogin ? "Não tem conta? Cadastre-se" : "Já tem conta? Faça login";
}

function login() {
    fetch("http://localhost:5000/login", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({
            email: document.getElementById("loginEmail").value,
            senha: document.getElementById("loginSenha").value
        })
    })
    .then(res => res.json())
    .then(data => {
        if (data.id) {
            localStorage.setItem("usuario_id", data.id);
            window.location.href = "index.html";
        } else {
            alert(data.error);
        }
    });
}

function cadastrar() {
    fetch("http://localhost:5000/register", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({
            nome: document.getElementById("cadNome").value,
            email: document.getElementById("cadEmail").value,
            senha: document.getElementById("cadSenha").value
        })
    })
    .then(res => res.json())
    .then(data => {
        alert(data.message || data.error);
        if (data.message) alternar();
    });
}