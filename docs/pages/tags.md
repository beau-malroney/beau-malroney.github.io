---
layout: default
title: "Tags"
permalink: /tags/
---

<h1>Categories</h1>
<ul>
{% for category in site.tags %}
  <li><a name="{{ category | first }}">{{ category | first }}</a>
    <ul>
    {% for post in tag.last %}
      <li><a href="{{ post.url }}">{{ post.title }}</a></li>
    {% endfor %}
    </ul>
  </li>
{% endfor %}
</ul>