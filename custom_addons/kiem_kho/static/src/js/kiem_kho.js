// JavaScript cho giao diện Kiểm Kho

let sessionId;
let items = [];

// DOM elements
let barcodeInput;
let scanButton;
let itemsGrid;
let itemsContainer;
let emptyState;
let itemCount;
let confirmButton;
let toast;

function initializeScanner() {
    // Lấy DOM elements
    barcodeInput = document.getElementById('barcodeInput');
    scanButton = document.getElementById('scanButton');
    itemsGrid = document.getElementById('itemsGrid');
    itemsContainer = document.getElementById('itemsContainer');
    emptyState = document.getElementById('emptyState');
    itemCount = document.getElementById('itemCount');
    confirmButton = document.getElementById('confirmButton');
    toast = document.getElementById('toast');

    // Lấy sessionId từ global variable
    sessionId = window.sessionId;

    // Event listeners
    if (scanButton) {
        scanButton.addEventListener('click', addItem);
    }
    
    if (barcodeInput) {
        barcodeInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                addItem();
            }
        });
        barcodeInput.focus();
    }

    if (confirmButton) {
        confirmButton.addEventListener('click', confirmItems);
    }

    // Load initial data
    loadSessionData();

    // Auto refresh every 30 seconds
    setInterval(loadSessionData, 30000);
}

function addItem() {
    const barcode = barcodeInput.value.trim();
    
    if (!barcode) {
        showToast('Vui lòng nhập mã vạch', 'warning');
        return;
    }

    // Call API to add item
    fetch('/kiem_kho/add_item', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            jsonrpc: '2.0',
            method: 'call',
            params: {
                session_id: sessionId,
                barcode: barcode
            }
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.result && data.result.success) {
            showToast(data.result.message, 'success');
            barcodeInput.value = '';
            barcodeInput.focus();
            loadSessionData(); // Refresh data
        } else {
            showToast(data.result ? data.result.message : 'Có lỗi xảy ra', 'error');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        showToast('Lỗi kết nối', 'error');
    });
}

function removeItem(lineId) {
    if (!confirm('Bạn có chắc muốn xóa sản phẩm này?')) {
        return;
    }

    fetch('/kiem_kho/remove_item', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            jsonrpc: '2.0',
            method: 'call',
            params: {
                line_id: lineId
            }
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.result && data.result.success) {
            showToast(data.result.message, 'info');
            loadSessionData(); // Refresh data
        } else {
            showToast(data.result ? data.result.message : 'Có lỗi xảy ra', 'error');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        showToast('Lỗi kết nối', 'error');
    });
}

function loadSessionData() {
    fetch('/kiem_kho/get_session_data', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            jsonrpc: '2.0',
            method: 'call',
            params: {
                session_id: sessionId
            }
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.result && data.result.success) {
            items = data.result.lines;
            renderItems();
            updateUI();
        }
    })
    .catch(error => {
        console.error('Error loading session data:', error);
    });
}

function renderItems() {
    if (!itemsGrid || !emptyState) return;

    if (items.length === 0) {
        itemsGrid.style.display = 'none';
        emptyState.style.display = 'flex';
        return;
    }

    itemsGrid.style.display = 'grid';
    emptyState.style.display = 'none';

    itemsGrid.innerHTML = items.map(item => `
        <div class="item-card" data-id="${item.id}">
            <button class="remove-btn" onclick="removeItem(${item.id})">×</button>
            <div class="barcode-text">${item.barcode}</div>
            <div class="product-name">${item.product_name}</div>
            <div class="item-time">${item.scan_time}</div>
        </div>
    `).join('');
}

function updateUI() {
    if (itemCount) {
        itemCount.textContent = items.length;
    }
    
    if (confirmButton) {
        confirmButton.disabled = items.length === 0;
    }
}

function confirmItems() {
    if (items.length === 0) {
        showToast('Không có sản phẩm để xử lý', 'warning');
        return;
    }

    if (!confirm(`Xác nhận hoàn thành kiểm kho với ${items.length} sản phẩm?`)) {
        return;
    }

    showToast(`Đang xử lý ${items.length} sản phẩm...`, 'info');
    
    // Redirect back to Odoo after 2 seconds
    setTimeout(() => {
        window.location.href = `/web#id=${sessionId}&action=kiem_kho.action_kiem_kho_session&model=kiem.kho.session&view_type=form`;
    }, 2000);
}

function showToast(message, type = 'info') {
    if (!toast) return;

    toast.textContent = message;
    toast.className = 'toast show';
    
    // Add type-specific styling
    if (type === 'success') {
        toast.style.backgroundColor = '#2ecc71';
    } else if (type === 'warning') {
        toast.style.backgroundColor = '#f39c12';
    } else if (type === 'error') {
        toast.style.backgroundColor = '#e74c3c';
    } else {
        toast.style.backgroundColor = '#2c3e50';
    }

    setTimeout(() => {
        toast.classList.remove('show');
    }, 3000);
}

// Keyboard shortcuts
document.addEventListener('keydown', (e) => {
    // Ctrl+D for demo barcode
    if (e.ctrlKey && e.key === 'd') {
        e.preventDefault();
        const demoBarcodes = [
            'SKU123456789',
            'PROD987654321',
            'ITEM456789123',
            'WARE789123456',
            'INV321654987'
        ];
        const randomBarcode = demoBarcodes[Math.floor(Math.random() * demoBarcodes.length)];
        if (barcodeInput) {
            barcodeInput.value = randomBarcode;
            addItem();
        }
    }
    
    // F2 to focus barcode input
    if (e.key === 'F2') {
        e.preventDefault();
        if (barcodeInput) {
            barcodeInput.focus();
            barcodeInput.select();
        }
    }
});

// Make functions global
window.removeItem = removeItem;
window.initializeScanner = initializeScanner;
