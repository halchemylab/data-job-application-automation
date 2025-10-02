import tkinter as tk
import random
import time

def run_balloon_animation(canvas):
    colors = ["#ff6666", "#66ff66", "#6666ff", "#ffff66", "#ff66ff", "#66ffff"]
    balloons = []
    
    # Create balloon objects with timestamp
    for _ in range(5):
        x = random.randint(50, 650)
        y = 800
        size = random.randint(30, 50)
        color = random.choice(colors)
        balloon = canvas.create_oval(x, y, x+size, y+size, fill=color, outline="black")
        string = canvas.create_line(x+size/2, y+size, x+size/2, y+size+30, fill="black")
        # Add creation time to each balloon
        balloons.append({
            'balloon': balloon,
            'string': string,
            'created_at': time.time()
        })
    
    def animate():
        current_time = time.time()
        # Create a new list for remaining balloons
        remaining_balloons = []
        
        for balloon_info in balloons:
            # Check if balloon should be removed (2 seconds passed)
            if current_time - balloon_info['created_at'] < 2:
                # Move balloon up if less than 2 seconds old
                canvas.move(balloon_info['balloon'], 0, -5)
                canvas.move(balloon_info['string'], 0, -5)
                remaining_balloons.append(balloon_info)
            else:
                # Delete balloon if 2 seconds passed
                canvas.delete(balloon_info['balloon'])
                canvas.delete(balloon_info['string'])
        
        # Update balloons list
        balloons[:] = remaining_balloons
        
        # Continue animation if there are balloons left
        if remaining_balloons:
            canvas.after(50, animate)
    
    animate()
