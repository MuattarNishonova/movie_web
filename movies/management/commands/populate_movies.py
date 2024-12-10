import random
from faker import Faker
from django.core.management.base import BaseCommand
from movies.models import Movie, Genre, MovieGenre, QualityChoices, MovieStatusChoices, MovieTypeChoices

fake = Faker()


file_names = [
    'movie_images/bridge_to_terabithia.jpg', 'movie_images/do_not_knock_twice.jpg',
    'movie_images/frozen.jpeg','movie_images/home_alone.jpeg',
    'movie_images/inside_out2.jpeg','movie_images/moana2.jpg',
    'movie_images/the_day_after_tomorrow.jpg','movie_images/zootopia.jpeg'
]
movie_title = [
    'Bridge To Terabithia', 'Do Not Knock Twice','Frozen',
    'Home Alone', 'Inside Out 2','Moana 2', 'The Day After Tomorrow','Zootopia'
]
video_files = [
    'movies/bridge_to_terabithia.mp4', 'movies/do_not_knock_twice.mp4',
    'movies/frozen.mp4','movies/home_alone.mp4',
    'movies/inside_out2.mp4','movies/moana2.mp4',
    'movies/the_day_after_tomorrow.mp4','movies/zootopia.mp4'
]

class Command(BaseCommand):
    help = "Populate the database with random movies and genres"

    def handle(self, *args, **kwargs):
        self.create_genres()
        self.create_movies()
        self.stdout.write(self.style.SUCCESS("Successfully populated the database!"))

    def create_genres(self):
        genres = ['Action', 'Comedy', 'Drama', 'Horror', 'Sci-Fi', 'Documentary']
        for genre_name in genres:
            Genre.objects.get_or_create(name=genre_name)

    def create_movies(self):
        genres = list(Genre.objects.all())
        for i in range(8):  # Adjust the number of movies as needed
            movie = Movie.objects.create(
                title=movie_title[i],
                description=fake.paragraph(nb_sentences=random.randrange(5, 10)),
                duration=random.randint(80, 180),
                movie_type=fake.word(ext_word_list=["Action", "Romance", "Thriller", "Animation"]),
                studios=fake.company(),
                release_date=fake.date_between(start_date="-10y", end_date="today"),
                rating=round(random.uniform(5, 10), 1),
                views=random.randint(100, 10000),
                quality=random.choice([choice[0] for choice in QualityChoices.choices]),
                scores=round(random.uniform(4, 10), 1),
                status=random.choice([choice[0] for choice in MovieStatusChoices.choices]),
                type=random.choice([choice[0] for choice in MovieTypeChoices.choices]),
                image=file_names[i],
                video=video_files[i],
                thumb=video_files[i]
            )
            movie.save()

            # Assign random genres to the movie
            assigned_genres = random.sample(genres, random.randint(1, 3))
            for genre in assigned_genres:
                MovieGenre.objects.create(movie=movie, genre=genre)
