const apiUrl = "http://localhost:5000";

async function listarProdutos() {
    const resposta = await fetch(`${apiUrl}/produtos`);
    const dados = await resposta.json();
    return dados;
}

async function cadastrarProduto(nome) {
    const resposta = await fetch(`${apiUrl}/produtos`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ nome })
    });
    return await resposta.json();
}

async function ativarProduto(nome) {
    const resposta = await fetch(`${apiUrl}/produtos/${nome}/ativar`, {
        method: "PUT"
    });
    return await resposta.json();
}

async function desativarProduto(nome) {
    const resposta = await fetch(`${apiUrl}/produtos/${nome}/desativar`, {
        method: "PUT"
    });
    return await resposta.json();
}

async function removerProduto(nome) {
    const resposta = await fetch(`${apiUrl}/produtos/${nome}`, {
        method: "DELETE"
    });
    return await resposta.json();
}

async function emitirNotaFiscal(produto, cliente, email_destino) {
    const resposta = await fetch(`${apiUrl}/nota_fiscal`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ produto, cliente, email_destino })
    });
    return await resposta.json();
}


// Esse é uma parte do código para o HTML, copia e cola no index.html logo depois de "<script src="funcoes.js"></script>"
// OBS: é pra colar SEM ESSE {/* antes do <script>
// OBS: O index.html tem que estar na mesma pasta do funcoes.js


{/* <script>
        async function addProduct() {
            const nome = document.getElementById("product-name-input").value;
            const res = await cadastrarProduto(nome);
            alert(res.message || res.error);
            loadProducts();
        }

        async function activateProduct() {
            const nome = document.getElementById("manage-product-name-input").value;
            const res = await ativarProduto(nome);
            alert(res.message || res.error);
            loadProducts();
        }

        async function deactivateProduct() {
            const nome = document.getElementById("manage-product-name-input").value;
            const res = await desativarProduto(nome);
            alert(res.message || res.error);
            loadProducts();
        }

        async function removeProduct() {
            const nome = document.getElementById("manage-product-name-input").value;
            const res = await removerProduto(nome);
            alert(res.message || res.error);
            loadProducts();
        }

        async function emitInvoice() {
            const produto = document.getElementById("invoice-product-name-input").value;
            const cliente = document.getElementById("invoice-client-name-input").value;
            const email = document.getElementById("invoice-email-input").value;

            const res = await emitirNota(produto, cliente, email);
            alert(res.message || res.error);
        }

        async function loadProducts() {
            const lista = document.getElementById("product-list");
            lista.innerHTML = "";

            const dados = await listarProdutos();

            if (dados.message) {
                lista.innerHTML = `<p class="text-gray-500">${dados.message}</p>`;
                return;
            }

            dados.forEach(p => {
                const div = document.createElement("div");
                div.className = "p-3 rounded-lg bg-white shadow flex justify-between items-center border";
                div.innerHTML = `<span>${p.nome}</span><span class="text-sm ${p.ativo ? 'text-green-600' : 'text-gray-400'}">${p.ativo ? 'Ativo' : 'Inativo'}</span>`;
                lista.appendChild(div);
            });
        }

        window.onload = loadProducts;
    </script> */}