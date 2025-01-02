---
title: {{ category.metadata.name }}
---

# {{ category.metadata.name }}

{{ category.metadata.description }}

## Contenido

{% set stats = category.get_stats() %}
|   | Tipo              | Cantidad                   |
| - | ----------------- | -------------------------- |
{% for type,count in stats.types.items() %}| ![{{ type }}]({{ icons_url }}/{{ type }}.svg) | {{ Quiz.SUPPORTED_QUESTIONS[type]['description'] }} | {{ count }} |
{% endfor %}|   | **TOTAL**         | {{ stats.total }} |

{% if category.categories %}
## Categorías
| Nombre              | Descripción                   | Preguntas |
| ------------------- | ----------------------------- | --------- |
{% for subcategory in category.categories %}| [{{ subcategory.metadata.name }}]({{ subcategory.name }}) | {{ subcategory.metadata.description }} | {{ subcategory.metadata.stats.total }} |
{% endfor %}
{% endif %}


{% if category.activities %}
## Actividades
| Nombre              | Descripción                   | Dificultad | Preguntas |
| ------------------- | ----------------------------- | ---------- | --------- |
{% for activity in category.activities %}| [{{ activity.metadata.name }}]({{ activity.name }}) | {{ activity.metadata.description }} | {{ activity.metadata.difficulty | difficulty_to_minibadge }} | {{ activity.metadata.full_stats.total }} |
{% endfor %}
{% endif %}

---
Generated with :heart: by [{{project_name}} v{{ project_version }}]({{project_url}})