import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# Import data (Make sure to parse dates. Consider setting index column to 'date'.)
df = pd.read_csv('fcc-forum-pageviews.csv', parse_dates=['date'], index_col='date')


# Clean data
df = df[(df['value']>df['value'].quantile(0.025)) & (df['value'] < df['value'].quantile(0.975))]


def draw_line_plot():
    # Draw line plot

    #for some reason this is not working and the figsize has to be set in the plot function
    #fig = plt.figure(figsize=(20, 10))

    fig = df.plot(title='Daily freeCodeCamp Forum Page Views 5/2016-12/2019', xlabel='Date', ylabel='Page Views', color='red', legend=False, layout='tight', figsize=(18, 6)) 
    fig = sns.lineplot(data=df, x='date', y='value', color='red').figure



    # Save image and return fig (don't change this part)
    fig.savefig('line_plot.png')
    return fig

def draw_bar_plot():
    # Copy and modify data for monthly bar plot
    df_bar = df.copy()
    
    #date column is the index column, check line 8 - cannot be called by 'date' name
    df_bar["year"] = df_bar.index.year
    df_bar["months"] = df_bar.index.month_name()
    df_bar = df_bar.groupby(["year", "months"])["value"].mean().round(0)
    
    df_bar = df_bar.unstack(level=-1, fill_value=0)

    #reorder months in correct order
    df_bar = df_bar[['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']] 
    #print(df_bar)

    # Draw bar plot
    fig = df_bar.plot(xlabel='Years', ylabel='Average Page Views', kind='bar', figsize=(10, 10)).figure
    
    # Save image and return fig (don't change this part)
    fig.savefig('bar_plot.png')
    return fig

def draw_box_plot():
    # Prepare data for box plots (this part is done!)
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box['Year'] = [d.year for d in df_box.date]
    df_box['Month'] = [d.strftime('%b') for d in df_box.date]

    # Draw box plots (using Seaborn)
    df_box = df_box.rename(columns={'value': 'Page Views'})

    print(df_box)

    fig, (ax1, ax2) = plt.subplots(1, 2)
    fig.set_figwidth(20)
    ax1.title.set_text('Year-wise Box Plot (Trend)')
    ax2.title.set_text('Month-wise Box Plot (Seasonality)')
    ax1 = sns.boxplot(data=df_box, x='Year', y='Page Views', ax=ax1, palette='hsv')
    ax2 = sns.boxplot(data=df_box, x='Month', y='Page Views', ax=ax2, palette='hsv', order=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])    

    # Save image and return fig (don't change this part)
    fig.savefig('box_plot.png')
    return fig
