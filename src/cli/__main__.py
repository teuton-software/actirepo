import time
from actirepo.moodle.quiz import Quiz
from actirepo.activity import Activity

def main():
    start_time = time.time()
    
    #quiz = Quiz('tests/sample1/questions.xml')
    #print(quiz.generate_images())
    #print(quiz.questions)
    #print(quiz.get_stats())

    activity = Activity('tests/sample1')
    #activity.save()
    activity.create_readme(force=True)

    print(f"Elapsed time: {time.time() - start_time:.2f} s")

if __name__ == "__main__":
    main()

