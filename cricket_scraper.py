import pandas as pd
import requests
from bs4 import BeautifulSoup
import time
import random
from datetime import datetime

class CricketDataCollector:
    """
    Multi-source Cricket World Cup Data Collector
    Includes: Wikipedia scraping, Kaggle download, and sample data generator
    """
    
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
    
    # ========== METHOD 1: WIKIPEDIA SCRAPING (MOST RELIABLE) ==========
    
    def scrape_wikipedia_world_cups(self):
        """
        Scrape Cricket World Cup data from Wikipedia
        """
        print("\n" + "="*70)
        print("METHOD 1: SCRAPING FROM WIKIPEDIA")
        print("="*70 + "\n")
        
        url = "https://en.wikipedia.org/wiki/Cricket_World_Cup"
        
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Find the results table
            tables = soup.find_all('table', class_='wikitable')
            
            tournaments = []
            for table in tables:
                rows = table.find_all('tr')[1:]  # Skip header
                for row in rows:
                    cols = row.find_all('td')
                    if len(cols) >= 4:
                        try:
                            tournament = {
                                'year': cols[0].text.strip(),
                                'host': cols[1].text.strip(),
                                'winner': cols[2].text.strip() if len(cols) > 2 else None,
                                'runner_up': cols[3].text.strip() if len(cols) > 3 else None,
                            }
                            tournaments.append(tournament)
                        except:
                            continue
            
            df = pd.DataFrame(tournaments)
            print(f"✓ Scraped {len(df)} World Cup tournaments")
            return df
            
        except Exception as e:
            print(f"✗ Wikipedia scraping failed: {e}")
            return pd.DataFrame()
    
    def scrape_wikipedia_batting_records(self):
        """
        Scrape batting records from Wikipedia
        """
        print("\nScraping batting records from Wikipedia...")
        
        url = "https://en.wikipedia.org/wiki/List_of_Cricket_World_Cup_records"
        
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')
            
            tables = soup.find_all('table', class_='wikitable')
            
            batting_records = []
            
            # Look for batting tables
            for table in tables[:5]:  # Check first few tables
                rows = table.find_all('tr')[1:]
                for row in rows:
                    cols = row.find_all(['td', 'th'])
                    if len(cols) >= 3:
                        try:
                            record = {
                                'player': cols[0].text.strip(),
                                'country': cols[1].text.strip() if len(cols) > 1 else None,
                                'stat_value': cols[2].text.strip() if len(cols) > 2 else None,
                            }
                            batting_records.append(record)
                        except:
                            continue
            
            df = pd.DataFrame(batting_records)
            print(f"✓ Scraped {len(df)} batting records")
            return df
            
        except Exception as e:
            print(f"✗ Batting records scraping failed: {e}")
            return pd.DataFrame()
    
    # ========== METHOD 2: KAGGLE DATASET DOWNLOAD ==========
    
    def download_from_kaggle(self, dataset_name="rohanrao/cricket-world-cup-2023"):
        """
        Download Cricket dataset from Kaggle
        Requires: pip install kaggle
        Setup: Place kaggle.json in ~/.kaggle/
        """
        print("\n" + "="*70)
        print("METHOD 2: KAGGLE DATASET DOWNLOAD")
        print("="*70 + "\n")
        
        try:
            import kaggle
            
            print(f"Downloading dataset: {dataset_name}")
            kaggle.api.dataset_download_files(dataset_name, path='./kaggle_data', unzip=True)
            print(f"✓ Dataset downloaded to ./kaggle_data/")
            
            # List downloaded files
            import os
            files = os.listdir('./kaggle_data')
            print(f"✓ Files downloaded: {files}")
            
        except ImportError:
            print("✗ Kaggle library not installed. Run: pip install kaggle")
            print("   Also setup Kaggle API: https://github.com/Kaggle/kaggle-api")
        except Exception as e:
            print(f"✗ Kaggle download failed: {e}")
    
    # ========== METHOD 3: GENERATE REALISTIC SAMPLE DATA ==========
    
    def generate_sample_dataset(self, num_matches=100, num_players=50):
        """
        Generate realistic sample Cricket World Cup data
        Perfect for testing and dashboard development
        """
        print("\n" + "="*70)
        print("METHOD 3: GENERATING SAMPLE DATASET")
        print("="*70 + "\n")
        
        # Countries
        countries = ['India', 'Australia', 'England', 'Pakistan', 'South Africa', 
                    'New Zealand', 'West Indies', 'Sri Lanka', 'Bangladesh', 'Afghanistan']
        
        # Players by country
        indian_players = ['Virat Kohli', 'Rohit Sharma', 'Sachin Tendulkar', 'MS Dhoni', 'Hardik Pandya']
        australian_players = ['Ricky Ponting', 'Adam Gilchrist', 'Steve Smith', 'David Warner', 'Glenn Maxwell']
        england_players = ['Joe Root', 'Jos Buttler', 'Ben Stokes', 'Eoin Morgan', 'Jonny Bairstow']
        
        all_players = {
            'India': indian_players,
            'Australia': australian_players,
            'England': england_players,
            'Pakistan': ['Babar Azam', 'Shaheen Afridi', 'Mohammad Rizwan'],
            'South Africa': ['AB de Villiers', 'Quinton de Kock', 'Kagiso Rabada'],
        }
        
        # Venues
        venues = [
            {'name': 'Wankhede Stadium', 'city': 'Mumbai', 'country': 'India', 'lat': 18.9388, 'lon': 72.8258},
            {'name': 'Eden Gardens', 'city': 'Kolkata', 'country': 'India', 'lat': 22.5645, 'lon': 88.3433},
            {'name': 'M. Chinnaswamy Stadium', 'city': 'Bangalore', 'country': 'India', 'lat': 12.9791, 'lon': 77.5998},
            {'name': 'Narendra Modi Stadium', 'city': 'Ahmedabad', 'country': 'India', 'lat': 23.0938, 'lon': 72.5950},
            {'name': "Lord's Cricket Ground", 'city': 'London', 'country': 'England', 'lat': 51.5294, 'lon': -0.1728},
            {'name': 'The Oval', 'city': 'London', 'country': 'England', 'lat': 51.4839, 'lon': -0.1146},
            {'name': 'MCG', 'city': 'Melbourne', 'country': 'Australia', 'lat': -37.8200, 'lon': 144.9834},
            {'name': 'SCG', 'city': 'Sydney', 'country': 'Australia', 'lat': -33.8915, 'lon': 151.2246},
        ]
        
        # Generate Matches
        print("Generating match data...")
        matches = []
        for i in range(num_matches):
            team1, team2 = random.sample(countries, 2)
            venue = random.choice(venues)
            winner = random.choice([team1, team2])
            
            match = {
                'match_id': f'WC_{2015 + i//20}_{i%20 + 1}',
                'tournament_year': 2015 + (i // 20),
                'date': f'2015-0{(i%9)+1}-{(i%28)+1:02d}',
                'venue': venue['name'],
                'city': venue['city'],
                'country': venue['country'],
                'team1': team1,
                'team2': team2,
                'team1_score': random.randint(200, 400),
                'team2_score': random.randint(180, 380),
                'winner': winner,
                'margin': f'{random.randint(1, 100)} runs' if random.random() > 0.5 else f'{random.randint(1, 9)} wickets',
                'toss_winner': random.choice([team1, team2]),
                'toss_decision': random.choice(['bat', 'field']),
            }
            matches.append(match)
        
        df_matches = pd.DataFrame(matches)
        print(f"✓ Generated {len(df_matches)} matches")
        
        # Generate Player Statistics
        print("Generating player statistics...")
        players = []
        for country, player_list in all_players.items():
            for player in player_list:
                for year in [2015, 2019, 2023]:
                    player_stat = {
                        'player_name': player,
                        'country': country,
                        'tournament_year': year,
                        'matches': random.randint(5, 11),
                        'innings': random.randint(5, 11),
                        'runs': random.randint(200, 800),
                        'highest_score': random.randint(50, 183),
                        'average': round(random.uniform(30.0, 60.0), 2),
                        'strike_rate': round(random.uniform(80.0, 140.0), 2),
                        'hundreds': random.randint(0, 4),
                        'fifties': random.randint(0, 6),
                        'fours': random.randint(20, 80),
                        'sixes': random.randint(5, 30),
                        'balls_faced': random.randint(200, 800),
                        'wide_balls_bowled': random.randint(0, 15),  # For bowling
                        'no_balls_bowled': random.randint(0, 8),
                    }
                    players.append(player_stat)
        
        df_players = pd.DataFrame(players)
        print(f"✓ Generated statistics for {len(df_players)} player-tournament combinations")
        
        # Generate Team Statistics
        print("Generating team statistics...")
        teams = []
        for country in countries:
            for year in [2015, 2019, 2023]:
                team_stat = {
                    'team_name': country,
                    'tournament_year': year,
                    'matches_played': random.randint(8, 12),
                    'matches_won': random.randint(4, 10),
                    'matches_lost': random.randint(2, 6),
                    'matches_tied': random.randint(0, 1),
                    'total_runs': random.randint(2000, 4000),
                    'total_wickets': random.randint(70, 120),
                    'highest_score': random.randint(300, 417),
                    'lowest_score': random.randint(100, 200),
                    'win_percentage': round(random.uniform(40.0, 85.0), 2),
                }
                teams.append(team_stat)
        
        df_teams = pd.DataFrame(teams)
        print(f"✓ Generated statistics for {len(df_teams)} team-tournament combinations")
        
        # Venues DataFrame
        df_venues = pd.DataFrame(venues)
        
        # Add performance data for India at venues
        india_venue_performance = []
        for venue in venues:
            perf = {
                'team': 'India',
                'venue': venue['name'],
                'city': venue['city'],
                'country': venue['country'],
                'latitude': venue['lat'],
                'longitude': venue['lon'],
                'matches_played': random.randint(5, 20),
                'matches_won': random.randint(3, 15),
                'win_percentage': round(random.uniform(50.0, 85.0), 2),
                'avg_runs_scored': random.randint(250, 320),
            }
            india_venue_performance.append(perf)
        
        df_india_venues = pd.DataFrame(india_venue_performance)
        print(f"✓ Generated venue performance data for India")
        
        return {
            'matches': df_matches,
            'players': df_players,
            'teams': df_teams,
            'venues': df_venues,
            'india_venues': df_india_venues
        }
    
    # ========== SAVE DATA ==========
    
    def save_datasets(self, data_dict, output_dir='cricket_data'):
        """
        Save all datasets to CSV files
        """
        import os
        
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        print(f"\n{'='*70}")
        print("SAVING DATASETS")
        print(f"{'='*70}\n")
        
        for name, df in data_dict.items():
            if not df.empty:
                filename = f'{output_dir}/{name}.csv'
                df.to_csv(filename, index=False)
                print(f"✓ Saved: {filename} ({len(df)} records)")
        
        print(f"\n{'='*70}")
        print("✓ ALL DATA SAVED SUCCESSFULLY!")
        print(f"{'='*70}\n")
        print(f"📁 Location: ./{output_dir}/")
        print("\nNext Steps:")
        print("1. Open Google Looker Studio")
        print("2. Upload these CSV files as data sources")
        print("3. Start building your dashboard!")


# ========== MAIN EXECUTION ==========

def main():
    collector = CricketDataCollector()
    
    print("\n" + "🏏"*35)
    print("   CRICKET WORLD CUP DATA COLLECTION SUITE")
    print("🏏"*35 + "\n")
    
    # Try Wikipedia first (most reliable)
    wiki_data = {}
    
    print("Attempting Wikipedia scraping...")
    df_tournaments = collector.scrape_wikipedia_world_cups()
    if not df_tournaments.empty:
        wiki_data['tournaments'] = df_tournaments
    
    df_batting = collector.scrape_wikipedia_batting_records()
    if not df_batting.empty:
        wiki_data['batting_records'] = df_batting
    
    # Generate comprehensive sample dataset
    print("\n" + "="*70)
    print("GENERATING COMPREHENSIVE SAMPLE DATASET")
    print("(Recommended for dashboard development)")
    print("="*70)
    
    sample_data = collector.generate_sample_dataset(num_matches=150, num_players=50)
    
    # Combine Wikipedia and sample data
    all_data = {**wiki_data, **sample_data}
    
    # Save everything
    collector.save_datasets(all_data)
    
    # Display preview
    print("\n" + "="*70)
    print("DATA PREVIEW")
    print("="*70 + "\n")
    
    if 'matches' in all_data:
        print("📊 MATCHES (First 5 rows):")
        print(all_data['matches'].head())
        print("\n")
    
    if 'players' in all_data:
        print("🏏 PLAYER STATISTICS (First 5 rows):")
        print(all_data['players'].head())
        print("\n")
    
    if 'india_venues' in all_data:
        print("📍 INDIA VENUE PERFORMANCE:")
        print(all_data['india_venues'].head())


if __name__ == "__main__":
    main()