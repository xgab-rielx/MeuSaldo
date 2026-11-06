async function carregarGastos() {
    const resposta = await fetch("/spendings");
    const gastos = await resposta.json();
    
    const lista = document.querySelector("#spendings-list");

    lista.textContent = ""
    
    for (const gasto of gastos) {
        const item = document.createElement("li");
        item.textContent = `Descrição: ${gasto.description}\nCategoria: ${gasto.category}\nGasto: ${gasto.value}\nData: ${gasto.date}`;

        lista.appendChild(item);
    }
}

carregarGastos();

const formulario = document.querySelector("#spending-form");

formulario.addEventListener("submit", async function(cadastro) {
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
    await carregarGastos()
  }

  console.log(resposta.status);
});