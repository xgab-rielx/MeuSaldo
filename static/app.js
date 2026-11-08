function showMessage(message) {
  const feedback = document.querySelector("#form-message");
  feedback.textContent = message;

}

async function carregarGastos() {
  let url = "/spendings";

  const categoria = document.querySelector("#filtro-category").value
  const de = document.querySelector("#start-date").value
  const ate = document.querySelector("#end-date").value

  const params = new URLSearchParams();
  if (categoria) params.set("category", categoria);
  if (de) params.set("start_date", de);
  if (ate) params.set("end_date", ate);

  const query = params.toString();
  url = query ? `/spendings?${query}` : "/spendings";

  const resposta = await fetch(url);
  const gastos = await resposta.json();

  const lista = document.querySelector("#spendings-list");

  lista.textContent = ""

  for (const gasto of gastos) {
    const item = document.createElement("li");
    const botao = document.createElement("button");
    const edit = document.createElement("button");

    botao.textContent = "Excluir"
    botao.addEventListener("click", async function deletar() {
      const apagar = await fetch(`/spendings/${gasto.spending_id}`, {
        method: "DELETE",
      });
      if (apagar.ok) {
        await carregarGastos()
      }
    })

    edit.textContent = "Editar"
    edit.addEventListener("click", async function editar() {
      const descricao = prompt("Nova descriçao:", gasto.description);
      const categoria = prompt("Nova categoria:", gasto.category);
      const valor = prompt("Novo valor:", gasto.value);

      const edicao = {
        "description": descricao,
        "category": categoria,
        "value": valor
      };

      const att = await fetch(`/spendings/${gasto.spending_id}`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(edicao)
      });

      if (att.ok) {
        await carregarGastos()
      }

      console.log(att.status);
    })

    item.textContent = `Descrição: ${gasto.description}\nCategoria: ${gasto.category}\nGasto: ${gasto.value}\nData: ${gasto.date}`;

    item.appendChild(edit);
    item.appendChild(botao);
    lista.appendChild(item);
  }
}

carregarGastos();

const categoria = document.querySelector("#filtro-category");
categoria.addEventListener("input", function filtrar() {
  carregarGastos();
});

const de = document.querySelector("#start-date");
de.addEventListener("input", function filtrar() {
  carregarGastos();
});

const ate = document.querySelector("#end-date");
ate.addEventListener("input", function filtrar() {
  carregarGastos();
});

const formulario = document.querySelector("#spending-form");

formulario.addEventListener("submit", async function (cadastro) {
  cadastro.preventDefault();
  const descricao = document.querySelector("#description").value;
  const categoria = document.querySelector("#category").value;
  const valor = document.querySelector("#value").value;
  const data = document.querySelector("#date").value;

  const gasto = {
    "description": descricao,
    "category": categoria,
    "value": valor,
    "date": data
  };

  const resposta = await fetch("/spendings", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(gasto)
  });
  if (resposta.ok) {
    await carregarGastos();

    formulario.reset();

    showMessage(
      "Gasto cadastrado com sucesso!"
    );
  } else {
    showMessage(
      "Falha ao tentar cadastrar Gasto"
    )
  }

  console.log(resposta.status);
});


async function totalMensal() {
  const d = new Date();
  const ano = d.getFullYear();
  const mes = d.getMonth() + 1;

  const resposta = await fetch(`/spendings/monthly_total?year=${ano}&month=${mes}`);

  const gasto_mes = await resposta.json();

  const total = document.querySelector("#monthly-total")
  total.textContent = `Total de ${mes} de ${ano} | Gasto: R$ ${gasto_mes.total}`

  console.log(gasto_mes);
}
totalMensal()