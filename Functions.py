
import gams
import pandas as pd

def symbol_to_df(db, symbol, cols='None'):
    """
    Loads a symbol from a GDX database into a pandas dataframe

    Args:
        db (GamsDatabase): The loaded gdx file
        symbol (string): The wanted symbol in the gdx file
        cols (list): The columns
    """   
    df = dict( (tuple(rec.keys), rec.value) for rec in db[symbol] )
    df = pd.DataFrame(df, index=['Value']).T.reset_index() # Convert to dataframe
    if cols != 'None':
        try:
            df.columns = cols
        except:
            pass
    return df 

def gdx_to_dict(symbolBal,scenarios,system_directory,file_path):
    """
    create dictionary of balmorel & optiflow parameters
    input:
    1) strings of parameters to read from Balmorel
    2) strings of parameters to read from OptiFlow
    3) strings of scenarios to read in the format ..MainResults_SCENARIO.gdx 
    output:
    1) a dictionary of dataframes for the chosen parameters
    """
    # open gams workspace
    gams_sys_dir = system_directory
    ws = gams.GamsWorkspace(system_directory=gams_sys_dir)
    # location of GDX files
    gdx_file_path = file_path
    # make room for dataframes
    dfsBal = {symbol : pd.DataFrame({}) for symbol in symbolBal}
    
    for scenario in scenarios:
        # Fetch gdx files
        file1 = gdx_file_path + "\\MainResults_" + scenario + ".gdx"
        gdx_file1 = ws.add_database_from_gdx(file1)
        # Converting to dataframes and putting in dictionary
        for symbol in symbolBal:
            temp = symbol_to_df(gdx_file1, symbol)
            temp["Scenario"] = scenario
            dfsBal[symbol] = pd.concat((dfsBal[symbol],temp))
        dfs = dfsBal
    print("Finished, making dictionary of dataframes.")
    print("")
    return dfs
