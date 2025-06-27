from flask import Flask, render_template_string, request, redirect, url_for, session
import qrcode
import io
import base64

app = Flask(__name__)
app.secret_key = 'rahasia-fara'

barang_list = [
    {'id': 1, 'nama': 'kemeja Putih', 'harga': 80000, 'gambar': 'static/Kemeja_Putih.jpg', 'jenis': 'pakaian', 'stok': 150},
    {'id': 2, 'nama': 'Celana Hitam', 'harga': 50000, 'gambar': 'static/Celana_Hitam.jpg', 'jenis': 'pakaian', 'stok': 150},
    {'id': 3, 'nama': 'Ikat Pinggang', 'harga': 20000, 'gambar': 'static/Ikat_Pinggang.jpg', 'jenis': 'all_size', 'stok': 150},
    {'id': 4, 'nama': 'Kerudung putih', 'harga': 25000, 'gambar': 'static/Kerudung_Putih.jpg', 'jenis': 'all_size', 'stok': 150},
    {'id': 5, 'nama': 'Sepatu Fantofel Pria', 'harga': 85000, 'gambar': 'static/Sepatu_Cowok.jpg', 'jenis': 'sepatu_pria', 'stok': 150},
    {'id': 6, 'nama': 'Hasduk Merah Putih', 'harga': 15000, 'gambar': 'static/Hasduk_Merah_Putih.jpg', 'jenis': 'all_size', 'stok': 150},
    {'id': 7, 'nama': 'Ring Rotan', 'harga': 5000, 'gambar': 'static/Ring_Rotan.jpg', 'jenis': 'all_size', 'stok': 150},
    {'id': 8, 'nama': 'Pin Garuda', 'harga': 10000, 'gambar': 'static/Pin_Garuda.jpg', 'jenis': 'all_size', 'stok': 150},
    {'id': 9, 'nama': 'Rok Hitam', 'harga': 50000, 'gambar': 'static/Rok_Hitam.jpg', 'jenis': 'pakaian', 'stok': 150},
    {'id': 10, 'nama': 'Pin Merah Putih', 'harga': 10000, 'gambar': 'static/Pin_Merah_Putih.jpg', 'jenis': 'all_size', 'stok': 150},
    {'id': 11, 'nama': 'Kaus Kaki', 'harga': 15000, 'gambar': 'static/Kaus_Kaki.jpg', 'jenis': 'all_size', 'stok': 150},
    {'id': 12, 'nama': 'Sepatu Fantofel Wanita', 'harga': 80000, 'gambar': 'static/Sepatu_Cewek.jpg', 'jenis': 'sepatu_wanita', 'stok': 150},
]

DISKON_PERSEN = 10

HTML_INDEX = '''
<!DOCTYPE html>
<html>
<head>
  <title>FaraShop</title>
  <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;600&display=swap" rel="stylesheet">
  <style>
    body {
      font-family: 'Poppins', sans-serif;
      background: linear-gradient(135deg, #f5f7fa, #c3cfe2);
      padding: 30px;
      margin: 0;
    }
    .welcome {
      background-color: #007bff;
      color: white;
      padding: 25px;
      border-radius: 15px;
      text-align: center;
      margin-bottom: 30px;
      box-shadow: 0 4px 10px rgba(0,0,0,0.1);
    }
    .produk {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
      gap: 20px;
      justify-content: center;
    }
    .item {
      background: white;
      padding: 15px;
      border-radius: 12px;
      box-shadow: 0 4px 8px rgba(0,0,0,0.1);
      text-align: center;
      transition: transform 0.2s;
    }
    .item:hover {
      transform: scale(1.05);
    }
    img {
      max-width: 100%;
      height: 150px;
      object-fit: cover;
      border-radius: 10px;
    }
    h2 {
      text-align: center;
      margin-bottom: 20px;
      color: #333;
    }
    .btn {
      margin-top: 10px;
      display: inline-block;
      padding: 8px 15px;
      background: #007bff;
      color: white;
      border-radius: 8px;
      text-decoration: none;
      font-weight: bold;
      transition: background 0.3s;
    }
    .btn:hover {
      background: #0056b3;
    }
    .btn-disabled {
      background: #cccccc;
      cursor: not-allowed;
    }
    .keranjang-link {
      display: block;
      margin: 30px auto;
      width: max-content;
      font-size: 16px;
    }
    .stok-info {
      font-size: 14px;
      color: #666;
      margin: 5px 0;
    }
    .stok-habis {
      color: #dc3545;
      font-weight: bold;
    }
  </style>
</head>
<body>
  <div class="welcome">
    <h1>Selamat Datang di mabaneed's 👋</h1>
    <p>Temukan fashion terbaik dengan harga ramah dompet 💸</p>
  </div>
  <h2>Barang Dijual 🛒</h2>
  <div class="produk">
    {% for barang in barang_list %}
      <div class="item">
        <img src="{{ barang.gambar }}">
        <h3>{{ barang.nama }}</h3>
        <p><strong>Rp{{ "{:,.0f}".format(barang.harga) }}</strong></p>
        <p class="stok-info">Stok: {{ barang.stok }}</p>
        {% if barang.stok <= 0 %}
          <p class="stok-habis">Stok habis</p>
        {% endif %}
        <a class="btn" href="{{ url_for('kurangi', id=barang.id) }}">Kurangi</a>
        <form method="POST" action="{{ url_for('tambah') }}">
          <input type="hidden" name="id" value="{{ barang.id }}">
          {% if barang.jenis == 'sepatu_pria' %}
            <select name="ukuran" required {% if barang.stok <= 0 %}disabled{% endif %}>
              <option value="">Ukuran</option>
              <option value="38">38</option>
              <option value="39">39</option>
              <option value="40">40</option>
              <option value="41">41</option>
              <option value="42">42</option>
            </select>
          {% elif barang.jenis == 'sepatu_wanita' %}
            <select name="ukuran" required {% if barang.stok <= 0 %}disabled{% endif %}>
              <option value="">Ukuran</option>
              <option value="36">36</option>
              <option value="37">37</option>
              <option value="38">38</option>
              <option value="39">39</option>
              <option value="40">40</option>
            </select>
          {% elif barang.jenis == 'all_size' %}
            <input type="hidden" name="ukuran" value="All Size">
            <span>All Size</span>
          {% else %}
            <select name="ukuran" required {% if barang.stok <= 0 %}disabled{% endif %}>
              <option value="">Ukuran</option>
              <option value="S">S</option>
              <option value="M">M</option>
              <option value="L">L</option>
              <option value="XL">XL</option>
            </select>
          {% endif %}
          <button class="btn {% if barang.stok <= 0 %}btn-disabled{% endif %}" 
                  type="submit" {% if barang.stok <= 0 %}disabled{% endif %}>
            Tambah
          </button>
        </form>
      </div>
    {% endfor %}
  </div>
  <a class="btn keranjang-link" href="{{ url_for('keranjang') }}">🧺 Lihat Keranjang</a>
</body>
</html>
'''

HTML_KERANJANG = '''
<!DOCTYPE html>
<html>
<head>
  <title>Keranjang Belanja</title>
  <style>
    body {
      font-family: 'Poppins', sans-serif;
      background-color: #f0f2f5;
      padding: 30px;
    }
    h1 {
      text-align: center;
      color: #333;
    }
    ul {
      list-style-type: none;
      padding: 0;
      max-width: 500px;
      margin: auto;
    }
    li {
      background: white;
      margin-bottom: 10px;
      padding: 15px;
      border-radius: 10px;
      box-shadow: 0 2px 6px rgba(0,0,0,0.1);
    }
    form {
      text-align: center;
      margin-top: 20px;
    }
    input[type="text"] {
      padding: 10px;
      width: 300px;
      border: 1px solid #ccc;
      border-radius: 8px;
      margin-bottom: 10px;
    }
    button {
      padding: 10px 20px;
      background-color: #28a745;
      color: white;
      border: none;
      border-radius: 8px;
      cursor: pointer;
      font-weight: bold;
    }
    button:hover {
      background-color: #218838;
    }
    a {
      display: block;
      margin-top: 30px;
      text-align: center;
      color: #007bff;
      text-decoration: none;
    }
    a:hover {
      text-decoration: underline;
    }
    .error {
      color: #dc3545;
      text-align: center;
      margin-bottom: 15px;
    }
  </style>
</head>
<body>
  <h1>Keranjang Belanja 🧺</h1>
  {% if error %}
    <p class="error">{{ error }}</p>
  {% endif %}
  {% if items %}
    <ul>
      {% for item in items %}
        <li>{{ item.nama }} x {{ item.jumlah }} = <strong>Rp{{ "{:,.0f}".format(item.subtotal) }}</strong></li>
      {% endfor %}
    </ul>
    <p style="text-align: center;">Total setelah diskon: <strong>Rp{{ "{:,.0f}".format(total) }}</strong></p>
    <form method="POST" action="{{ url_for('checkout') }}">
      <input type="hidden" name="total" value="{{ total }}">
      <input type="text" name="alamat" placeholder="Alamat pengiriman" required><br>
      <button type="submit">Checkout Sekarang 🚚</button>
    </form>
  {% else %}
    <p style="text-align:center;">Keranjang kosong 😞</p>
  {% endif %}
  <a href="{{ url_for('index') }}">← Kembali ke Belanja</a>
</body>
</html>
'''

HTML_CHECKOUT = '''
<!DOCTYPE html>
<html>
<head>
  <title>Checkout</title>
  <style>
    body {
      font-family: 'Poppins', sans-serif;
      background: #fefefe;
      padding: 40px;
      text-align: center;
    }
    h1 {
      color: #28a745;
    }
    p {
      font-size: 18px;
    }
    img {
      margin-top: 20px;
      width: 200px;
      height: 200px;
    }
    a {
      display: inline-block;
      margin-top: 30px;
      padding: 10px 15px;
      background: #007bff;
      color: white;
      text-decoration: none;
      border-radius: 8px;
    }
    a:hover {
      background: #0056b3;
    }
  </style>
</head>
<body>
  <h1>Terima Kasih Telah Berbelanja! 🛍️</h1>
  <p><strong>Total:</strong> Rp{{ "{:,.0f}".format(total) }}</p>
  <p><strong>Alamat Pengiriman:</strong> {{ alamat }}</p>
  <img src="data:image/png;base64,{{ qr }}">
  <br><a href="{{ url_for('index') }}">← Kembali ke Halaman Utama</a>
</body>
</html>
'''

def find_barang(id):
    """Helper function to find a product by ID"""
    for barang in barang_list:
        if barang['id'] == id:
            return barang
    return None

@app.route('/')
def index():
    return render_template_string(HTML_INDEX, barang_list=barang_list)

@app.route('/tambah', methods=['POST'])
def tambah():
    id = int(request.form['id'])
    ukuran = request.form.get('ukuran', 'All Size')

    barang = find_barang(id)
    if not barang or barang['stok'] <= 0:
        return redirect(url_for('index'))

    keranjang = session.get('keranjang', {})
    key = f"{id}_{ukuran}" if ukuran != 'All Size' else str(id)
    
    # Hitung jumlah yang sudah ada di keranjang
    jumlah_di_keranjang = keranjang.get(key, 0)
    
    # Periksa apakah stok mencukupi
    if jumlah_di_keranjang >= barang['stok']:
        return redirect(url_for('index'))
    
    keranjang[key] = jumlah_di_keranjang + 1
    session['keranjang'] = keranjang
    return redirect(url_for('index'))

@app.route('/kurangi/<int:id>')
def kurangi(id):
    keranjang = session.get('keranjang', {})
    # Cari semua item di keranjang yang sesuai dengan ID
    keys_to_update = [k for k in keranjang.keys() if k.startswith(f"{id}_") or k == str(id)]
    
    for key in keys_to_update:
        keranjang[key] -= 1
        if keranjang[key] <= 0:
            del keranjang[key]
    
    session['keranjang'] = keranjang
    return redirect(url_for('index'))

@app.route('/keranjang')
def keranjang():
    keranjang = session.get('keranjang', {})
    item_keranjang = []
    total = 0
    error = None

    for key, jumlah in keranjang.items():
        if '_' in key:
            id, ukuran = key.split('_')
        else:
            id = key
            ukuran = 'All Size'
        
        barang = find_barang(int(id))
        if barang:
            # Validasi stok
            if jumlah > barang['stok']:
                error = f"Stok {barang['nama']} tidak mencukupi"
                jumlah = barang['stok']
                keranjang[key] = jumlah
            
            subtotal = barang['harga'] * jumlah
            total += subtotal
            
            # Format tampilan ukuran
            if barang['jenis'] == 'all_size':
                display_size = ''
            else:
                display_size = f" (Ukuran {ukuran})"
            
            item_keranjang.append({
                'nama': f"{barang['nama']}{display_size}",
                'harga': barang['harga'],
                'jumlah': jumlah,
                'subtotal': subtotal
            })

    if total > 0:
        diskon = total * DISKON_PERSEN // 100
        total -= diskon
    else:
        diskon = 0

    session['keranjang'] = keranjang
    return render_template_string(HTML_KERANJANG, items=item_keranjang, total=total, error=error)

@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    if request.method == 'POST':
        # Validasi stok sebelum checkout
        keranjang = session.get('keranjang', {})
        for key, jumlah in keranjang.items():
            if '_' in key:
                id = int(key.split('_')[0])
            else:
                id = int(key)
            
            barang = find_barang(id)
            if not barang or jumlah > barang['stok']:
                return redirect(url_for('keranjang'))
        
        # Kurangi stok
        for key, jumlah in keranjang.items():
            if '_' in key:
                id = int(key.split('_')[0])
            else:
                id = int(key)
            
            barang = find_barang(id)
            if barang:
                barang['stok'] -= jumlah

        alamat = request.form['alamat']
        total = int(request.form['total'])

        qr = qrcode.make(f'Transfer Rp{total} ke 1234567890\nAlamat: {alamat}')
        buffer = io.BytesIO()
        qr.save(buffer, format="PNG")
        img_b64 = base64.b64encode(buffer.getvalue()).decode()

        session.pop('keranjang', None)
        return render_template_string(HTML_CHECKOUT, qr=img_b64, total=total, alamat=alamat)

    return redirect(url_for('keranjang'))

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)