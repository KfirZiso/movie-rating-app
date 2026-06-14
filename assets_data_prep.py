def prepare_data(df):
    # Create a copy to avoid modifying the original dataframe
    X = df.copy()

    # ==========================================
    # 1. Data Cleaning & Type Conversion
    # ==========================================
    
    # Convert runtime to numeric, turning invalid text into NaN
    if 'runtimeMinutes' in X.columns:
        X['runtimeMinutes'] = pd.to_numeric(X['runtimeMinutes'], errors='coerce')

    # Clean 'startYear': convert to numeric, filter out unrealistic years, and use nullable Int
    if 'startYear' in X.columns:
        X['startYear'] = pd.to_numeric(X['startYear'], errors='coerce')
        invalid_years_mask = (X['startYear'].notna()) & ((X['startYear'] < 1000) | (X['startYear'] > 9999))
        X.loc[invalid_years_mask, 'startYear'] = np.nan
        X['startYear'] = X['startYear'].astype('Int64')

    # Clean 'genres': remove list-like brackets, quotes, and handle raw database nulls ('\\N')
    if 'genres' in X.columns:
        X['genres'] = X['genres'].dropna().astype(str)
        X['genres'] = X['genres'].str.replace(r"[\[\]\'\"]", "", regex=True)
        X['genres'] = X['genres'].apply(lambda x: '' if x in ['\\N', 'N', '\\\\N'] else x)

    # Clean 'lead_actors_ids': similar text cleaning as genres, handling string nulls
    if 'lead_actors_ids' in X.columns:
        X['lead_actors_ids'] = X['lead_actors_ids'].fillna('').astype(str)
        X['lead_actors_ids'] = X['lead_actors_ids'].replace(['\\N', '\\\\N', 'N', 'nan', 'None'], '')
        X['lead_actors_ids'] = X['lead_actors_ids'].str.replace(r"[\[\]\'\"]", "", regex=True)

    # ==========================================
    # 2. Text Standardization (Country & Language)
    # ==========================================
    valid_countries_list = [
        'USA', 'United States', 'UK', 'United Kingdom', 'Canada', 'France', 'Germany', 'Italy',
        'Spain', 'Japan', 'China', 'India', 'South Korea', 'Australia', 'Israel', 'Argentina',
        'Brazil', 'Mexico', 'Netherlands', 'Sweden', 'Switzerland', 'Russia', 'Turkey', 'Belgium'
    ]
    valid_languages_list = [
        'English', 'Hebrew', 'Arabic', 'French', 'Spanish', 'German', 'Italian', 'Japanese',
        'Mandarin', 'Cantonese', 'Chinese', 'Korean', 'Russian', 'Hindi', 'Tamil', 'Telugu',
        'Portuguese', 'Dutch', 'Swedish', 'Turkish'
    ]

    # Helper function to extract valid items from noisy scraped text and normalize names
    def clean_scraped_text_to_nan(val, valid_list):
        if pd.isna(val) or val in ['\\N', '\\\\N', 'N', 'nan', 'None', '']:
            return None
        val_str = str(val)
        found_items = []
        for item in valid_list:
            if item.lower() in val_str.lower():
                if item in ['United States', 'USA']: found_items.append('USA')
                elif item in ['United Kingdom', 'UK']: found_items.append('UK')
                else: found_items.append(item)
        found_items = list(set(found_items))
        return ", ".join(found_items) if found_items else None

    # Apply the cleaner function
    if 'Country' in X.columns:
        X['Country'] = X['Country'].apply(lambda x: clean_scraped_text_to_nan(x, valid_countries_list))
    if 'Language' in X.columns:
        X['Language'] = X['Language'].apply(lambda x: clean_scraped_text_to_nan(x, valid_languages_list))

    # ==========================================
    # 3. Target Variable & Data Leakage Prevention
    # ==========================================
    
    # Drop rows missing the target variable to ensure clean training/evaluation
    if 'averageRating' in X.columns:
        X = X.dropna(subset=['averageRating'])

    X = X.reset_index(drop=True)

    # Remove features that cause data leakage (information not available before release)
    leakage_columns = ['numVotes', 'BoxOffice']
    X = X.drop(columns=[col for col in leakage_columns if col in X.columns], errors='ignore')

    # Separate target variable from feature matrix
    if 'averageRating' in X.columns:
        X = X.drop(columns=['averageRating'])

    # Fill remaining NaNs with empty strings for text processing
    if 'genres' in X.columns: X['genres'] = X['genres'].fillna('')
    if 'lead_actors_ids' in X.columns: X['lead_actors_ids'] = X['lead_actors_ids'].fillna('')
    if 'Language' in X.columns: X['Language'] = X['Language'].fillna('')
    if 'Country' in X.columns: X['Country'] = X['Country'].fillna('')

    # ==========================================
    # 4. Feature Engineering
    # ==========================================
    
    # Count the number of genres per movie
    if 'genres' in X.columns:
        X['genre_count'] = X['genres'].apply(lambda x: len([g for g in str(x).split(',') if g.strip()]) if str(x).strip() else 0)
    else:
        X['genre_count'] = 0

    # Binary flag: Movie released during/after the digital era (IMDb founding year)
    if 'startYear' in X.columns:
        X['is_post_imdb'] = (X['startYear'] >= 1991).fillna(False).astype(int)
    else:
        X['is_post_imdb'] = 0

    # Count A-list actors based on a predefined set of high-performing actor IDs
    if 'lead_actors_ids' in X.columns:
        current_top_actors = set(['[]', "'nm0262635'", "'nm0001485'", "['nm0001815'", "['nm0000136'", '"nm0005351"', 'nm0695435', "'nm0000172'", "['nm0000078'", "['nm0000034'", '["nm0000151"', "'nm0001001'", "['nm0000331'", "'nm0413168'", "['nm0001088'", "['nm0000044'", "['nm0000134'", '"nm0476223"', "['nm0000011'", '"nm0000168"', "['nm0001076'", '["nm0394690"', "'nm0000336'", 'nm0342488', "'nm0001522'", 'nm0914612', "'nm0039989'", "['nm0000158'", "'nm0472603'", "'nm0000177'", '["nm0005351"', "'nm0334689'", "'nm0001599'", "['nm0000125'", "'nm0001424'", "'nm0000679'", "['nm0001635'", 'nm0705356', "['nm0001766'", "['nm0001522'", '"nm0000609"', '["nm0000060"', '"nm1347153"', '"nm0034519"', '"nm0001136"', "'nm0491590']", "['nm0000056'", '["nm0136797"', '"nm0682074"', '"nm0000982"', "'nm0001691'", '"nm0001626"', '["nm0000241"', "'nm0000104'", "'nm0001958'", "['nm0000064'", '["nm0001958"', "'nm0000587'", '["nm0265492"', "'nm0000897'", "['nm0000288'", "['nm0000375'", '"nm0667664"', "'nm0000350'", "'nm0749263']", '["nm0001224"', "'nm0000992']", '["nm0222426"', "'nm0914113'", '"nm0613147"', '"nm0005048"', '["nm0000859"', "['nm0001791'", "'nm0000023'", "['nm0000142'", '"nm0000460"', "'nm0428086'", "'nm0000987'", "'nm0654239'", '"nm1043075"', '["nm0000120"', "'nm0000380'", '"nm0101350"', '"nm0005541"', "'nm0000947'", "'nm0927240'", "'nm0090123'", "['nm0001224'", "'nm0662223'", '"nm0129894"', "['nm0001772'", "['nm0000126'", '"nm0505249"', "'nm0877270']", '"nm0000973"', '"nm0001872"', '"nm0001570"', '"nm1258970"', '["nm0000245"', '"nm0000634"', '"nm1443527"', '"nm1706767"', "'nm0000661'", "['nm0198072'", "'nm1399741'", '["nm0001774"', '"nm0669681"', '"nm0628091"', "'nm0182839'", '"nm0827663"', "'nm0721073'", "['nm0000432'", "'nm0001174'", '"nm0451307"', "['nm0000276'", "'nm0041281'", "['nm0000702'", '"nm0001557"', 'nm0002091', '["nm0000858"', 'nm0177896', "'nm0570615']", "['nm1940449'", "'nm0875861'", '"nm0912001"', "'nm14476135'", '["nm0005327"', "'nm1297015'", "'nm0005196'", "['nm0000947'", "'nm0233352'", "'nm0837959'", '"nm0446672"]', "'nm0108406'", "'nm0000554'", '["nm0002071"', '"nm0000242"', "['nm0000401'", "'nm0002332'", "['nm0912487'", "['nm0000219'", '["nm0000598"', '"nm0316079"', "'nm0206478'", "'nm1716941'", "'nm0169806']", '["nm0654110"', "'nm0005162']", '"nm0225419"', "'nm0388872'", "'nm0173735'", "'nm0001695'", "['nm1431656'", "['nm0041405'", "'nm0000173'", "'nm0001520'", "'nm0132257'", '"nm0534317"', "'nm0000271'", "['nm0001428'", "'nm0001800'", '"nm0000174"', "'nm0000730'", "'nm0000079'", "'nm0007220'", 'nm0004874', 'nm0757855', 'nm1176985', "'nm0000308'", "['nm0634159'", "'nm0448765'", '["nm0124930"', "'nm0218131'", "'nm0001028'", '"nm0507212"', '["nm0000140"', "['nm0004496'", "['nm0318105'", "'nm0000840'", "'nm0943978'", '"nm0958335"', "'nm0001624']", "'nm1343961'", "'nm0000932'", "['nm0000621'", "['nm0425005'", "['nm0000102'", "'nm0187981'", "'nm0799777'", "'nm0843401'", '"nm0048414"', "'nm0803785'", "'nm1431940'", '["nm0000336"', '"nm0004496"', '"nm0525601"', '"nm0671738"]', "'nm0000210'", "'nm0910278'", "['nm0228715'", '"nm0001434"', "['nm0400998'", "['nm0438463'", "'nm0004866'", "'nm0269647'", "['nm0706368'", "'nm0001656'", "'nm0000039'", '"nm0860233"', '"nm0227759"', '"nm0007234"', '["nm0000177"', '"nm0000177"', "'nm0415591'", '"nm0403134"', "'nm0867694'", "'nm0000763'", '"nm1683094"', "'nm2225369'", "['nm0428065'", "'nm0480465'", "['nm5397459'", "'nm3915784'", "'nm1209966'", '"nm0001800"', "'nm0666604'", "'nm0611898'", '["nm0947447"', "'nm0000748']", "'nm0832011'", "'nm0440514'", "'nm4928333'", '"nm0000547"', '"nm0306786"', "['nm0000140'", "'nm0000375'", '"nm0001993"', "['nm0001062'", '"nm0623762"', '"nm0202966"', '"nm0397928"', "'nm0019996'", "'nm0179154'", '"nm0112043"', "'nm0001884'", '["nm0000152"', "'nm0000244'", "'nm0757855'", "['nm0941777'", '"nm0045741"', "'nm10771694'", "['nm0000009'", "['nm0322513'", "'nm0000744'", "'nm0000959'", "['nm0000560'", "'nm0000130'", '"nm2812744"', "'nm0000286'", "'nm0407959'", "'nm0000704'", "'nm0483653']", "'nm0000518'", "'nm0166706'", "'nm0369814'", "'nm0268225'", '"nm0000336"', "'nm0000169'", '"nm0698764"', '["nm0000277"', '["nm0001791"', '["nm0000199"', "'nm0000099'", '"nm0433150"', '"nm0557339"', "'nm0574534'", "'nm0005212'", '"nm0000502"', "'nm6533985'", "'nm0006893'", "'nm0735442'", "'nm0000149'", "'nm0140865'", '"nm0870543"', "['nm0682074'", "'nm0001191'", "['nm0185819'", "'nm0254975'", "['nm0000297'", "'nm0000204'", "['nm1165110'", "'nm0380965'", "'nm0587534']", "'nm0001701'", '"nm0001520"]', "'nm0000496'", '"nm0001283"', "['nm0000424'", "'nm0000114'", "'nm0436642'"])

        def count_a_listers(actors_str):
            if str(actors_str).strip() == '':
                return 0
            movie_actors = [a.strip() for a in str(actors_str).split(',')]
            return sum(1 for a in movie_actors if a in current_top_actors)

        X['num_a_list_actors'] = X['lead_actors_ids'].apply(count_a_listers)
    else:
        X['num_a_list_actors'] = 0

    # Create binary flags for English language and USA origin
    if 'Language' in X.columns:
        X['is_english'] = X['Language'].apply(lambda x: 1 if 'English' in str(x) else 0)
    else:
        X['is_english'] = 0

    if 'Country' in X.columns:
        X['is_usa'] = X['Country'].apply(lambda x: 1 if 'USA' in str(x) or 'United States' in str(x) else 0)
    else:
        X['is_usa'] = 0

    # Categorize runtime into bins (1: Short, 2: Medium, 3: Long) for better model interpretability
    if 'runtimeMinutes' in X.columns:
        X['runtime_category_num'] = pd.cut(
            X['runtimeMinutes'],
            bins=[0, 85, 130, 1000],
            labels=[1, 2, 3],
            ordered=True
        ).astype(float)
    else:
        X['runtime_category_num'] = np.nan

    # Perform custom One-Hot Encoding for the most common genres
    top_genres = ['Action', 'Comedy', 'Drama', 'Thriller', 'Romance', 'Sci-Fi', 'Horror', 'Documentary']
    for genre in top_genres:
        if 'genres' in X.columns:
            X[f'genre_{genre}'] = X['genres'].apply(lambda x: 1 if genre in str(x) else 0)
        else:
            X[f'genre_{genre}'] = 0

    # Ensure all remaining categorical/string features are cast to 'object' 
    # to avoid Scikit-Learn Pipeline errors with Pandas' new StringDtype
    categorical_cols = X.select_dtypes(include=['object', 'string']).columns
    for col in categorical_cols:
        X[col] = X[col].astype(object)

    # ==========================================
    # 5. Final Feature Selection
    # ==========================================
    
    # Drop raw text, IDs, and redundant columns before returning the final feature set
    cols_to_drop = [
        'tconst', 'primaryTitle', 'plot',
        'startYear', 'genres', 'lead_actors_ids',
        'Language', 'Country', 'budget'
    ]
    X = X.drop(columns=[col for col in cols_to_drop if col in X.columns], errors='ignore')

    return X