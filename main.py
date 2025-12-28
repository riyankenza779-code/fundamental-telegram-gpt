response = client.responses.create(
    model="gpt-4.1-mini",
    input="""
Buat analisa fundamental XAUUSD hari ini secara ringkas dan profesional (maksimal 4 poin).

WAJIB mencakup:
1. Kondisi USD dan arah kebijakan Federal Reserve terbaru
2. Inflasi AS dan ekspektasi suku bunga
3. Geopolitik global sebagai faktor safe haven
4. Jika sedang mendekati, berlangsung, atau baru selesai FOMC:
   - Sikap pasar (risk-on / risk-off / wait and see)
   - Potensi dampak keputusan FOMC ke XAUUSD
   - Bias XAUUSD (Bullish / Bearish / Netral)

Catatan penting:
- Update otomatis, tidak terikat tanggal tertentu
- Gunakan bahasa Indonesia
- Ringkas, objektif, tanpa rekomendasi entry
"""
)
