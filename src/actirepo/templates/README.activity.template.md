---
title: {{ activity.name }}{% if activity.metadata.author %}
author: {{ activity.metadata.author.name }} ({{ activity.metadata.author.email }}){% endif %}
---

# {{ activity.name }}
{% set difficulty = activity.metadata.difficulty %}
{% if difficulty == 'hard' %}
![Dificultad](https://img.shields.io/badge/Dificultad-Alta-red)
{% elif difficulty == 'medium' %}
![Dificultad](https://img.shields.io/badge/Dificultad-Media-yellow)
{% elif difficulty == 'easy' %}
![Dificultad](https://img.shields.io/badge/Dificultad-Baja-green)
{% else %}
![Dificultad](https://img.shields.io/badge/Dificultad-Sin%20especificar-black)
{% endif %}

{{ activity.description }}

## Contenido

Ficheros de preguntas disponibles en esta actividad:

{% for quiz in activity.quizzes %}

### [{{quiz.filename}}]({{ quiz.filename }})

{% set stats = quiz.get_stats() %}
|   | Tipo              | Cantidad                   |
| - | ----------------- | -------------------------- |
{% for type,count in stats.types.items() %}| ![{{ type }}]({{ icons_url }}/{{ type }}.svg) | [{{ Quiz.SUPPORTED_QUESTIONS[type]['description'] }}](#{{ Quiz.SUPPORTED_QUESTIONS[type]['description'] | anchorify }}) | {{ count }} |
{% endfor %}|   | **TOTAL**         | {{ stats.total }} |

{% for type,questions in quiz.questions.items() %}
#### {{ Quiz.SUPPORTED_QUESTIONS[type]['description'] }}

{% for question in questions %}
![{{ question.image_filename }}](images/{{ question.image_filename }})
{% endfor %}

{% endfor %}

{% endfor %}
