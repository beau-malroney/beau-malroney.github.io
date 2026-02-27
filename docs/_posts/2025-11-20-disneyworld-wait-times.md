---
layout: post
title: "Real-Time Disney World Ride Wait Times"
date: 2025-11-20
categories: disney parks
tags: wait times API
---

Today, we're showing live ride wait times at Disney World using the [Queue Times API](https://queue-times.com/en-US/pages/api).  
Below, you’ll see real-time updates for popular rides at Magic Kingdom.

<div id="wait-times"></div>

<script>
  fetch('https://queue-times.com/en-US/pages/api') // Use the actual API endpoint here
    .then(response => response.json())
    .then(data => {
      const rides = data['parks']['magic-kingdom'].rides;
      let html = '<ul>';
      for (const ride in rides) {
        html += `<li><strong>${ride}:</strong> ${rides[ride].waitTime} minutes</li>`;
      }
      html += '</ul>';
      document.getElementById('wait-times').innerHTML = html;
    })
    .catch(error => {
      document.getElementById('wait-times').innerHTML = 'Unable to fetch wait times at this moment.';
      console.error('Error fetching wait times:', error);
    });
</script>
