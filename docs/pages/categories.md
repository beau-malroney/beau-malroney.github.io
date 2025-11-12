---
layout: page
title: "Categories"
permalink: /categories/
---

<h1>Browse by Category</h1>

<ul class="category-index">
  {% assign sorted_categories = site.categories | sort %}
  {% for category in sorted_categories %}
    <li>
      <a href="#{{ category[0] | slugify }}">{{ category[0] }}</a>
      <span>({{ category[1].size }} posts)</span>
    </li>
  {% endfor %}
</ul>

{% for category in sorted_categories %}
  <h2 id="{{ category[0] | slugify }}">{{ category[0] }}</h2>
  <ul class="category-posts">
    {% for post in category[1] %}
      <li>
        <a href="{{ post.url }}">{{ post.title }}</a>
        <span>— {{ post.date | date: "%b %d, %Y" }}</span>
      </li>
    {% endfor %}
  </ul>
{% endfor %}
