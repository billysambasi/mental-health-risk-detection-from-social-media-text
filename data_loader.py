import pandas as pd
import os
from pathlib import Path

class MentalHealthDataLoader:
    def __init__(self, base_path="src/data/raw"):
        self.base_path = Path(base_path)
        self.adhd_path = self.base_path / "ADHD_Reddit_dataset"
        self.mental_health_path = self.base_path / "Mental_Health_datasets"
    
    def _read_csv_safe(self, filepath):
        """Safely read CSV with multiple encoding attempts"""
        encodings = ['utf-8', 'latin-1', 'iso-8859-1', 'cp1252']
        
        for encoding in encodings:
            try:
                return pd.read_csv(filepath, encoding=encoding, low_memory=False)
            except UnicodeDecodeError:
                continue
            except Exception as e:
                print(f"Error reading {filepath} with {encoding}: {e}")
                continue
        
        print(f"Failed to read {filepath} with any encoding")
        return None
    
    def load_adhd_data(self):
        """Load ADHD-related datasets"""
        data = {}
        adhd_files = {
            'adhd_comments': 'ADHD-comment.csv',
            'adhd_posts': 'ADHD.csv',
            'adhd_women_comments': 'adhdwomen-comment.csv',
            'adhd_women_posts': 'adhdwomen.csv'
        }
        
        for key, filename in adhd_files.items():
            filepath = self.adhd_path / filename
            if filepath.exists():
                df = self._read_csv_safe(filepath)
                if df is not None:
                    data[key] = df
        
        return data
    
    def load_mental_health_data(self):
        """Load general mental health datasets"""
        data = {}
        mh_files = {
            'conversations': 'Conversation.csv',
            'depression_reddit': 'depression_dataset_reddit_cleaned.csv',
            'health_anxiety': 'healthanxiety_dataset.csv',
            'reddit_mental_health': 'reddit_mental_health_data.csv',
            'stress': 'Stress.csv',            
            'suicide_ideation': 'Suicide_Ideation_Dataset.csv'
        }
        
        for key, filename in mh_files.items():
            filepath = self.mental_health_path / filename
            if filepath.exists():
                try:
                    if filename.endswith('.xlsx'):
                        data[key] = pd.read_excel(filepath)
                    else:
                        df = self._read_csv_safe(filepath)
                        if df is not None:
                            data[key] = df
                except Exception as e:
                    print(f"Failed to load {key}: {e}")
        
        return data
    
    def load_all_data(self):
        """Load all datasets"""
        all_data = {}
        all_data.update(self.load_adhd_data())
        all_data.update(self.load_mental_health_data())
        return all_data
    
    def get_dataset_info(self):
        """Get information about all datasets"""
        all_data = self.load_all_data()
        info = {}
        
        for name, df in all_data.items():
            info[name] = {
                'shape': df.shape,
                'columns': list(df.columns),
                'memory_usage': f"{df.memory_usage(deep=True).sum() / 1024**2:.2f} MB"
            }
        
        return info

# # Usage functions
# def load_data():
#     """Quick function to load all data"""
#     loader = MentalHealthDataLoader()
#     return loader.load_all_data()

# def get_data_info():
#     """Quick function to get dataset information"""
#     loader = MentalHealthDataLoader()
#     return loader.get_dataset_info()