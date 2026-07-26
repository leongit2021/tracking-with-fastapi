from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

app = FastAPI(title="Distributor Sparepart Tracking")

# Setup template engine Jinja2
templates = Jinja2Templates(directory="templates")

# Mock Data untuk Simulasi Tracking
MOCK_SHIPMENTS = {
    # Contoh Resi Import
    "IMP-100293": {
        "status": "CUSTOMS_CLEARANCE",
        "tipe": "Principal Import (Japan)",
        "part_name": "Hydraulic Pump Excavator Type EX200",
        "qty": "5 Units",
        "estimasi": "22 Juli 2026",
        "history": [
            {"tanggal": "10 Juli 2026", "lokasi": "Tanjung Priok Port", "detail": "Proses pemeriksaan Bea Cukai (Customs Clearance)"},
            {"tanggal": "05 Juli 2026", "lokasi": "Transit Hub Singapore", "detail": "Keberangkatan kapal menuju Jakarta"},
            {"tanggal": "28 Juni 2026", "lokasi": "Kobe Port, Japan", "detail": "Barang dimuat ke dalam kontainer (Loading)"}
        ]
    },
    # Contoh Resi Lokal
    "LOK-882910": {
        "status": "ON_DELIVERY",
        "tipe": "Distribusi Lokal (Domestik)",
        "part_name": "V-Belt Industrial Grade A-32",
        "qty": "100 Pcs",
        "estimasi": "12 Juli 2026",
        "history": [
            {"tanggal": "10 Juli 2026", "lokasi": "Semarang Hub", "detail": "Paket sedang dibawa oleh kurir menuju lokasi Anda"},
            {"tanggal": "09 Juli 2026", "lokasi": "Main Warehouse Jakarta", "detail": "Barang telah diserahkan ke ekspedisi lokal"}
        ]
    }
}

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    # Menampilkan halaman utama landing page
    return templates.TemplateResponse(
            {"request": request, "shipment": None, "searched": False},
            "index.html"
        )

@app.post("/", response_class=HTMLResponse)
async def track_shipment(request: Request, tracking_id: str = Form(...)):
    # Membersihkan input dari spasi
    tracking_id = tracking_id.strip()
    
    # Cari data di mock database
    shipment_data = MOCK_SHIPMENTS.get(tracking_id)
    
    return templates.TemplateResponse(
        {
            "request": request, 
            "shipment": shipment_data, 
            "tracking_id": tracking_id,
            "searched": True
        },
        "index.html"
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="69.62.73.150", port=8086, reload=True)