# Modül 3 — Agent Düşüncesi

> Prompt yazmak bir şeyi çözmektir. Agent tasarlamak bir sistemi işletmektir. Bu fark küçük değil.

---

## 3.1 — Üç Katman: Prompt → Zincir → Agent

Çoğu insan "AI kullanmak" derken bu üç katmandan birinde çalışıyor. Ama hangi katmanda çalıştıklarını bilmiyorlar. Bu modül onu netleştiriyor.

---

### Katman 1: Tek Prompt

```
Kullanıcı → [LLM] → Çıktı
```

Bellek yok. Planlama yok. Her çağrı bağımsız.

**İyi olduğu yer:** Metin üretme, özetleme, sınıflandırma, tek seferlik analiz.  
**Sınırı:** Bir sonraki adım ne olacak bilmiyor. Sadece şu an ne sorulduğunu biliyor.

---

### Katman 2: Prompt Zinciri

```
Kullanıcı → [LLM₁] → ara çıktı → [LLM₂] → final çıktı
```

Adımlar birbirini besliyor ama her adım hâlâ insan tarafından tetikleniyor ya da sabit bir akışla bağlı.

**İyi olduğu yer:** Belge üretme pipeline'ları, veri dönüşüm süreçleri, çok adımlı analiz.  
**Sınırı:** Beklenmedik durumlara adapte olamıyor. Akış önceden tanımlanmış.

---

### Katman 3: Agent

```
Hedef → [Plan] → [Araç Seç] → [Çalıştır] → [Gözlemle] → [Tekrar Plan?] → Sonuç
         ↑_______________________________________________|
```

Kendi kendine karar veriyor. Gözlemlediğine göre planını güncelliyor. Araçlara erişimi var.

**İyi olduğu yer:** Araştırma görevleri, kod yazma + test etme, çok adımlı veri işleme, otonom müşteri etkileşimi.  
**Sınırı:** Kırılgan. Uzun zincirlerde hata birikir. Belirsiz hedeflerle başarısız olur.

---

## 3.2 — ReAct Döngüsü

Agent'ın kalbi. 2022'de Yao et al. tarafından tanımlanan çerçeve. Adı "Reasoning + Acting"in kısaltması.

```
┌─────────────────────────────────────────────┐
│                                             │
│   Düşün                                     │
│   "Hedefime ulaşmak için ne yapmalıyım?"    │
│                                             │
│         ↓                                  │
│                                             │
│   Hareket et                                │
│   "Şu aracı çalıştır: web_search('...')"   │
│                                             │
│         ↓                                  │
│                                             │
│   Gözlemle                                  │
│   "Araç şunu döndürdü: ..."                 │
│                                             │
│         ↓                                  │
│                                             │
│   Tekrar düşün                              │
│   "Bu beni hedefe götürdü mü?"              │
│   → Evet: bitir                             │
│   → Hayır: döngüye geri dön                 │
│                                             │
└─────────────────────────────────────────────┘
```

### Gerçek Bir Trace

Aşağıdaki gerçek bir araştırma agent'ının iç monologundan alınmış (GPT-4, LangChain, Ocak 2024):

```
Düşünce: Kullanıcı 2023 yılında Türkiye'nin AI yatırımlarını soruyor. 
         Web'de aramalıyım.

Hareket: web_search("Turkey AI investment 2023")

Gözlem: [Arama sonuçları döndü — 3 kaynak, farklı rakamlar]

Düşünce: Rakamlar çelişkili. En güvenilir kaynak hangisi? 
         OECD raporu daha güvenilir görünüyor.
         
Hareket: fetch_url("https://oecd.org/...")

Gözlem: [Sayfa içeriği döndü]

Düşünce: Veri var ama 2022 yılına ait. 2023 için güncel veri yok.
         Kullanıcıya bunu söylemeliyim.

Cevap: "2023 verisi henüz yayınlanmamış, 2022 verisi şu şekilde..."
```

**Kritik not:** Model burada ne yaptı? Belirsizliği tespit etti ve dürüst davrandı. Bu agent'ın doğru çalıştığının göstergesi.

---

## 3.3 — Agent Anatomisi

### Araçlar (Tools)

Agent'ın "elleri." Modelin dışarıyla etkileşim kurmasını sağlar.

| Araç Tipi | Örnekler | Risk Seviyesi |
|-----------|----------|---------------|
| Okuma | Web search, dosya okuma, DB sorgusu | Düşük |
| Yazma | Dosya kaydetme, e-posta gönderme | Orta |
| Çalıştırma | Kod çalıştırma, API çağrısı | Yüksek |
| Silme | Veritabanı silme, dosya silme | Çok Yüksek |

**Tasarım prensibi:** Agenta mümkün olan en az yetkiyi verin. İhtiyaç duymadığı araçları vermeyin.

---

### Hafıza Katmanları

```
                    ┌──────────────────────┐
Kısa vadeli  →      │  Konuşma geçmişi     │  Bu session boyunca
                    │  (bağlam penceresi)  │  Sonra kayboluyor
                    └──────────────────────┘

                    ┌──────────────────────┐
Orta vadeli  →      │  Vector store        │  Uzun dönem, aranabilir
                    │  (embeddings DB)     │  Tasarım gerektirir
                    └──────────────────────┘

                    ┌──────────────────────┐
Uzun vadeli  →      │  ❌ Yok              │  LLM doğası gereği
                    │  (gerçek anlamda)    │  stateless
                    └──────────────────────┘
```

**Yanılgı:** "Agent öğreniyor." Hayır. Konuşma içinde adapte oluyor. Konuşma kapandığında — her şey sıfırlanıyor (vector store kaydedilmediyse).

---

### Planlama

Agent hedefi alt görevlere nasıl böler?

**Plan-and-Execute yaklaşımı:**
```
1. Kullanıcı hedefi al
2. Hedefi adımlara böl (planning step)
3. Her adımı sırayla çalıştır
4. Her adımdan sonra planı güncelle (gerekirse)
```

**Tree-of-Thought yaklaşımı (daha gelişmiş):**
```
1. Birden fazla yol düşün
2. Her yolun olasılığını değerlendir
3. En umut verici yolu seç
4. Başarısız olursa geri dön, farklı yol dene
```

---

## 3.4 — Güvenilirlik Sınırları (Dürüst Bir Değerlendirme)

Agent'lar güçlü. Ama hâlâ kırılıyorlar. Nerede ve neden:

### Hata Birikimi

10 adımlı bir zincirde her adım %90 doğruluksa: 0.90^10 = %35. Yani sistemin bütünü sadece %35 güvenilir.

**Çözüm:** Kritik adımlarda insan onayı noktaları koyun. Hata toleransı olmayan adımları elle yapın.

### Belirsiz Hedef Çöküşü

```
# Agent için tehlikeli hedef
"Şirketimizin sosyal medya stratejisini iyileştir."

# Agent için çalışabilir hedef  
"Bu haftaki 5 tweet'imizi analiz et, engagement oranlarını çıkar, 
en düşük performanslı 2'si için alternatif versiyon öner."
```

Agent hedefi ölçemiyorsa bitiremez. Belirsiz hedefler sonsuz döngüye ya da rastgele çıktılara yol açar.

### Araç Hataları Kaskadı

Bir araç başarısız olduğunda agent ne yapıyor? İyi tasarlanmışsa: "araç başarısız oldu, alternatif yol deniyorum." Kötü tasarlanmışsa: başarısız araç çıktısını gerçekmiş gibi kullanmaya devam ediyor.

**Tasarım kuralı:** Her araç çağrısından sonra "bu başarılı mıydı?" kontrolü zorunlu.

---

### Ne İşe Yarıyor, Ne Yaramıyor

**Gerçekten iyi çalıştığı yerler:**

| Kullanım Alanı | Neden İyi Çalışıyor |
|----------------|---------------------|
| Kod review + test | Araçlar deterministik, başarı ölçülebilir |
| Müşteri sınıflandırma | Kısa zincir, net kriterler |
| Doküman özetleme | Tek yönlü, çıktı doğrulanabilir |
| Veri temizleme | Kurallar net, hata düzeltilir |

**Dikkatli olunması gereken yerler:**

| Kullanım Alanı | Risk |
|----------------|------|
| Açık uçlu araştırma | Bitiş noktası belirsiz |
| Çok adımlı müzakere | Her adım önceki bağlamla bağlı |
| Finansal işlemler | Geri dönüşü yok |
| Kişisel veri işleme | Gizlilik, hata toleransı sıfır |

---

## 3.5 — Kendi Agent'ınızı Tasarlamak

Eğitimde kullandığımız çerçeve. Bir sayfa, üç soru:

### Soru 1: Hangi görevi otomatize etmek istiyorsunuz?

İyi hedefler şu kriterleri karşılar:
- ✅ Tekrarlayan (her gün / her hafta yapılıyor)
- ✅ Kurallarla tanımlanabilir ("eğer X ise Y yap")
- ✅ Başarı ölçülebilir
- ❌ Sübjektif değerlendirme gerektirmiyor
- ❌ "Her seferinde farklı" değil

### Soru 2: Hangi araçlara erişim gerekiyor?

```
Veri kaynakları: [web / dahili DB / dosyalar / API]
Yazma izinleri: [e-posta / dosya / form / hiçbiri]
Dış servisler: [hangi API'lar]
```

### Soru 3: İnsan onayı nerede gerekli?

```
Hiçbir zaman onay gerekmez: [...]
Her seferinde onay gerekir: [...]
Belirli koşullarda onay gerekir: [...]
```

Bu üç sorunun cevabı agent sistem tasarımınızın taslağıdır.

---

## 3.6 — Minimal Çalışan Örnek

Kod yazmayanlar için: Akışı anlayın, uygulamayı takımınızdaki teknik kişiye devredin.  
Kod yazanlar için: Bu LangChain ile çalışan minimal bir araştırma agent'ı.

```python
# Gereksinimler: langchain, openai, tavily-python
# pip install langchain langchain-openai langchain-community tavily-python

from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor, create_react_agent
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain.prompts import PromptTemplate

# --- Araç tanımla ---
search_tool = TavilySearchResults(max_results=3)
tools = [search_tool]

# --- Agent prompt'u ---
# Not: Bu prompt agent'ın "düşünme" stilini belirliyor
agent_prompt = PromptTemplate.from_template("""
Sen titiz bir araştırma asistanısın. Verilen soruyu yanıtlamak için 
web araması yaparsın. Her araçtan sonra sonucu değerlendirir ve 
gerekirse farklı bir arama yaparsın.

Önemli kurallar:
- Emin olmadığın şeyleri uydurma
- Çelişkili kaynakları belirt
- "Bilmiyorum" demekten çekinme

Eriştiğin araçlar: {tools}
Araç isimleri: {tool_names}

Soru: {input}

{agent_scratchpad}
""")

# --- LLM ve agent oluştur ---
llm = ChatOpenAI(model="gpt-4o", temperature=0)
agent = create_react_agent(llm, tools, agent_prompt)
agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True,          # ReAct döngüsünü görmek için
    max_iterations=5,      # Sonsuz döngü önlemi
    handle_parsing_errors=True
)

# --- Çalıştır ---
result = agent_executor.invoke({
    "input": "2024 yılında Türkiye'nin AI alanında öne çıkan startup'ları hangileri?"
})

print(result["output"])
```

**verbose=True neden önemli:** ReAct döngüsünü canlı görürsünüz. Agent'ın "düşünce" adımları, araç çağrıları ve gözlemleri ekrana basılır. Bunu kapatmadan önce en az birkaç kez izleyin — ne yaptığını anlamak için.

---

## Modül Özeti

| Katman | Karar mekanizması | Bellek | İnsan müdahalesi |
|--------|-------------------|--------|------------------|
| Tek Prompt | Yok | Yok | Her adımda |
| Zincir | Sabit akış | Sınırlı | Akış tasarımında |
| Agent | Dinamik | Araçla | Kritik noktalarda |

**Agent tasarımının altın kuralı:** Önce mümkün olan en basit şeyi yap. Tek prompt yetiyorsa agent kurma. Zincir yetiyorsa agent kurma. Agent ancak dinamik karar verme gerçekten gerektiğinde değer üretiyor.

---

## Devam

→ [Egzersiz 3: Agent Tasarım Taslağı](../../exercises/03-agent-design-exercise.md)  
→ [Örnek: Gerçek Agent Pipeline'ları](../../examples/advanced/)  
→ [Makale: Multi-Agent Sistemler](../../docs/multi-agent-systems.md)
