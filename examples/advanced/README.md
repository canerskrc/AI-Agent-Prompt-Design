# İleri Düzey Örnekler — Agent Pipeline'ları

Bu örnekler çalışan kod içeriyor. Python bilgisi gerekiyor.  
Kod yazmıyorsanız: Akışı anlayın, ne yaptığını görün. Teknik uygulama için ekibinizdeki geliştiriciye referans verin.

---

## Örnek 13 — Belge Analiz Pipeline'ı

**Senaryo:** 50 sayfalık ihale belgesi → Kritik maddeler özeti + risk analizi

**Neden agent değil zincir?** Akış sabittir. Her belge için aynı adımlar. Dinamik karar verme gerekmiyor.

```python
"""
Belge Analiz Pipeline'ı
Araçlar: LangChain, OpenAI, PyPDF2
Kullanım: python doc_pipeline.py --file ihale.pdf --output ozet.md
"""

import os
from pathlib import Path
from langchain_openai import ChatOpenAI
from langchain.text_splitter import RecursiveCharacterTextSplitter
import PyPDF2

# --- Konfigürasyon ---
LLM = ChatOpenAI(model="gpt-4o", temperature=0)
CHUNK_SIZE = 3000
CHUNK_OVERLAP = 200


def extract_text(pdf_path: str) -> str:
    """PDF'den metin çıkar."""
    with open(pdf_path, "rb") as f:
        reader = PyPDF2.PdfReader(f)
        return "\n".join(
            page.extract_text() for page in reader.pages
        )


def chunk_document(text: str) -> list[str]:
    """Büyük belgeyi işlenebilir parçalara böl."""
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        separators=["\n\n", "\n", ".", " "]
    )
    return splitter.split_text(text)


def extract_key_clauses(chunks: list[str]) -> list[str]:
    """
    Adım 1: Her chunk'tan kritik maddeleri çıkar.
    Bu adım paralel çalışabilir — büyük belgeler için önemli.
    """
    extraction_prompt = """
Rol: Sözleşme analisti

Görev: Aşağıdaki metin bölümünden şunları çıkar:
1. Finansal yükümlülükler (rakamlar, vadeler)
2. Cezai şartlar
3. Teslim tarihleri ve kilometre taşları
4. Tarafların hakları ve sorumlulukları
5. Fesih koşulları

Kısıt:
- Sadece belgede gerçekten olanı yaz
- Bulunmayan kategoriler için "Bu bölümde yok" de
- Her madde için sayfa/bölüm referansı ver (varsa)

Format: Madde madde, kategori başlıkları altında

Metin:
{chunk}
"""
    results = []
    for i, chunk in enumerate(chunks):
        print(f"Chunk {i+1}/{len(chunks)} işleniyor...")
        response = LLM.invoke(
            extraction_prompt.format(chunk=chunk)
        )
        results.append(response.content)
    return results


def synthesize_findings(clause_lists: list[str]) -> str:
    """
    Adım 2: Parçalardan gelen bulgular birleştiriliyor.
    Tekrarlar temizleniyor, çelişkiler işaretleniyor.
    """
    synthesis_prompt = """
Rol: Kıdemli hukuki danışman

Bağlam: Aşağıdaki bulgular büyük bir belgenin farklı bölümlerinden 
        çıkarıldı. Tekrarlar ve tutarsızlıklar olabilir.

Görev: Bu bulguları konsolide et:
1. Tekrar eden bilgileri birleştir
2. Çelişkili bilgileri işaretle: [ÇAKIŞAN: ...]
3. Belge genelinde kritik bağımlılıkları tespit et

Çıktı: Temizlenmiş, konsolide bulgu listesi

Bulgular:
{findings}
"""
    combined = "\n\n---\n\n".join(clause_lists)
    response = LLM.invoke(
        synthesis_prompt.format(findings=combined)
    )
    return response.content


def risk_assessment(consolidated: str) -> str:
    """
    Adım 3: Risk değerlendirmesi.
    Bulgulardan değil, bulgular + iş perspektifinden.
    """
    risk_prompt = """
Rol: İş riski değerlendirme uzmanısın. 
     Hukuki değil, operasyonel perspektiften bakıyorsun.

Bağlam: Aşağıdaki sözleşme maddeleri analiz edildi.

Görev: Risk değerlendirmesi yap:

Her risk için:
- Açıklama: Ne riski bu?
- Tetikleyici: Ne olursa bu risk gerçekleşir?
- Etki: Mali veya operasyonel sonucu ne?
- Seviye: KRİTİK / YÜKSEK / ORTA / DÜŞÜK
- Önlem: Ne yapılabilir?

Kısıt:
- En fazla 10 risk listele
- Teorik değil, bu belgede gerçekten görülen riskleri yaz
- "Hukuki danışmana danışın" genel tavsiyesini verme

Format: Sıralı liste, seviyeye göre yüksekten düşüğe

Maddeler:
{consolidated}
"""
    response = LLM.invoke(
        risk_prompt.format(consolidated=consolidated)
    )
    return response.content


def generate_executive_summary(consolidated: str, risks: str) -> str:
    """
    Adım 4: Yönetici özeti. C-suite için.
    """
    summary_prompt = """
Rol: Yönetici asistanı — özetleme ve önceliklendirme konusunda uzmansın.

Bağlam: Bir sözleşme analizi tamamlandı. Bulgular ve riskler hazır.

Görev: CEO için 1 sayfalık özet hazırla.

Yapı:
1. Anlaşmanın özü (3 cümle — ne, kim, ne kadar)
2. Kritik tarihler (tablo)
3. En önemli 3 risk (madde madde)
4. Karar noktaları (CEO'nun onaylaması gereken 2-3 şey)
5. Önerilen aksiyon (1 cümle)

Ton: Doğrudan. CEO'nun zamanı kıt.

Bulgular:
{consolidated}

Riskler:
{risks}
"""
    response = LLM.invoke(
        summary_prompt.format(
            consolidated=consolidated,
            risks=risks
        )
    )
    return response.content


def run_pipeline(pdf_path: str, output_path: str):
    """Ana pipeline akışı."""
    print(f"Belge yükleniyor: {pdf_path}")
    
    # Adım 0: Metin çıkar
    text = extract_text(pdf_path)
    chunks = chunk_document(text)
    print(f"Toplam {len(chunks)} chunk oluşturuldu")
    
    # Adım 1: Her chunk'tan madde çıkar
    clauses = extract_key_clauses(chunks)
    
    # Adım 2: Konsolide et
    print("Bulgular birleştiriliyor...")
    consolidated = synthesize_findings(clauses)
    
    # Adım 3: Risk değerlendirmesi
    print("Risk analizi yapılıyor...")
    risks = risk_assessment(consolidated)
    
    # Adım 4: Yönetici özeti
    print("Yönetici özeti hazırlanıyor...")
    summary = generate_executive_summary(consolidated, risks)
    
    # Kaydet
    output = f"""# Belge Analiz Raporu
Kaynak: {pdf_path}

## Yönetici Özeti
{summary}

## Kritik Maddeler (Detaylı)
{consolidated}

## Risk Değerlendirmesi
{risks}
"""
    Path(output_path).write_text(output, encoding="utf-8")
    print(f"Rapor kaydedildi: {output_path}")


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", required=True)
    parser.add_argument("--output", default="analiz_raporu.md")
    args = parser.parse_args()
    
    run_pipeline(args.file, args.output)
```

---

## Örnek 14 — Otonom Araştırma Agent'ı

**Senaryo:** "X sektöründeki son 3 aydaki gelişmeleri araştır" → Yapılandırılmış rapor

**Neden agent?** Araştırma sürecinde dinamik karar verme var. Hangi kaynakları takip edeceği veriye bağlı.

```python
"""
Araştırma Agent'ı
Araçlar: LangChain, Tavily Search, OpenAI

Önemli: Bu agent maksimum 8 iterasyonla sınırlandırılmış.
         Üretimde bu tür sınırlar kritik.
"""

from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor, create_react_agent
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.tools import tool
from langchain.prompts import PromptTemplate
from datetime import datetime


# --- Araç 1: Web araması ---
search = TavilySearchResults(
    max_results=5,
    include_answer=True,
    include_raw_content=False,
    include_images=False
)

# --- Araç 2: Özel not alma aracı ---
# Agent'ın kendi kendine not almasını sağlar
# Bu agent'a "çalışma belleği" kazandırır
research_notes = []

@tool
def save_note(note: str) -> str:
    """
    Önemli bir bulguyu not al. 
    Araştırma boyunca bu notlara erişebilirsin.
    Kullanım: save_note("Türkiye fintech pazarı 2024'te %34 büyüdü — Bloomberg")
    """
    research_notes.append(f"[{datetime.now().strftime('%H:%M')}] {note}")
    return f"Not kaydedildi. Toplam not: {len(research_notes)}"

@tool
def get_all_notes() -> str:
    """
    Şimdiye kadar aldığın tüm notları getir.
    Rapor yazmadan önce bunu çalıştır.
    """
    if not research_notes:
        return "Henüz not yok."
    return "\n".join(research_notes)


tools = [search, save_note, get_all_notes]

# --- Agent System Prompt'u ---
# Bu prompt agent'ın "kişiliğini" ve çalışma stilini belirliyor
AGENT_PROMPT = PromptTemplate.from_template("""
Sen titiz ve analitik bir sektör araştırmacısısın.
Bugünün tarihi: {date}

Araştırma görevin: {input}

Nasıl çalışırsın:
1. Önce ne arayacağını planla
2. Ara, oku, değerlendir
3. Önemli bulguları hemen not al (save_note aracıyla)
4. Farklı kaynaklarla doğrula — tek kaynaktan büyük iddia kabul etme
5. Çelişkili bilgileri işaretle, uydurma
6. Tüm notları topladıktan sonra raporu yaz

Rapor formatı:
## Yönetici Özeti (3 cümle)
## Ana Gelişmeler (madde madde, tarihle)
## Dikkat Çeken Sinyaller (zayıf ama önemli)
## Kaynaklar

Çalışman boyunca şu soruları sor:
- Bu bilgi ne kadar güncel?
- Bu kaynağın çıkarı var mı?
- Alternatif yorum nedir?

Mevcut araçlar: {tools}
Araç isimleri: {tool_names}

{agent_scratchpad}
""")

# --- LLM ve Agent ---
llm = ChatOpenAI(
    model="gpt-4o",
    temperature=0.1  # Araştırma için düşük sıcaklık
)

agent = create_react_agent(llm, tools, AGENT_PROMPT)
agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True,
    max_iterations=8,        # Kritik: sonsuz döngü önlemi
    max_execution_time=120,  # Kritik: 2 dakika zaman sınırı
    handle_parsing_errors=True,
    return_intermediate_steps=True  # Debug için
)


def run_research(topic: str) -> dict:
    """
    Araştırma agent'ını çalıştır.
    
    Returns:
        output: Final rapor
        steps: Tüm araç çağrıları (debug için)
        notes: Agent'ın aldığı notlar
    """
    research_notes.clear()  # Önceki araştırmadan kalan notları temizle
    
    result = agent_executor.invoke({
        "input": topic,
        "date": datetime.now().strftime("%d %B %Y")
    })
    
    return {
        "output": result["output"],
        "steps": len(result.get("intermediate_steps", [])),
        "notes": research_notes.copy()
    }


# Örnek kullanım:
if __name__ == "__main__":
    topic = """
    Türkiye'nin üretim sektöründe son 3 ayda öne çıkan 
    AI ve otomasyon uygulamaları nelerdir?
    Somut şirket örnekleri ve sonuçlar dahil.
    """
    
    result = run_research(topic)
    
    print("\n" + "="*50)
    print("ARAŞTIRMA RAPORU")
    print("="*50)
    print(result["output"])
    print(f"\n[{result['steps']} araç çağrısı yapıldı]")
```

---

## Örnek 15 — Multi-Agent: Kod Review Sistemi

**Senaryo:** Kod → Güvenlik Analisti + Performans Analisti + Kıdemli Geliştirici (koordinatör)

**Neden multi-agent?** Her perspektif farklı uzmanlık gerektiriyor. Paralel çalışma süreci hızlandırıyor.

```python
"""
Multi-Agent Kod Review Sistemi
Her agent farklı perspektiften aynı kodu analiz ediyor.
Koordinatör agent sonuçları birleştiriyor.

NOT: Bu basit bir implementasyon. Production için 
LangGraph ya da AutoGen önerilir.
"""

import asyncio
from langchain_openai import ChatOpenAI


# Farklı "kişilik" promptları — aynı model, farklı perspektif
SECURITY_ANALYST_PROMPT = """
Sen uygulama güvenliği konusunda uzman bir analistsin.
OWASP Top 10 ve yaygın güvenlik açıklarını iyi biliyorsun.

Kodu yalnızca güvenlik perspektifinden incele:
- Injection riskleri (SQL, command, XSS)
- Authentication/authorization zayıflıkları
- Hassas veri ifşası
- Güvensiz kriptografi
- Hatalı hata işleme (stack trace ifşası gibi)

Her bulgu için:
🔴 KRİTİK: Hemen düzeltilmeli
🟡 YÜKSEK: Bu PR'da düzeltilmeli
🟢 ORTA: Backlog'a alınabilir

Güvenlik sorunu görmüyorsan "Güvenlik açısından temiz görünüyor" de.
Uydurma.
"""

PERFORMANCE_ANALYST_PROMPT = """
Sen backend performans optimizasyonu konusunda uzmansın.
Veritabanı sorguları, bellek kullanımı ve ölçeklenebilirlik konularında iyisin.

Kodu yalnızca performans perspektifinden incele:
- N+1 sorgu problemleri
- Gereksiz veri yükleme
- Blocking I/O
- Bellek sızıntısı riskleri
- Önbelleğe alınabilecek işlemler

Her bulgu için tahmini etki belirt: "100 req/s'de yaklaşık X ms ek gecikme"
Ölçemiyorsan ölçüm öner.
"""

SENIOR_DEV_PROMPT = """
Sen 10+ yıl deneyimli bir kıdemli geliştiricisin.
Kod kalitesi, maintainability ve ekip pratikleri konusunda uzmansın.

Kodu şu açılardan değerlendir:
- Okunabilirlik ve isimler
- Tekrar eden kod (DRY ihlalleri)
- Test edilebilirlik
- Hata işleme bütünlüğü
- Dokümantasyon kalitesi

Junior geliştiricilere öğretici ton kullan.
Her eleştiriyle birlikte "nasıl düzeltilir" göster.
"""

COORDINATOR_PROMPT = """
Sen kıdemli bir mühendislik liderisin. 
Üç farklı analistin kod değerlendirmelerini aldın.

Görev: Bu üç perspektifi sentezle ve ekibe net bir özet sun.

Sentez şunları içermeli:
1. En kritik sorunlar (herhangi bir analistten)
2. Çakışan bulgular (birden fazla analist aynı şeyi bulmuş)
3. Çelişkili öneriler (varsa — neden çelişkili olduğunu açıkla)
4. Merge kararı: ONAY / RED / ŞARTLI ONAY
5. Şartlı onay ise: hangi koşullar sağlanmalı

Yapıcı, öğretici ton. Junior bu review'dan bir şeyler öğrenmeli.
"""


async def run_parallel_review(code: str) -> dict:
    """
    Üç analisti paralel çalıştır, koordinatör sentezlesin.
    asyncio ile paralel — sırayla değil.
    """
    llm = ChatOpenAI(model="gpt-4o", temperature=0)
    
    async def get_review(system_prompt: str, code: str) -> str:
        """Tek bir analyst review'u."""
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Bu kodu review et:\n\n```python\n{code}\n```"}
        ]
        response = await llm.ainvoke(messages)
        return response.content
    
    # Üç review paralel başlatılıyor
    print("Güvenlik, performans ve kod kalitesi analizleri paralel başlatıldı...")
    
    security_review, performance_review, quality_review = await asyncio.gather(
        get_review(SECURITY_ANALYST_PROMPT, code),
        get_review(PERFORMANCE_ANALYST_PROMPT, code),
        get_review(SENIOR_DEV_PROMPT, code)
    )
    
    print("Paralel review tamamlandı. Koordinatör sentezliyor...")
    
    # Koordinatör sentezleme
    coord_input = f"""
Güvenlik Analisti Raporu:
{security_review}

---

Performans Analisti Raporu:
{performance_review}

---

Kıdemli Geliştirici Raporu:
{quality_review}
"""
    
    messages = [
        {"role": "system", "content": COORDINATOR_PROMPT},
        {"role": "user", "content": coord_input}
    ]
    
    final_review = await llm.ainvoke(messages)
    
    return {
        "security": security_review,
        "performance": performance_review,
        "quality": quality_review,
        "final": final_review.content
    }


# Kullanım:
if __name__ == "__main__":
    sample_code = '''
def get_user_data(user_id):
    query = f"SELECT * FROM users WHERE id = {user_id}"
    conn = get_db_connection()
    result = conn.execute(query)
    users = []
    for row in result:
        user = {
            "id": row["id"],
            "name": row["name"],
            "email": row["email"],
            "password": row["password"],  # tam da burada
            "api_key": row["api_key"]
        }
        orders = get_orders(user["id"])  # her user için ayrı sorgu
        user["orders"] = orders
        users.append(user)
    return users
'''
    
    result = asyncio.run(run_parallel_review(sample_code))
    
    print("\n" + "="*60)
    print("FINAL CODE REVIEW")
    print("="*60)
    print(result["final"])
```

Bu kodda ne kadar güvenlik ve performans sorunu var? Agent'ların nasıl yakaladığını çalıştırarak görün.

---

→ [Egzersizler](../../exercises/)  
→ [Belgeler: Multi-Agent Sistemler](../../docs/multi-agent-systems.md)
