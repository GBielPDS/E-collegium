document.addEventListener("DOMContentLoaded", () => {
    buscarTurmas();
});

async function buscarTurmas() {
    const professorId = localStorage.getItem("usuario_id");

    if (!professorId) {
        alert("Usuário não logado!");
        window.location.href = "login.html";
        return;
    }

    if (!professorId) {
        alert("Digite um ID válido!");
        return;
    }

    const response = await fetch(`http://127.0.0.1:5000/usuarios/${professorId}/turmas`);

    if (!response.ok) {
        alert("Professor não encontrado ou sem turmas.");
        return;
    }

    const turmas = await response.json();

    const tbody = document.querySelector("#tabelaTurmas tbody");
    tbody.innerHTML = "";

    turmas.forEach(turma => {
        const row = `
            <tr class="linha-turma" data-id="${turma.id}">
                <td>${turma.id}</td>
                <td>${turma.nome}</td>
                <td>${turma.escola}</td>
                <td>${turma.nota_aprovacao}</td>
                <td>${turma.nota_recuperacao}</td>
                <td>${turma.nota_reprovacao}</td>

                <td>
                    <button class="btn btn-warning btn-sm me-2"
                        onclick="editarTurma(${turma.id}, event)">
                        Editar
                    </button>

                    <button class="btn btn-danger btn-sm"
                    onclick="excluirTurma(${turma.id})">
                    Excluir
                </button>
                </td>
            </tr>
        `;
        tbody.innerHTML += row;
    });
    document.querySelectorAll(".linha-turma").forEach(linha => {

        linha.addEventListener("click", function (e) {

            if (e.target.tagName === "BUTTON" || e.target.tagName === "INPUT") {
                return;
            }

            const turmaId = this.getAttribute("data-id");
            irParaAlunos(turmaId);
        });

    });
}

//########  EDITAR  ########
async function editarTurma(id, event) {

    event.stopPropagation();

    const linha = event.target.closest("tr");
    const botao = event.target;

    // Se já estiver em modo salvar
    if (botao.textContent.trim() === "Salvar") {

        const inputs = linha.querySelectorAll("input");

        const dadosAtualizados = {
            nome: inputs[0].value,
            escola: inputs[1].value,
            nota_aprovacao: parseFloat(inputs[2].value),
            nota_recuperacao: parseFloat(inputs[3].value),
            nota_reprovacao: parseFloat(inputs[4].value)
        };

        const response = await fetch(`http://127.0.0.1:5000/turmas/${id}`, {
            method: "PUT",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(dadosAtualizados)
        });

        if (response.ok) {
            buscarTurmas();
        } else {
            alert("Erro ao salvar.");
        }

        return;
    }

    const colunas = linha.querySelectorAll("td");

    for (let i = 1; i <= 5; i++) {
        const valor = colunas[i].innerText.trim();

        colunas[i].innerHTML = `
            <input type="text"
                   class="form-control form-control-sm"
                   value="${valor}">
        `;
    }

    botao.textContent = "Salvar";
}

//########  EXCLUIR  ########
async function excluirTurma(id) {

    const confirmar = confirm("Tem certeza que deseja excluir essa turma?");

    if (!confirmar) {
        return;
    }

    const response = await fetch(`http://127.0.0.1:5000/turmas/${id}`, {
        method: "DELETE"
    });

    if (response.ok) {
        alert("Turma excluída com sucesso!");
        buscarTurmas();
    } else {
        alert("Erro ao excluir.");
    }
}

function irParaAlunos(turmaId) {
    window.location.href = `alunos.html?turma=${turmaId}`;
}

// ####### ADICIONAR #######

async function adicionarTurma() {

    const tabela = document.querySelector("#tabelaTurmas tbody");

    const novaLinha = document.createElement("tr");

    novaLinha.innerHTML = `
        <td></td>
        <td><input type="text" class="form-control form-control-sm" placeholder="Nome"></td>
        <td><input type="text" class="form-control form-control-sm" placeholder="Escola"></td>
        <td><input type="number" step="0.1" class="form-control form-control-sm" placeholder="Nota aprovação"></td>
        <td><input type="number" step="0.1" class="form-control form-control-sm" placeholder="Nota recuperação"></td>
        <td><input type="number" step="0.1" class="form-control form-control-sm" placeholder="Nota reprovação"></td>
        <td>
            <button class="btn btn-success btn-sm me-2"
                onclick="event.stopPropagation(); salvarNovaTurma(this)">
                Salvar
            </button>

            <button class="btn btn-secondary btn-sm"
                onclick="event.stopPropagation(); this.closest('tr').remove()">
                Cancelar
            </button>
        </td>
    `;

    tabela.prepend(novaLinha);
}

async function salvarNovaTurma(botao) {

    const linha = botao.closest("tr");
    const inputs = linha.querySelectorAll("input");

    const professorId = localStorage.getItem("usuario_id");

    const nome = inputs[0].value;
    const escola = inputs[1].value;
    const nota_aprovacao = parseFloat(inputs[2].value);
    const nota_recuperacao = parseFloat(inputs[3].value);
    const nota_reprovacao = parseFloat(inputs[4].value);

    if (
        !professorId ||
        !nome ||
        !escola ||
        isNaN(nota_aprovacao) ||
        isNaN(nota_recuperacao) ||
        isNaN(nota_reprovacao)
    ) {
        alert("Preencha todos os campos corretamente!");
        return;
    }

    const response = await fetch("http://127.0.0.1:5000/turmas", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            nome: nome,
            escola: escola,
            nota_aprovacao: nota_aprovacao,
            nota_recuperacao: nota_recuperacao,
            nota_reprovacao: nota_reprovacao,
            professor_id: parseInt(professorId)
        })
    });

    if (response.ok) {
        buscarTurmas();
    } else {
        const erro = await response.text();
        console.log(erro);
        alert("Erro ao salvar turma.");
    }
}
