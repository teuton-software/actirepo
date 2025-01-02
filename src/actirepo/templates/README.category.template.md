---
title: {{ category.metadata.name }}
---

# {{ category.metadata.name }}

{{ category.metadata.description }}

## Contenido

{% set stats = category.get_stats() %}
|   | Tipo              | Cantidad                   |
| - | ----------------- | -------------------------- |
{% for type,count in stats.types.items() %}| ![{{ type }}]({{ icons_url }}/{{ type }}.svg) | [{{ Quiz.SUPPORTED_QUESTIONS[type]['description'] }}](#{{ Quiz.SUPPORTED_QUESTIONS[type]['description'] | anchorify }}) | {{ count }} |
{% endfor %}|   | **TOTAL**         | {{ stats.total }} |

{% if category.categories %}
## Subcategorías
{% for subcategory in category.categories %}
- [{{ subcategory.name }}]({{ subcategory.filename }})
{% endfor %}
{% endif %}

{% if category.activities %}
## Actividades
| Nombre              | Descripción                   | Dificultad | Preguntas |
| ------------------- | ----------------------------- | ---------- | --------- |
{% for activity in category.activities %}| [{{ activity.metadata.name }}]({{ activity.name }}) | {{ activity.metadata.description }} | {{ activity.metadata.difficulty | difficulty_to_badge }} | {{ activity.metadata.full_stats.total }} |
{% endfor %}
{% endif %}
