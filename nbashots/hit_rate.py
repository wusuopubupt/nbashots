import requests
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle, Arc
import pandas as pd
import config

def draw_court(ax=None, color='gray', lw=1, outer_lines=False):
    """Returns an axes with a basketball court drawn onto to it.

    This function draws a court based on the x and y-axis values that the NBA
    stats API provides for the shot chart data.  For example the center of the
    hoop is located at the (0,0) coordinate.  Twenty-two feet from the left of
    the center of the hoop in is represented by the (-220,0) coordinates.
    So one foot equals +/-10 units on the x and y-axis.

    Parameters
    ----------
    ax : Axes, optional
        The Axes object to plot the court onto.
    color : matplotlib color, optional
        The color of the court lines.
    lw : float, optional
        The linewidth the of the court lines.
    outer_lines : boolean, optional
        If `True` it draws the out of bound lines in same style as the rest of
        the court.

    Returns
    -------
    ax : Axes
        The Axes object with the court on it.

    """
    if ax is None:
        ax = plt.gca()

    # Create the various parts of an NBA basketball court

    # Create the basketball hoop
    hoop = Circle((0, 0), radius=7.5, linewidth=lw, color=color, fill=False)

    # Create backboard
    backboard = Rectangle((-30, -12.5), 60, 0, linewidth=lw, color=color)

    # The paint
    # Create the outer box 0f the paint, width=16ft, height=19ft
    outer_box = Rectangle((-80, -47.5), 160, 190, linewidth=lw, color=color,
                          fill=False)
    # Create the inner box of the paint, widt=12ft, height=19ft
    inner_box = Rectangle((-60, -47.5), 120, 190, linewidth=lw, color=color,
                          fill=False)

    # Create free throw top arc
    top_free_throw = Arc((0, 142.5), 120, 120, theta1=0, theta2=180,
                         linewidth=lw, color=color, fill=False)
    # Create free throw bottom arc
    bottom_free_throw = Arc((0, 142.5), 120, 120, theta1=180, theta2=0,
                            linewidth=lw, color=color, linestyle='dashed')
    # Restricted Zone, it is an arc with 4ft radius from center of the hoop
    restricted = Arc((0, 0), 80, 80, theta1=0, theta2=180, linewidth=lw,
                     color=color)

    # Three point line
    # Create the right side 3pt lines, it's 14ft long before it arcs
    corner_three_a = Rectangle((-220, -47.5), 0, 140, linewidth=lw,
                               color=color)
    # Create the right side 3pt lines, it's 14ft long before it arcs
    corner_three_b = Rectangle((220, -47.5), 0, 140, linewidth=lw, color=color)
    # 3pt arc - center of arc will be the hoop, arc is 23'9" away from hoop
    three_arc = Arc((0, 0), 475, 475, theta1=22, theta2=158, linewidth=lw,
                    color=color)

    # Center Court
    center_outer_arc = Arc((0, 422.5), 120, 120, theta1=180, theta2=0,
                           linewidth=lw, color=color)
    center_inner_arc = Arc((0, 422.5), 40, 40, theta1=180, theta2=0,
                           linewidth=lw, color=color)

    # List of the court elements to be plotted onto the axes
    court_elements = [hoop, backboard, outer_box, inner_box, top_free_throw,
                      bottom_free_throw, restricted, corner_three_a,
                      corner_three_b, three_arc, center_outer_arc,
                      center_inner_arc]

    if outer_lines:
        # Draw the half court line, baseline and side out bound lines
        outer_lines = Rectangle((-250, -47.5), 500, 470, linewidth=lw,
                                color=color, fill=False)
        court_elements.append(outer_lines)

    # Add the court elements onto the axes
    for element in court_elements:
        ax.add_patch(element)

    return ax

# Fix non-browser request issue
HEADERS = {'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'}

# Get the webpage containing the data
response = requests.get(config.shot_chart_url, headers=HEADERS)
   
# Grab the headers to be used as column headers for our DataFrame
headers = response.json()['resultSets'][0]['headers']
# Grab the shot chart dat v   deda
shots = response.json()['resultSets'][0]['rowSet']

# pandas groupby sum
shot_df = pd.DataFrame(shots, columns=headers)
grouped = shot_df.groupby([shot_df['SHOT_TYPE'], shot_df['SHOT_ZONE_AREA']])
for (shot_type, shot_zone_area), group in grouped:
    print shot_type, shot_zone_area, group['SHOT_MADE_FLAG'].sum(), group['SHOT_ATTEMPTED_FLAG'].sum(), group['SHOT_MADE_FLAG'].mean()

# View the head of the DataFrame and all its columns
from IPython.display import display
with pd.option_context('display.max_columns', None):
    display(shot_df.head(200))
 
# create a 15:28 window
plt.figure(figsize=(7.5, 14))
# draw scatter plot by x and y
"""
  =====   =======
      Alias   Color
      =====   =======
      'b'     blue
      'g'     green
      'r'     red
      'c'     cyan
      'm'     magenta
      'y'     yellow
      'k'     black
      'w'     white
      =====   =======
"""
plt.scatter(shot_df.LOC_X, shot_df.LOC_Y, c='r', alpha=0.4)
draw_court(outer_lines=True)
# Descending values along the axis from left to right
plt.xlim(300, -300)

font = {'family': 'serif',
        'color':  'black',
        'weight': 'normal',
        'size': 16,
        }

for (shot_type, shot_zone_area), group in grouped:
    hit_rate = str(round(group['SHOT_MADE_FLAG'].mean() * 100, 2))+'%'
    
    if shot_type == '2PT Field Goal':
        if shot_zone_area == 'Center(C)':
            plt.text(0, 50, hit_rate,fontdict=font)
        if shot_zone_area == 'Left Side Center(LC)':
            plt.text(150, 120, hit_rate,fontdict=font)
        if shot_zone_area == 'Left Side(L)':
            plt.text(250, 50, hit_rate,fontdict=font)
        if shot_zone_area == 'Right Side Center(RC)':
            plt.text(-150, 120, hit_rate,fontdict=font)
        if shot_zone_area == 'Right Side(R)':
            plt.text(-130, 50, hit_rate,fontdict=font)
    elif shot_type == '3PT Field Goal':
        if shot_zone_area == 'Back Court(BC)':
            plt.text(0, 400, hit_rate,fontdict=font)
        if shot_zone_area == 'Center(C)':
            plt.text(0, 300, hit_rate,fontdict=font)
        if shot_zone_area == 'Left Side Center(LC)':
            plt.text(150, 250, hit_rate,fontdict=font)
        if shot_zone_area == 'Left Side(L)':
            plt.text(200, 20, hit_rate,fontdict=font)
        if shot_zone_area == 'Right Side Center(RC)':
            plt.text(-150, 250, hit_rate,fontdict=font)
        if shot_zone_area == 'Right Side(R)':
            plt.text(-200, 20, hit_rate,fontdict=font)
        

            
plt.show()
