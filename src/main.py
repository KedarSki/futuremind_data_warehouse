from src.pipeline.distributor_loader import DistributorLoader
from src.pipeline.movie_loader import MovieLoader

def main():
    DistributorLoader().run()
    MovieLoader().run()

if __name__ == "__main__":
    main()