from src.pipeline.distributor_loader import DistributorLoader
from src.pipeline.fact_revenue_loader import FactRevenueLoader
from src.pipeline.movie_loader import MovieLoader

def main():
    DistributorLoader().run()
    MovieLoader().run()
    FactRevenueLoader().run()

if __name__ == "__main__":
    main()