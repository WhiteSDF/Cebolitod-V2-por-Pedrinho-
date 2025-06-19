function mostrarToast(mensagem, tipo = "success") {
    const toast = document.getElementById("toast");
    const msg = document.getElementById("toast-msg");
    toast.className = "toast show " + tipo;
    msg.innerText = mensagem;
    setTimeout(() => {
        toast.className = "toast " + tipo;
    }, 3200);
}

function fazerTarefas() {
    const ra = document.getElementById("ra").value;
    const digito = document.getElementById("digito").value;
    const senha = document.getElementById("senha").value;

    if (!ra || !digito || !senha) {
        mostrarToast("Preencha todos os campos!", "warning");
        return;
    }

    const raCompleto = ra + digito;

    fetch("http://localhost:8000/fazer-tarefas", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ ra: raCompleto, senha })
    })
    .then(res => res.json())
    .then(data => {
        if (data.status === "ok") {
            const lista = data.feitas || [];
            if (lista.length > 0) {
                let i = 0;
                const mostrarLicao = () => {
                    if (i < lista.length) {
                        mostrarToast("Fazendo: " + lista[i]);
                        i++;
                        setTimeout(mostrarLicao, 3500);
                    } else {
                        mostrarToast("Todas as lições foram feitas!", "success");
                    }
                };
                mostrarLicao();
            }
        } else if (data.status === "sem_tarefas") {
            mostrarToast("Nenhuma tarefa SP encontrada!", "warning");
        } else {
            mostrarToast("Erro ao fazer login!", "error");
        }
    })
    .catch(() => {
        mostrarToast("Erro ao conectar ao servidor!", "error");
    });
}