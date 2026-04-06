# Kaynaklar ve Araçlar

*Güncel kalmak için: Bu alan 3-6 ayda bir dramatik değişiyor. Bu liste Nisan 2026 itibarıyla geçerli.*

---

## Hızlı Başlangıç Araçları

### Prompt Geliştirme

| Araç | Ne İşe Yarar | Ücretsiz mi? |
|------|-------------|--------------|
| [Claude.ai](https://claude.ai) | Genel amaçlı, uzun bağlam, güvenli | Kısmen |
| [ChatGPT](https://chat.openai.com) | En geniş ekosistem | Kısmen |
| [Gemini](https://gemini.google.com) | Google entegrasyonu, büyük bağlam | Kısmen |
| [Playground (OpenAI)](https://platform.openai.com/playground) | Sıcaklık, sistem prompt kontrolü | API maliyeti |

**Ne zaman hangisini?**
- Kod: Claude Sonnet / GPT-4o
- Uzun doküman: Claude (200K bağlam)
- Google entegrasyonu: Gemini
- Deney/parametre: OpenAI Playground

---

### Agent ve Otomasyon

| Araç | Seviye | Kullanım |
|------|--------|---------|
| [n8n](https://n8n.io) | No-code | Workflow otomasyonu, self-hosted |
| [Make (Integromat)](https://make.com) | No-code | SaaS entegrasyonları |
| [LangChain](https://langchain.com) | Kod | Agent framework, Python/JS |
| [LangGraph](https://langgraph.com) | Kod | Karmaşık agent akışları |
| [AutoGen](https://microsoft.github.io/autogen/) | Kod | Multi-agent, Microsoft |

---

### RAG (Retrieval Augmented Generation)

| Araç | Ne İşe Yarar |
|------|-------------|
| [Pinecone](https://pinecone.io) | Vector veritabanı, managed |
| [Chroma](https://trychroma.com) | Local, ücretsiz, Python |
| [Weaviate](https://weaviate.io) | Open source, self-hosted |
| [LlamaIndex](https://llamaindex.ai) | RAG pipeline framework |

---

## Okuma Listesi

### Temel (Teknik olmayan)

- **"Co-Intelligence"** — Ethan Mollick (2024)  
  Wharton profesöründen pratik AI kullanımı. Akademik ama okunabilir.

- **"The Alignment Problem"** — Brian Christian (2020)  
  AI güvenliği ve değer hizalaması. Teknik değil, analitik.

### Uygulama Odaklı

- **"Building LLMs for Production"** — Vicki Boykis et al.  
  Ücretsiz, online. Production LLM sistemleri için pratik rehber.

- **LangChain Cookbook** — github.com/langchain-ai/langchain  
  Güncel, notebook formatında, çalışan örnekler.

### Akademik (İleri)

- **"Attention Is All You Need"** (Vaswani et al., 2017)  
  Transformatör mimarisinin orijinal makalesi. Teknik.

- **"Chain-of-Thought Prompting Elicits Reasoning in LLMs"** (Wei et al., 2022)  
  CoT'un akademik temeli. Erişilebilir.

- **"ReAct: Synergizing Reasoning and Acting in Language Models"** (Yao et al., 2022)  
  Agent düşüncesinin temeli. Bu eğitimde referans verdik.

- **"Prompt Injection Attacks and Defenses in LLM-Integrated Applications"** (Liu et al., 2023)  
  Güvenlik açısı. Production geliştiriyorsanız zorunlu.

---

## Takip Edilecek Kaynaklar

### Bültenler

- **The Batch** (deeplearning.ai) — Haftalık, teknik ama sindirilebilir
- **Import AI** (Jack Clark) — Haftalık, araştırma odaklı
- **The Algorithmic Bridge** — Toplumsal etki perspektifi

### Podcast

- **Lex Fridman Podcast** — Uzun format, araştırmacı röportajları
- **The TWIML AI Podcast** — Teknik, ML odaklı
- **Hard Fork (NYT)** — Teknoloji gazetecilik perspektifi

### Türkçe Kaynaklar

- **Yapay Zeka Türkiye** (LinkedIn topluluğu) — Güncel haberler
- **Veri Bilimi Okulu** — Türkçe teknik içerik
- **AI Summit Turkey** — Yıllık konferans, networking

---

## Benchmark ve Değerlendirme

Bir modeli ya da sistemi değerlendiriyorsanız:

| Benchmark | Ne Ölçüyor |
|-----------|-----------|
| MMLU | Genel bilgi, çok disiplinli |
| HumanEval | Kod yazma |
| HellaSwag | Sağduyu akıl yürütme |
| TruthfulQA | Halüsinasyon direnci |
| MT-Bench | Çok turlu konuşma kalitesi |

**Not:** Benchmark performansı ile gerçek kullanım kalitesi her zaman örtüşmüyor. Kendi use-case'inizle test edin.

---

## Maliyet Tahmini (Nisan 2026)

*Fiyatlar sık değişiyor. Bu tabloya gelmeden önce güncel fiyatları kontrol edin.*

### Kaba Tahmin (1M token = ~750,000 kelime = ~1500 sayfa)

| Model | Input (1M token) | Output (1M token) |
|-------|-----------------|------------------|
| GPT-4o | ~$2.50 | ~$10.00 |
| Claude 3.5 Sonnet | ~$3.00 | ~$15.00 |
| GPT-4o mini | ~$0.15 | ~$0.60 |
| Claude Haiku | ~$0.25 | ~$1.25 |

**Kurumsal kullanım için kural:** Geliştirme ve test için pahalı model, production için ucuz model (yeterli kalitede ise). Fark genellikle 10-20x.

---

## Güvenlik ve Uyumluluk Notları

Kurumsal kullanım için kritik:

**Veri gizliliği:**
- OpenAI Enterprise, Azure OpenAI: Veri eğitime kullanılmıyor (sözleşmeyle)
- Claude for Enterprise (Anthropic): Benzer garanti
- On-premise (Ollama + açık model): Veri dışarı çıkmıyor

**GDPR / KVKK uyumu:**
- Kişisel veri içeren promptlar dikkat gerektirir
- AB veri sınırı gerektiren kullanımlar için EU-hosted hizmetlere bakın
- Azure OpenAI: AB veri merkezi seçeneği var

**Şirket politikası:**
- Hangi veriler AI'ya gönderilebilir? Politika yazılı olmalı
- Çalışan eğitimi: "Hassas veriyi promptta paylaşmayın"
- Çıktı denetimi: Kritik kararlar için insan onayı

---

*Son güncelleme: Nisan 2026*  
*Bu listeye katkı için repo'ya PR açabilirsiniz.*
