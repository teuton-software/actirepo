import time
from pprint import pprint
from actirepo.moodle.quiz import Quiz
from actirepo.activity import Activity
from actirepo.category import Category

def main():
    start_time = time.time()
    
    #quiz = Quiz('tests/category/sample1/questions1.xml')
    #print(quiz.generate_images())
    #print(quiz.questions)
    #print(quiz.get_stats())

    #activity = Activity('tests/category/sample1')
    #activity.save()
    #activity.create_readme(True)
    #print(activity.get_stats())

    category = Category('tests/category')
    category.create_readme()

    #Category.create('tests/category', False)

    print(f"Elapsed time: {time.time() - start_time:.2f} s")

if __name__ == "__main__":
    main()

