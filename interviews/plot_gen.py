
# views.py
import matplotlib.pyplot as plt
from django.http import HttpResponse
from django.utils import timezone
from datetime import timedelta,datetime
from collections import defaultdict
from interviews.models import Interview 
import io,base64,mpld3,urllib, base64
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime



# Define a function to get consecutive dates
def get_consecutive_dates(start_date, end_date):
    # Create a lambda function for incrementing the date
    increment_date = lambda date: date + timedelta(days=1)
    
    # Generate consecutive dates using a list comprehension
    consecutive_dates = []
    current_date = start_date
    
    while current_date <= end_date:
        consecutive_dates.append(current_date)
        current_date = increment_date(current_date)  # Use the lambda function to increment

    return consecutive_dates



def plot_interview_status_toottip():
    try:
        # Sample data (Replace with your actual data fetching logic)
        # Example Interview data
        interview_dates = np.array([1, 5, 10, 15, 20, 25, 30])  # Replace with your actual dates
        interview_statuses = ['Passed', 'Failed', 'WaitingList', 'Passed', 'Failed', 'WaitingList', 'Not Scheduled']

        # Assign color based on status
        status_colors = {
            'Passed': 'green',
            'Failed': 'red',
            'WaitingList': 'blue',
            'Not Scheduled': 'gray'
        }
        colors = [status_colors[status] for status in interview_statuses]

        # Create a scatter plot
        fig, ax = plt.subplots()
        scatter = ax.scatter(interview_dates, interview_dates, s=100, c=colors, edgecolor='black')

        # Create tooltip labels
        labels = [f"Day: {date}<br>Status: {status}" for date, status in zip(interview_dates, interview_statuses)]

        # Attach tooltips to the scatter plot
        tooltip = mpld3.plugins.PointHTMLTooltip(scatter, labels=labels, 
                                                 hoffset=20, voffset=20, 
                                                 css='.mpld3-tooltip{background-color: #cbc; padding: 15px}')
        mpld3.plugins.connect(fig, tooltip)

        # Set labels and title
        ax.set_title('Interview Status Plot')
        ax.set_xlabel('Interview Day')
        ax.set_ylabel('Interview Day')

        # Display the plot using mpld3
        mpld3.show()

    except Exception as e:
        print(f"Error: {e}")


def plot_interview_status():
    try:
        
        weekstart = datetime(year=2024, month=9, day=20)
        current = datetime.now()
        
        # Calculate the number of days between the weekstart and the current date
        days = current - weekstart
        
        # Fetch all interview data
        int_data = Interview.objects.all()

        if days.days > int_data.count():
            # Get consecutive dates from weekstart to current (implement your logic for this)
            dates = get_consecutive_dates(weekstart, current)

            # Generate xpoints and ypoints based on interview data
            ypoints = np.array([i.date.day for i in int_data])
            xpoints = ypoints
        else:
            return None  # If no data, return None or handle accordingly
        
        # Create a new figure
        plt.figure()

        # Loop through each interview data point and plot with a condition-based color
        for x, interview in zip(xpoints, int_data):
            # Assume 'status' is an attribute of the Interview model
            if interview.status == 'Passed':
                plt.plot(x, interview.date.day, marker='o', color='green', label='Passed')  # Green for passed
            elif interview.status == 'Failed':
                plt.plot(x, interview.date.day, marker='o', color='red', label='Failed')  # Red for failed
            elif interview.status == 'WaitingList':
                plt.plot(x, interview.date.day, marker='o', color='blue', label='WaitingList')  # Blue for pending
            else:
                plt.plot(x, interview.date.day, marker='o', color='gray', label='Not Scheduled')  # Gray for other statuses

        # Set x-axis tick marks for all days of the month
        plt.xticks([i*7 for i in range(0, 6)])
        plt.yticks([i*2 for i in range(0, 16)])

        # Optionally, add labels and a title
        plt.title('Interview Status Plot')
        plt.xlabel('Week of the Month')
        plt.ylabel('Interview Day')
        
        # Save the plot to a buffer
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        plt.close()

        # Return the image as a base64 string
        buf.seek(0)
        image_base64 = base64.b64encode(buf.read()).decode('utf-8')

        return image_base64
    
    except Exception as e:
        print(f"Error: {e}")
        return None    


def mm():
    # Get the current date and the date for 7 days ago
    today = timezone.now().date()
    week_start = today - timedelta(days=7)

    # Query interviews for the last week
    interviews = Interview.objects.filter(date__gte=week_start, date__lte=today, is_deleted=False)

    # Prepare data for plotting
    status_counts = defaultdict(lambda: {'passed': 0, 'failed': 0})

    for interview in interviews:
        week = interview.date.isocalendar()[1]  # Get the week number
        if interview.status.lower() == 'passed':
            status_counts[week]['passed'] += 1
        else:
            status_counts[week]['failed'] += 1

    # Prepare x and y data for plotting
    weeks = list(status_counts.keys())
    passed_counts = [status_counts[week]['passed'] for week in weeks]
    failed_counts = [status_counts[week]['failed'] for week in weeks]

    # Plotting
    plt.figure(figsize=(10, 6))

    bar_width = 0.35
    index = range(len(weeks))

    # Create bar plots for passed and failed
    plt.bar(index, passed_counts, bar_width, label='Passed', color='green')
    plt.bar([i + bar_width for i in index], failed_counts, bar_width, label='Failed', color='red')

    # Adding labels and titles
    plt.xlabel('Week')
    plt.ylabel('Number of Interviews')
    plt.title('Interview Status by Week')
    plt.xticks([i + bar_width / 2 for i in index], weeks)
    plt.legend()

    # Save plot to a BytesIO object and encode it as a base64 string
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    plt.close()  # Close the plot to free up memory
    buf.seek(0)
    image_base64 = base64.b64encode(buf.read()).decode('utf-8')

    # Render the image in HTML
    # return HttpResponse(f'<img src="data:image/png;base64,{image_base64}"/>')
    return image_base64


