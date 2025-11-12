---
layout: page
title: "Tags"
permalink: /tags/
---

<h1>Browse by tag</h1>

<ul class="tag-index">
  {% assign sorted_tags = site.tags | sort %}
  {% for tag in sorted_tags %}
    <li>
      <a href="#{{ tag[0] | slugify }}">{{ tag[0] }}</a>
      <span>({{ tag[1].size }} posts)</span>
    </li>
  {% endfor %}
</ul>

{% for tag in sorted_tags %}
  <h2 id="{{ tag[0] | slugify }}">{{ tag[0] }}</h2>
  <ul class="tag-posts">
    {% for post in tag[1] %}
      <li>
        <a href="{{ post.url }}">{{ post.title }}</a>
        <span>— {{ post.date | date: "%b %d, %Y" }}</span>
      </li>
    {% endfor %}
  </ul>
{% endfor %}
