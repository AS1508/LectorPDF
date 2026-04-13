import concurrent.futures
import time
import httpx
import io

URL = "http://localhost:8000/upload"

def send_request(worker_id):
    # Generar un archvo PDF "Fake" de ~8MB en memoria (simulando un libro gordo en RAM)
    file_content = b"%PDF-1.4\n" + (b"A" * (8 * 1024 * 1024))
    
    # httpx expects files as a dictionary where the value is a tuple of (filename, bytes_stream, mimetype)
    # wait httpx actually uses a different API sometimes, but tuple is safe: {"file": ("name", bytes, "type")}
    files = {"file": (f"libro_pesado_{worker_id}.pdf", io.BytesIO(file_content), "application/pdf")}
    data = {"lang": "es"}
    
    print(f"[Worker {worker_id}] Disparando carga de 8MB al Docker...")
    start_time = time.time()
    try:
        response = httpx.post(URL, files=files, data=data, timeout=60.0)
        elapsed = time.time() - start_time
        return worker_id, response.status_code, elapsed, response.json().get('detail', 'OK')
    except Exception as e:
        elapsed = time.time() - start_time
        return worker_id, 500, elapsed, str(e)

def run_stress_test(num_workers=10):
    print(f"=== INICIANDO ESTRÉS ({num_workers} Ataques Simultáneos) ===")
    start_global = time.time()
    results = []
    
    # Abrimos 10 compuertas a la vez usando hilos concurrentes
    with concurrent.futures.ThreadPoolExecutor(max_workers=num_workers) as executor:
        futures = {executor.submit(send_request, i): i for i in range(num_workers)}
        for future in concurrent.futures.as_completed(futures):
            results.append(future.result())
            
    print(f"\n--- REPORTE FINAL ({time.time() - start_global:.2f}s totales) ---")
    errores = 0
    for r in results:
        print(f"Worker {r[0]}: HTTP {r[1]} - Tiempo: {r[2]:.2f}s -> {r[3][:30]}")
        if r[1] != 200: errores += 1
        
    print(f"=====================================")
    print(f">= Tasa de Éxito API: {(10 - errores) * 10}%")
    print(f"=====================================")

if __name__ == "__main__":
    run_stress_test(10)
