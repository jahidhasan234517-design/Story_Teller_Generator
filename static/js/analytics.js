document.addEventListener('DOMContentLoaded', () => {
  fetch('/api/analytics/')
    .then((response) => response.json())
    .then((data) => {
      const categories = data.categories || [];
      const sentiments = data.sentiments || [];
      const topics = data.topics || [];
      const sources = data.sources || [];
      const byDay = data.by_day || [];

      const categoryCtx = document.getElementById('categoryChart');
      if (categoryCtx) {
        new Chart(categoryCtx, {
          type: 'bar',
          data: {
            labels: categories.map((item) => item.category || 'Unknown'),
            datasets: [{
              label: 'Articles',
              data: categories.map((item) => item.count || 0),
              backgroundColor: '#3461ff'
            }]
          },
          options: { responsive: true, maintainAspectRatio: false }
        });
      }

      const sentimentCtx = document.getElementById('sentimentChart');
      if (sentimentCtx) {
        new Chart(sentimentCtx, {
          type: 'doughnut',
          data: {
            labels: sentiments.map((item) => item.sentiment || 'Unknown'),
            datasets: [{
              data: sentiments.map((item) => item.count || 0),
              backgroundColor: ['#1f9d68', '#f5a524', '#d94c4c']
            }]
          },
          options: { responsive: true, maintainAspectRatio: false }
        });
      }

      const timelineCtx = document.getElementById('timelineChart');
      if (timelineCtx) {
        new Chart(timelineCtx, {
          type: 'line',
          data: {
            labels: byDay.map((item) => item.day || ''),
            datasets: [{
              label: 'Articles',
              data: byDay.map((item) => item.count || 0),
              borderColor: '#3461ff',
              tension: 0.3,
              fill: false
            }]
          },
          options: { responsive: true, maintainAspectRatio: false }
        });
      }

      const keywordCtx = document.getElementById('keywordsChart');
      if (keywordCtx) {
        new Chart(keywordCtx, {
          type: 'bar',
          data: {
            labels: topics.map((item) => item.label || 'Topic'),
            datasets: [{
              label: 'Mentions',
              data: topics.map((item) => item.value || 0),
              backgroundColor: '#7aa2ff'
            }]
          },
          options: {
            indexAxis: 'y',
            responsive: true,
            maintainAspectRatio: false
          }
        });
      }

      const sourceCtx = document.getElementById('sourceChart');
      if (sourceCtx) {
        new Chart(sourceCtx, {
          type: 'pie',
          data: {
            labels: sources.map((item) => item.source || 'Unknown'),
            datasets: [{
              data: sources.map((item) => item.count || 0),
              backgroundColor: ['#3461ff', '#1f9d68', '#f5a524', '#d94c4c', '#8c5ef5']
            }]
          },
          options: { responsive: true, maintainAspectRatio: false }
        });
      }
    })
    .catch((error) => console.error('Analytics data failed to load', error));
});
