const output = document.getElementById('output');
const messageBox = document.getElementById('message');

function showMessage(text, isError = false) {
  messageBox.textContent = text;
  messageBox.style.display = 'block';
  messageBox.style.background = isError ? '#fee2e2' : '#e0f2fe';
  messageBox.style.color = isError ? '#991b1b' : '#0f172a';
}

function renderJson(data) {
  output.textContent = JSON.stringify(data, null, 2);
}

async function apiFetch(url, options = {}) {
  const response = await fetch(url, {
    headers: { 'Content-Type': 'application/json' },
    ...options,
  });

  const payload = await response.json().catch(() => ({}));

  if (!response.ok) {
    throw new Error(payload.detail || 'Erro na operação');
  }

  return payload;
}

async function createClient(event) {
  event.preventDefault();
  const form = event.currentTarget;
  const payload = Object.fromEntries(new FormData(form).entries());
  payload.id = Number(payload.id);
  try {
    const result = await apiFetch('/clientes', {
      method: 'POST',
      body: JSON.stringify(payload),
    });
    renderJson(result);
    showMessage('Cliente cadastrado com sucesso!');
    form.reset();
  } catch (error) {
    showMessage(error.message, true);
  }
}

async function createVehicle(event) {
  event.preventDefault();
  const form = event.currentTarget;
  const payload = Object.fromEntries(new FormData(form).entries());
  payload.id = Number(payload.id);
  payload.ano = Number(payload.ano);
  payload.cliente_id = Number(payload.cliente_id);
  try {
    const result = await apiFetch('/veiculos', {
      method: 'POST',
      body: JSON.stringify(payload),
    });
    renderJson(result);
    showMessage('Veículo cadastrado com sucesso!');
    form.reset();
  } catch (error) {
    showMessage(error.message, true);
  }
}

async function createService(event) {
  event.preventDefault();
  const form = event.currentTarget;
  const payload = Object.fromEntries(new FormData(form).entries());
  payload.id = Number(payload.id);
  payload.valor = Number(payload.valor);
  try {
    const result = await apiFetch('/servicos', {
      method: 'POST',
      body: JSON.stringify(payload),
    });
    renderJson(result);
    showMessage('Serviço cadastrado com sucesso!');
    form.reset();
  } catch (error) {
    showMessage(error.message, true);
  }
}

async function createPart(event) {
  event.preventDefault();
  const form = event.currentTarget;
  const payload = Object.fromEntries(new FormData(form).entries());
  payload.id = Number(payload.id);
  payload.valor = Number(payload.valor);
  payload.quantidade_estoque = Number(payload.quantidade_estoque);
  try {
    const result = await apiFetch('/pecas', {
      method: 'POST',
      body: JSON.stringify(payload),
    });
    renderJson(result);
    showMessage('Peça cadastrada com sucesso!');
    form.reset();
  } catch (error) {
    showMessage(error.message, true);
  }
}

async function createEmployee(event) {
  event.preventDefault();
  const form = event.currentTarget;
  const payload = Object.fromEntries(new FormData(form).entries());
  payload.id = Number(payload.id);
  try {
    const result = await apiFetch('/funcionarios', {
      method: 'POST',
      body: JSON.stringify(payload),
    });
    renderJson(result);
    showMessage('Funcionário cadastrado com sucesso!');
    form.reset();
  } catch (error) {
    showMessage(error.message, true);
  }
}

async function createOrder(event) {
  event.preventDefault();
  const form = event.currentTarget;
  const payload = Object.fromEntries(new FormData(form).entries());
  payload.id = Number(payload.id);
  payload.cliente_id = Number(payload.cliente_id);
  payload.veiculo_id = Number(payload.veiculo_id);
  try {
    const result = await apiFetch('/ordens', {
      method: 'POST',
      body: JSON.stringify(payload),
    });
    renderJson(result);
    showMessage('Ordem criada com sucesso!');
    form.reset();
  } catch (error) {
    showMessage(error.message, true);
  }
}

async function listClients() {
  try {
    const data = await apiFetch('/clientes');
    renderJson(data);
    showMessage('Clientes carregados.');
  } catch (error) {
    showMessage(error.message, true);
  }
}

async function listVehicles() {
  try {
    const data = await apiFetch('/veiculos');
    renderJson(data);
    showMessage('Veículos carregados.');
  } catch (error) {
    showMessage(error.message, true);
  }
}

async function listServices() {
  try {
    const data = await apiFetch('/servicos');
    renderJson(data);
    showMessage('Serviços carregados.');
  } catch (error) {
    showMessage(error.message, true);
  }
}

async function listParts() {
  try {
    const data = await apiFetch('/pecas');
    renderJson(data);
    showMessage('Peças carregadas.');
  } catch (error) {
    showMessage(error.message, true);
  }
}

async function listEmployees() {
  try {
    const data = await apiFetch('/funcionarios');
    renderJson(data);
    showMessage('Funcionários carregados.');
  } catch (error) {
    showMessage(error.message, true);
  }
}

async function listOrders() {
  try {
    const data = await apiFetch('/ordens');
    renderJson(data);
    showMessage('Ordens carregadas.');
  } catch (error) {
    showMessage(error.message, true);
  }
}

document.getElementById('clienteForm').addEventListener('submit', createClient);
document.getElementById('veiculoForm').addEventListener('submit', createVehicle);
document.getElementById('servicoForm').addEventListener('submit', createService);
document.getElementById('pecaForm').addEventListener('submit', createPart);
document.getElementById('funcionarioForm').addEventListener('submit', createEmployee);
document.getElementById('ordemForm').addEventListener('submit', createOrder);

document.getElementById('listarClientesBtn').addEventListener('click', listClients);
document.getElementById('listarVeiculosBtn').addEventListener('click', listVehicles);
document.getElementById('listarServicosBtn').addEventListener('click', listServices);
document.getElementById('listarPecasBtn').addEventListener('click', listParts);
document.getElementById('listarFuncionariosBtn').addEventListener('click', listEmployees);
document.getElementById('listarOrdensBtn').addEventListener('click', listOrders);
