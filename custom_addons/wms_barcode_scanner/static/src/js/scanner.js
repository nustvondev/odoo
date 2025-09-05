(function () {
  // State
  let items = [];
  let itemIdCounter = 0;

  // DOM
  function $(id) { return document.getElementById(id); }
  function initDom() {
    return {
      barcodeInput: $('barcodeInput'),
      scanButton: $('scanButton'),
      itemsGrid: $('itemsGrid'),
      itemsContainer: $('itemsContainer'),
      emptyState: $('emptyState'),
      itemCount: $('itemCount'),
      confirmButton: $('confirmButton'),
      toast: $('toast'),
    };
  }

  function mount() {
    const d = initDom();
    if (!d.barcodeInput) return; // chưa render xong

    d.scanButton.addEventListener('click', addItem);
    d.barcodeInput.addEventListener('keypress', (e) => {
      if (e.key === 'Enter') addItem();
    });
    d.confirmButton.addEventListener('click', confirmItems);

    document.addEventListener('keydown', (e) => {
      if (e.ctrlKey && e.key === 'd') {
        e.preventDefault();
        const demoBarcodes = ['SKU123456789','PROD987654321','ITEM456789123','WARE789123456','INV321654987'];
        d.barcodeInput.value = demoBarcodes[Math.floor(Math.random() * demoBarcodes.length)];
        addItem();
      }
    });

    updateUI();
    d.barcodeInput.focus();
  }

  function addItem() {
    const d = initDom();
    const barcode = d.barcodeInput.value.trim();
    if (!barcode) return showToast('Please enter a barcode', 'warning');
    if (items.some((it) => it.barcode === barcode)) return showToast('This barcode already exists in the list', 'warning');

    items.push({ id: ++itemIdCounter, barcode, timestamp: new Date() });
    renderItems();
    updateUI();
    d.barcodeInput.value = '';
    d.barcodeInput.focus();
    showToast('Item added successfully', 'success');
  }

  function removeItem(id) {
    items = items.filter((it) => it.id !== id);
    renderItems();
    updateUI();
    showToast('Item removed', 'info');
  }
  window.removeItem = removeItem; // để dùng trong onclick của template

  function renderItems() {
    const d = initDom();
    if (items.length === 0) {
      d.itemsGrid.style.display = 'none';
      d.emptyState.style.display = 'flex';
      d.itemsGrid.innerHTML = '';
      return;
    }
    d.itemsGrid.style.display = 'grid';
    d.emptyState.style.display = 'none';
    d.itemsGrid.innerHTML = items.map((item) => `
      <div class="item-card" data-id="${item.id}">
        <button class="remove-btn" onclick="removeItem(${item.id})">×</button>
        <div class="barcode-text">${item.barcode}</div>
        <div class="item-time">${formatTime(item.timestamp)}</div>
      </div>
    `).join('');
  }

  function updateUI() {
    const d = initDom();
    d.itemCount.textContent = items.length;
    d.confirmButton.disabled = items.length === 0;
  }

  function formatTime(date) {
    return date.toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit', second: '2-digit' });
  }

  function confirmItems() {
    const d = initDom();
    if (items.length === 0) return;
    showToast(`Processing ${items.length} items...`, 'success');
    setTimeout(() => {
      items = [];
      renderItems();
      updateUI();
      showToast('All items processed successfully!', 'success');
    }, 1500);
  }

  function showToast(message, type = 'info') {
    const d = initDom();
    const toast = d.toast;
    toast.textContent = message;
    toast.className = 'toast show';
    toast.style.backgroundColor = (type === 'success') ? '#2ecc71' : (type === 'warning') ? '#f39c12' : (type === 'error') ? '#e74c3c' : '#2c3e50';
    setTimeout(() => toast.classList.remove('show'), 3000);
  }

  // Mount khi DOM sẵn sàng
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', mount);
  } else {
    mount();
  }
})();