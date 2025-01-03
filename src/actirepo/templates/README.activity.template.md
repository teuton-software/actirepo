---
title: {{ activity.metadata.name }}{% if activity.metadata.author %}
author: {{ activity.metadata.author.name }} ({{ activity.metadata.author.email }}){% endif %}
---

# {{ activity.metadata.name }}

{{ activity.metadata.difficulty | difficulty_to_badge }}

{{ activity.metadata.description }}

## Contenido

Ficheros de preguntas disponibles en esta actividad:

{% for quiz in activity.quizzes %}

### [{{quiz.filename}}]({{ quiz.filename | quote }})

{% set stats = quiz.get_stats() %}
|   | Tipo              | Cantidad                   |
| - | ----------------- | -------------------------- |
{% for type,count in stats.types.items() %}| ![{{ type }}]({{ icons_url }}/{{ type }}.svg) | [{{ Quiz.SUPPORTED_QUESTIONS[type]['description'] }}](#{{ Quiz.SUPPORTED_QUESTIONS[type]['description'] | anchorify }}) | {{ count }} |
{% endfor %}|   | **TOTAL**         | {{ stats.total }} |

{% for type,questions in quiz.questions.items() %}
#### {{ Quiz.SUPPORTED_QUESTIONS[type]['description'] }}

{% for question in questions[:activity.metadata.limit] %}
![{{ question.name }}](images/{{ question.image_filename | quote }})
{% endfor %}

{% endfor %}

{% endfor %}
