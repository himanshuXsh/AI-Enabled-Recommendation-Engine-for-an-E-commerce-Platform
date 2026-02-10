import pandas as pd
import os

# Change to the script's directory to ensure relative paths work
os.chdir(os.path.dirname(os.path.abspath(__file__)))

def create_placeholder_items():
    print("Checking data files...")
    
    # Check if data folder exists
    if not os.path.exists('data'):
        os.makedirs('data')
        print("Created data/ folder. Please move your CSV files there!")
        return

    try:
        # Load Matrix to get Item IDs
        matrix_path = 'data/user_item_matrix.csv'
        if not os.path.exists(matrix_path):
            print(f"❌ Error: {matrix_path} not found. Move your file here.")
            return

        matrix = pd.read_csv(matrix_path, index_col=0)
        item_ids = matrix.columns.tolist()
        
        # Create Dataframe
        items_df = pd.DataFrame({
            'item_id': item_ids,
            'value': [f"Product #{pid}" for pid in item_ids],
            'property': ['General Category' for _ in item_ids]
        })
        
        # Save
        items_df.to_csv('data/clean_items.csv', index=False)
        print(f"✅ Success! Generated 'data/clean_items.csv' with {len(items_df)} items.")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    create_placeholder_items()
