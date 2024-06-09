from companies import load_companies
from profiles import load_profiles
from jobs import load_jobs

def main():
    print("Loading data...")
    load_companies()
    load_profiles()
    load_jobs()
    print("Data loaded.")

if __name__ == "__main__":
    main()