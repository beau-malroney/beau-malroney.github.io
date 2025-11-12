---
layout: post
title: "Draft: [Your Theme Here]"
description: "Curated picks for [audience/use case]—modular, resilient, and ready to publish."
date: 2025-09-11
categories: [drafts, affiliate]
tags: [amazon, gear, workflow]
image: /assets/images/drafts/cover.jpg
published: false
status: draft
---

> ⚠️ This post is a draft. It’s not live yet, but it’s scaffolded for clarity, customization, and symbolic overlays.

---

## 🧰 Featured Gear Blocks

{% assign items = site.data.amazon_picks %}

{% for item in items %}
### 🔹 {{ item.name }}
![{{ item.alt }}]({{ item.image }})  
**Why I chose it:**  
- {{ item.feature1 }}  
- {{ item.feature2 }}  
- {{ item.overlay | default: "Symbolic resonance: [add metaphor]" }}

👉 [Buy on Amazon]({{ item.link }})
{% endfor %}

---

## 🧠 Selection Criteria

- Modular design  
- Visual clarity  
- Earth-tone resilience  
- Symbolic alignment with agent workflows  
- Long-term adaptability

---

## 🛍️ Bonus Picks

- 🎧 [Focus headphones](https://www.amazon.com/dp/YOUR-ASIN?tag=YOURTAG-20)  
- 🧳 [Travel gear for Disneyland](https://www.amazon.com/dp/YOUR-ASIN?tag=YOURTAG-20)  
- 🧼 [Pool troubleshooting tools](https://www.amazon.com/dp/YOUR-ASIN?tag=YOURTAG-20)

---

## 🌿 Notes to Self

- Add symbolic overlays for each item  
- Style image cards with earth-tone borders  
- Consider adding voice preview module for product descriptions  
- Link to related Jekyll posts via tag navigation

---

## 🔄 Publish Checklist

- [ ] Finalize item list  
- [ ] Add affiliate tags  
- [ ] Optimize images  
- [ ] Test layout on mobile  
- [ ] Switch `published: true` when ready

---

Want me to scaffold the `amazon_picks.yml` data file or build a reusable include for gear blocks? I can also help you style this with persistent theme switching or visual overlays. Just say the word.