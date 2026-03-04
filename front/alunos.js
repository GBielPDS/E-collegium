const usuarioId = localStorage.getItem("usuario_id");

if (!usuarioId) {
    alert("Usuário não logado!");
    window.location.href = "login.html";
}

const urlParams = new URLSearchParams(window.location.search);
const turmaId = urlParams.get("turma");

if (!turmaId) {
    alert("Turma inválida!");
    window.location.href = "index.html";
}

document.addEventListener("DOMContentLoaded", () => {
    buscarAlunos();

    const botaoAdd = document.querySelector(".btn-add-aluno");

    if (botaoAdd) {
        botaoAdd.addEventListener("click", adicionarAluno);
    }
});

async function buscarAlunos() {

    const response = await fetch(`http://127.0.0.1:5000/turmas/${turmaId}/alunos`);
    const alunos = await response.json();

    const tbody = document.querySelector("#tabelaAlunos tbody");
    tbody.innerHTML = "";

    alunos.forEach(aluno => {
        const row = `
            <tr>
                <td>${aluno.id}</td>
                <td>${aluno.nome}</td>
                <td>${aluno.nota1}</td>
                <td>${aluno.nota2}</td>
                <td>${aluno.nota3}</td>
                <td>${aluno.nota4}</td>
                <td>${aluno.nota_final}</td>
                <td>
                    <button class="btn btn-warning btn-sm me-2" onclick="editarAluno(${aluno.id}, event)">
                        Editar
                    </button>

                    <button class="btn btn-danger btn-sm" onclick="excluirAluno(${aluno.id})">
                        Excluir
                    </button>
                </td>
            </tr>
        `;
        tbody.innerHTML += row;
    });
}

async function editarAluno(id, event) {

    const linha = event.target.closest("tr");
    const botao = event.target;

    if (botao.textContent === "Salvar") {

        const inputs = linha.querySelectorAll("input");

        const dados = {
            nome: inputs[0].value,
            nota1: parseFloat(inputs[1].value),
            nota2: parseFloat(inputs[2].value),
            nota3: parseFloat(inputs[3].value),
            nota4: parseFloat(inputs[4].value)
        };

        await fetch(`http://127.0.0.1:5000/alunos/${id}`, {
            method: "PUT",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(dados)
        });

        buscarAlunos();
        return;
    }

    const colunas = linha.querySelectorAll("td");

    for (let i = 1; i <= 5; i++) {
        const valor = colunas[i].textContent;
        colunas[i].innerHTML = `<input type="text" value="${valor}">`;
    }

    botao.textContent = "Salvar";
}

async function excluirAluno(id) {

    if (!confirm("Tem certeza que deseja excluir este aluno?")) return;

    await fetch(`http://127.0.0.1:5000/alunos/${id}`, {
        method: "DELETE"
    });

    buscarAlunos();
}

// ######## ADICIONAR #######

function adicionarAluno() {

    const tabela = document.querySelector("#tabelaAlunos tbody");

    const novaLinha = document.createElement("tr");

    novaLinha.innerHTML = `
        <td></td>
        <td><input type="text" placeholder="Nome"></td>
        <td><input type="number" step="0.1" value="0"></td>
        <td><input type="number" step="0.1" value="0"></td>
        <td><input type="number" step="0.1" value="0"></td>
        <td><input type="number" step="0.1" value="0"></td>
        <td><input type="number" step="0.1" value="0"></td>
        <td>
            <button onclick="salvarNovoAluno(this)">Salvar</button>
            <button onclick="this.closest('tr').remove()">Cancelar</button>
        </td>
    `;

    tabela.prepend(novaLinha);
}

async function salvarNovoAluno(botao) {

    const linha = botao.closest("tr");
    const inputs = linha.querySelectorAll("input");

    const nome = inputs[0].value;
    const nota1 = parseFloat(inputs[1].value);
    const nota2 = parseFloat(inputs[2].value);
    const nota3 = parseFloat(inputs[3].value);
    const nota4 = parseFloat(inputs[4].value);
    const nota_final = parseFloat(inputs[5].value);

    if (
        !nome ||
        isNaN(nota1) ||
        isNaN(nota2) ||
        isNaN(nota3) ||
        isNaN(nota4) ||
        isNaN(nota_final)
    ) {
        alert("Preencha todos os campos corretamente!");
        return;
    }

    const response = await fetch("http://127.0.0.1:5000/alunos", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            nome: nome,
            nota1: nota1,
            nota2: nota2,
            nota3: nota3,
            nota4: nota4,
            nota_final: nota_final,
            turma_id: parseInt(turmaId)
        })
    });

    if (response.ok) {
        buscarAlunos();
    } else {
        alert("Erro ao salvar aluno.");
    }
}
